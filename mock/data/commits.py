from datetime import datetime
from typing import Dict, List, Optional

from data.users import USERS

# Repository commit data
# Format: {repo_key: {commit_sha: commit_data}}
REPOSITORY_COMMITS = {
    "admin/repo1": {
        "abcdef1234567890abcdef1234567890abcdef12": {
            "url": "/api/v3/repos/admin/repo1/commits/abcdef1234567890abcdef1234567890abcdef12",
            "sha": "abcdef1234567890abcdef1234567890abcdef12",
            "html_url": "/admin/repo1/commit/abcdef1234567890abcdef1234567890abcdef12",
            "comment_url": "/api/v3/repos/admin/repo1/commits/abcdef1234567890abcdef1234567890abcdef12/comments",
            "commit": {
                "url": "/api/v3/repos/admin/repo1/git/commits/abcdef1234567890abcdef1234567890abcdef12",
                "author": {
                    "name": "Admin User",
                    "email": "admin@example.com",
                    "date": datetime(2023, 1, 15, 10, 0, 0),
                },
                "committer": {
                    "name": "Admin User",
                    "email": "admin@example.com",
                    "date": datetime(2023, 1, 15, 10, 0, 0),
                },
                "message": "Initial commit",
                "comment_count": 0,
                "tree": {
                    "url": "/api/v3/repos/admin/repo1/git/trees/1234567890abcdef1234567890abcdef12345678",
                    "sha": "1234567890abcdef1234567890abcdef12345678",
                },
            },
            "author": USERS["admin"],
            "committer": USERS["admin"],
            "parents": [],
            "stats": {"additions": 10, "deletions": 0, "total": 10},
            "files": [
                {
                    "filename": "README.md",
                    "additions": 10,
                    "deletions": 0,
                    "changes": 10,
                    "status": "added",
                    "raw_url": "/admin/repo1/raw/abcdef1234567890abcdef1234567890abcdef12/README.md",
                    "blob_url": "/admin/repo1/blob/abcdef1234567890abcdef1234567890abcdef12/README.md",
                    "patch": "@@ -0,0 +1,10 @@\\n+# Repository 1\\n+\\n+This is a test repository.",
                }
            ],
        },
        "1234567890abcdef1234567890abcdef12345678": {
            "url": "/api/v3/repos/admin/repo1/commits/1234567890abcdef1234567890abcdef12345678",
            "sha": "1234567890abcdef1234567890abcdef12345678",
            "html_url": "/admin/repo1/commit/1234567890abcdef1234567890abcdef12345678",
            "comment_url": "/api/v3/repos/admin/repo1/commits/1234567890abcdef1234567890abcdef12345678/comments",
            "commit": {
                "url": "/api/v3/repos/admin/repo1/git/commits/1234567890abcdef1234567890abcdef12345678",
                "author": {
                    "name": "Admin User",
                    "email": "admin@example.com",
                    "date": datetime(2023, 1, 16, 11, 0, 0),
                },
                "committer": {
                    "name": "Admin User",
                    "email": "admin@example.com",
                    "date": datetime(2023, 1, 16, 11, 0, 0),
                },
                "message": "Add file.txt",
                "comment_count": 0,
                "tree": {
                    "url": "/api/v3/repos/admin/repo1/git/trees/2345678901abcdef2345678901abcdef23456789",
                    "sha": "2345678901abcdef2345678901abcdef23456789",
                },
            },
            "author": USERS["admin"],
            "committer": USERS["admin"],
            "parents": [
                {
                    "url": "/api/v3/repos/admin/repo1/git/commits/abcdef1234567890abcdef1234567890abcdef12",
                    "sha": "abcdef1234567890abcdef1234567890abcdef12",
                }
            ],
            "stats": {"additions": 1, "deletions": 0, "total": 1},
            "files": [
                {
                    "filename": "file.txt",
                    "additions": 1,
                    "deletions": 0,
                    "changes": 1,
                    "status": "added",
                    "raw_url": "/admin/repo1/raw/1234567890abcdef1234567890abcdef12345678/file.txt",
                    "blob_url": "/admin/repo1/blob/1234567890abcdef1234567890abcdef12345678/file.txt",
                    "patch": "@@ -0,0 +1 @@\\n+This is a test file.",
                }
            ],
        },
    },
    "user1/repo2": {
        "2345678901abcdef2345678901abcdef23456789": {
            "url": "/api/v3/repos/user1/repo2/commits/2345678901abcdef2345678901abcdef23456789",
            "sha": "2345678901abcdef2345678901abcdef23456789",
            "html_url": "/user1/repo2/commit/2345678901abcdef2345678901abcdef23456789",
            "comment_url": "/api/v3/repos/user1/repo2/commits/2345678901abcdef2345678901abcdef23456789/comments",
            "commit": {
                "url": "/api/v3/repos/user1/repo2/git/commits/2345678901abcdef2345678901abcdef23456789",
                "author": {
                    "name": "User 1",
                    "email": "user1@example.com",
                    "date": datetime(2023, 2, 10, 14, 0, 0),
                },
                "committer": {
                    "name": "User 1",
                    "email": "user1@example.com",
                    "date": datetime(2023, 2, 10, 14, 0, 0),
                },
                "message": "Initial commit",
                "comment_count": 0,
                "tree": {
                    "url": "/api/v3/repos/user1/repo2/git/trees/3456789012abcdef3456789012abcdef34567890",
                    "sha": "3456789012abcdef3456789012abcdef34567890",
                },
            },
            "author": USERS["user1"],
            "committer": USERS["user1"],
            "parents": [],
            "stats": {"additions": 5, "deletions": 0, "total": 5},
            "files": [
                {
                    "filename": "README.md",
                    "additions": 5,
                    "deletions": 0,
                    "changes": 5,
                    "status": "added",
                    "raw_url": "/user1/repo2/raw/2345678901abcdef2345678901abcdef23456789/README.md",
                    "blob_url": "/user1/repo2/blob/2345678901abcdef2345678901abcdef23456789/README.md",
                    "patch": "@@ -0,0 +1,5 @@\\n+# Repository 2\\n+\\n+This is another test repository.",
                }
            ],
        }
    },
}

