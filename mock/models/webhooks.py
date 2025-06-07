from typing import List, Optional

from .base import ApiPath, BaseApiModel


class ApiWebhookConfig(BaseApiModel):
    """Webhook config model for API responses."""

    content_type: str
    url: str


class ApiWebhook(BaseApiModel):
    """Webhook model for API responses."""

    type: str
    id: int
    name: str
    active: bool
    events: List[str]
    config: ApiWebhookConfig
    url: ApiPath


class CreateARepositoryWebhookConfig(BaseApiModel):
    """Model for webhook configuration when creating a webhook."""

    url: str
    content_type: str = "form"
    insecure_ssl: str = "0"
    secret: Optional[str] = None


class CreateARepositoryWebhook(BaseApiModel):
    """Model for creating a webhook."""

    name: str = "web"
    config: CreateARepositoryWebhookConfig
    events: List[str] = ["push"]
    active: bool = True

    def is_valid(self) -> bool:
        """Validate the webhook."""
        return self.config.content_type in ["form", "json"]


class UpdateARepositoryWebhook(BaseApiModel):
    """Model for updating a webhook."""

    name: str = "web"
    config: CreateARepositoryWebhookConfig
    events: List[str] = ["push"]
    add_events: List[str] = []
    remove_events: List[str] = []
    active: bool = True

    def is_valid(self) -> bool:
        """Validate the webhook."""
        return self.config.content_type in ["form", "json"]
