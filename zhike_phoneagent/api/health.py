from typing import Any

from fastapi import APIRouter

from zhike_phoneagent.version import APP_VERSION

router = APIRouter(prefix="/api", tags=["health"])


@router.get("/health")
async def health_check() -> dict[str, Any]:
    return {
        "status": "healthy",
        "version": APP_VERSION,
    }
