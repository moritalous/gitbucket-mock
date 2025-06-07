from typing import List, Optional

from .base import ApiPath, BaseApiModel


class ApiContents(BaseApiModel):
    """Contents model for API responses.

    This model represents both files and directories in repository contents.
    The response is always an array of ApiContents objects:
    - For files: Array contains a single object with 'content' and 'encoding' fields
    - For directories: Array contains multiple objects without 'content' and 'encoding' fields

    This unified approach avoids Union types for better OpenAPI schema compatibility.
    """

    type: str  # "file" or "dir"
    name: str
    path: str
    sha: str
    content: Optional[str] = None  # Base64-encoded content, only present for files
    encoding: Optional[str] = None  # Always "base64" when present, only for files
    download_url: ApiPath


class CreateAFile(BaseApiModel):
    """Model for creating or updating a file."""

    message: str
    content: str
    sha: Optional[str] = None
    branch: Optional[str] = None
    committer: Optional["ApiPusher"] = None
    author: Optional["ApiPusher"] = None


class ApiPusher(BaseApiModel):
    """Pusher model for API responses."""

    name: str
    email: str


class ApiCommit(BaseApiModel):
    """Commit model for file creation/update API responses."""

    sha: str
    url: ApiPath
    html_url: ApiPath
    author: ApiPusher
    committer: ApiPusher
    message: str
    tree: "ApiCommitTree"
    parents: List["ApiCommitParent"]


class ApiCommitTree(BaseApiModel):
    """Commit tree model for file creation/update API responses."""

    sha: str
    url: ApiPath


class ApiCommitParent(BaseApiModel):
    """Commit parent model for file creation/update API responses."""

    sha: str
    url: ApiPath
    html_url: ApiPath


# Resolve forward references

CreateAFile.model_rebuild()
ApiCommit.model_rebuild()
