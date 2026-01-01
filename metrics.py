# metrics.py
from datetime import datetime, timedelta, timezone
from app.clients.prometheus import PrometheusClient
from app.agents.metrics import MetricsAgent

# -----------------------------
# Prometheus setup
# -----------------------------
PROMETHEUS_URL = "https://prometheus.wrm.sweps-wrm4-training8.ops.swe.ops.enlab.biz"
client = PrometheusClient(base_url=PROMETHEUS_URL)
agent = MetricsAgent(client)

# -----------------------------
# Define time window
# -----------------------------
end = datetime.now(timezone.utc)          # UTC-aware datetime
start = end - timedelta(minutes=30)

# Convert to UNIX timestamps for Prometheus
start_ts = start.timestamp()
end_ts = end.timestamp()

# -----------------------------
# Collect metrics
# -----------------------------
# Collect metrics
try:
    signals = agent.collect_signals(start_ts, end_ts)
    print("=== Metrics Signals ===")
    # Pydantic v2: use model_dump_json instead of json
    print(signals.model_dump_json(indent=2))
except Exception as e:
    print("Error collecting metrics:", e)
