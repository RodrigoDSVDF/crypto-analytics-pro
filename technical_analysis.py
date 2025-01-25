import pandas as pd
import numpy as np

def calculate_technical_indicators(df):
    # Médias Móveis
    df['MA20'] = df['close'].rolling(window=20).mean()
    df['MA50'] = df['close'].rolling(window=50).mean()
    df['MA200'] = df['close'].rolling(window=200).mean()
    
    # RSI
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    # Bandas de Bollinger
    df['Upper_BB'] = df['MA20'] + (df['close'].rolling(20).std() * 2)
    df['Lower_BB'] = df['MA20'] - (df['close'].rolling(20).std() * 2)
    
    # MACD
    exp12 = df['close'].ewm(span=12, adjust=False).mean()
    exp26 = df['close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = exp12 - exp26
    df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
    
    # Volatilidade
    df['Volatility'] = df['close'].pct_change().rolling(window=30).std() * np.sqrt(365)
    
    return df.dropna()

def calculate_risk_return(df):
    df['Return'] = df['close'].pct_change()
    df['Risk'] = df['Return'].rolling(window=30).std() * np.sqrt(365)
    return df