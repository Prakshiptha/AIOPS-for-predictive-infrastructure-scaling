import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from xgboost import XGBRegressor
import numpy as np

# Load data
df = pd.read_parquet("traffic_data.parquet")

# Ensure correct timestamp format
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Extract time-based features
df['minute'] = df['timestamp'].dt.minute
df['hour'] = df['timestamp'].dt.hour
df['day'] = df['timestamp'].dt.day
df['weekday'] = df['timestamp'].dt.weekday

# Define features and target
features = ['minute', 'hour', 'day', 'weekday', 'cpu_usage', 'memory_usage', 'net_rx', 'net_tx']
target = 'request_rate'

X = df[features]
y = df[target]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = XGBRegressor()
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
print(f"✅ Model trained with RMSE: {rmse:.4f}")

# Save model
joblib.dump(model, "traffic_predictor.pkl")
print("✅ Model saved as traffic_predictor.pkl")
