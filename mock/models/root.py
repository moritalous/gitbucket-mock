from typing import Optional

from .base import ApiPath, BaseApiModel


class ApiEndPoint(BaseApiModel):
    """Root endpoint model for API responses."""

    rate_limit_url: ApiPath = ApiPath("/api/v3/rate_limit")


class ApiError(BaseApiModel):
    """Error model for API responses."""

    message: str
    documentation_url: Optional[str] = None


class ApiPluginProvider(BaseApiModel):
    """Plugin provider model for API responses."""

    name: str
    url: str


class ApiPlugin(BaseApiModel):
    """Plugin model for API responses."""

    id: str
    name: str
    version: str
    description: str
    provider: ApiPluginProvider
