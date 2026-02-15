"""
🏦 BlackRock Ultra Screener — Dashboard Streamlit
═══════════════════════════════════════════════════
Interface web interactive pour le screener.

Lancer: streamlit run dashboard.py
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ═══════════════════════════════════════════════════════════════════
#                         PAGE CONFIG
# ═══════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="🏦 BlackRock Ultra Screener",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        background: linear-gradient(90deg, #1e3a5f, #2d5a87);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
    }
    .buy-signal { color: #00c853; font-weight: bold; }
    .sell-signal { color: #ff1744; font-weight: bold; }
    .hold-signal { color: #ffc107; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════
#                         SIDEBAR
# ═══════════════════════════════════════════════════════════════════
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/bank-building.png", width=80)
    st.title("⚙️ Configuration")
    
    # Profil de trading
    profile = st.selectbox(
        "📊 Profil de Trading",
        ["INVESTISSEUR_1AN", "SWING_MAX", "SCALP_MAX", "INTRADAY_MAX", 
         "BALANCED", "NASDAQ_SNIPER", "SP500_VALUE"],
        index=0
    )
    
    # Score minimum
    score_min = st.slider("🎯 Score Minimum", 40, 80, 55)
    
    # Nombre de résultats
    top_n = st.slider("📈 Top N résultats", 5, 50, 20)
    
    # Options
    st.subheader("🔧 Options")
    include_us = st.checkbox("🇺🇸 Inclure US (NASDAQ/S&P)", True)
    include_eu = st.checkbox("🇪🇺 Inclure Europe (PEA)", True)
    include_crypto = st.checkbox("₿ Inclure Crypto", False)
    
    # Bouton d'analyse
    run_analysis = st.button("🚀 Lancer l'Analyse", type="primary", use_container_width=True)
    
    st.divider()
    st.caption("🏦 BlackRock Ultra Screener v10")
    st.caption(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}")

# ═══════════════════════════════════════════════════════════════════
#                         MAIN CONTENT
# ═══════════════════════════════════════════════════════════════════
st.markdown('<h1 class="main-header">🏦 BlackRock Ultra Screener</h1>', unsafe_allow_html=True)
st.markdown("---")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📊 Résultats", "📈 Analyse Détaillée", "🛡️ Risk Management", "📉 Backtesting"])

# ═══════════════════════════════════════════════════════════════════
#                         TAB 1: RÉSULTATS
# ═══════════════════════════════════════════════════════════════════
with tab1:
    if run_analysis:
        with st.spinner("🔄 Analyse en cours... (peut prendre 2-5 minutes)"):
            try:
                # Import et exécution du screener
                import stock_screener_ultra_v10 as screener
                
                config = screener.Config.charger()
                config.appliquer_profil(profile)
                config.SCORE_MINIMUM = score_min
                config.FAST_MODE = True
                config.INCLURE_US = include_us
                config.INCLURE_NASDAQ100 = include_us
                config.INCLURE_SP500 = include_us
                config.MODE_PEA = include_eu and not include_us
                config.ML_MAX_SYMBOLES = 150
                
                # Progress bar
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                def update_progress(symbole, current, total):
                    progress = current / total if total > 0 else 0
                    progress_bar.progress(progress)
                    status_text.text(f"📊 Analyse: {symbole} ({current}/{total})")
                
                moteur = screener.MoteurAnalyse(config)
                results = moteur.executer(callback=update_progress)
                
                progress_bar.empty()
                status_text.empty()
                
                # Stocker en session
                st.session_state['results'] = results
                st.session_state['profile'] = profile
                
                st.success(f"✅ Analyse terminée ! {len(results)} titres analysés.")
                
            except Exception as e:
                st.error(f"❌ Erreur: {str(e)}")
                st.exception(e)
    
    # Afficher les résultats
    if 'results' in st.session_state and st.session_state['results']:
        results = st.session_state['results'][:top_n]
        
        # Métriques globales
        col1, col2, col3, col4 = st.columns(4)
        
        buy_count = sum(1 for r in results if 'ACHAT' in r.get('decision', ''))
        sell_count = sum(1 for r in results if 'VENTE' in r.get('decision', ''))
        hold_count = len(results) - buy_count - sell_count
        avg_score = np.mean([r.get('score_final', 0) for r in results])
        
        col1.metric("🟢 Signaux ACHAT", buy_count)
        col2.metric("🔴 Signaux VENTE", sell_count)
        col3.metric("🟡 NEUTRE", hold_count)
        col4.metric("📊 Score Moyen", f"{avg_score:.1f}")
        
        st.divider()
        
        # Tableau des résultats
        df = pd.DataFrame(results)
        
        # Colonnes à afficher
        display_cols = ['symbole', 'nom', 'score_final', 'decision', 'prix', 
                       'variation_pct', 'sl_price', 'tp_price', 'kelly_pct', 'risk_score']
        display_cols = [c for c in display_cols if c in df.columns]
        
        if len(display_cols) > 0:
            df_display = df[display_cols].copy()
            
            # Formater
            if 'score_final' in df_display.columns:
                df_display['score_final'] = df_display['score_final'].round(1)
            if 'variation_pct' in df_display.columns:
                df_display['variation_pct'] = df_display['variation_pct'].apply(lambda x: f"{x:+.2f}%" if pd.notna(x) else "N/A")
            if 'kelly_pct' in df_display.columns:
                df_display['kelly_pct'] = df_display['kelly_pct'].apply(lambda x: f"{x:.1f}%" if pd.notna(x) else "N/A")
            
            # Renommer colonnes
            df_display.columns = ['Symbole', 'Nom', 'Score', 'Décision', 'Prix', 
                                 'Variation', 'Stop-Loss', 'Take-Profit', 'Kelly%', 'Risk'][:len(display_cols)]
            
            st.dataframe(
                df_display,
                use_container_width=True,
                height=600
            )
            
            # Graphique des scores
            st.subheader("📊 Distribution des Scores")
            fig = px.bar(
                df_display.head(20),
                x='Symbole',
                y='Score',
                color='Score',
                color_continuous_scale='RdYlGn',
                title=f"Top 20 - Profil {st.session_state.get('profile', 'N/A')}"
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("👆 Cliquez sur 'Lancer l'Analyse' pour démarrer")
        
        # Afficher un exemple
        st.subheader("📋 Exemple de résultats")
        example_data = {
            'Symbole': ['NVDA', 'AAPL', 'MSFT', 'GOOGL', 'META'],
            'Score': [87, 82, 79, 76, 74],
            'Décision': ['🟢 ACHAT FORT', '🟢 ACHAT', '🟢 ACHAT', '🟡 NEUTRE', '🟡 NEUTRE'],
            'Prix': [850.50, 185.20, 415.30, 175.80, 520.40],
            'Kelly%': ['15.2%', '12.8%', '10.5%', '8.2%', '7.1%']
        }
        st.dataframe(pd.DataFrame(example_data), use_container_width=True)

# ═══════════════════════════════════════════════════════════════════
#                         TAB 2: ANALYSE DÉTAILLÉE
# ═══════════════════════════════════════════════════════════════════
with tab2:
    st.subheader("📈 Analyse Technique Détaillée")
    
    # Sélection du symbole
    symbol = st.text_input("🔍 Symbole à analyser", value="AAPL")
    
    if st.button("📊 Analyser", key="analyze_single"):
        with st.spinner(f"Analyse de {symbol}..."):
            try:
                import yfinance as yf
                
                ticker = yf.Ticker(symbol)
                hist = ticker.history(period="1y")
                info = ticker.info
                
                if len(hist) > 0:
                    col1, col2, col3 = st.columns(3)
                    
                    current_price = hist['Close'].iloc[-1]
                    change = ((current_price / hist['Close'].iloc[-2]) - 1) * 100
                    year_high = hist['High'].max()
                    year_low = hist['Low'].min()
                    
                    col1.metric("💰 Prix actuel", f"${current_price:.2f}", f"{change:+.2f}%")
                    col2.metric("📈 Plus haut 52s", f"${year_high:.2f}")
                    col3.metric("📉 Plus bas 52s", f"${year_low:.2f}")
                    
                    # Graphique candlestick
                    fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                                       vertical_spacing=0.1,
                                       row_heights=[0.7, 0.3])
                    
                    fig.add_trace(go.Candlestick(
                        x=hist.index,
                        open=hist['Open'],
                        high=hist['High'],
                        low=hist['Low'],
                        close=hist['Close'],
                        name='Prix'
                    ), row=1, col=1)
                    
                    # Volume
                    fig.add_trace(go.Bar(
                        x=hist.index,
                        y=hist['Volume'],
                        name='Volume',
                        marker_color='rgba(100,100,200,0.5)'
                    ), row=2, col=1)
                    
                    fig.update_layout(
                        title=f"{symbol} - 1 An",
                        xaxis_rangeslider_visible=False,
                        height=600
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Infos fondamentales
                    st.subheader("📋 Données Fondamentales")
                    col1, col2, col3, col4 = st.columns(4)
                    
                    col1.metric("P/E Ratio", f"{info.get('trailingPE', 'N/A'):.1f}" if info.get('trailingPE') else "N/A")
                    col2.metric("Market Cap", f"${info.get('marketCap', 0)/1e9:.1f}B" if info.get('marketCap') else "N/A")
                    col3.metric("Dividend Yield", f"{info.get('dividendYield', 0)*100:.2f}%" if info.get('dividendYield') else "N/A")
                    col4.metric("Beta", f"{info.get('beta', 'N/A'):.2f}" if info.get('beta') else "N/A")
                    
            except Exception as e:
                st.error(f"Erreur: {e}")

# ═══════════════════════════════════════════════════════════════════
#                         TAB 3: RISK MANAGEMENT
# ═══════════════════════════════════════════════════════════════════
with tab3:
    st.subheader("🛡️ Calculateur de Risk Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 💰 Position Sizing (Kelly)")
        
        capital = st.number_input("Capital total ($)", value=10000, step=1000)
        win_rate = st.slider("Win Rate (%)", 30, 80, 55) / 100
        rr_ratio = st.slider("Ratio Reward/Risk", 1.0, 5.0, 2.0, 0.1)
        
        # Kelly Criterion
        kelly = win_rate - (1 - win_rate) / rr_ratio
        kelly_half = kelly / 2  # Half-Kelly (plus conservateur)
        
        position_kelly = capital * kelly if kelly > 0 else 0
        position_half = capital * kelly_half if kelly_half > 0 else 0
        
        st.metric("📊 Kelly Full", f"{kelly*100:.1f}%", f"${position_kelly:,.0f}")
        st.metric("📊 Half-Kelly (recommandé)", f"{kelly_half*100:.1f}%", f"${position_half:,.0f}")
    
    with col2:
        st.markdown("### 📉 Value at Risk (VaR)")
        
        portfolio_value = st.number_input("Valeur du portefeuille ($)", value=50000, step=5000)
        confidence = st.selectbox("Niveau de confiance", [0.95, 0.99], index=0)
        volatility = st.slider("Volatilité annuelle (%)", 10, 50, 20) / 100
        
        # VaR parametrique (1 jour)
        from scipy import stats
        z_score = stats.norm.ppf(1 - confidence)
        daily_vol = volatility / np.sqrt(252)
        var_1d = portfolio_value * z_score * daily_vol
        var_5d = var_1d * np.sqrt(5)
        
        st.metric("📉 VaR 1 jour", f"${abs(var_1d):,.0f}")
        st.metric("📉 VaR 5 jours", f"${abs(var_5d):,.0f}")
        
        st.info(f"💡 Avec {confidence*100:.0f}% de confiance, votre perte maximale sur 1 jour ne dépassera pas ${abs(var_1d):,.0f}")

# ═══════════════════════════════════════════════════════════════════
#                         TAB 4: BACKTESTING
# ═══════════════════════════════════════════════════════════════════
with tab4:
    st.subheader("📉 Backtesting Simplifié")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        bt_symbol = st.text_input("Symbole", value="SPY", key="bt_symbol")
        bt_period = st.selectbox("Période", ["1y", "2y", "5y"], index=0)
        bt_strategy = st.selectbox("Stratégie", [
            "Buy & Hold",
            "SMA Crossover (20/50)",
            "RSI Oversold (< 30)",
            "Momentum (ROC > 0)"
        ])
        
        run_bt = st.button("▶️ Lancer Backtest", type="primary")
    
    with col2:
        if run_bt:
            with st.spinner("Backtesting..."):
                try:
                    import yfinance as yf
                    
                    data = yf.download(bt_symbol, period=bt_period, progress=False)
                    
                    if len(data) > 50:
                        data['Returns'] = data['Close'].pct_change()
                        data['Cumulative'] = (1 + data['Returns']).cumprod()
                        
                        # Stratégies simples
                        if bt_strategy == "Buy & Hold":
                            data['Signal'] = 1
                        elif bt_strategy == "SMA Crossover (20/50)":
                            data['SMA20'] = data['Close'].rolling(20).mean()
                            data['SMA50'] = data['Close'].rolling(50).mean()
                            data['Signal'] = (data['SMA20'] > data['SMA50']).astype(int)
                        elif bt_strategy == "RSI Oversold (< 30)":
                            delta = data['Close'].diff()
                            gain = (delta.where(delta > 0, 0)).rolling(14).mean()
                            loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
                            rs = gain / loss
                            data['RSI'] = 100 - (100 / (1 + rs))
                            data['Signal'] = (data['RSI'] < 30).astype(int).shift(1).fillna(0)
                        else:  # Momentum
                            data['ROC'] = data['Close'].pct_change(20)
                            data['Signal'] = (data['ROC'] > 0).astype(int)
                        
                        data['Strategy_Returns'] = data['Returns'] * data['Signal'].shift(1)
                        data['Strategy_Cumulative'] = (1 + data['Strategy_Returns']).cumprod()
                        
                        # Métriques
                        total_return = (data['Strategy_Cumulative'].iloc[-1] - 1) * 100
                        bh_return = (data['Cumulative'].iloc[-1] - 1) * 100
                        sharpe = data['Strategy_Returns'].mean() / data['Strategy_Returns'].std() * np.sqrt(252)
                        max_dd = ((data['Strategy_Cumulative'].cummax() - data['Strategy_Cumulative']) / data['Strategy_Cumulative'].cummax()).max() * 100
                        
                        # Affichage
                        c1, c2, c3, c4 = st.columns(4)
                        c1.metric("📈 Return Stratégie", f"{total_return:.1f}%")
                        c2.metric("📊 Return Buy&Hold", f"{bh_return:.1f}%")
                        c3.metric("📉 Max Drawdown", f"{max_dd:.1f}%")
                        c4.metric("📊 Sharpe Ratio", f"{sharpe:.2f}")
                        
                        # Graphique
                        fig = go.Figure()
                        fig.add_trace(go.Scatter(x=data.index, y=data['Strategy_Cumulative'], name='Stratégie', line=dict(color='green')))
                        fig.add_trace(go.Scatter(x=data.index, y=data['Cumulative'], name='Buy & Hold', line=dict(color='blue', dash='dash')))
                        fig.update_layout(title=f"Backtest: {bt_strategy}", height=400)
                        st.plotly_chart(fig, use_container_width=True)
                        
                except Exception as e:
                    st.error(f"Erreur: {e}")

# ═══════════════════════════════════════════════════════════════════
#                         FOOTER
# ═══════════════════════════════════════════════════════════════════
st.divider()
st.markdown("""
<div style="text-align: center; color: #666;">
    <p>🏦 BlackRock Ultra Screener v10 — Dashboard by Naknak 🧞</p>
    <p>⚠️ Ce logiciel est fourni à titre éducatif uniquement. Pas de conseil en investissement.</p>
</div>
""", unsafe_allow_html=True)
