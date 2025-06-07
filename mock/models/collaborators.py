from .base import BaseApiModel
from .users import ApiUser


class ApiRepositoryCollaborator(BaseApiModel):
    """Collaborator model for API responses."""

    permission: str
    user: ApiUser


class AddACollaborator(BaseApiModel):
    """Model for adding a collaborator to a repository."""

    permission: str

    @property
    def role(self) -> str:
        """Convert permission to role."""
        if self.permission == "admin":
            return "ADMIN"
        elif self.permission == "push":
            return "DEVELOPER"
        elif self.permission == "pull":
            return "GUEST"
        return self.permission
