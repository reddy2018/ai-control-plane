# Purpose:

# Structured, auditable plan

# Reasoning agent output

# Ready for human approval

from typing import List
from pydantic import BaseModel
from datetime import datetime


class FixStepSchema(BaseModel):
    description: str       # e.g., "Increase memory limit from 512Mi -> 1Gi"
    risk: str              # low / medium / high
    rollback_available: bool = True


class PlanSchema(BaseModel):
    steps: List[FixStepSchema] = []
    proposed_at: datetime
