"""
Schémas de réponse standardisés
"""

from pydantic import BaseModel, Field
from typing import Generic, TypeVar, Optional, Any
from datetime import datetime

T = TypeVar('T')

class APIResponse(BaseModel, Generic[T]):
    success: bool
    data: Optional[T] = None
    error: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)

class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    per_page: int
    total_pages: int