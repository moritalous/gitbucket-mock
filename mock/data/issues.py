from datetime import datetime
from typing import Dict, List, Optional

from data.users import USERS

# Repository issue data
# Format: {repo_key: {issue_number: issue_data}}
REPOSITORY_ISSUES = {
    "admin/repo1": {
        1: {
            "number": 1,
            "title": "First issue",
            "user": USERS["admin"],
            "assignees": [USERS["admin"]],
            "labels": [
                {
                    "name": "bug",
                    "color": "fc2929",
                    "url": "/api/v3/repos/admin/repo1/labels/bug",
                }
            ],
            "state": "open",
            "created_at": datetime(2023, 1, 20, 10, 0, 0),
            "updated_at": datetime(2023, 1, 20, 10, 0, 0),
            "body": "This is the first issue.",
            "milestone": {
                "url": "/api/v3/repos/admin/repo1/milestones/1",
                "html_url": "/admin/repo1/milestone/1",
                "id": 1,
                "number": 1,
                "state": "open",
                "title": "v1.0",
                "description": "Version 1.0 milestone",
                "open_issues": 1,
                "closed_issues": 0,
                "closed_at": None,
                "due_on": datetime(2023, 3, 1),
            },
            "id": 1001,
            "assignee": USERS["admin"],
            "comments_url": "/api/v3/repos/admin/repo1/issues/1/comments",
            "html_url": "/admin/repo1/issues/1",
            "pull_request": None,
        },
        2: {
            "number": 2,
            "title": "Second issue",
            "user": USERS["user1"],
            "assignees": [],
            "labels": [],
            "state": "closed",
            "created_at": datetime(2023, 1, 21, 11, 0, 0),
            "updated_at": datetime(2023, 1, 22, 12, 0, 0),
            "body": "This is the second issue.",
            "milestone": None,
            "id": 1002,
            "assignee": None,
            "comments_url": "/api/v3/repos/admin/repo1/issues/2/comments",
            "html_url": "/admin/repo1/issues/2",
            "pull_request": None,
        },
    },
    "user1/repo2": {
        1: {
            "number": 1,
            "title": "Feature request",
            "user": USERS["user1"],
            "assignees": [USERS["user1"]],
            "labels": [
                {
                    "name": "enhancement",
                    "color": "84b6eb",
                    "url": "/api/v3/repos/user1/repo2/labels/enhancement",
                }
            ],
            "state": "open",
            "created_at": datetime(2023, 2, 15, 14, 0, 0),
            "updated_at": datetime(2023, 2, 15, 14, 0, 0),
            "body": "Please add this feature.",
            "milestone": None,
            "id": 1003,
            "assignee": USERS["user1"],
            "comments_url": "/api/v3/repos/user1/repo2/issues/1/comments",
            "html_url": "/user1/repo2/issues/1",
            "pull_request": None,
        }
    },
}

# Issue comment data
# Format: {repo_key: {issue_number: {comment_id: comment_data}}}
ISSUE_COMMENTS = {
    "admin/repo1": {
        1: {
            1: {
                "id": 1,
                "user": USERS["admin"],
                "body": "This is a comment on the first issue.",
                "created_at": datetime(2023, 1, 20, 10, 30, 0),
                "updated_at": datetime(2023, 1, 20, 10, 30, 0),
                "html_url": "/admin/repo1/issues/1#comment-1",
            },
            2: {
                "id": 2,
                "user": USERS["user1"],
                "body": "I can help with this issue.",
                "created_at": datetime(2023, 1, 20, 11, 0, 0),
                "updated_at": datetime(2023, 1, 20, 11, 0, 0),
                "html_url": "/admin/repo1/issues/1#comment-2",
            },
        },
        2: {
            3: {
                "id": 3,
                "user": USERS["user1"],
                "body": "I've fixed this issue.",
                "created_at": datetime(2023, 1, 22, 12, 0, 0),
                "updated_at": datetime(2023, 1, 22, 12, 0, 0),
                "html_url": "/admin/repo1/issues/2#comment-3",
            }
        },
    },
    "user1/repo2": {
        1: {
            4: {
                "id": 4,
                "user": USERS["admin"],
                "body": "This is a good feature request.",
                "created_at": datetime(2023, 2, 15, 15, 0, 0),
                "updated_at": datetime(2023, 2, 15, 15, 0, 0),
                "html_url": "/user1/repo2/issues/1#comment-4",
            }
        }
    },
}