# Commit status data
# Format: {repo_key: {commit_sha: [status_data]}}
COMMIT_STATUSES = {
    "admin/repo1": {
        "abcdef1234567890abcdef1234567890abcdef12": [
            {
                "created_at": datetime(2023, 1, 15, 10, 30, 0),
                "updated_at": datetime(2023, 1, 15, 10, 30, 0),
                "state": "success",
                "target_url": "https://ci.example.com/build/1",
                "description": "Build succeeded",
                "id": 1,
                "context": "continuous-integration/jenkins",
                "creator": USERS["admin"],
                "url": "/api/v3/repos/admin/repo1/statuses/abcdef1234567890abcdef1234567890abcdef12",
            }
        ],
        "1234567890abcdef1234567890abcdef12345678": [
            {
                "created_at": datetime(2023, 1, 16, 11, 30, 0),
                "updated_at": datetime(2023, 1, 16, 11, 30, 0),
                "state": "pending",
                "target_url": "https://ci.example.com/build/2",
                "description": "Build in progress",
                "id": 2,
                "context": "continuous-integration/jenkins",
                "creator": USERS["admin"],
                "url": "/api/v3/repos/admin/repo1/statuses/1234567890abcdef1234567890abcdef12345678",
            }
        ],
    }
}


def get_repository_commits(
    owner: str,
    repo_name: str,
    sha: Optional[str] = None,
    path: Optional[str] = None,
    author: Optional[str] = None,
    since: Optional[datetime] = None,
    until: Optional[datetime] = None,
    page: int = 1,
    per_page: int = 30,
) -> Optional[List[Dict]]:
    """Get list of commits for a repository"""
    repo_key = f"{owner}/{repo_name}"
    if repo_key not in REPOSITORY_COMMITS:
        return None

    commits = list(REPOSITORY_COMMITS[repo_key].values())

    # Filtering
    if sha:
        commits = [c for c in commits if c["sha"].startswith(sha)]

    if path:
        commits = [c for c in commits if any(f["filename"] == path for f in c["files"])]

    if author:
        commits = [
            c
            for c in commits
            if c["commit"]["author"]["email"] == author
            or (c["author"] and c["author"]["login"] == author)
        ]

    if since:
        commits = [c for c in commits if c["commit"]["author"]["date"] >= since]

    if until:
        commits = [c for c in commits if c["commit"]["author"]["date"] <= until]

    # Sort (by date, descending)
    commits.sort(key=lambda c: c["commit"]["author"]["date"], reverse=True)

    # Pagination
    start = (page - 1) * per_page
    end = start + per_page

    return commits[start:end]


def get_commit(owner: str, repo_name: str, sha: str) -> Optional[Dict]:
    """Get specific commit information"""
    repo_key = f"{owner}/{repo_name}"
    if repo_key not in REPOSITORY_COMMITS or sha not in REPOSITORY_COMMITS[repo_key]:
        return None

    return REPOSITORY_COMMITS[repo_key][sha]


