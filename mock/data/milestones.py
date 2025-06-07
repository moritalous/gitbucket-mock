from datetime import datetime
from typing import Dict, List, Optional

# Repository milestone data
# Format: {repo_key: {milestone_number: milestone_data}}
REPOSITORY_MILESTONES = {
    "admin/repo1": {
        1: {
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
        2: {
            "url": "/api/v3/repos/admin/repo1/milestones/2",
            "html_url": "/admin/repo1/milestone/2",
            "id": 2,
            "number": 2,
            "state": "closed",
            "title": "v0.9",
            "description": "Version 0.9 milestone",
            "open_issues": 0,
            "closed_issues": 2,
            "closed_at": datetime(2023, 1, 15),
            "due_on": datetime(2023, 1, 15),
        },
    },
    "user1/repo2": {
        1: {
            "url": "/api/v3/repos/user1/repo2/milestones/1",
            "html_url": "/user1/repo2/milestone/1",
            "id": 3,
            "number": 1,
            "state": "open",
            "title": "v1.0",
            "description": "First release",
            "open_issues": 1,
            "closed_issues": 0,
            "closed_at": None,
            "due_on": datetime(2023, 4, 1),
        }
    },
}


def get_repository_milestones(
    owner: str, repo_name: str, state: str = "all"
) -> Optional[List[Dict]]:
    """Get list of milestones for a repository"""
    repo_key = f"{owner}/{repo_name}"
    if repo_key not in REPOSITORY_MILESTONES:
        return None

    milestones = []
    for milestone_data in REPOSITORY_MILESTONES[repo_key].values():
        if state == "all" or milestone_data["state"] == state:
            milestones.append(milestone_data)

    # Sort (by number, ascending)
    milestones.sort(key=lambda m: m["number"])

    return milestones


def get_milestone(owner: str, repo_name: str, milestone_number: int) -> Optional[Dict]:
    """Get a specific milestone"""
    repo_key = f"{owner}/{repo_name}"
    if (
        repo_key not in REPOSITORY_MILESTONES
        or milestone_number not in REPOSITORY_MILESTONES[repo_key]
    ):
        return None

    return REPOSITORY_MILESTONES[repo_key][milestone_number]


def create_milestone(
    owner: str, repo_name: str, milestone_data: Dict
) -> Optional[Dict]:
    """Create a milestone"""
    repo_key = f"{owner}/{repo_name}"
    if repo_key not in REPOSITORY_MILESTONES:
        REPOSITORY_MILESTONES[repo_key] = {}

    # Generate new milestone number
    milestone_number = 1
    if REPOSITORY_MILESTONES[repo_key]:
        milestone_number = max(REPOSITORY_MILESTONES[repo_key].keys()) + 1

    # Create new milestone
    new_milestone = {
        "url": f"/api/v3/repos/{owner}/{repo_name}/milestones/{milestone_number}",
        "html_url": f"/{owner}/{repo_name}/milestone/{milestone_number}",
        "id": get_next_milestone_id(),
        "number": milestone_number,
        "state": milestone_data.get("state", "open"),
        "title": milestone_data["title"],
        "description": milestone_data.get("description", ""),
        "open_issues": 0,
        "closed_issues": 0,
        "closed_at": None,
        "due_on": milestone_data.get("due_on"),
    }

    REPOSITORY_MILESTONES[repo_key][milestone_number] = new_milestone
    return new_milestone


def update_milestone(
    owner: str, repo_name: str, milestone_number: int, update_data: Dict
) -> Optional[Dict]:
    """Update a milestone"""
    repo_key = f"{owner}/{repo_name}"
    if (
        repo_key not in REPOSITORY_MILESTONES
        or milestone_number not in REPOSITORY_MILESTONES[repo_key]
    ):
        return None

    milestone = REPOSITORY_MILESTONES[repo_key][milestone_number]

    # Process updatable fields
    if "title" in update_data:
        milestone["title"] = update_data["title"]

    if "description" in update_data:
        milestone["description"] = update_data["description"]

    if "state" in update_data:
        old_state = milestone["state"]
        new_state = update_data["state"]
        milestone["state"] = new_state

        # Update closed_at if state is changed
        if old_state != new_state:
            if new_state == "closed":
                milestone["closed_at"] = datetime.now()
            else:
                milestone["closed_at"] = None

    if "due_on" in update_data:
        milestone["due_on"] = update_data["due_on"]

    return milestone


def delete_milestone(owner: str, repo_name: str, milestone_number: int) -> bool:
    """Delete a milestone"""
    repo_key = f"{owner}/{repo_name}"
    if (
        repo_key not in REPOSITORY_MILESTONES
        or milestone_number not in REPOSITORY_MILESTONES[repo_key]
    ):
        return False

    # Delete milestone
    del REPOSITORY_MILESTONES[repo_key][milestone_number]
    return True


def get_next_milestone_id() -> int:
    """Generate next milestone ID"""
    max_id = 0
    for repo_milestones in REPOSITORY_MILESTONES.values():
        for milestone in repo_milestones.values():
            max_id = max(max_id, milestone["id"])
    return max_id + 1
