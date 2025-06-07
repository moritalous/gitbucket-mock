from datetime import datetime
from typing import List, Optional

from data.users import USERS

# Repository data
REPOSITORIES = {
    "admin/repo1": {
        "name": "repo1",
        "full_name": "admin/repo1",
        "description": "Repository 1",
        "watchers": 2,
        "forks": 1,
        "private": False,
        "default_branch": "main",
        "owner": USERS["admin"],
        "has_issues": True,
        "id": 1001,
        "forks_count": 1,
        "watchers_count": 2,
        "url": "/api/v3/repos/admin/repo1",
        "clone_url": "https://example.com/admin/repo1.git",
        "html_url": "/admin/repo1",
        "ssh_url": "git@example.com:admin/repo1.git",
    },
    "user1/repo2": {
        "name": "repo2",
        "full_name": "user1/repo2",
        "description": "Repository 2",
        "watchers": 1,
        "forks": 0,
        "private": False,
        "default_branch": "main",
        "owner": USERS["user1"],
        "has_issues": True,
        "id": 1002,
        "forks_count": 0,
        "watchers_count": 1,
        "url": "/api/v3/repos/user1/repo2",
        "clone_url": "https://example.com/user1/repo2.git",
        "html_url": "/user1/repo2",
        "ssh_url": "git@example.com:user1/repo2.git",
    },
    "org1/repo3": {
        "name": "repo3",
        "full_name": "org1/repo3",
        "description": "Repository 3",
        "watchers": 3,
        "forks": 2,
        "private": False,
        "default_branch": "main",
        "owner": {
            "login": "org1",
            "id": 101,
            "email": "org1@example.com",
            "type": "Organization",
            "site_admin": False,
            "created_at": datetime(2023, 1, 5),
            "url": "/api/v3/users/org1",
            "html_url": "/org1",
            "avatar_url": "/org1/avatar",
        },
        "has_issues": True,
        "id": 1003,
        "forks_count": 2,
        "watchers_count": 3,
        "url": "/api/v3/repos/org1/repo3",
        "clone_url": "https://example.com/org1/repo3.git",
        "html_url": "/org1/repo3",
        "ssh_url": "git@example.com:org1/repo3.git",
    },
}

# Repository tag data
REPOSITORY_TAGS = {
    "admin/repo1": [
        {
            "name": "v1.0.0",
            "commit": {
                "sha": "abcdef1234567890",
                "url": "/api/v3/repos/admin/repo1/commits/abcdef1234567890",
            },
            "zipball_url": "/api/v3/repos/admin/repo1/zipball/v1.0.0",
            "tarball_url": "/api/v3/repos/admin/repo1/tarball/v1.0.0",
        }
    ],
    "user1/repo2": [],
    "org1/repo3": [
        {
            "name": "v1.0.0",
            "commit": {
                "sha": "1234567890abcdef",
                "url": "/api/v3/repos/org1/repo3/commits/1234567890abcdef",
            },
            "zipball_url": "/api/v3/repos/org1/repo3/zipball/v1.0.0",
            "tarball_url": "/api/v3/repos/org1/repo3/tarball/v1.0.0",
        },
        {
            "name": "v1.1.0",
            "commit": {
                "sha": "234567890abcdef1",
                "url": "/api/v3/repos/org1/repo3/commits/234567890abcdef1",
            },
            "zipball_url": "/api/v3/repos/org1/repo3/zipball/v1.1.0",
            "tarball_url": "/api/v3/repos/org1/repo3/tarball/v1.1.0",
        },
    ],
}

# Repository file contents
REPOSITORY_CONTENTS = {
    "admin/repo1": {
        "README.md": "# Repository 1\n\nThis is a test repository.",
        "file.txt": "This is a test file.",
    },
    "user1/repo2": {"README.md": "# Repository 2\n\nThis is another test repository."},
    "org1/repo3": {
        "README.md": "# Repository 3\n\nThis is an organization repository.",
        "src/main.py": "print('Hello, World!')",
    },
}


def get_repository(owner: str, repo_name: str) -> Optional[dict]:
    """Get repository by owner and repository name"""
    repo_key = f"{owner}/{repo_name}"
    return REPOSITORIES.get(repo_key)


def get_user_repositories(username: str) -> List[dict]:
    """Get repositories for a user"""
    return [
        repo
        for repo_key, repo in REPOSITORIES.items()
        if repo_key.startswith(f"{username}/")
    ]


def get_organization_repositories(org_name: str) -> List[dict]:
    """Get repositories for an organization"""
    return [
        repo
        for repo_key, repo in REPOSITORIES.items()
        if repo_key.startswith(f"{org_name}/")
    ]


def get_all_public_repositories() -> List[dict]:
    """Get all public repositories"""
    return [repo for repo in REPOSITORIES.values() if not repo["private"]]


def create_repository(owner: str, repo_data: dict) -> Optional[dict]:
    """Create a new repository"""
    repo_name = repo_data["name"]
    repo_key = f"{owner}/{repo_name}"

    if repo_key in REPOSITORIES:
        return None

    # Get owner information
    from data.organizations import get_organization_by_name
    from data.users import get_user_by_username

    owner_info = get_user_by_username(owner) or get_organization_by_name(owner)
    if not owner_info:
        return None

    # Create new repository
    new_repo = {
        "name": repo_name,
        "full_name": repo_key,
        "description": repo_data.get("description", ""),
        "watchers": 0,
        "forks": 0,
        "private": repo_data.get("private", False),
        "default_branch": "main",
        "owner": owner_info,
        "has_issues": True,
        "id": len(REPOSITORIES) + 1001,
        "forks_count": 0,
        "watchers_count": 0,
        "url": f"/api/v3/repos/{repo_key}",
        "clone_url": f"https://example.com/{repo_key}.git",
        "html_url": f"/{repo_key}",
        "ssh_url": f"git@example.com:{repo_key}.git",
    }

    REPOSITORIES[repo_key] = new_repo

    # Create initial content (if auto_init is True)
    if repo_data.get("auto_init", False):
        if repo_key not in REPOSITORY_CONTENTS:
            REPOSITORY_CONTENTS[repo_key] = {}

        REPOSITORY_CONTENTS[repo_key]["README.md"] = (
            f"# {repo_name}\n\n{repo_data.get('description', '')}"
        )

    # Initialize empty list for tags
    if repo_key not in REPOSITORY_TAGS:
        REPOSITORY_TAGS[repo_key] = []

    return new_repo


def get_repository_tags(owner: str, repo_name: str) -> Optional[List[dict]]:
    """Get tags for a repository"""
    repo_key = f"{owner}/{repo_name}"
    if repo_key not in REPOSITORIES:
        return None

    return REPOSITORY_TAGS.get(repo_key, [])
