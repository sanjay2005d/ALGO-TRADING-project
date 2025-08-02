import yfinance as yf
import pandas as pd
import joblib

# Load model and encoder
model = joblib.load("trained_model.pkl")
label_encoder = joblib.load("label_encoder.pkl")

# List of stocks
stocks = ['TCS.NS', 'INFY.NS', 'HDFCBANK.NS', 'RELIANCE.NS', 'BHARTIARTL.NS', 'ICICIBANK.NS']
features = ['RSI', '20DMA', '50DMA', 'Close']

# Date range
end_date = pd.Timestamp.today()
start_date = end_date - pd.Timedelta(days=150)

all_data = []

# RSI function
def compute_rsi(series, window=14):
    delta = series.diff()
    gain = delta.where(delta > 0, 0).rolling(window=window).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

for symbol in stocks:
    print(f"\n📥 Fetching data for {symbol}...")

    # FIX: group_by = 'ticker' causes multi-index -> set it to 'column' or remove it
    df = yf.download(symbol, start=start_date, end=end_date, auto_adjust=False)
    
    if df.empty:
        print(f"❌ No data for {symbol}")
        continue

    # FLATTEN multi-index if needed
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.droplevel(1)

    df.reset_index(inplace=True)
    df['Stock'] = symbol.replace('.NS', '')

    # Use 'Adj Close' if 'Close' missing
    if 'Close' not in df.columns:
        if 'Adj Close' in df.columns:
            df['Close'] = df['Adj Close']
            print(f"⚠️ Used 'Adj Close' as 'Close' for {symbol}")
        else:
            print(f"❌ No usable price column for {symbol}. Skipping...")
            continue

    # Calculate indicators
    df['20DMA'] = df['Close'].rolling(window=20).mean()
    df['50DMA'] = df['Close'].rolling(window=50).mean()
    df['RSI'] = compute_rsi(df['Close'])

    # Check required features
    missing_cols = [col for col in features if col not in df.columns]
    if missing_cols:
        print(f"⚠️ Missing columns for {symbol}: {missing_cols}. Skipping.")
        continue

    # Drop rows with missing data
    df.dropna(subset=features, inplace=True)

    if df.empty:
        print(f"⚠️ No usable data for {symbol} after dropna.")
        continue

    # Predict
    preds = model.predict(df[features])
    df['Predicted_Signal'] = label_encoder.inverse_transform(preds)

    print(f"📊 {symbol} Predictions (Last 5 Days):")
    print(df[['Date', 'Stock', 'RSI', '20DMA', '50DMA', 'Close', 'Predicted_Signal']].tail(5))

    all_data.append(df)

# Save all predictions
if all_data:
    result_df = pd.concat(all_data, ignore_index=True)
    result_df.to_csv("predicted_new_data.csv", index=False)
    print("\n✅ All predictions saved to predicted_new_data.csv")
else:
    print("\n⚠️ No predictions generated.")
