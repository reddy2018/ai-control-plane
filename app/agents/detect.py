from datetime import datetime
from typing import List

from app.agents.metrics import MetricsAgent
from app.agents.k8s import K8sAgent
from app.schemas.signals import PodState, ProblemSignal


class DetectAgent:
    """
    Detects problems from collected signals.
    """

    def __init__(self, metrics_agent: MetricsAgent, k8s_agent: K8sAgent):
        self.metrics_agent = metrics_agent
        self.k8s_agent = k8s_agent

    def run_detection(self) -> List[ProblemSignal]:
        problems: List[ProblemSignal] = []

        problems.extend(self._detect_pod_issues())

        # Metrics detection can be added later safely
        return problems

    def _detect_pod_issues(self) -> List[ProblemSignal]:
        problems: List[ProblemSignal] = []

        pods: List[PodState] = self.k8s_agent.collect()

        for pod in pods:
            if pod.status != "Running" or pod.restarts > 0:
                problems.append(
                    ProblemSignal(
                        source="k8s",
                        type="pod_issue",
                        description=(
                            f"Pod {pod.name} in {pod.namespace} "
                            f"is {pod.status} with {pod.restarts} restarts"
                        ),
                        timestamp=datetime.utcnow().isoformat(),
                    )
                )

        return problems
