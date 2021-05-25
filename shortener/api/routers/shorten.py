import re

import structlog
from fastapi import APIRouter, Depends, HTTPException, Response

from ...settings import URL_REGEX
from ...shortener import Shortener
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
async def shorten(url: str, shortener: Shortener = Depends(get_shortener)):
    LOG.info("api.shorten.received")
    if not re.match(URL_REGEX, url):
        raise HTTPException(status_code=422, detail="Invalid URL")
    short_url = await shortener.shorten(url)
    LOG.info("api.shorten.done", short_url=short_url)
    return Response(content=short_url, media_type="text/plain")
