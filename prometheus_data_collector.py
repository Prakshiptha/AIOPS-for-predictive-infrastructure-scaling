#prometheus_Data_collector.py
import time
import requests
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from datetime import datetime

PROMETHEUS_URL = "http://localhost:9090"
METRICS = {
    "request_rate": 'rate(http_requests_total[1m])',
    "cpu_usage": 'rate(container_cpu_usage_seconds_total[1m])',
    "memory_usage": 'container_memory_usage_bytes',
    "net_rx": 'rate(container_network_receive_bytes_total[1m])',
    "net_tx": 'rate(container_network_transmit_bytes_total[1m])'
}

PARQUET_FILE = "traffic_data.parquet"

def query_prometheus(metric):
    response = requests.get(f"{PROMETHEUS_URL}/api/v1/query", params={"query": metric})
    response.raise_for_status()
    results = response.json()["data"]["result"]
    return results

def collect_metrics():
    timestamp = datetime.utcnow()
    data = {"timestamp": timestamp}

    for key, query in METRICS.items():
        try:
            result = query_prometheus(query)
            value = float(result[0]['value'][1]) if result else 0.0
        except Exception as e:
            print(f"Error collecting {key}: {e}")
            value = 0.0
        data[key] = value

    return pd.DataFrame([data])

def append_to_parquet(df, file_path):
    table = pa.Table.from_pandas(df)
    try:
        existing = pq.read_table(file_path)
        combined = pa.concat_tables([existing, table])
    except FileNotFoundError:
        combined = table
    pq.write_table(combined, file_path)

def main():
    while True:
        df = collect_metrics()
        append_to_parquet(df, PARQUET_FILE)
        print(f"[{datetime.utcnow()}] Collected and stored: {df.to_dict('records')[0]}")
        time.sleep(60)

if __name__ == "__main__":
    main()
