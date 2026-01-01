# Purpose:

# Detecting problems is isolated

# Reasoning agent populates this section

# app/schemas/problems.py
from pydantic import BaseModel

class ProblemSignal(BaseModel):
    source: str        # "metrics" or "k8s"
    type: str          # metric name or "pod_issue"
    description: str
    timestamp: str