def get_branches_for_head_commit(
    owner: str, repo_name: str, sha: str
) -> Optional[List[Dict]]:
    """Get branches where specific commit is HEAD"""
    from data.branches import REPOSITORY_BRANCHES

    repo_key = f"{owner}/{repo_name}"
    if repo_key not in REPOSITORY_BRANCHES:
        return None

    branches = []
    for branch_name, branch_data in REPOSITORY_BRANCHES[repo_key].items():
        if branch_data["commit"]["sha"] == sha:
            branches.append(
                {
                    "name": branch_name,
                    "commit": branch_data["commit"],
                    "protected": branch_data["protection"]["enabled"],
                }
            )

    return branches


def get_commit_statuses(owner: str, repo_name: str, ref: str) -> Optional[List[Dict]]:
    """Get list of statuses for a specific reference"""
    repo_key = f"{owner}/{repo_name}"

    # Resolve SHA from reference
    sha = resolve_ref_to_sha(owner, repo_name, ref)
    if not sha:
        return None

    if repo_key not in COMMIT_STATUSES or sha not in COMMIT_STATUSES[repo_key]:
        return []

    return COMMIT_STATUSES[repo_key][sha]


def get_combined_status(owner: str, repo_name: str, ref: str) -> Optional[Dict]:
    """Get combined status for a specific reference"""
    from data.repositories import REPOSITORIES

    repo_key = f"{owner}/{repo_name}"
    if repo_key not in REPOSITORIES:
        return None

    # Resolve SHA from reference
    sha = resolve_ref_to_sha(owner, repo_name, ref)
    if not sha:
        return None

    statuses = get_commit_statuses(owner, repo_name, sha) or []

    # Calculate combined status
    state = "success"
    if not statuses:
        state = "pending"
    elif any(s["state"] == "failure" for s in statuses):
        state = "failure"
    elif any(s["state"] == "error" for s in statuses):
        state = "error"
    elif any(s["state"] == "pending" for s in statuses):
        state = "pending"

    return {
        "state": state,
        "sha": sha,
        "total_count": len(statuses),
        "statuses": statuses,
        "repository": REPOSITORIES[repo_key],
        "url": f"/api/v3/repos/{owner}/{repo_name}/commits/{sha}/status",
    }


def create_commit_status(
    owner: str, repo_name: str, sha: str, status_data: Dict
) -> Optional[Dict]:
    """Create a commit status"""
    repo_key = f"{owner}/{repo_name}"

    # Check repository and commit existence
    if repo_key not in REPOSITORY_COMMITS or sha not in REPOSITORY_COMMITS[repo_key]:
        return None

    # Prepare status data
    if repo_key not in COMMIT_STATUSES:
        COMMIT_STATUSES[repo_key] = {}

    if sha not in COMMIT_STATUSES[repo_key]:
        COMMIT_STATUSES[repo_key][sha] = []

    # Generate new status ID
    status_id = 1
    if COMMIT_STATUSES[repo_key][sha]:
        status_id = max(s["id"] for s in COMMIT_STATUSES[repo_key][sha]) + 1

    # Default value for context
    context = status_data.get("context", "default")

    # Update existing context or create new one
    now = datetime.now()
    existing_status = next(
        (s for s in COMMIT_STATUSES[repo_key][sha] if s["context"] == context), None
    )

    if existing_status:
        existing_status["state"] = status_data["state"]
        existing_status["updated_at"] = now

        if "target_url" in status_data:
            existing_status["target_url"] = status_data["target_url"]

        if "description" in status_data:
            existing_status["description"] = status_data["description"]

        return existing_status
    else:
        new_status = {
            "created_at": now,
            "updated_at": now,
            "state": status_data["state"],
            "target_url": status_data.get("target_url"),
            "description": status_data.get("description"),
            "id": status_id,
            "context": context,
            "creator": USERS[
                "admin"
            ],  # In actual implementation, use authenticated user
            "url": f"/api/v3/repos/{owner}/{repo_name}/statuses/{sha}",
        }

        COMMIT_STATUSES[repo_key][sha].append(new_status)
        return new_status


def resolve_ref_to_sha(owner: str, repo_name: str, ref: str) -> Optional[str]:
    """Resolve reference (branch name, tag name, SHA) to SHA"""
    repo_key = f"{owner}/{repo_name}"

    # Return as-is if already SHA
    if repo_key in REPOSITORY_COMMITS and ref in REPOSITORY_COMMITS[repo_key]:
        return ref

    # For branches
    from data.branches import REPOSITORY_BRANCHES

    if repo_key in REPOSITORY_BRANCHES and ref in REPOSITORY_BRANCHES[repo_key]:
        return REPOSITORY_BRANCHES[repo_key][ref]["commit"]["sha"]

    # For tags
    from data.repositories import REPOSITORY_TAGS

    if repo_key in REPOSITORY_TAGS:
        for tag in REPOSITORY_TAGS[repo_key]:
            if tag["name"] == ref:
                return tag["commit"]["sha"]

    # Return None if not found
    return None
