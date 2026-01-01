# test-detect.py
from app.agents.metrics import MetricsAgent
from app.agents.k8s import K8sAgent
from app.agents.detect import DetectAgent
from app.clients.prometheus import PrometheusClient
from app.clients.kubernetes import K8sClient

# Prometheus setup (metrics agent)
prom_client = PrometheusClient("https://prometheus.wrm.sweps-wrm4-training8.ops.swe.ops.enlab.biz")
metrics_agent = MetricsAgent(prom_client)

# Kubernetes setup (k8s agent)
k8s_client = K8sClient(kubeconfig_path="./kube-config")  # path to your kubeconfig
k8s_agent = K8sAgent(k8s_client)

# DetectAgent requires both agents
detect_agent = DetectAgent(metrics_agent, k8s_agent)

# Run detection
problems = detect_agent.run_detection()
for p in problems:
    print(p.model_dump_json(indent=2))  # Pydantic v2

