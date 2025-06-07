from datetime import datetime
from typing import Dict, List, Optional, Tuple, Union

from data.issues import REPOSITORY_ISSUES
from data.repositories import REPOSITORIES
from data.users import USERS

# Repository pull request data
# Format: {repo_key: {pr_number: pr_data}}
REPOSITORY_PULL_REQUESTS = {
    "admin/repo1": {
        1: {
            "number": 1,
            "state": "open",
            "updated_at": datetime(2023, 1, 25, 10, 0, 0),
            "created_at": datetime(2023, 1, 25, 10, 0, 0),
            "head": {
                "sha": "1234567890abcdef1234567890abcdef12345678",
                "ref": "feature-branch",
                "repo": REPOSITORIES["admin/repo1"],
                "label": "admin:feature-branch",
                "user": USERS["admin"],
            },
            "base": {
                "sha": "abcdef1234567890abcdef1234567890abcdef12",
                "ref": "main",
                "repo": REPOSITORIES["admin/repo1"],
                "label": "admin:main",
                "user": USERS["admin"],
            },
            "mergeable": True,
            "merged": False,
            "merged_at": None,
            "merged_by": None,
            "title": "Add new feature",
            "body": "This pull request adds a new feature.",
            "user": USERS["admin"],
            "labels": [
                {
                    "name": "enhancement",
                    "color": "84b6eb",
                    "url": "/api/v3/repos/admin/repo1/labels/enhancement",
                }
            ],
            "assignees": [USERS["admin"]],
            "draft": False,
            "id": 2001,
            "assignee": USERS["admin"],
            "html_url": "/admin/repo1/pull/1",
            "url": "/api/v3/repos/admin/repo1/pulls/1",
            "commits_url": "/api/v3/repos/admin/repo1/pulls/1/commits",
            "review_comments_url": "/api/v3/repos/admin/repo1/pulls/1/comments",
            "review_comment_url": "/api/v3/repos/admin/repo1/pulls/comments/{number}",
            "comments_url": "/api/v3/repos/admin/repo1/issues/1/comments",
            "statuses_url": "/api/v3/repos/admin/repo1/statuses/1234567890abcdef1234567890abcdef12345678",
        },
        2: {
            "number": 2,
            "state": "closed",
            "updated_at": datetime(2023, 1, 26, 11, 0, 0),
            "created_at": datetime(2023, 1, 26, 10, 0, 0),
            "head": {
                "sha": "2345678901abcdef2345678901abcdef23456789",
                "ref": "bugfix-branch",
                "repo": REPOSITORIES["admin/repo1"],
                "label": "admin:bugfix-branch",
                "user": USERS["admin"],
            },
            "base": {
                "sha": "abcdef1234567890abcdef1234567890abcdef12",
                "ref": "main",
                "repo": REPOSITORIES["admin/repo1"],
                "label": "admin:main",
                "user": USERS["admin"],
            },
            "mergeable": True,
            "merged": True,
            "merged_at": datetime(2023, 1, 26, 11, 0, 0),
            "merged_by": USERS["admin"],
            "title": "Fix bug",
            "body": "This pull request fixes a bug.",
            "user": USERS["user1"],
            "labels": [
                {
                    "name": "bug",
                    "color": "fc2929",
                    "url": "/api/v3/repos/admin/repo1/labels/bug",
                }
            ],
            "assignees": [USERS["admin"]],
            "draft": False,
            "id": 2002,
            "assignee": USERS["admin"],
            "html_url": "/admin/repo1/pull/2",
            "url": "/api/v3/repos/admin/repo1/pulls/2",
            "commits_url": "/api/v3/repos/admin/repo1/pulls/2/commits",
            "review_comments_url": "/api/v3/repos/admin/repo1/pulls/2/comments",
            "review_comment_url": "/api/v3/repos/admin/repo1/pulls/comments/{number}",
            "comments_url": "/api/v3/repos/admin/repo1/issues/2/comments",
            "statuses_url": "/api/v3/repos/admin/repo1/statuses/2345678901abcdef2345678901abcdef23456789",
        },
    }
}

