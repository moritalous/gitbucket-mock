from typing import List

from .base import ApiPath, BaseApiModel


class ApiLabel(BaseApiModel):
    """Label model for API responses."""

    name: str
    color: str
    url: ApiPath


class CreateALabel(BaseApiModel):
    """Model for creating a label."""

    name: str
    color: str

    def is_valid(self) -> bool:
        """Validate the label."""
        # Check name length and format
        if (
            len(self.name) > 100
            or self.name.startswith("_")
            or self.name.startswith("-")
        ):
            return False

        # Check color format (6 character hex code)
        if len(self.color) != 6 or not all(
            c in "0123456789abcdefABCDEF" for c in self.color
        ):
            return False

        return True


class UpdateALabel(BaseApiModel):
    """Model for updating a label."""

    name: str
    color: str

    def is_valid(self) -> bool:
        """Validate the label."""
        # Check name length and format
        if (
            len(self.name) > 100
            or self.name.startswith("_")
            or self.name.startswith("-")
        ):
            return False

        # Check color format (6 character hex code)
        if len(self.color) != 6 or not all(
            c in "0123456789abcdefABCDEF" for c in self.color
        ):
            return False

        return True


class AddLabelsToAnIssue(BaseApiModel):
    """Model for adding labels to an issue."""

    labels: List[str]


class ReplaceAllLabelsForAnIssue(BaseApiModel):
    """Model for replacing all labels for an issue."""

    labels: List[str]
