"""
Pull Request models for GitBucket API mock.

IMPORTANT: GitBucket's Pull Request API has implementation issues:

1. Merge Status Check Issue:
   - GitBucket's checkConflict() checks merge POSSIBILITY, not merge STATUS
   - GET /pulls/:id/merge returns 204 for mergeable, conflicted, AND actually merged PRs
   - Cannot reliably determine if a PR is actually merged using the API

2. This affects the reliability of merge status information.

This implementation follows GitBucket's actual (flawed) API behavior.
"""

from datetime import datetime
from typing import List, Optional

from .base import ApiPath, BaseApiModel
from .labels import ApiLabel
from .repositories import ApiRepository
from .users import ApiUser


class ApiPullRequestCommit(BaseApiModel):
    """Pull request commit model for API responses."""

    sha: str
    ref: str
    repo: ApiRepository

    @property
    def label(self) -> str:
        """Get the label for the commit."""
        base_owner = self.repo.owner.login
        return (
            f"{base_owner}:{self.ref}"
            if base_owner != self.repo.owner.login
            else self.ref
        )

    @property
    def user(self) -> ApiUser:
        """Get the user for the commit."""
        return self.repo.owner


class ApiPullRequest(BaseApiModel):
    """Pull request model for API responses."""

    number: int
    state: str
    updated_at: datetime
    created_at: datetime
    head: ApiPullRequestCommit
    base: ApiPullRequestCommit
    mergeable: Optional[bool] = None
    merged: bool
    merged_at: Optional[datetime] = None
    merged_by: Optional[ApiUser] = None
    title: str
    body: str
    user: ApiUser
    labels: List[ApiLabel]
    assignees: List[ApiUser]
    draft: Optional[bool] = None
    id: int = 0
    assignee: Optional[ApiUser] = None
    html_url: ApiPath
    url: ApiPath
    commits_url: ApiPath
    review_comments_url: ApiPath
    review_comment_url: ApiPath
    comments_url: ApiPath
    statuses_url: ApiPath


class CreateAPullRequest(BaseApiModel):
    """Model for creating a pull request.

    This API supports two ways to create a pull request:

    1. Create a new pull request with title and body:
       - title: Required. The title of the pull request
       - head: Required. The name of the branch where your changes are implemented
       - base: Required. The name of the branch you want the changes pulled into
       - body: Optional. The contents of the pull request
       - maintainer_can_modify: Optional. Whether maintainers can modify the pull request
       - draft: Optional. Whether to create a draft pull request

    2. Create a pull request from an existing issue:
       - issue: Required. The issue number to convert to a pull request
       - head: Required. The name of the branch where your changes are implemented
       - base: Required. The name of the branch you want the changes pulled into
       - maintainer_can_modify: Optional. Whether maintainers can modify the pull request

    Note: When using method 2 (issue field), the title and body fields should be omitted
    as they will be taken from the existing issue.
    """

    # Method 1: Create new pull request
    title: Optional[str] = None
    body: Optional[str] = None
    draft: Optional[bool] = None

    # Method 2: Create from existing issue
    issue: Optional[int] = None

    # Common fields for both methods
    head: str
    base: str
    maintainer_can_modify: Optional[bool] = None


class UpdateAPullRequest(BaseApiModel):
    """Model for updating a pull request."""

    title: Optional[str] = None
    body: Optional[str] = None
    state: Optional[str] = None
    base: Optional[str] = None
    maintainer_can_modify: Optional[bool] = None


class MergeAPullRequest(BaseApiModel):
    """Model for merging a pull request."""

    commit_title: Optional[str] = None
    commit_message: Optional[str] = None
    merge_method: Optional[str] = None


class SuccessToMergePrResponse(BaseApiModel):
    """Response model for successful pull request merge."""

    sha: str
    merged: bool
    message: str


class FailToMergePrResponse(BaseApiModel):
    """Response model for failed pull request merge."""

    documentation_url: str
    message: str
