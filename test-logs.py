from datetime import datetime, timedelta, timezone
import urllib3
from app.clients.loki import LokiClient
from app.agents.logs import LogsAgent

# Suppress SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LOKI_URL = "https://loki.wrm.sweps-wrm4-training8.ops.swe.ops.enlab.biz"
client = LokiClient(base_url=LOKI_URL)
agent = LogsAgent(client)

# Last 2 minutes
end = datetime.now(timezone.utc)
start = end - timedelta(minutes=2)

# Loki expects **nanoseconds**
start_ns = int(start.timestamp() * 1_000_000_000)
end_ns = int(end.timestamp() * 1_000_000_000)

print("start_ns:", start_ns)
print("end_ns:", end_ns)

try:
    signals = agent.collect_logs('{job=~".*"}', start_ns, end_ns)
    print("=== Logs Signals ===")
    print(signals.model_dump_json(indent=2))
except Exception as e:
    print("Error collecting logs:", e)
