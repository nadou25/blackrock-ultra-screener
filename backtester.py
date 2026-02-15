"""
📉 BlackRock Ultra Screener — Backtesting Engine
═══════════════════════════════════════════════════
Module de backtesting pour tester les stratégies.

Usage:
    from backtester import Backtester
    bt = Backtester(initial_capital=10000)
    results = bt.run("AAPL", strategy="sma_crossover", period="2y")
    bt.report()
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Callable
import warnings
warnings.filterwarnings('ignore')

try:
    import yfinance as yf
except ImportError:
    yf = None


@dataclass
class Trade:
    """Représente un trade."""
    symbol: str
    entry_date: datetime
    entry_price: float
    exit_date: Optional[datetime] = None
    exit_price: Optional[float] = None
    shares: int = 0
    side: str = "long"  # long ou short
    pnl: float = 0.0
    pnl_pct: float = 0.0
    
    @property
    def is_closed(self) -> bool:
        return self.exit_date is not None


@dataclass
class BacktestResult:
    """Résultats du backtest."""
    symbol: str
    strategy: str
    period: str
    initial_capital: float
    final_capital: float
    total_return_pct: float
    benchmark_return_pct: float
    sharpe_ratio: float
    sortino_ratio: float
    max_drawdown_pct: float
    win_rate: float
    profit_factor: float
    total_trades: int
    winning_trades: int
    losing_trades: int
    avg_win_pct: float
    avg_loss_pct: float
    trades: List[Trade] = field(default_factory=list)
    equity_curve: Optional[pd.Series] = None
    benchmark_curve: Optional[pd.Series] = None


class Backtester:
    """
    Moteur de backtesting pour les stratégies de trading.
    
    Strategies disponibles:
        - buy_hold: Buy and Hold simple
        - sma_crossover: Croisement de moyennes mobiles
        - rsi_oversold: Achat sur RSI survendu
        - macd_signal: Signal MACD
        - momentum: Momentum (ROC)
        - mean_reversion: Mean Reversion (Bollinger)
    """
    
    STRATEGIES = {
        'buy_hold': 'Buy & Hold',
        'sma_crossover': 'SMA Crossover (20/50)',
        'rsi_oversold': 'RSI Oversold (<30)',
        'macd_signal': 'MACD Signal',
        'momentum': 'Momentum (ROC 20)',
        'mean_reversion': 'Mean Reversion (Bollinger)',
    }
    
    def __init__(self, initial_capital: float = 10000, commission: float = 0.001):
        """
        Args:
            initial_capital: Capital initial en $
            commission: Commission par trade (0.001 = 0.1%)
        """
        self.initial_capital = initial_capital
        self.commission = commission
        self.results: Optional[BacktestResult] = None
        
    def _fetch_data(self, symbol: str, period: str = "2y") -> pd.DataFrame:
        """Télécharge les données historiques."""
        if yf is None:
            raise ImportError("yfinance requis: pip install yfinance")
        
        data = yf.download(symbol, period=period, progress=False)
        if len(data) == 0:
            raise ValueError(f"Aucune donnée pour {symbol}")
        return data
    
    def _calculate_indicators(self, data: pd.DataFrame) -> pd.DataFrame:
        """Calcule tous les indicateurs techniques."""
        df = data.copy()
        
        # Prix
        df['Returns'] = df['Close'].pct_change()
        
        # SMA
        df['SMA20'] = df['Close'].rolling(20).mean()
        df['SMA50'] = df['Close'].rolling(50).mean()
        df['SMA200'] = df['Close'].rolling(200).mean()
        
        # EMA
        df['EMA12'] = df['Close'].ewm(span=12).mean()
        df['EMA26'] = df['Close'].ewm(span=26).mean()
        
        # MACD
        df['MACD'] = df['EMA12'] - df['EMA26']
        df['MACD_Signal'] = df['MACD'].ewm(span=9).mean()
        df['MACD_Hist'] = df['MACD'] - df['MACD_Signal']
        
        # RSI
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        
        # Bollinger Bands
        df['BB_Mid'] = df['Close'].rolling(20).mean()
        df['BB_Std'] = df['Close'].rolling(20).std()
        df['BB_Upper'] = df['BB_Mid'] + 2 * df['BB_Std']
        df['BB_Lower'] = df['BB_Mid'] - 2 * df['BB_Std']
        
        # Momentum / ROC
        df['ROC'] = df['Close'].pct_change(20) * 100
        
        # ATR
        df['TR'] = np.maximum(
            df['High'] - df['Low'],
            np.maximum(
                abs(df['High'] - df['Close'].shift(1)),
                abs(df['Low'] - df['Close'].shift(1))
            )
        )
        df['ATR'] = df['TR'].rolling(14).mean()
        
        return df
    
    def _generate_signals(self, data: pd.DataFrame, strategy: str) -> pd.Series:
        """Génère les signaux de trading (1=long, 0=out, -1=short)."""
        signals = pd.Series(0, index=data.index)
        
        if strategy == 'buy_hold':
            signals[:] = 1
            
        elif strategy == 'sma_crossover':
            signals = np.where(data['SMA20'] > data['SMA50'], 1, 0)
            
        elif strategy == 'rsi_oversold':
            # Achat quand RSI < 30, vente quand RSI > 70
            position = 0
            for i in range(len(data)):
                if data['RSI'].iloc[i] < 30:
                    position = 1
                elif data['RSI'].iloc[i] > 70:
                    position = 0
                signals.iloc[i] = position
                
        elif strategy == 'macd_signal':
            signals = np.where(data['MACD'] > data['MACD_Signal'], 1, 0)
            
        elif strategy == 'momentum':
            signals = np.where(data['ROC'] > 0, 1, 0)
            
        elif strategy == 'mean_reversion':
            # Achat sous bande inférieure, vente au-dessus de la moyenne
            position = 0
            for i in range(len(data)):
                if data['Close'].iloc[i] < data['BB_Lower'].iloc[i]:
                    position = 1
                elif data['Close'].iloc[i] > data['BB_Mid'].iloc[i]:
                    position = 0
                signals.iloc[i] = position
        
        return pd.Series(signals, index=data.index)
    
    def run(self, symbol: str, strategy: str = 'sma_crossover', 
            period: str = '2y') -> BacktestResult:
        """
        Exécute le backtest.
        
        Args:
            symbol: Symbole à backtester
            strategy: Nom de la stratégie
            period: Période (1y, 2y, 5y, max)
            
        Returns:
            BacktestResult avec toutes les métriques
        """
        # Récupérer les données
        data = self._fetch_data(symbol, period)
        data = self._calculate_indicators(data)
        
        # Générer les signaux
        data['Signal'] = self._generate_signals(data, strategy)
        data['Signal'] = data['Signal'].shift(1).fillna(0)  # Éviter le look-ahead bias
        
        # Calculer les returns de la stratégie
        data['Strategy_Returns'] = data['Returns'] * data['Signal']
        
        # Appliquer les commissions (entrée/sortie)
        signal_changes = data['Signal'].diff().abs()
        data['Strategy_Returns'] -= signal_changes * self.commission
        
        # Equity curve
        data['Equity'] = self.initial_capital * (1 + data['Strategy_Returns']).cumprod()
        data['Benchmark'] = self.initial_capital * (1 + data['Returns']).cumprod()
        
        # Extraire les trades
        trades = self._extract_trades(data, symbol)
        
        # Calculer les métriques
        final_capital = data['Equity'].iloc[-1]
        total_return = (final_capital / self.initial_capital - 1) * 100
        benchmark_return = (data['Benchmark'].iloc[-1] / self.initial_capital - 1) * 100
        
        # Sharpe Ratio (annualisé)
        strategy_returns = data['Strategy_Returns'].dropna()
        sharpe = strategy_returns.mean() / strategy_returns.std() * np.sqrt(252) if strategy_returns.std() > 0 else 0
        
        # Sortino Ratio
        downside_returns = strategy_returns[strategy_returns < 0]
        sortino = strategy_returns.mean() / downside_returns.std() * np.sqrt(252) if len(downside_returns) > 0 and downside_returns.std() > 0 else 0
        
        # Max Drawdown
        rolling_max = data['Equity'].cummax()
        drawdown = (data['Equity'] - rolling_max) / rolling_max
        max_dd = drawdown.min() * 100
        
        # Win rate et profit factor
        winning = [t for t in trades if t.pnl > 0]
        losing = [t for t in trades if t.pnl < 0]
        win_rate = len(winning) / len(trades) * 100 if trades else 0
        
        total_wins = sum(t.pnl for t in winning) if winning else 0
        total_losses = abs(sum(t.pnl for t in losing)) if losing else 1
        profit_factor = total_wins / total_losses if total_losses > 0 else 0
        
        avg_win = np.mean([t.pnl_pct for t in winning]) if winning else 0
        avg_loss = np.mean([t.pnl_pct for t in losing]) if losing else 0
        
        self.results = BacktestResult(
            symbol=symbol,
            strategy=self.STRATEGIES.get(strategy, strategy),
            period=period,
            initial_capital=self.initial_capital,
            final_capital=final_capital,
            total_return_pct=total_return,
            benchmark_return_pct=benchmark_return,
            sharpe_ratio=sharpe,
            sortino_ratio=sortino,
            max_drawdown_pct=max_dd,
            win_rate=win_rate,
            profit_factor=profit_factor,
            total_trades=len(trades),
            winning_trades=len(winning),
            losing_trades=len(losing),
            avg_win_pct=avg_win,
            avg_loss_pct=avg_loss,
            trades=trades,
            equity_curve=data['Equity'],
            benchmark_curve=data['Benchmark']
        )
        
        return self.results
    
    def _extract_trades(self, data: pd.DataFrame, symbol: str) -> List[Trade]:
        """Extrait les trades individuels."""
        trades = []
        position = 0
        entry_date = None
        entry_price = None
        
        for i in range(1, len(data)):
            signal = data['Signal'].iloc[i]
            
            # Entrée en position
            if signal == 1 and position == 0:
                position = 1
                entry_date = data.index[i]
                entry_price = data['Close'].iloc[i]
                
            # Sortie de position
            elif signal == 0 and position == 1:
                exit_date = data.index[i]
                exit_price = data['Close'].iloc[i]
                pnl = exit_price - entry_price
                pnl_pct = (exit_price / entry_price - 1) * 100
                
                trades.append(Trade(
                    symbol=symbol,
                    entry_date=entry_date,
                    entry_price=entry_price,
                    exit_date=exit_date,
                    exit_price=exit_price,
                    shares=int(self.initial_capital / entry_price),
                    side="long",
                    pnl=pnl,
                    pnl_pct=pnl_pct
                ))
                
                position = 0
                entry_date = None
                entry_price = None
        
        return trades
    
    def report(self) -> str:
        """Génère un rapport textuel."""
        if not self.results:
            return "❌ Aucun backtest exécuté."
        
        r = self.results
        
        report = f"""
