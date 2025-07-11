import pandas as pd
from sklearn.ensemble import IsolationForest

print("🚀 MiniBuster is running...")

# Step 1: Load enhanced log file
df = pd.read_csv('system_logs.csv')
print("📊 Logs:\n", df)

# Step 2: Train model on all columns
model = IsolationForest(contamination=0.2)
model.fit(df)

# Step 3: Predict anomalies
df['anomaly'] = model.predict(df)
print("\n🤖 Detection Results:\n", df)

# Step 4: Show anomalies
anomalies = df[df['anomaly'] == -1]
print("\n🚨 ALERT: Suspicious activity detected!")
print(anomalies)

# Step 5: Save to new file
df.to_csv('minibuster_report.csv', index=False)
print("\n✅ Report saved to 'minibuster_report.csv'")

