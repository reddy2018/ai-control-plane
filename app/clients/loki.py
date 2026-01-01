# app/clients/loki.py
import requests
from typing import List, Optional

class LokiClient:
    def __init__(self, base_url: str, username: Optional[str] = None, password: Optional[str] = None):
        self.base_url = base_url.rstrip("/")
        self.auth = (username, password) if username and password else None

    def query_range(self, query: str, start_ns: int, end_ns: int, limit: int = 200) -> list:
        url = f"{self.base_url}/loki/api/v1/query_range"
        params = {
            "query": query,
            "start": start_ns,
            "end": end_ns,
            "limit": limit
        }
        response = requests.get(url, params=params, auth=self.auth, verify=False)
        response.raise_for_status()
        data = response.json().get("data", {}).get("result", [])
        logs = []
        for stream in data:
            for value in stream.get("values", []):
                ts_ns, msg = value
                logs.append({
                    "timestamp": int(ts_ns) / 1_000_000_000,  # convert ns -> seconds
                    "message": msg,
                    "labels": stream.get("stream", {})
                })
        return logs

