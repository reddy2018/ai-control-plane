from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class MetricSignal(BaseModel):
    name: str
    value: float
    threshold: Optional[float] = None
    timestamp: datetime


class LogSignal(BaseModel):
    timestamp: datetime
    message: str
    labels: dict


class PodState(BaseModel):
    name: str
    namespace: str
    status: str
    restarts: int
    node: Optional[str] = None


class ClusterSignals(BaseModel):
    """
    Aggregated signals collected from all agents.
    This is the single input to DetectAgent.
    """
    metrics: List[MetricSignal] = []
    logs: List[LogSignal] = []
    k8s_state: List[PodState] = []

class ProblemSignal(BaseModel):
    source: str                  # e.g., "k8s", "metrics", "logs"
    type: str                    # e.g., "pod_issue", "high_latency"
    description: str
    timestamp: str               # ISO format string