# Pull request commit data
# Format: {repo_key: {pr_number: [commit_data]}}
PULL_REQUEST_COMMITS = {
    "admin/repo1": {
        1: [
            {
                "sha": "1234567890abcdef1234567890abcdef12345678",
                "commit": {
                    "author": {
                        "name": "Admin User",
                        "email": "admin@example.com",
                        "date": datetime(2023, 1, 25, 10, 0, 0),
                    },
                    "committer": {
                        "name": "Admin User",
                        "email": "admin@example.com",
                        "date": datetime(2023, 1, 25, 10, 0, 0),
                    },
                    "message": "Add new feature",
                    "tree": {"sha": "9876543210fedcba9876543210fedcba98765432"},
                },
                "author": USERS["admin"],
                "committer": USERS["admin"],
                "parents": [{"sha": "abcdef1234567890abcdef1234567890abcdef12"}],
            }
        ],
        2: [
            {
                "sha": "2345678901abcdef2345678901abcdef23456789",
                "commit": {
                    "author": {
                        "name": "User 1",
                        "email": "user1@example.com",
                        "date": datetime(2023, 1, 26, 10, 0, 0),
                    },
                    "committer": {
                        "name": "User 1",
                        "email": "user1@example.com",
                        "date": datetime(2023, 1, 26, 10, 0, 0),
                    },
                    "message": "Fix bug",
                    "tree": {"sha": "8765432109fedcba8765432109fedcba87654321"},
                },
                "author": USERS["user1"],
                "committer": USERS["user1"],
                "parents": [{"sha": "abcdef1234567890abcdef1234567890abcdef12"}],
            }
        ],
    }
}


def get_repository_pull_requests(
    owner: str, repo_name: str, state: str = "open", page: int = 1, per_page: int = 30
) -> Optional[List[Dict]]:
    """Get list of pull requests for a repository"""
    repo_key = f"{owner}/{repo_name}"
    if repo_key not in REPOSITORY_PULL_REQUESTS:
        return None

    pull_requests = []
    for pr_data in REPOSITORY_PULL_REQUESTS[repo_key].values():
        if state == "all" or pr_data["state"] == state:
            pull_requests.append(pr_data)

    # Sort (by number, descending)
    pull_requests.sort(key=lambda p: p["number"], reverse=True)

    # Pagination
    start = (page - 1) * per_page
    end = start + per_page

    return pull_requests[start:end]


def get_pull_request(owner: str, repo_name: str, pr_number: int) -> Optional[Dict]:
    """Get a specific pull request"""
    repo_key = f"{owner}/{repo_name}"
    if (
        repo_key not in REPOSITORY_PULL_REQUESTS
        or pr_number not in REPOSITORY_PULL_REQUESTS[repo_key]
    ):
        return None

    return REPOSITORY_PULL_REQUESTS[repo_key][pr_number]


