from typing import Dict, List, Optional

# Repository label data
# Format: {repo_key: {label_name: {name: str, color: str, url: str}}}
REPOSITORY_LABELS = {
    "admin/repo1": {
        "bug": {
            "name": "bug",
            "color": "fc2929",
            "url": "/api/v3/repos/admin/repo1/labels/bug",
        },
        "enhancement": {
            "name": "enhancement",
            "color": "84b6eb",
            "url": "/api/v3/repos/admin/repo1/labels/enhancement",
        },
        "help wanted": {
            "name": "help wanted",
            "color": "159818",
            "url": "/api/v3/repos/admin/repo1/labels/help%20wanted",
        },
    },
    "user1/repo2": {
        "enhancement": {
            "name": "enhancement",
            "color": "84b6eb",
            "url": "/api/v3/repos/user1/repo2/labels/enhancement",
        },
        "documentation": {
            "name": "documentation",
            "color": "0075ca",
            "url": "/api/v3/repos/user1/repo2/labels/documentation",
        },
    },
}

# Issue label data
# Format: {repo_key: {issue_number: set(label_name)}}
ISSUE_LABELS = {"admin/repo1": {1: {"bug"}}, "user1/repo2": {1: {"enhancement"}}}


def get_repository_labels(owner: str, repo_name: str) -> Optional[List[Dict]]:
    """Get list of labels for a repository"""
    repo_key = f"{owner}/{repo_name}"
    if repo_key not in REPOSITORY_LABELS:
        return None

    return list(REPOSITORY_LABELS[repo_key].values())


def get_label(owner: str, repo_name: str, label_name: str) -> Optional[Dict]:
    """Get a specific label"""
    repo_key = f"{owner}/{repo_name}"
    if (
        repo_key not in REPOSITORY_LABELS
        or label_name not in REPOSITORY_LABELS[repo_key]
    ):
        return None

    return REPOSITORY_LABELS[repo_key][label_name]


def create_label(owner: str, repo_name: str, label_data: Dict) -> Optional[Dict]:
    """Create a label"""
    repo_key = f"{owner}/{repo_name}"
    if repo_key not in REPOSITORY_LABELS:
        REPOSITORY_LABELS[repo_key] = {}

    label_name = label_data["name"]

    # Fail if already exists
    if label_name in REPOSITORY_LABELS[repo_key]:
        return None

    # Create new label
    new_label = {
        "name": label_name,
        "color": label_data["color"],
        "url": f"/api/v3/repos/{owner}/{repo_name}/labels/{label_name.replace(' ', '%20')}",
    }

    REPOSITORY_LABELS[repo_key][label_name] = new_label
    return new_label


def update_label(
    owner: str, repo_name: str, old_label_name: str, label_data: Dict
) -> Optional[Dict]:
    """Update a label"""
    repo_key = f"{owner}/{repo_name}"
    if (
        repo_key not in REPOSITORY_LABELS
        or old_label_name not in REPOSITORY_LABELS[repo_key]
    ):
        return None

    new_label_name = label_data["name"]

    # If name is changed, check if new name already exists
    if (
        old_label_name != new_label_name
        and new_label_name in REPOSITORY_LABELS[repo_key]
    ):
        return None

    # Update label
    updated_label = {
        "name": new_label_name,
        "color": label_data["color"],
        "url": f"/api/v3/repos/{owner}/{repo_name}/labels/{new_label_name.replace(' ', '%20')}",
    }

    # Delete old label and add new label
    del REPOSITORY_LABELS[repo_key][old_label_name]
    REPOSITORY_LABELS[repo_key][new_label_name] = updated_label

    # Update issue labels as well
    if repo_key in ISSUE_LABELS:
        for issue_number, labels in ISSUE_LABELS[repo_key].items():
            if old_label_name in labels:
                labels.remove(old_label_name)
                labels.add(new_label_name)

    return updated_label


