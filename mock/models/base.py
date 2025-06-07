from pydantic import BaseModel


class ApiPath(str):
    """GitBucket API path representation."""

    def __init__(self, path: str):
        self.path = path

    def __get_pydantic_core_schema__(self, handler):
        return {"type": "str"}


class SshPath(str):
    """GitBucket SSH path representation."""

    def __init__(self, path: str):
        self.path = path

    def __get_pydantic_core_schema__(self, handler):
        return {"type": "str"}


class BaseApiModel(BaseModel):
    """Base model for all API models."""