def create_pull_request(
    owner: str, repo_name: str, pr_data: Dict, creator_username: str
) -> Optional[Dict]:
    """Create a pull request"""
    repo_key = f"{owner}/{repo_name}"
    if repo_key not in REPOSITORIES:
        return None

    # Get creator information
    creator = USERS.get(creator_username)
    if not creator:
        return None

    # Generate new pull request number
    pr_number = 1
    if repo_key in REPOSITORY_PULL_REQUESTS and REPOSITORY_PULL_REQUESTS[repo_key]:
        pr_number = max(REPOSITORY_PULL_REQUESTS[repo_key].keys()) + 1

    # When creating pull request from issue
    if "issue" in pr_data:
        issue_number = pr_data["issue"]
        if (
            repo_key not in REPOSITORY_ISSUES
            or issue_number not in REPOSITORY_ISSUES[repo_key]
        ):
            return None

        issue = REPOSITORY_ISSUES[repo_key][issue_number]
        title = issue["title"]
        body = issue["body"]
    else:
        title = pr_data["title"]
        body = pr_data.get("body", "")

    # Parse head and base
    head_ref = pr_data["head"]
    base_ref = pr_data["base"]

    # For cross-repository pull requests (username:branch format)
    head_parts = head_ref.split(":")
    if len(head_parts) > 1:
        head_owner = head_parts[0]
        head_branch = head_parts[1]
        head_repo_key = f"{head_owner}/repo1"  # For simplification
    else:
        head_owner = owner
        head_branch = head_ref
        head_repo_key = repo_key

    # Get head repository
    head_repo = REPOSITORIES.get(head_repo_key, REPOSITORIES[repo_key])

    # Create new pull request
    now = datetime.now()
    new_pr = {
        "number": pr_number,
        "state": "open",
        "updated_at": now,
        "created_at": now,
        "head": {
            "sha": generate_sha(),
            "ref": head_branch,
            "repo": head_repo,
            "label": f"{head_owner}:{head_branch}",
            "user": USERS.get(head_owner, creator),
        },
        "base": {
            "sha": generate_sha(),
            "ref": base_ref,
            "repo": REPOSITORIES[repo_key],
            "label": f"{owner}:{base_ref}",
            "user": USERS.get(owner, creator),
        },
        "mergeable": True,
        "merged": False,
        "merged_at": None,
        "merged_by": None,
        "title": title,
        "body": body,
        "user": creator,
        "labels": [],
        "assignees": [],
        "draft": pr_data.get("draft", False),
        "id": get_next_pr_id(),
        "assignee": None,
        "html_url": f"/{owner}/{repo_name}/pull/{pr_number}",
        "url": f"/api/v3/repos/{owner}/{repo_name}/pulls/{pr_number}",
        "commits_url": f"/api/v3/repos/{owner}/{repo_name}/pulls/{pr_number}/commits",
        "review_comments_url": f"/api/v3/repos/{owner}/{repo_name}/pulls/{pr_number}/comments",
        "review_comment_url": f"/api/v3/repos/{owner}/{repo_name}/pulls/comments/{{number}}",
        "comments_url": f"/api/v3/repos/{owner}/{repo_name}/issues/{pr_number}/comments",
        "statuses_url": f"/api/v3/repos/{owner}/{repo_name}/statuses/{generate_sha()}",
    }

    # Save pull request
    if repo_key not in REPOSITORY_PULL_REQUESTS:
        REPOSITORY_PULL_REQUESTS[repo_key] = {}

    REPOSITORY_PULL_REQUESTS[repo_key][pr_number] = new_pr

    # Initialize commit data
    if repo_key not in PULL_REQUEST_COMMITS:
        PULL_REQUEST_COMMITS[repo_key] = {}

    PULL_REQUEST_COMMITS[repo_key][pr_number] = []

    return new_pr


def update_pull_request(
    owner: str, repo_name: str, pr_number: int, update_data: Dict
) -> Optional[Dict]:
    """Update a pull request"""
    repo_key = f"{owner}/{repo_name}"
    if (
        repo_key not in REPOSITORY_PULL_REQUESTS
        or pr_number not in REPOSITORY_PULL_REQUESTS[repo_key]
    ):
        return None

    pr = REPOSITORY_PULL_REQUESTS[repo_key][pr_number]

    # Process updatable fields
    if "title" in update_data:
        pr["title"] = update_data["title"]

    if "body" in update_data:
        pr["body"] = update_data["body"]

    if "state" in update_data:
        pr["state"] = update_data["state"]

    if "base" in update_data:
        base_ref = update_data["base"]
        pr["base"]["ref"] = base_ref
        pr["base"]["label"] = f"{owner}:{base_ref}"

    # Update modification time
    pr["updated_at"] = datetime.now()

    return pr


