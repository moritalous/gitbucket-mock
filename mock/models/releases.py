"""
Release models for GitBucket API mock.

IMPORTANT: GitBucket's Release API differs significantly from GitHub's API:
- No Release ID concept: GitBucket uses tag names instead of release IDs
- Draft/Prerelease not supported: These fields are ignored in GitBucket
- Asset handling: Assets are identified by file_id, not asset_id
- Tag-based operations: All operations use tag names as identifiers

ASSET UPLOAD LIMITATIONS:
- GitBucket's asset upload may fail with 500 errors in restricted environments
- File system dependencies can cause upload failures
- Implementation uses request.inputStream.available() which can be unreliable

This implementation follows GitBucket's actual API behavior, including limitations.
"""

from typing import List, Optional

from .base import ApiPath, BaseApiModel
from .users import ApiUser


class ApiReleaseAsset(BaseApiModel):
    """Release asset model for API responses.

    GitBucket Specific: Uses file_id instead of GitHub's asset_id.
    """

    name: str
    size: int
    label: str
    file_id: str  # GitBucket uses file_id instead of GitHub's asset_id
    browser_download_url: ApiPath


class ApiRelease(BaseApiModel):
    """Release model for API responses.

    GitBucket Specific: No release ID field, tag_name is the primary identifier.
    """

    name: str
    tag_name: str  # Primary identifier in GitBucket (no release ID)
    body: Optional[str] = None
    author: ApiUser
    assets: List[ApiReleaseAsset]


class CreateARelease(BaseApiModel):
    """Model for creating a release.

    GitBucket Specific: draft and prerelease fields are ignored.
    """

    tag_name: str
    target_commitish: Optional[str] = None
    name: Optional[str] = None
    body: Optional[str] = None
    draft: Optional[bool] = None  # Ignored in GitBucket
    prerelease: Optional[bool] = None  # Ignored in GitBucket


class UpdateARelease(BaseApiModel):
    """Model for updating a release.

    GitBucket Specific: draft and prerelease fields are ignored.
    """

    tag_name: Optional[str] = None
    target_commitish: Optional[str] = None
    name: Optional[str] = None
    body: Optional[str] = None
    draft: Optional[bool] = None  # Ignored in GitBucket
    prerelease: Optional[bool] = None  # Ignored in GitBucket
