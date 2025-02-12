import requests
import logging

from datetime import datetime, date
from typing_extensions import TypedDict
from typing import List, Annotated, Any, Union, Tuple
from pprint import pprint, pformat

from fastapi import APIRouter, Request, status, Body, HTTPException, Query, Depends
from fastapi_versioning import version
from fastapi.responses import FileResponse, JSONResponse

from app.utils.db import get_session
from app.utils.auth import get_users


logger = logging.getLogger("EasyImovelAPI")
router = APIRouter()


@router.post(
    "/post_urls",
    status_code=status.HTTP_200_OK,
    response_model=None,
)
@version(1, 0)
async def post_urls(
    request: Request,
    urls: Annotated[List[str], Body(title="Lista de URLs")],
    db = Depends(get_session),
) -> JSONResponse:

    sql = """
    INSERT INTO urls (url, platform)
    VALUES (%s, 'olx') AS alias
    ON DUPLICATE KEY UPDATE
    platform = alias.platform,
    updated_at = CURRENT_TIMESTAMP
    """
    rows_affected = await db.insertmany(sql, urls)
    rows_updated = int(rows_affected-len(urls))
    return JSONResponse(status_code=201, content={"detail": f"{rows_affected} rows were inserted successfully. {rows_updated} rows were updated successfully"})