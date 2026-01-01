# app/main.py
import sys
from pathlib import Path
from datetime import datetime
from fastapi import FastAPI

# Add project root to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

app = FastAPI(title="AI Observability Control Plane")

# Function to import agents at runtime (Option 3)
def get_agents():
    try:
        from app.agents.k8s import detect_pod_issues
        from app.agents.reasoning import analyze_issue
        return detect_pod_issues, analyze_issue
    except Exception as e:
        print("Agent import failed:", e)  # Debug info in console
        return None, None



@app.get("/health")
def health_check():
    return {"status": "ok", "timestamp": str(datetime.now())}

@app.get("/detect-and-analyze")
def detect_and_analyze():
    detect_pod_issues, analyze_issue = get_agents()
    
    if detect_pod_issues is None or analyze_issue is None:
        return {
            "error": "Failed to load agents",
            "details": "Check imports and agent code",
            "timestamp": str(datetime.now())
        }

    # Step 1: Detect issues
    try:
        detected_issues = detect_pod_issues()
        if not detected_issues:
            return {
                "message": "No issues detected",
                "issues": [],
                "timestamp": str(datetime.now())
            }
    except Exception as e:
        return {
            "error": "Failed to detect issues",
            "details": str(e),
            "timestamp": str(datetime.now())
        }

    # Step 2: Analyze each detected issue
    analyzed_results = []
    for issue in detected_issues:
        try:
            result = analyze_issue(issue)
            analyzed_results.append(result)
        except Exception as e:
            analyzed_results.append({
                "pod": issue.get("description", "unknown"),
                "error": f"Reasoning failed: {str(e)}"
            })

    # Step 3: Return results
    return {
        "detected_count": len(detected_issues),
        "issues": analyzed_results,
        "timestamp": str(datetime.now())
    }

@app.post("/analyze-issues")
def analyze_issues(issues: list[dict]):
    detect_pod_issues, analyze_issue = get_agents()
    
    if analyze_issue is None:
        return {
            "error": "Failed to load reasoning agent",
            "timestamp": str(datetime.now())
        }

    analyzed_results = []
    for issue in issues:
        try:
            analyzed_results.append(analyze_issue(issue))
        except Exception as e:
            analyzed_results.append({
                "pod": issue.get("description", "unknown"),
                "error": f"Reasoning failed: {str(e)}"
            })

    return {
        "analyzed_count": len(analyzed_results),
        "issues": analyzed_results,
        "timestamp": str(datetime.now())
    }
