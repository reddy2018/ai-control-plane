from datetime import datetime, timezone
from typing import List

from app.clients.prometheus import PrometheusClient
from app.schemas.signals import MetricSignal


class MetricsAgent:
    """
    Collects metric-based signals from Prometheus.
    This agent does NOT decide problems — it only emits raw signals.
    """

    def __init__(self, client: PrometheusClient):
        self.client = client

    def collect(self, start: str, end: str) -> List[MetricSignal]:
        signals: List[MetricSignal] = []

        try:
            latency = self._fetch_latency_p95(start, end)
            signals.append(latency)
        except Exception as e:
            print(f"Error collecting latency metric: {e}")

        try:
            error_rate = self._fetch_error_rate(start, end)
            signals.append(error_rate)
        except Exception as e:
            print(f"Error collecting error rate metric: {e}")

        return signals

    def _fetch_latency_p95(self, start: str, end: str) -> MetricSignal:
        results = self.client.query_range(
            query="http_request_duration_seconds_p95",
            start=start,
            end=end,
        )

        value = self._extract_latest_value(results)

        return MetricSignal(
            name="latency_p95",
            value=value,
            threshold=None,
            timestamp=datetime.now(timezone.utc),
        )

    def _fetch_error_rate(self, start: str, end: str) -> MetricSignal:
        results = self.client.query_range(
            query='sum(rate(http_requests_total{status=~"5.."}[5m]))',
            start=start,
            end=end,
        )

        value = self._extract_latest_value(results)

        return MetricSignal(
            name="error_rate",
            value=value,
            threshold=None,
            timestamp=datetime.now(timezone.utc),
        )

    @staticmethod
    def _extract_latest_value(results: list) -> float:
        """
        Safely extract the most recent numeric value from Prometheus results.
        """
        if not results:
            return 0.0

        values = results[0].get("values", [])
        if not values:
            return 0.0

        _, value = values[-1]
        try:
            return float(value)
        except Exception:
            return 0.0
