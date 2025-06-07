from typing import Optional

from pydantic import Field

from .base import ApiPath, BaseApiModel, SshPath
from .users import ApiUser


class ApiRepository(BaseApiModel):
    """Repository model for API responses."""

    name: str
    full_name: str
    description: str
    watchers: int
    forks: int
    private: bool = Field(alias="private")
    default_branch: str
    owner: ApiUser
    has_issues: bool
    id: int = 0
    forks_count: int
    watchers_count: int
    url: ApiPath
    clone_url: ApiPath
    html_url: ApiPath
    ssh_url: Optional[SshPath] = None


class CreateARepository(BaseApiModel):
    """Model for creating a new repository."""

    name: str
    description: Optional[str] = None
    private: bool = False
    auto_init: bool = False

    def is_valid(self) -> bool:
        """Validate the repository creation data."""
        # Check name format and length
        if (
            len(self.name) < 1
            or len(self.name) > 100
            or not all(c.isalnum() or c in "-_." for c in self.name)
            or self.name.startswith(".")
            or self.name.endswith(".")
        ):
            return False

        # Check description length if provided
        if self.description and len(self.description) > 350:
            return False

        return True


class ApiTag(BaseApiModel):
    """Tag model for API responses.

    Note: Tags API models are kept in repositories.py due to their close relationship
    with repository operations. If Tags API becomes more complex in the future,
    consider moving to a separate tags.py file.
    """

    name: str
    commit: "ApiTagCommit"
    zipball_url: ApiPath
    tarball_url: ApiPath


class ApiTagCommit(BaseApiModel):
    """Tag commit model for API responses."""

    sha: str
    url: ApiPath


# Resolve forward references
ApiTag.model_rebuild()
