# Purpose:

# Tracks human approval

# Decouples reasoning from execution

from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class ApprovalSchema(BaseModel):
    status: str = "pending"           # pending / approved / rejected
    approver: Optional[str] = None
    approved_at: Optional[datetime] = None
