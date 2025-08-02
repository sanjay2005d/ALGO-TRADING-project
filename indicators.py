#import the library 
import pandas as pd
import numpy as np 

#rsi calculation 

def calculate_rsi(df,period=14,column='Close'):
    delta = df['Close'].diff()

    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    # Make sure gain and loss are 1D arrays
    gain = gain.values.flatten()
    loss = loss.values.flatten()

    avg_gain = pd.Series(gain).rolling(window=period).mean()
    avg_loss = pd.Series(loss).rolling(window=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    df['RSI'] = rsi
    return df


#moving average calculation 
def calculate_moving_average(df, short_window=20,long_window=50,column='Close'):
    df['20DMA']= df[column].rolling(window=short_window).mean()
    df['50DMA']= df[column].rolling(window=long_window).mean()
    return df
#combined functions 
def add_indicators(df):
    df = calculate_rsi(df)
    df = calculate_moving_average(df)
    return df