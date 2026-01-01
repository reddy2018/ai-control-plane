# app/agents/logs.py
from pydantic import BaseModel
from typing import List
from app.clients.loki import LokiClient

class LogSignal(BaseModel):
    timestamp: int
    message: str
    labels: dict

class LogsSignals(BaseModel):
    metrics: List[dict] = []
    logs: List[LogSignal] = []
    k8s_state: List[dict] = []

class LogsAgent:
    def __init__(self, client: LokiClient):
        self.client = client

    def collect_logs(self, query: str, start_sec: int, end_sec: int) -> LogsSignals:
        logs_data = self.client.query_range(query, start_sec, end_sec, limit=200)
        logs = [LogSignal(timestamp=log["timestamp"], message=log["message"], labels=log["labels"])
                for log in logs_data]
        return LogsSignals(logs=logs)
