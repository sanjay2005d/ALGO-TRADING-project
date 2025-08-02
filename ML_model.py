import pandas as pd
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder
import joblib

# 📁 Define your data folder and stock list
data_folder = "stock_data"
stocks = ['TCS', 'INFY', 'HDFCBANK', 'RELIANCE', 'BHARTIARTL', 'ICICIBANK']
features = ['RSI', '20DMA', '50DMA', 'Close']
target = 'Signal'

# 🧹 Combine all stock data for training
combined_df = pd.DataFrame()

for stock in stocks:
    file_path = os.path.join(data_folder, f"{stock}_signals.csv")
    if not os.path.exists(file_path):
        print(f"❌ Missing: {file_path}")
        continue
    df = pd.read_csv(file_path)
    df['Stock'] = stock
    combined_df = pd.concat([combined_df, df], ignore_index=True)

# 🧠 Clean and prepare data
combined_df.dropna(subset=features + [target], inplace=True)
label_encoder = LabelEncoder()
combined_df['Signal_encoded'] = label_encoder.fit_transform(combined_df[target])

X = combined_df[features]
y = combined_df['Signal_encoded']

# 🎯 Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 🌲 Train the model
model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
model.fit(X_train, y_train)

# 💾 Save model and label encoder
joblib.dump(model, "trained_model.pkl")
joblib.dump(label_encoder, "label_encoder.pkl")

# 📊 Evaluate model
y_pred = model.predict(X_test)
print("\n📊 Classification Report:")
print(classification_report(y_test, y_pred, target_names=label_encoder.classes_))

# 🧪 Sample predictions on TCS
tcs_df = combined_df[combined_df['Stock'] == 'TCS'].copy()
tcs_df['Predicted_Signal'] = label_encoder.inverse_transform(model.predict(tcs_df[features]))
print("\n📍 Sample Predictions on TCS:")
print(tcs_df[['Date', 'RSI', '20DMA', '50DMA', 'Close', 'Signal', 'Predicted_Signal']].tail(10))

# 📦 Inference on latest row of each stock
print("\n📅 Running inference for latest row of all stocks...")
latest_predictions = []

for stock in stocks:
    file_path = os.path.join(data_folder, f"{stock}_signals.csv")
    if not os.path.exists(file_path):
        print(f"❌ Missing: {file_path}")
        continue

    stock_df = pd.read_csv(file_path)
    stock_df.dropna(subset=features, inplace=True)
    
    if stock_df.empty:
        print(f"⚠️ No valid data for {stock}. Skipping.")
        continue

    stock_df['Predicted_Signal'] = label_encoder.inverse_transform(
        model.predict(stock_df[features])
    )
    
    # Get the last row (assumed to be today's data)
    latest_row = stock_df.iloc[-1].copy()
    latest_row['Stock'] = stock
    latest_predictions.append(latest_row)

# 📝 Save all latest predictions to one CSV
if latest_predictions:
    prediction_df = pd.DataFrame(latest_predictions)
    prediction_df.to_csv("predicted_new_data.csv", index=False)
    print("\n✅ Combined latest predictions saved to predicted_new_data.csv")
    print(prediction_df[['Date', 'Stock', 'RSI', '20DMA', '50DMA', 'Close', 'Predicted_Signal']])
else:
    print("⚠️ No predictions made due to missing or invalid stock data.")

