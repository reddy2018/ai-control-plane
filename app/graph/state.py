# cluster diagnosis state
# Agents never overwrite each other

# Each agent writes only to signals or detected_problems

# Reasoning agent consumes signals

# Produces detected_problems + proposed_plan

# Approval and execution are separate

# Safe human-in-the-loop

# Time windows everywhere

# Ensures auditability and reproducibility

# Structured facts

# No free-form text except evidence and description

# The state will include:

# Cluster Scope

# Namespaces, services, workloads

# Time window for analysis

# Signals / Facts

# Metrics → Prometheus

# Logs → Loki

# K8s state → pods, nodes, events

# Detected Problems

# Type, severity, evidence

# Proposed Fix / Plan

# Steps to fix

# Risk level

# Optional rollback info

# Approval Status

# Pending / approved / rejected

# Approver info (once we integrate approval API)

# Execution Result

# Success / failure of applied fixes

from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

# ----------------------------------------
# signals / Facts
# ----------------------------------------

class MetricSignal(BaseModel):
    name: str
    value: float
    threshold: Optional[float] = None
    timestamp: datetime
    
class LogSignal(BaseModel):
    level: str # e.g: ERROR, WARN
    message: str
    timestamp: datetime
    
class K8sSignal(BaseModel):
    resource_type: str # e.g: pod, node
    name: str
    namespace: str
    status: str
    timestamp: datetime
    
class Signals(BaseModel):
    metrics: List[MetricSignal] = []
    logs: List[LogSignal] = []
    k8s_state: List[K8sSignal] = []
    
# -----------------------------
# Detected Problems
# -----------------------------
class Problem(BaseModel):
    type: str  # e.g., "OOMKill", "HighLatency"
    severity: str  # e.g., "low", "medium", "high"
    evidence: List[str]  # human-readable reasoning / references
    detected_at: datetime
    
# -----------------------------
# Proposed Plan / Fix
# -----------------------------
class FixStep(BaseModel):
    description: str  # e.g., "Increase memory limit from 512Mi -> 1Gi"
    risk: str  # low / medium / high
    rollback_available: bool = True


class Plan(BaseModel):
    steps: List[FixStep] = []
    proposed_at: datetime

# -----------------------------
# Approval Status
# -----------------------------
class Approval(BaseModel):
    status: str = "pending"  # pending / approved / rejected
    approver: Optional[str] = None
    approved_at: Optional[datetime] = None


# -----------------------------
# Execution Result
# -----------------------------
class ExecutionResult(BaseModel):
    success: bool = False
    applied_at: Optional[datetime] = None
    details: Optional[str] = None


# -----------------------------
# Full Diagnosis State
# -----------------------------
class DiagnosisState(BaseModel):
    cluster: str
    namespaces: List[str] = []
    services: List[str] = []
    time_window_start: datetime
    time_window_end: datetime

    signals: Signals = Signals()
    detected_problems: List[Problem] = []
    proposed_plan: Optional[Plan] = None
    approval: Optional[Approval] = None
    execution_result: Optional[ExecutionResult] = None