╔══════════════════════════════════════════════════════════════╗
║               📉 RAPPORT DE BACKTEST                         ║
╠══════════════════════════════════════════════════════════════╣
║  Symbole:     {r.symbol:<15} Stratégie: {r.strategy:<20}
║  Période:     {r.period:<15} Trades:    {r.total_trades:<20}
╠══════════════════════════════════════════════════════════════╣
║  💰 PERFORMANCE                                               ║
║  ─────────────────────────────────────────────────────────────║
║  Capital Initial:    ${r.initial_capital:>12,.2f}                       
║  Capital Final:      ${r.final_capital:>12,.2f}                       
║  Return Stratégie:   {r.total_return_pct:>+12.2f}%                       
║  Return Benchmark:   {r.benchmark_return_pct:>+12.2f}%                       
║  Alpha:              {r.total_return_pct - r.benchmark_return_pct:>+12.2f}%                       
╠══════════════════════════════════════════════════════════════╣
║  📊 MÉTRIQUES DE RISQUE                                       ║
║  ─────────────────────────────────────────────────────────────║
║  Sharpe Ratio:       {r.sharpe_ratio:>12.2f}                       
║  Sortino Ratio:      {r.sortino_ratio:>12.2f}                       
║  Max Drawdown:       {r.max_drawdown_pct:>12.2f}%                       
╠══════════════════════════════════════════════════════════════╣
║  🎯 STATISTIQUES TRADES                                       ║
║  ─────────────────────────────────────────────────────────────║
║  Win Rate:           {r.win_rate:>12.1f}%                       
║  Profit Factor:      {r.profit_factor:>12.2f}                       
║  Trades Gagnants:    {r.winning_trades:>12}                       
║  Trades Perdants:    {r.losing_trades:>12}                       
║  Gain Moyen:         {r.avg_win_pct:>+12.2f}%                       
║  Perte Moyenne:      {r.avg_loss_pct:>+12.2f}%                       
╚══════════════════════════════════════════════════════════════╝
"""
        return report


# ═══════════════════════════════════════════════════════════════════
#                         CLI INTERFACE
# ═══════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="📉 BlackRock Backtester")
    parser.add_argument("symbol", help="Symbole à backtester (ex: AAPL)")
    parser.add_argument("-s", "--strategy", default="sma_crossover",
                       choices=list(Backtester.STRATEGIES.keys()),
                       help="Stratégie de trading")
    parser.add_argument("-p", "--period", default="2y",
                       help="Période (1y, 2y, 5y, max)")
    parser.add_argument("-c", "--capital", type=float, default=10000,
                       help="Capital initial")
    
    args = parser.parse_args()
    
    print(f"\n🔄 Backtesting {args.symbol} avec {args.strategy}...\n")
    
    bt = Backtester(initial_capital=args.capital)
    results = bt.run(args.symbol, strategy=args.strategy, period=args.period)
    
    print(bt.report())
