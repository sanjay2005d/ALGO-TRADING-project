import subprocess

print("📥 Fetching latest stock data...")
subprocess.run(["python", "data_fetcher.py"])

print("🧹 Fixing double headers...")
subprocess.run(["python", "fix_double_header_stockdata.py"])

print("📊 Applying technical indicators...")
subprocess.run(["python", "indicators_apply.py"])

print("📈 Applying rule-based strategy...")
subprocess.run(["python", "strategy3.py"])

print("🧠 Running ML signal prediction...")
subprocess.run(["python", "ML_model.py"])
#subprocess.run(["python", "livedata_and_MLpred.py"])
print("✅ Pipeline completed.")
