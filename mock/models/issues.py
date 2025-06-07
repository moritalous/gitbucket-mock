from datetime import datetime
from typing import Dict, List, Optional

from .base import ApiPath, BaseApiModel
from .labels import ApiLabel
from .milestones import ApiMilestone
from .users import ApiUser


class ApiIssue(BaseApiModel):
    """Issue model for API responses."""

    number: int
    title: str
    user: ApiUser
    assignees: List[ApiUser]
    labels: List[ApiLabel]
    state: str
    created_at: datetime
    updated_at: datetime
    body: str
    milestone: Optional[ApiMilestone] = None
    id: int = 0
    assignee: Optional[ApiUser] = None
    comments_url: ApiPath
    html_url: ApiPath
    pull_request: Optional[Dict[str, ApiPath]] = None


class CreateAnIssue(BaseApiModel):
    """Model for creating a new issue."""

    title: str
    body: Optional[str] = None
    assignees: List[str] = []
    milestone: Optional[int] = None
    labels: List[str] = []

    def is_valid(self) -> bool:
        """Validate the issue creation data."""
        # Check title length
        if len(self.title) < 1 or len(self.title) > 256:
            return False

        # Check body length if provided
        if self.body and len(self.body) > 65536:
            return False

        # Check assignees list length
        if len(self.assignees) > 10:
            return False

        # Check labels list length
        if len(self.labels) > 100:
            return False

        return True


class ApiComment(BaseApiModel):
    """Comment model for API responses."""

    id: int
    user: ApiUser
    body: str
    created_at: datetime
    updated_at: datetime
    html_url: ApiPath


class CreateAComment(BaseApiModel):
    """Model for creating a comment."""

    body: str