# Map of all comments (to get comment data from comment ID)
ALL_COMMENTS = {}
for repo_key, issues in ISSUE_COMMENTS.items():
    for issue_number, comments in issues.items():
        for comment_id, comment_data in comments.items():
            ALL_COMMENTS[comment_id] = {
                "repo_key": repo_key,
                "issue_number": issue_number,
                "data": comment_data,
            }


def get_repository_issues(
    owner: str, repo_name: str, state: str = "open", page: int = 1, per_page: int = 30
) -> Optional[List[Dict]]:
    """Get list of issues for a repository"""
    repo_key = f"{owner}/{repo_name}"
    if repo_key not in REPOSITORY_ISSUES:
        return None

    issues = []
    for issue_data in REPOSITORY_ISSUES[repo_key].values():
        if state == "all" or issue_data["state"] == state:
            issues.append(issue_data)

    # Sort (by number, descending)
    issues.sort(key=lambda i: i["number"], reverse=True)

    # Pagination
    start = (page - 1) * per_page
    end = start + per_page

    return issues[start:end]


def get_issue(owner: str, repo_name: str, issue_number: int) -> Optional[Dict]:
    """Get a specific issue"""
    repo_key = f"{owner}/{repo_name}"
    if (
        repo_key not in REPOSITORY_ISSUES
        or issue_number not in REPOSITORY_ISSUES[repo_key]
    ):
        return None

    return REPOSITORY_ISSUES[repo_key][issue_number]


def create_issue(
    owner: str, repo_name: str, issue_data: Dict, creator_username: str
) -> Optional[Dict]:
    """Create an issue"""
    repo_key = f"{owner}/{repo_name}"
    if repo_key not in REPOSITORY_ISSUES:
        return None

    # Generate new issue number
    issue_number = 1
    if REPOSITORY_ISSUES[repo_key]:
        issue_number = max(REPOSITORY_ISSUES[repo_key].keys()) + 1

    # Get creator information
    creator = USERS.get(creator_username)
    if not creator:
        return None

    # Resolve assignee users
    assignees = []
    assignee = None
    if "assignees" in issue_data and issue_data["assignees"]:
        for username in issue_data["assignees"]:
            if username in USERS:
                assignees.append(USERS[username])
        if assignees:
            assignee = assignees[0]

    # Resolve milestone (omitted in mock implementation)
    milestone = None

    # Resolve labels (omitted in mock implementation)
    labels = []

    # Create new issue
    now = datetime.now()
    new_issue = {
        "number": issue_number,
        "title": issue_data["title"],
        "user": creator,
        "assignees": assignees,
        "labels": labels,
        "state": "open",
        "created_at": now,
        "updated_at": now,
        "body": issue_data.get("body", ""),
        "milestone": milestone,
        "id": len(ALL_COMMENTS) + 1000,
        "assignee": assignee,
        "comments_url": f"/api/v3/repos/{owner}/{repo_name}/issues/{issue_number}/comments",
        "html_url": f"/{owner}/{repo_name}/issues/{issue_number}",
        "pull_request": None,
    }

    REPOSITORY_ISSUES[repo_key][issue_number] = new_issue

    # Initialize dictionary for issue comments
    if repo_key not in ISSUE_COMMENTS:
        ISSUE_COMMENTS[repo_key] = {}
    ISSUE_COMMENTS[repo_key][issue_number] = {}

    return new_issue


