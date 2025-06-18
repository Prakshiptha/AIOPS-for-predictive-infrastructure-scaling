AIOps for Predictive Infrastructure Scaling

An AI-powered Kubernetes system that forecasts traffic using XGBoost and autoscale pods before spikes occur — improving resilience and reducing downtime. Developed a smart autoscaling solution by integrating Prometheus, Pushgateway, and a Python-based 
ML predictor to anticipate web traffic. Designed HPA with custom metrics and visualized predictions 
using Grafana for real-time infrastructure scaling.
Tech Stack
- Kubernetes (Minikube)
- Prometheus + Pushgateway
- Grafana
- Python (XGBoost)
- Node.js (Express)
- HPA + Prometheus Adapter
How It Works
1. Prometheus collects CPU, memory, request rate & network metrics.
2. Python trains an XGBoost model on the data.
3. The model predicts traffic and sends results to Prometheus via Pushgateway.
4. HPA uses Prometheus Adapter to scale pods based on predictions.
Features
- AI-driven predictive autoscaling
- Real-time monitoring via Grafana
- Proactive scaling before traffic spikes
- Resilient, self-healing architecture
