from datetime import datetime
from typing import Optional

from .base import ApiPath, BaseApiModel


class ApiUser(BaseApiModel):
    """User model for API responses."""

    login: str
    id: int = 0
    node_id: Optional[str] = None
    avatar_url: ApiPath
    gravatar_id: Optional[str] = None
    url: ApiPath
    html_url: ApiPath
    followers_url: Optional[ApiPath] = None
    following_url: Optional[ApiPath] = None
    gists_url: Optional[ApiPath] = None
    starred_url: Optional[ApiPath] = None
    subscriptions_url: Optional[ApiPath] = None
    organizations_url: Optional[ApiPath] = None
    repos_url: Optional[ApiPath] = None
    events_url: Optional[ApiPath] = None
    received_events_url: Optional[ApiPath] = None
    type: str
    site_admin: bool
    name: Optional[str] = None
    company: Optional[str] = None
    blog: Optional[str] = None
    location: Optional[str] = None
    email: str
    hireable: Optional[bool] = None
    bio: Optional[str] = None
    twitter_username: Optional[str] = None
    public_repos: Optional[int] = None
    public_gists: Optional[int] = None
    followers: Optional[int] = None
    following: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    suspended: Optional[bool] = None


class CreateAUser(BaseApiModel):
    """Model for creating a new user."""

    login: str
    password: str
    email: str
    fullName: Optional[str] = None
    isAdmin: Optional[bool] = None
    description: Optional[str] = None
    url: Optional[str] = None

    def is_valid(self) -> bool:
        """Validate the user creation data."""
        # Check login format and length
        if (
            len(self.login) < 1
            or len(self.login) > 39
            or not self.login.replace("-", "").replace("_", "").isalnum()
        ):
            return False

        # Check password length
        if len(self.password) < 1:
            return False

        # Check email format (basic validation)
        if "@" not in self.email or "." not in self.email.split("@")[-1]:
            return False

        # Check URL format if provided
        if self.url and not (
            self.url.startswith("http://") or self.url.startswith("https://")
        ):
            return False

        return True


class UpdateAUser(BaseApiModel):
    """Model for updating a user."""

    name: Optional[str] = None
    email: Optional[str] = None
    blog: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    hireable: Optional[bool] = None
    bio: Optional[str] = None

    def is_valid(self) -> bool:
        """Validate the user update data."""
        # Check email format if provided
        if self.email and (
            "@" not in self.email or "." not in self.email.split("@")[-1]
        ):
            return False

        # Check blog URL format if provided
        if self.blog and not (
            self.blog.startswith("http://") or self.blog.startswith("https://")
        ):
            return False

        return True
