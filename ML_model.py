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

# 🧹 Combine all stock data
combined_df = pd.DataFrame()

for stock in stocks:
    file_path = os.path.join(data_folder, f"{stock}_signals.csv")
    if not os.path.exists(file_path):
        print(f"❌ Missing: {file_path}")
        continue
    df = pd.read_csv(file_path)
    df['Stock'] = stock  # add stock column for traceability
    combined_df = pd.concat([combined_df, df], ignore_index=True)

# 🧠 Select features and target
features = ['RSI', '20DMA', '50DMA', 'Close']
target = 'Signal'

# 🔍 Drop rows with missing values
combined_df.dropna(subset=features + [target], inplace=True)

# 🔢 Encode the Signal column (Buy, Sell, Hold) → (0,1,2)
label_encoder = LabelEncoder()
combined_df['Signal_encoded'] = label_encoder.fit_transform(combined_df[target])

X = combined_df[features]
y = combined_df['Signal_encoded']

# 🎯 Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 🌲 Train the Random Forest Classifier
model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
model.fit(X_train, y_train)

# 💾 Save the model and encoder
joblib.dump(model, "trained_model.pkl")
joblib.dump(label_encoder, "label_encoder.pkl")

# 📈 Evaluate the model
y_pred = model.predict(X_test)
print("\n📊 Classification Report:")
print(classification_report(y_test, y_pred, target_names=label_encoder.classes_))

# 🧪 Predict on existing data (TCS) for verification
tcs_df = combined_df[combined_df['Stock'] == 'TCS'].copy()
tcs_df['Predicted_Signal'] = label_encoder.inverse_transform(model.predict(tcs_df[features]))

print("\n📍 Sample Predictions on TCS:")
print(tcs_df[['Date', 'RSI', '20DMA', '50DMA', 'Close', 'Signal', 'Predicted_Signal']].tail(10))

# 🆕 Inference on new daily data
new_data_path = "new_data.csv"
if os.path.exists(new_data_path):
    new_df = pd.read_csv(new_data_path)
    print("\n📅 Predicting on new_data.csv...")

    # Drop rows with missing values
    new_df.dropna(subset=features, inplace=True)

    # Predict using trained model
    new_predictions = model.predict(new_df[features])
    new_df['Predicted_Signal'] = label_encoder.inverse_transform(new_predictions)

    print("\n📢 New Data Predictions:")
    print(new_df[['Date', 'RSI', '20DMA', '50DMA', 'Close', 'Predicted_Signal']].tail(10))

    # Save predictions
    new_df.to_csv("predicted_new_data.csv", index=False)
else:
    print("⚠️ new_data.csv not found. Skipping prediction on new data.")