def update_issue(
    owner: str, repo_name: str, issue_number: int, update_data: Dict
) -> Optional[Dict]:
    """Update an issue"""
    repo_key = f"{owner}/{repo_name}"
    if (
        repo_key not in REPOSITORY_ISSUES
        or issue_number not in REPOSITORY_ISSUES[repo_key]
    ):
        return None

    issue = REPOSITORY_ISSUES[repo_key][issue_number]

    # Process updatable fields
    if "title" in update_data:
        issue["title"] = update_data["title"]

    if "body" in update_data:
        issue["body"] = update_data["body"]

    if "state" in update_data:
        issue["state"] = update_data["state"]

    # Update assignee users
    if "assignees" in update_data:
        assignees = []
        for username in update_data["assignees"]:
            if username in USERS:
                assignees.append(USERS[username])
        issue["assignees"] = assignees
        issue["assignee"] = assignees[0] if assignees else None

    # Update milestone (omitted in mock implementation)

    # Update labels (omitted in mock implementation)

    # Update modification time
    issue["updated_at"] = datetime.now()

    return issue


def get_issue_comments(
    owner: str, repo_name: str, issue_number: int
) -> Optional[List[Dict]]:
    """Get list of comments for an issue"""
    repo_key = f"{owner}/{repo_name}"
    if repo_key not in ISSUE_COMMENTS or issue_number not in ISSUE_COMMENTS[repo_key]:
        return []

    return list(ISSUE_COMMENTS[repo_key][issue_number].values())


def get_comment(comment_id: int) -> Optional[Dict]:
    """Get a specific comment"""
    if comment_id not in ALL_COMMENTS:
        return None

    return ALL_COMMENTS[comment_id]["data"]


def create_comment(
    owner: str,
    repo_name: str,
    issue_number: int,
    comment_data: Dict,
    creator_username: str,
) -> Optional[Dict]:
    """Create a comment"""
    repo_key = f"{owner}/{repo_name}"
    if (
        repo_key not in REPOSITORY_ISSUES
        or issue_number not in REPOSITORY_ISSUES[repo_key]
    ):
        return None

    # Initialize comment dictionary for repository and issue
    if repo_key not in ISSUE_COMMENTS:
        ISSUE_COMMENTS[repo_key] = {}
    if issue_number not in ISSUE_COMMENTS[repo_key]:
        ISSUE_COMMENTS[repo_key][issue_number] = {}

    # Generate new comment ID
    comment_id = 1
    if ALL_COMMENTS:
        comment_id = max(ALL_COMMENTS.keys()) + 1

    # Get creator information
    creator = USERS.get(creator_username)
    if not creator:
        return None

    # Create new comment
    now = datetime.now()
    new_comment = {
        "id": comment_id,
        "user": creator,
        "body": comment_data["body"],
        "created_at": now,
        "updated_at": now,
        "html_url": f"/{owner}/{repo_name}/issues/{issue_number}#comment-{comment_id}",
    }

    # Save comment
    ISSUE_COMMENTS[repo_key][issue_number][comment_id] = new_comment
    ALL_COMMENTS[comment_id] = {
        "repo_key": repo_key,
        "issue_number": issue_number,
        "data": new_comment,
    }

    # Update issue modification time
    REPOSITORY_ISSUES[repo_key][issue_number]["updated_at"] = now

    return new_comment


def update_comment(comment_id: int, update_data: Dict) -> Optional[Dict]:
    """Update a comment"""
    if comment_id not in ALL_COMMENTS:
        return None

    comment_info = ALL_COMMENTS[comment_id]
    comment = comment_info["data"]

    # Process updatable fields
    if "body" in update_data:
        comment["body"] = update_data["body"]

    # Update modification time
    comment["updated_at"] = datetime.now()

    return comment


def delete_comment(comment_id: int) -> bool:
    """Delete a comment"""
    if comment_id not in ALL_COMMENTS:
        return False

    comment_info = ALL_COMMENTS[comment_id]
    repo_key = comment_info["repo_key"]
    issue_number = comment_info["issue_number"]

    # Delete comment
    del ISSUE_COMMENTS[repo_key][issue_number][comment_id]
    del ALL_COMMENTS[comment_id]

    return True
