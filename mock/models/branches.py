from typing import Dict, List, Optional

from .base import ApiPath, BaseApiModel


class ApiBranchCommit(BaseApiModel):
    """Branch commit model for API responses."""

    sha: str


class ApiBranchForList(BaseApiModel):
    """Branch model for list API responses."""

    name: str
    commit: ApiBranchCommit


class ApiBranchProtectionStatus(BaseApiModel):
    """Branch protection status model for API responses."""

    url: Optional[ApiPath] = None
    enforcement_level: str
    contexts: List[str]
    contexts_url: Optional[ApiPath] = None


class ApiBranchProtection(BaseApiModel):
    """Branch protection model for API responses."""

    url: Optional[ApiPath] = None
    enabled: bool
    required_status_checks: Optional[ApiBranchProtectionStatus] = None


class ApiBranch(BaseApiModel):
    """Branch model for API responses."""

    name: str
    commit: ApiBranchCommit
    protection: ApiBranchProtection
    _links: Dict[str, ApiPath]


class ApiBranchForHeadCommit(BaseApiModel):
    """Branch model for head commit API responses."""

    name: str
    commit: ApiBranchCommit
    protected: bool


class BranchProtectionUpdateRequest(BaseApiModel):
    """Model for updating branch protection."""

    enabled: bool
    required_status_checks: Optional[ApiBranchProtectionStatus] = None


class ApiBranchProtectionUpdate(BaseApiModel):
    """Model for updating branch protection."""

    protection: BranchProtectionUpdateRequest
