import requests
from datetime import datetime
from typing import List


class PrometheusClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    # This is only for testing
    def query_range(self, query: str, start: str, end: str, step: str = "30s") -> list:
        """
        Perform a range query against Prometheus.
        Disables SSL verification for internal/self-signed certs.
        """
        url = f"{self.base_url}/api/v1/query_range"
        params = {"query": query, "start": start, "end": end, "step": step}
        response = requests.get(url, params=params, verify=False)  # <--- ignore SSL
        response.raise_for_status()
        return response.json().get("data", {}).get("result", [])

    # def query_range(self, query: str, start: str, end: str, step: str = "30s") -> List[dict]:
    #     """
    #     Perform a range query against Prometheus.
    #     Returns raw results.
    #     """
    #     url = f"{self.base_url}/api/v1/query_range"
    #     params = {"query": query, "start": start, "end": end, "step": step}
    #     response = requests.get(url, params=params)
    #     response.raise_for_status()
    #     result = response.json()
    #     return result.get("data", {}).get("result", [])
    
    
    
