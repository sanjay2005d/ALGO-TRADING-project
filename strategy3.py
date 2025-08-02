#import library 
import pandas as pd
import os

#create signals
def generate_signals(df):
    #Generate buy/sell signals based on RSI and moving average crossover
    
    # Remove rows with missing values in indicators
    df = df.dropna(subset=['RSI', '20DMA', '50DMA']).copy()

    # Create an empty signal column
    df['Signal'] = 'Hold'

    # Apply Buy condition
    buy_condition = (df['RSI'] < 30) & (df['20DMA'] > df['50DMA'])
    df.loc[buy_condition, 'Signal'] = 'Buy'

    # Apply Sell condition
    sell_condition = (df['RSI'] > 70) | (df['20DMA'] < df['50DMA'])
    df.loc[sell_condition, 'Signal'] = 'Sell'

    return df

#save the signal to the data frame
def process_stock(file_name, output_name):
    #Load a CSV with indicators, apply strategy, save new file with signals.
    
    df = pd.read_csv(file_name)
    df = generate_signals(df)
    df.to_csv(output_name, index=False)
    print(f" Signals saved to {output_name}")

if __name__ == "__main__":
    data_folder = "stock_data"

    stocks = ['TCS', 'INFY', 'HDFCBANK','RELIANCE','BHARTIARTL','ICICIBANK']

    for stock in stocks:
        input_file = os.path.join(data_folder, f"{stock}_with_indicator.csv")
        output_file = os.path.join(data_folder, f"{stock}_signals.csv")

        if not os.path.exists(input_file):
            print(f" Missing: {input_file}")
            continue

        process_stock(input_file, output_file)
