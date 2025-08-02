import pandas as pd
import os
# the files with double headers
raw_file = {
    'TCS':'TCS.csv',
    'INFY':'INFY.csv',
    'HDFCBANK':'HDFCBANK.csv',
    'RELIANCE': 'RELIANCE.csv',
    'BHARTIARTL': 'BHARTIARTL.csv',
    'ICICIBANK': 'ICICIBANK.csv'
}
#input and output folder 
folder = 'stock_data'

for name,filename in raw_file.items():
    filepath=os.path.join(folder,filename)

    #read the csv with the second row skiped
    df=pd.read_csv(filepath,skiprows=[1])
    #save the cleaned version of the stock data 
    cleaned_path = os.path.join(folder,f'{name}_clean.csv')
    df.to_csv(cleaned_path,index=False)
    print(f" Cleaned and saved: {cleaned_path}")