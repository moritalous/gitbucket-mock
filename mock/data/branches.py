from typing import Dict, List, Optional

# Repository branch data
# Format: {repo_key: {branch_name: branch_data}}
REPOSITORY_BRANCHES = {
    "admin/repo1": {
        "main": {
            "name": "main",
            "commit": {"sha": "abcdef1234567890abcdef1234567890abcdef12"},
            "protection": {
                "url": "/api/v3/repos/admin/repo1/branches/main/protection",
                "enabled": True,
                "required_status_checks": {
                    "url": "/api/v3/repos/admin/repo1/branches/main/protection/required_status_checks",
                    "enforcement_level": "non_admins",
                    "contexts": ["continuous-integration/jenkins"],
                    "contexts_url": "/api/v3/repos/admin/repo1/branches/main/protection/required_status_checks/contexts",
                },
            },
            "_links": {
                "self": "/api/v3/repos/admin/repo1/branches/main",
                "html": "/admin/repo1/tree/main",
            },
        },
        "develop": {
            "name": "develop",
            "commit": {"sha": "1234567890abcdef1234567890abcdef12345678"},
            "protection": {
                "url": "/api/v3/repos/admin/repo1/branches/develop/protection",
                "enabled": False,
                "required_status_checks": None,
            },
            "_links": {
                "self": "/api/v3/repos/admin/repo1/branches/develop",
                "html": "/admin/repo1/tree/develop",
            },
        },
    },
    "user1/repo2": {
        "main": {
            "name": "main",
            "commit": {"sha": "2345678901abcdef2345678901abcdef23456789"},
            "protection": {
                "url": "/api/v3/repos/user1/repo2/branches/main/protection",
                "enabled": False,
                "required_status_checks": None,
            },
            "_links": {
                "self": "/api/v3/repos/user1/repo2/branches/main",
                "html": "/user1/repo2/tree/main",
            },
        }
    },
    "org1/repo3": {
        "main": {
            "name": "main",
            "commit": {"sha": "3456789012abcdef3456789012abcdef34567890"},
            "protection": {
                "url": "/api/v3/repos/org1/repo3/branches/main/protection",
                "enabled": True,
                "required_status_checks": {
                    "url": "/api/v3/repos/org1/repo3/branches/main/protection/required_status_checks",
                    "enforcement_level": "everyone",
                    "contexts": [
                        "continuous-integration/travis",
                        "continuous-integration/jenkins",
                    ],
                    "contexts_url": "/api/v3/repos/org1/repo3/branches/main/protection/required_status_checks/contexts",
                },
            },
            "_links": {
                "self": "/api/v3/repos/org1/repo3/branches/main",
                "html": "/org1/repo3/tree/main",
            },
        },
        "feature": {
            "name": "feature",
            "commit": {"sha": "4567890123abcdef4567890123abcdef45678901"},
            "protection": {
                "url": "/api/v3/repos/org1/repo3/branches/feature/protection",
                "enabled": False,
                "required_status_checks": None,
            },
            "_links": {
                "self": "/api/v3/repos/org1/repo3/branches/feature",
                "html": "/org1/repo3/tree/feature",
            },
        },
    },
}


def get_repository_branches(owner: str, repo_name: str) -> Optional[List[Dict]]:
    """Get list of branches for a repository"""
    repo_key = f"{owner}/{repo_name}"
    if repo_key not in REPOSITORY_BRANCHES:
        return None

    branches = []
    for branch_name, branch_data in REPOSITORY_BRANCHES[repo_key].items():
        branches.append({"name": branch_name, "commit": branch_data["commit"]})

    return branches


def get_branch(owner: str, repo_name: str, branch_name: str) -> Optional[Dict]:
    """Get specific branch information"""
    repo_key = f"{owner}/{repo_name}"
    if (
        repo_key not in REPOSITORY_BRANCHES
        or branch_name not in REPOSITORY_BRANCHES[repo_key]
    ):
        return None

    return REPOSITORY_BRANCHES[repo_key][branch_name]


def get_branch_protection(
    owner: str, repo_name: str, branch_name: str
) -> Optional[Dict]:
    """Get branch protection settings"""
    branch = get_branch(owner, repo_name, branch_name)
    if branch is None:
        return None

    return branch["protection"]


def get_required_status_checks(
    owner: str, repo_name: str, branch_name: str
) -> Optional[Dict]:
    """Get required status checks for a branch"""
    protection = get_branch_protection(owner, repo_name, branch_name)
    if protection is None or not protection["enabled"]:
        return None

    return protection["required_status_checks"]


def get_required_status_check_contexts(
    owner: str, repo_name: str, branch_name: str
) -> Optional[List[str]]:
    """Get required status check contexts for a branch"""
    status_checks = get_required_status_checks(owner, repo_name, branch_name)
    if status_checks is None:
        return None

    return status_checks["contexts"]


def update_branch_protection(
    owner: str, repo_name: str, branch_name: str, protection_data: Dict
) -> Optional[Dict]:
    """Update branch protection settings"""
    repo_key = f"{owner}/{repo_name}"
    if (
        repo_key not in REPOSITORY_BRANCHES
        or branch_name not in REPOSITORY_BRANCHES[repo_key]
    ):
        return None

    branch = REPOSITORY_BRANCHES[repo_key][branch_name]

    # Update protection settings
    if "protection" in protection_data:
        protection = protection_data["protection"]
        branch["protection"]["enabled"] = protection["enabled"]

        if protection["enabled"] and "required_status_checks" in protection:
            if branch["protection"]["required_status_checks"] is None:
                branch["protection"]["required_status_checks"] = {
                    "url": f"/api/v3/repos/{owner}/{repo_name}/branches/{branch_name}/protection/required_status_checks",
                    "enforcement_level": "off",
                    "contexts": [],
                    "contexts_url": f"/api/v3/repos/{owner}/{repo_name}/branches/{branch_name}/protection/required_status_checks/contexts",
                }

            status_checks = protection["required_status_checks"]
            if "enforcement_level" in status_checks:
                branch["protection"]["required_status_checks"]["enforcement_level"] = (
                    status_checks["enforcement_level"]
                )

            if "contexts" in status_checks:
                branch["protection"]["required_status_checks"]["contexts"] = (
                    status_checks["contexts"]
                )

    return branch


def delete_branch_protection(owner: str, repo_name: str, branch_name: str) -> bool:
    """Delete branch protection settings"""
    repo_key = f"{owner}/{repo_name}"
    if (
        repo_key not in REPOSITORY_BRANCHES
        or branch_name not in REPOSITORY_BRANCHES[repo_key]
    ):
        return False

    branch = REPOSITORY_BRANCHES[repo_key][branch_name]

    # Disable protection settings
    branch["protection"]["enabled"] = False
    branch["protection"]["required_status_checks"] = None

    return True
