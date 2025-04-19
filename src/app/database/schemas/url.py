from datetime import date
from typing import Optional

from beanie import Document


class UrlSchema(Document):
    original: str
    shortened: str
    created_at: date = date.today()
    updated_at: date = date.today()
    access_count: int = 0
    last_accessed: Optional[date] = None
