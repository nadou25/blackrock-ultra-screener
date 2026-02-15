#!/usr/bin/env python3
"""
🏦 BlackRock Ultra Screener - Setup Script
Installation simplifiée du projet.
"""

from setuptools import setup, find_packages
import os

# Read README for long description
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return ""

# Read requirements
def read_requirements():
    req_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    if os.path.exists(req_path):
        with open(req_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return []

setup(
    name='blackrock-ultra-screener',
    version='10.0.0',
    author='nadou25',
    author_email='',
    description='🏦 Screener quantitatif multi-factoriel avec ML, PPO et Bot Telegram',
    long_description=read_readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/nadou25/blackrock-ultra-screener',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Financial and Insurance Industry',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Office/Business :: Financial :: Investment',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
    python_requires='>=3.10',
    install_requires=read_requirements(),
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'flake8>=6.0.0',
            'black>=23.0.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'screener=stock_screener_ultra_v10:main',
            'screener-bot=telegram_bot:main',
        ],
    },
    keywords=[
        'trading', 'screener', 'quantitative', 'machine-learning',
        'reinforcement-learning', 'ppo', 'stocks', 'finance',
        'blackrock', 'aladdin', 'risk-management', 'telegram-bot'
    ],
    project_urls={
        'Bug Reports': 'https://github.com/nadou25/blackrock-ultra-screener/issues',
        'Source': 'https://github.com/nadou25/blackrock-ultra-screener',
    },
)
