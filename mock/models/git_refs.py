from pydantic import Field

from .base import ApiPath, BaseApiModel


class ApiRefCommit(BaseApiModel):
    """Git reference commit model for API responses."""

    sha: str
    type: str
    url: ApiPath


class ApiRef(BaseApiModel):
    """Git reference model for API responses."""

    ref: str
    node_id: str = ""
    url: ApiPath
    object: ApiRefCommit = Field(alias="object")


class CreateARef(BaseApiModel):
    """Model for creating a Git reference."""

    ref: str
    sha: str


class UpdateARef(BaseApiModel):
    """Model for updating a Git reference."""

    sha: str
    force: bool = False
