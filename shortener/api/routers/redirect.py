import re

import structlog
from fastapi import APIRouter, HTTPException, Response

from ...settings import URL_ID_REGEX
from ..dependencies import get_shortener

LOG = structlog.get_logger(__name__)
router = APIRouter()


responses = {
    404: {"description": "Short URL ID not found in database"},
    422: {"description": f"Short URL ID is invalid according to regex: {URL_ID_REGEX}"},
    200: {
        "description": "Long URL",
        "content": {
            "text/plain": {
                "example": "https://www.engadget.com/nasa-ingenuity-mars-helicopter-third-flight-202654194.html"
            }
        },
    },
}


@router.get(
    "/{url_id}",
    response_model=str,
    responses=responses,
    summary="Get long URL from the short URL",
)
async def redirect(url_id: str):
    LOG.info("api.redirect.received", url_id=url_id)
    if not re.match(URL_ID_REGEX, url_id):
        raise HTTPException(status_code=422, detail="Invalid URL ID")
    shortener = await get_shortener()
    long_url = await shortener.get_long_url(url_id)
    LOG.info("api.redirect.done", url_id=url_id, long_url=long_url)
    if long_url:
        return Response(content=long_url, media_type="text/plain")
    raise HTTPException(status_code=404, detail="URL not found")
