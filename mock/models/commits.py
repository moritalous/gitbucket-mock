from datetime import datetime
from typing import List, Optional

from .base import ApiPath, BaseApiModel
from .repositories import ApiRepository
from .users import ApiUser


class ApiPersonIdent(BaseApiModel):
    """Person identification model for API responses."""

    name: str
    email: str
    date: datetime


class ApiCommitTree(BaseApiModel):
    """Commit tree model for API responses."""

    url: ApiPath
    sha: str


class ApiCommitStats(BaseApiModel):
    """Commit stats model for API responses."""

    additions: int
    deletions: int
    total: int


class ApiCommitFile(BaseApiModel):
    """Commit file model for API responses."""

    filename: str
    additions: int
    deletions: int
    changes: int
    status: str
    raw_url: ApiPath
    blob_url: ApiPath
    patch: str


class ApiCommitDetail(BaseApiModel):
    """Commit detail model for API responses."""

    url: ApiPath
    author: ApiPersonIdent
    committer: ApiPersonIdent
    message: str
    comment_count: int
    tree: ApiCommitTree


class ApiCommits(BaseApiModel):
    """Commit model for API responses."""

    url: ApiPath
    sha: str
    html_url: ApiPath
    comment_url: ApiPath
    commit: ApiCommitDetail
    author: ApiUser
    committer: ApiUser
    parents: List[ApiCommitTree]
    stats: ApiCommitStats
    files: List[ApiCommitFile]


class ApiCommitListItem(BaseApiModel):
    """Commit list item model for API responses."""

    sha: str
    commit: ApiCommitDetail
    url: ApiPath
    html_url: ApiPath
    comments_url: ApiPath
    author: Optional[ApiUser] = None
    committer: Optional[ApiUser] = None
    parents: List[ApiCommitTree]


class ApiCommitStatus(BaseApiModel):
    """Commit status model for API responses."""

    created_at: datetime
    updated_at: datetime
    state: str
    target_url: Optional[str] = None
    description: Optional[str] = None
    id: int
    context: str
    creator: ApiUser
    url: ApiPath


class ApiCombinedCommitStatus(BaseApiModel):
    """Combined commit status model for API responses."""

    state: str
    sha: str
    total_count: int
    statuses: List[ApiCommitStatus]
    repository: ApiRepository
    url: ApiPath


class CreateAStatus(BaseApiModel):
    """Model for creating a commit status."""

    state: str
    context: Optional[str] = None
    target_url: Optional[str] = None
    description: Optional[str] = None

    def is_valid(self) -> bool:
        """Validate the status."""
        # Check if state is valid
        valid_states = ["pending", "success", "error", "failure"]
        if self.state not in valid_states:
            return False

        # Check target_url format and length
        if self.target_url:
            if not (
                self.target_url.startswith("http://")
                or self.target_url.startswith("https://")
            ):
                return False
            if len(self.target_url) >= 255:
                return False

        # Check context length
        if self.context and len(self.context) >= 255:
            return False

        # Check description length
        if self.description and len(self.description) >= 1000:
            return False

        return True
