from fastapi import APIRouter

router = APIRouter(
    prefix="/health",
    tags=["health"],
)

@router.get("/live")
async def liveness():
    """
    Liveness probe:
    - Is the process running?
    - Should the platform restart it?
    """
    return {"status", "alive"}

@router.get("/ready")
async def readiness():
    """
    Readiness probs:
    - can the service accept traffic?
    - later we may check dependencies here
    """
    return {"status", "ready"}