def delete_label(owner: str, repo_name: str, label_name: str) -> bool:
    """Delete a label"""
    repo_key = f"{owner}/{repo_name}"
    if (
        repo_key not in REPOSITORY_LABELS
        or label_name not in REPOSITORY_LABELS[repo_key]
    ):
        return False

    # Delete label
    del REPOSITORY_LABELS[repo_key][label_name]

    # Remove label from issues as well
    if repo_key in ISSUE_LABELS:
        for issue_number, labels in ISSUE_LABELS[repo_key].items():
            if label_name in labels:
                labels.remove(label_name)

    return True


def get_issue_labels(
    owner: str, repo_name: str, issue_number: int
) -> Optional[List[Dict]]:
    """Get list of labels for an issue"""
    repo_key = f"{owner}/{repo_name}"
    if repo_key not in REPOSITORY_LABELS:
        return None

    if repo_key not in ISSUE_LABELS or issue_number not in ISSUE_LABELS[repo_key]:
        return []

    labels = []
    for label_name in ISSUE_LABELS[repo_key][issue_number]:
        if label_name in REPOSITORY_LABELS[repo_key]:
            labels.append(REPOSITORY_LABELS[repo_key][label_name])

    return labels


def add_labels_to_issue(
    owner: str, repo_name: str, issue_number: int, label_names: List[str]
) -> Optional[List[Dict]]:
    """Add labels to an issue"""
    repo_key = f"{owner}/{repo_name}"
    if repo_key not in REPOSITORY_LABELS:
        return None

    # Initialize issue labels
    if repo_key not in ISSUE_LABELS:
        ISSUE_LABELS[repo_key] = {}

    if issue_number not in ISSUE_LABELS[repo_key]:
        ISSUE_LABELS[repo_key][issue_number] = set()

    added_labels = []
    for label_name in label_names:
        # Create label if it does not exist
        if label_name not in REPOSITORY_LABELS[repo_key]:
            create_label(owner, repo_name, {"name": label_name, "color": "ededed"})

        # Add label to issue
        ISSUE_LABELS[repo_key][issue_number].add(label_name)
        added_labels.append(REPOSITORY_LABELS[repo_key][label_name])

    return added_labels


def remove_label_from_issue(
    owner: str, repo_name: str, issue_number: int, label_name: str
) -> Optional[List[Dict]]:
    """Remove a label from an issue"""
    repo_key = f"{owner}/{repo_name}"
    if (
        repo_key not in REPOSITORY_LABELS
        or repo_key not in ISSUE_LABELS
        or issue_number not in ISSUE_LABELS[repo_key]
        or label_name not in ISSUE_LABELS[repo_key][issue_number]
    ):
        return None

    # Remove label from issue
    ISSUE_LABELS[repo_key][issue_number].remove(label_name)

    # Return removed label
    if label_name in REPOSITORY_LABELS[repo_key]:
        return [REPOSITORY_LABELS[repo_key][label_name]]

    return []


def replace_all_labels(
    owner: str, repo_name: str, issue_number: int, label_names: List[str]
) -> Optional[List[Dict]]:
    """Replace all labels for an issue"""
    repo_key = f"{owner}/{repo_name}"
    if repo_key not in REPOSITORY_LABELS:
        return None

    # Initialize issue labels
    if repo_key not in ISSUE_LABELS:
        ISSUE_LABELS[repo_key] = {}

    # Clear existing labels
    ISSUE_LABELS[repo_key][issue_number] = set()

    # Add new labels
    return add_labels_to_issue(owner, repo_name, issue_number, label_names)


def remove_all_labels(owner: str, repo_name: str, issue_number: int) -> bool:
    """Remove all labels from an issue"""
    repo_key = f"{owner}/{repo_name}"
    if repo_key not in ISSUE_LABELS or issue_number not in ISSUE_LABELS[repo_key]:
        return False

    # Clear issue labels
    ISSUE_LABELS[repo_key][issue_number] = set()
    return True
