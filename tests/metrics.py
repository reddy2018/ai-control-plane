from datetime import datetime, timedelta
from app.clients.prometheus import PrometheusClient
from app.agents.metrics import MetricsAgent

client = PrometheusClient(base_url="https://prometheus.wrm.sweps-wrm4-training8.ops.swe.ops.enlab.biz")
agent = MetricsAgent(client)

end = datetime.utcnow()
start = end - timedelta(minutes=30)

signals = agent.collect_signals(start.isoformat(), end.isoformat())
print(signals.json(indent=2))