def get_pull_request_commits(
    owner: str, repo_name: str, pr_number: int
) -> Optional[List[Dict]]:
    """Get list of commits for a pull request"""
    repo_key = f"{owner}/{repo_name}"
    if (
        repo_key not in PULL_REQUEST_COMMITS
        or pr_number not in PULL_REQUEST_COMMITS[repo_key]
    ):
        return None

    return PULL_REQUEST_COMMITS[repo_key][pr_number]


def is_pull_request_merged(owner: str, repo_name: str, pr_number: int) -> bool:
    """Check if a pull request is merged

    IMPORTANT: This mock implementation returns the actual merge status.
    However, GitBucket's real implementation has a logical flaw:

    GitBucket's checkConflict() function returns:
    - Some(None): Mergeable (returns 204)
    - Some(Some(message)): Has conflicts (returns 204)
    - None: Status unknown (returns 404)

    This means GitBucket returns 204 for BOTH:
    1. Actually merged PRs (correct)
    2. Unmerged but mergeable/conflicted PRs (incorrect)

    The real GitBucket API cannot reliably distinguish between
    "merged" and "mergeable" pull requests.
    """
    repo_key = f"{owner}/{repo_name}"
    if (
        repo_key not in REPOSITORY_PULL_REQUESTS
        or pr_number not in REPOSITORY_PULL_REQUESTS[repo_key]
    ):
        return False

    return REPOSITORY_PULL_REQUESTS[repo_key][pr_number]["merged"]


def merge_pull_request(
    owner: str, repo_name: str, pr_number: int, merge_data: Dict, merger_username: str
) -> Optional[Union[Dict, Tuple[int, Dict]]]:
    """Merge a pull request"""
    repo_key = f"{owner}/{repo_name}"
    if (
        repo_key not in REPOSITORY_PULL_REQUESTS
        or pr_number not in REPOSITORY_PULL_REQUESTS[repo_key]
    ):
        return None

    pr = REPOSITORY_PULL_REQUESTS[repo_key][pr_number]

    # Return 405 error if already merged
    if pr["merged"]:
        return (
            405,
            {
                "documentation_url": "https://docs.github.com/rest/reference/pulls#merge-a-pull-request",
                "message": "Pull request is already merged",
            },
        )

    # Return 405 error if not mergeable
    if not pr["mergeable"]:
        return (
            405,
            {
                "documentation_url": "https://docs.github.com/rest/reference/pulls#merge-a-pull-request",
                "message": "Pull request is not mergeable",
            },
        )

    # Return 405 error if closed
    if pr["state"] == "closed":
        return (
            405,
            {
                "documentation_url": "https://docs.github.com/rest/reference/pulls#merge-a-pull-request",
                "message": "Pull request is closed",
            },
        )

    # Get merge executor
    merger = USERS.get(merger_username)
    if not merger:
        return None

    # Get merge method
    # merge_method = merge_data.get("merge_method", "merge-commit")  # Unused variable

    # SHA of merge commit
    merge_sha = generate_sha()

    # Merge pull request
    now = datetime.now()
    pr["merged"] = True
    pr["merged_at"] = now
    pr["merged_by"] = merger
    pr["state"] = "closed"
    pr["updated_at"] = now

    # Return merge success response
    return {
        "sha": merge_sha,
        "merged": True,
        "message": "Pull request successfully merged",
    }


def get_next_pr_id() -> int:
    """Generate next pull request ID"""
    max_id = 2000
    for repo_prs in REPOSITORY_PULL_REQUESTS.values():
        for pr in repo_prs.values():
            max_id = max(max_id, pr["id"])
    return max_id + 1


def generate_sha() -> str:
    """Generate random SHA"""
    import random
    import string

    # Generate 40-character random hexadecimal
    return "".join(random.choice(string.hexdigits.lower()) for _ in range(40))
