from fastapi import APIRouter

from ..schemas import health as schemas

router = APIRouter()


@router.get("/ping", response_model=schemas.PingResponse, summary="Health check")
async def ping():
    return {"status": "pong"}
