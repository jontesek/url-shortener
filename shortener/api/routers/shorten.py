import re

import structlog
from fastapi import APIRouter, HTTPException

from ...settings import URL_REGEX
from ..dependencies import get_shortener

LOG = structlog.get_logger(__name__)
router = APIRouter()

responses = {
    422: {"description": f"Input URL is invalid according to regex: `{URL_REGEX}`"},
    200: {
        "description": "Short URL",
        "content": {"text/plain": {"example": "https://domain.com/fjo7qpd"}},
    },
}


@router.get(
    "/shorten", response_model=str, responses=responses, summary="Shorten given URL"
)
async def shorten(url: str):
    LOG.info("api.shorten.received")
    if not re.match(URL_REGEX, url):
        raise HTTPException(status_code=422, detail="Invalid URL")
    shortener = await get_shortener()
    short_url = await shortener.shorten(url)
    LOG.info("api.shorten.done", short_url=short_url)
    return short_url
