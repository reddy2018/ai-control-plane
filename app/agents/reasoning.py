# root cause + fix suggestion

# app/agents/reasoning_agent.py
from datetime import datetime, timedelta

# Assuming you have these agent modules
from app.agents.metrics_agent import get_pod_metrics
from app.agents.logs_agent import get_pod_logs

# Thresholds or rules for reasoning
RESTART_THRESHOLD = 5

def analyze_issue(issue: dict) -> dict:
    """
    Analyze a detected issue and suggest possible root causes.
    """
    pod_name = issue["description"].split()[1]  # crude parsing, e.g., "Pod kube-proxy-bh7q7 ..."
    namespace = issue["description"].split()[-1]  # last word is namespace
    restarts = int(issue["description"].split()[-2])  # number of restarts
    
    root_cause = "Unknown"
    recommendations = []

    # Rule 1: High restart count
    if restarts > RESTART_THRESHOLD:
        metrics = get_pod_metrics(pod_name, namespace, lookback_minutes=60)
        logs = get_pod_logs(pod_name, namespace, lookback_minutes=60)

        # Example logic: OOM detection
        if any(m.get("reason") == "OOMKilled" for m in metrics):
            root_cause = "OOMKilled"
            recommendations.append("Increase memory limits or check memory leaks")

        # Example logic: CrashLoop detection
        elif "CrashLoopBackOff" in logs:
            root_cause = "CrashLoopBackOff"
            recommendations.append("Check container startup probes and application logs")

        else:
            root_cause = "Frequent restarts"
            recommendations.append("Investigate pod logs and dependencies")

    else:
        root_cause = "Minor issue"
        recommendations.append("Monitor but no immediate action required")

    return {
        "pod": pod_name,
        "namespace": namespace,
        "detected_at": issue["timestamp"],
        "root_cause": root_cause,
        "recommendations": recommendations
    }

# -------------------------
# Example usage in your pipeline
if __name__ == "__main__":
    import json

    # This would be the output from your test_detect.py
    detected_issues = [
        {
            "source": "k8s",
            "type": "pod_issue",
            "description": "Pod openebs-ndm-mmvsc in openebs is Running with 17 restarts",
            "timestamp": str(datetime.now())
        }
    ]

    for issue in detected_issues:
        analysis = analyze_issue(issue)
        print(json.dumps(analysis, indent=2))
