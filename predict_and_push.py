import time
import datetime
import joblib
import psutil
import socket
import os
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway

# === Load the trained model ===
model = joblib.load("traffic_predictor.pkl")

# === Pushgateway address ===
PUSHGATEWAY_URL = "http://localhost:9091"

# === Auto-detect current pod name and namespace ===
POD_NAME = socket.gethostname()
NAMESPACE = os.getenv("POD_NAMESPACE", "default")

# === Set up Prometheus metric registry ===
registry = CollectorRegistry()
predicted_traffic = Gauge(
    "predicted_traffic",
    "Predicted traffic load for scaling",
    ["pod", "namespace"],  # Both labels used for HPA and adapter mapping
    registry=registry
)

def predict_and_push():
    now = datetime.datetime.now()

    # System-level features
    cpu_usage = psutil.cpu_percent() / 100.0
    memory_usage = psutil.virtual_memory().used
    net_io = psutil.net_io_counters()
    net_rx = net_io.bytes_recv
    net_tx = net_io.bytes_sent

    # Time-based + system features
    features = [[
        now.minute,
        now.hour,
        now.day,
        now.weekday(),
        cpu_usage,
        memory_usage,
        net_rx,
        net_tx
    ]]

    # Make prediction
    prediction = model.predict(features)[0]
    print(f"📈 Predicted traffic: {prediction:.2f}")

    # Set metric with pod and namespace label
    predicted_traffic.labels(pod=POD_NAME, namespace=NAMESPACE).set(prediction)

    # Push to Prometheus Pushgateway
    push_to_gateway(
        PUSHGATEWAY_URL,
        job="ai_traffic_predictor",
        registry=registry
    )

if __name__ == "__main__":
    print("🚀 Starting prediction loop with rich features...")
    while True:
        predict_and_push()
        time.sleep(20)
