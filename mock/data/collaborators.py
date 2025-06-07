from typing import Dict, List, Optional, Tuple

from data.users import USERS

# Repository collaborator data
# Format: {repo_key: {username: permission}}
REPOSITORY_COLLABORATORS = {
    "admin/repo1": {"admin": "ADMIN", "user1": "DEVELOPER"},
    "user1/repo2": {"user1": "ADMIN", "admin": "GUEST"},
    "org1/repo3": {"admin": "ADMIN", "user1": "DEVELOPER"},
}


def get_repository_collaborators(owner: str, repo_name: str) -> Optional[List[Dict]]:
    """Get collaborators for a repository"""
    repo_key = f"{owner}/{repo_name}"
    if repo_key not in REPOSITORY_COLLABORATORS:
        return None

    collaborators = []
    for username, permission in REPOSITORY_COLLABORATORS[repo_key].items():
        if username in USERS:
            collaborators.append(USERS[username])

    return collaborators


def check_collaborator(owner: str, repo_name: str, username: str) -> bool:
    """Check if user is a repository collaborator"""
    repo_key = f"{owner}/{repo_name}"
    if repo_key not in REPOSITORY_COLLABORATORS:
        return False

    return username in REPOSITORY_COLLABORATORS[repo_key]


def get_collaborator_permission(
    owner: str, repo_name: str, username: str
) -> Optional[Tuple[str, Dict]]:
    """Get collaborator permissions"""
    repo_key = f"{owner}/{repo_name}"
    if (
        repo_key not in REPOSITORY_COLLABORATORS
        or username not in REPOSITORY_COLLABORATORS[repo_key]
    ):
        return None

    if username not in USERS:
        return None

    permission = REPOSITORY_COLLABORATORS[repo_key][username]
    return (permission, USERS[username])


def add_collaborator(
    owner: str, repo_name: str, username: str, permission: str
) -> bool:
    """Add a collaborator"""
    repo_key = f"{owner}/{repo_name}"

    # Fail if repository does not exist
    if repo_key not in REPOSITORY_COLLABORATORS:
        REPOSITORY_COLLABORATORS[repo_key] = {}

    # Fail if user does not exist
    if username not in USERS:
        return False

    # Set permissions
    REPOSITORY_COLLABORATORS[repo_key][username] = permission
    return True


def remove_collaborator(owner: str, repo_name: str, username: str) -> bool:
    """Remove a collaborator"""
    repo_key = f"{owner}/{repo_name}"

    # Fail if repository does not exist
    if repo_key not in REPOSITORY_COLLABORATORS:
        return False

    # Fail if user is not a collaborator
    if username not in REPOSITORY_COLLABORATORS[repo_key]:
        return False

    # Remove collaborator
    del REPOSITORY_COLLABORATORS[repo_key][username]
    return True
