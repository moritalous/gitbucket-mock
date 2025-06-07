from datetime import datetime
from typing import Optional

from .base import ApiPath, BaseApiModel


class ApiGroup(BaseApiModel):
    """Organization model for API responses."""

    login: str
    description: Optional[str] = None
    created_at: datetime
    id: int = 0
    url: ApiPath
    html_url: ApiPath
    avatar_url: ApiPath


class CreateAGroup(BaseApiModel):
    """Model for creating a new organization."""

    login: str
    admin: str
    profile_name: Optional[str] = None
    url: Optional[str] = None
