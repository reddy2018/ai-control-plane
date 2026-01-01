# app/clients/kubernetes.py
from kubernetes import client, config
import os

class K8sClient:
    def __init__(self, kubeconfig_path: str):
        """
        kubeconfig_path: path to kubeconfig file.
        """
        if not os.path.exists(kubeconfig_path):
            raise FileNotFoundError(f"Kubeconfig not found: {kubeconfig_path}")
        config.load_kube_config(config_file=kubeconfig_path)
        self.v1 = client.CoreV1Api()

    def list_pods(self):
        pod_list = self.v1.list_pod_for_all_namespaces(watch=False)
        pods = []
        for pod in pod_list.items:
            pods.append({
                "name": pod.metadata.name,
                "namespace": pod.metadata.namespace,
                "status": pod.status.phase,
                "node": pod.spec.node_name,
                "restarts": sum([c.restart_count for c in pod.status.container_statuses or []])
            })
        return pods
