from typing import Optional

from pydantic import BaseModel
from pydantic_core import Url


class ShortenBody(BaseModel):
    url: Url


class RequestParams(BaseModel):
    token: str


class EndpointResponse(BaseModel):
    success: bool
    url: str | None
    error: Optional[str]
