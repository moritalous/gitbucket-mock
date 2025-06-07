"""
Milestone models for GitBucket API mock.

IMPORTANT: GitBucket has very strict validation for milestone titles that differs from GitHub:
- Only alphanumeric characters, hyphens, plus signs, underscores, and periods allowed
- Pattern: [a-zA-Z0-9\\-\\+_.]+
- Maximum 100 characters
- NO spaces, Japanese characters, or other symbols permitted

This causes many POST/PATCH requests to fail with 404 errors in GitBucket.
"""

from datetime import datetime
from typing import Optional

from .base import ApiPath, BaseApiModel


class ApiMilestone(BaseApiModel):
    """Milestone model for API responses."""

    url: ApiPath
    html_url: ApiPath
    id: int
    number: int
    state: str
    title: str
    description: str
    open_issues: int
    closed_issues: int
    closed_at: Optional[datetime] = None
    due_on: Optional[datetime] = None


class CreateAMilestone(BaseApiModel):
    """Model for creating a milestone."""

    title: str
    state: str = "open"
    description: Optional[str] = None
    due_on: Optional[datetime] = None

    def is_valid(self) -> bool:
        """Validate the milestone according to GitBucket's strict rules.

        GitBucket's CreateAMilestone.isValid() implementation:
        - title.length <= 100
        - title.matches("[a-zA-Z0-9\\-\\+_.]+")

        This means:
        - Maximum 100 characters
        - Only alphanumeric characters, hyphens, plus signs, underscores, and periods
        - NO spaces, Japanese characters, or other symbols allowed

        This validation is stricter than GitHub's API and causes many requests to fail.
        """
        # Check title length and format (GitBucket's exact validation)
        if len(self.title) > 100 or not all(
            c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-+_."
            for c in self.title
        ):
            return False

        return True


class UpdateAMilestone(BaseApiModel):
    """Model for updating a milestone."""

    title: Optional[str] = None
    state: Optional[str] = None
    description: Optional[str] = None
    due_on: Optional[datetime] = None

    def is_valid(self) -> bool:
        """Validate the milestone according to GitBucket's strict rules.

        GitBucket's CreateAMilestone.isValid() implementation:
        - title.length <= 100
        - title.matches("[a-zA-Z0-9\\-\\+_.]+")

        This means:
        - Maximum 100 characters
        - Only alphanumeric characters, hyphens, plus signs, underscores, and periods
        - NO spaces, Japanese characters, or other symbols allowed

        This validation is stricter than GitHub's API and causes many requests to fail.
        """
        # Check title length and format if provided (GitBucket's exact validation)
        if self.title and (
            len(self.title) > 100
            or not all(
                c
                in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-+_."
                for c in self.title
            )
        ):
            return False

        return True
