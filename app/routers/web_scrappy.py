import uuid
import scrapy
import multiprocessing
import os
import re
import requests
import logging
import smtplib
import ssl

from email.message import EmailMessage
from datetime import datetime, date
from typing_extensions import TypedDict
from typing import List, Annotated, Any, Union, Tuple
from pprint import pprint, pformat
from urllib.parse import urlencode, urljoin, urlparse, parse_qs, urlunparse, unquote
from fnmatch import fnmatch

from fastapi import APIRouter, Request, status, Body, HTTPException, Query, Depends
from fastapi_versioning import version
from fastapi.responses import FileResponse, JSONResponse

from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor
from scrapy.settings import Settings
from scrapy_splash import SplashRequest

from twisted.internet import asyncioreactor

from app.utils.db import get_session
from app.utils.auth import get_users


logger = logging.getLogger("EasyImovelAPI")
router = APIRouter()

prefix_dir = "/mnt/scrappers"




@router.post(
    "/get_editals",
    status_code=status.HTTP_200_OK,
    response_model=None,
)
@version(1, 0)
async def get_editals(
    request: Request,
    db = Depends(get_session),
) -> Union[List[FileResponse], HTTPException, JSONResponse]:
    # users = await get_users(db)
    # print(users)
    return JSONResponse(status_code=201, content={"detail": "ok"})