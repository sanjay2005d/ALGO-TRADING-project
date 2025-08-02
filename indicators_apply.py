#import the library
import pandas as pd
from indicators import add_indicators
import os

#get the folder 
stocks = ['TCS','INFY','HDFCBANK','RELIANCE','BHARTIARTL','ICICIBANK']
data_folder = 'stock_data' #folder where the data is stored 

for stock in stocks:
    cleaned_file = os.path.join(data_folder,f"{stock}_clean.csv")
    output_file = os.path.join(data_folder,f"{stock}_with_indicator.csv")

    if not os.path.exists(cleaned_file):
        print(f"File not found: {cleaned_file}")
        continue
#read the cleaned csv 
    df= pd.read_csv(cleaned_file)

#apply the indicators like RSI  20DMA and 50DMA
    df = add_indicators(df)
    
#save the new file 
    df.to_csv(output_file,index=False)
    print(f"indicators applied and saved: {output_file}")