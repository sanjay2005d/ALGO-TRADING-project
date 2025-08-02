#import the library 

import yfinance as yf
import pandas as pd
import os
from datetime import datetime,timedelta

#choose the stocks to use
#fetch the data of that stock for last  6months with 1 day interval
stocks=["TCS.NS","INFY.NS","HDFCBANK.ns","RELIANCE.NS","BHARTIARTL.NS","ICICIBANK.NS"]
end_date=datetime.today()
start_date=end_date-timedelta(days=720) # last 2 years 
start_date_str= start_date.strftime('%y-%m-%d')
end_date_str=end_date.strftime('%y-%m-%d')

#create a folder if not exist
data_folder="stock_data"
os.makedirs(data_folder,exist_ok=True)
#download and save the data in a csv file
for stock in stocks:
    df = yf.download(stock,start=start_date,end=end_date,interval='1d')
    
    if df.empty:
        print(f"no data found for the stock {stock}")
        continue
    df.reset_index(inplace=True)
    filename=os.path.join(data_folder,f"{stock.replace('.NS','').replace('.ns', '')}.csv")
    df.to_csv(filename,index=False)
    print(f"saved {stock} data to {filename}")
