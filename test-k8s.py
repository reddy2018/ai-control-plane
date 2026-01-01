import os
from app.clients.kubernetes import K8sClient
from app.agents.k8s import K8sAgent

# Correct path to kubeconfig in your project directory
KUBECONFIG_PATH = os.path.join(os.path.dirname(__file__), "kube-config")

client = K8sClient(kubeconfig_path=KUBECONFIG_PATH)
agent = K8sAgent(client)

try:
    signals = agent.collect_state()
    print("=== K8s State Signals ===")
    print(signals.model_dump_json(indent=2))
except Exception as e:
    print("Error collecting K8s state:", e)
