from typing import List

from app.clients.kubernetes import K8sClient
from app.schemas.signals import PodState


class K8sAgent:
    """
    Collects Kubernetes cluster state (pods).
    """

    def __init__(self, client: K8sClient):
        self.client = client

    def collect(self) -> List[PodState]:
        """
        Collect pod states from all namespaces.
        """
        pods = self.client.list_pods()
        states: List[PodState] = []

        for pod in pods:
            states.append(
                PodState(
                    name=pod["name"],
                    namespace=pod["namespace"],
                    status=pod["status"],
                    restarts=pod["restarts"],
                    node=pod.get("node"),
                )
            )

        return states
