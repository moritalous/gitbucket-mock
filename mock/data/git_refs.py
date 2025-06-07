from typing import Dict, List, Optional

# Repository Git reference data
# Format: {repo_key: {ref: {ref: str, node_id: str, url: str, object: {sha: str, type: str, url: str}}}}
REPOSITORY_REFS = {
    "admin/repo1": {
        "refs/heads/main": {
            "ref": "refs/heads/main",
            "node_id": "MDM6UmVmMTpyZWZzL2hlYWRzL21haW4=",
            "url": "/api/v3/repos/admin/repo1/git/refs/heads/main",
            "object": {
                "sha": "abcdef1234567890abcdef1234567890abcdef12",
                "type": "commit",
                "url": "/api/v3/repos/admin/repo1/git/commits/abcdef1234567890abcdef1234567890abcdef12",
            },
        },
        "refs/heads/develop": {
            "ref": "refs/heads/develop",
            "node_id": "MDM6UmVmMTpyZWZzL2hlYWRzL2RldmVsb3A=",
            "url": "/api/v3/repos/admin/repo1/git/refs/heads/develop",
            "object": {
                "sha": "1234567890abcdef1234567890abcdef12345678",
                "type": "commit",
                "url": "/api/v3/repos/admin/repo1/git/commits/1234567890abcdef1234567890abcdef12345678",
            },
        },
        "refs/tags/v1.0.0": {
            "ref": "refs/tags/v1.0.0",
            "node_id": "MDM6UmVmMTpyZWZzL3RhZ3MvdjEuMC4w",
            "url": "/api/v3/repos/admin/repo1/git/refs/tags/v1.0.0",
            "object": {
                "sha": "abcdef1234567890abcdef1234567890abcdef12",
                "type": "commit",
                "url": "/api/v3/repos/admin/repo1/git/commits/abcdef1234567890abcdef1234567890abcdef12",
            },
        },
    },
    "user1/repo2": {
        "refs/heads/main": {
            "ref": "refs/heads/main",
            "node_id": "MDM6UmVmMjpyZWZzL2hlYWRzL21haW4=",
            "url": "/api/v3/repos/user1/repo2/git/refs/heads/main",
            "object": {
                "sha": "2345678901abcdef2345678901abcdef23456789",
                "type": "commit",
                "url": "/api/v3/repos/user1/repo2/git/commits/2345678901abcdef2345678901abcdef23456789",
            },
        }
    },
    "org1/repo3": {
        "refs/heads/main": {
            "ref": "refs/heads/main",
            "node_id": "MDM6UmVmMzpyZWZzL2hlYWRzL21haW4=",
            "url": "/api/v3/repos/org1/repo3/git/refs/heads/main",
            "object": {
                "sha": "3456789012abcdef3456789012abcdef34567890",
                "type": "commit",
                "url": "/api/v3/repos/org1/repo3/git/commits/3456789012abcdef3456789012abcdef34567890",
            },
        },
        "refs/heads/feature": {
            "ref": "refs/heads/feature",
            "node_id": "MDM6UmVmMzpyZWZzL2hlYWRzL2ZlYXR1cmU=",
            "url": "/api/v3/repos/org1/repo3/git/refs/heads/feature",
            "object": {
                "sha": "4567890123abcdef4567890123abcdef45678901",
                "type": "commit",
                "url": "/api/v3/repos/org1/repo3/git/commits/4567890123abcdef4567890123abcdef45678901",
            },
        },
    },
}


def get_all_refs(owner: str, repo_name: str) -> Optional[List[Dict]]:
    """Get all references for a repository"""
    repo_key = f"{owner}/{repo_name}"
    if repo_key not in REPOSITORY_REFS:
        return None

    return list(REPOSITORY_REFS[repo_key].values())


def get_ref(owner: str, repo_name: str, ref: str) -> Optional[Dict]:
    """Get a specific reference"""
    repo_key = f"{owner}/{repo_name}"
    if repo_key not in REPOSITORY_REFS:
        return None

    # Add "refs/" prefix if ref does not start with it
    if not ref.startswith("refs/"):
        ref = f"refs/{ref}"

    if ref not in REPOSITORY_REFS[repo_key]:
        return None

    return REPOSITORY_REFS[repo_key][ref]


def create_ref(owner: str, repo_name: str, ref_data: Dict) -> Optional[Dict]:
    """Create a new reference"""
    repo_key = f"{owner}/{repo_name}"
    if repo_key not in REPOSITORY_REFS:
        return None

    ref = ref_data["ref"]
    sha = ref_data["sha"]

    # Fail if ref already exists
    if ref in REPOSITORY_REFS[repo_key]:
        return None

    # Check SHA existence (omitted in mock implementation)

    # Create new reference
    new_ref = {
        "ref": ref,
        "node_id": generate_node_id(ref),
        "url": f"/api/v3/repos/{owner}/{repo_name}/git/refs/{ref.replace('refs/', '')}",
        "object": {
            "sha": sha,
            "type": "commit",
            "url": f"/api/v3/repos/{owner}/{repo_name}/git/commits/{sha}",
        },
    }

    REPOSITORY_REFS[repo_key][ref] = new_ref
    return new_ref


def update_ref(
    owner: str, repo_name: str, ref: str, update_data: Dict
) -> Optional[Dict]:
    """Update a reference"""
    repo_key = f"{owner}/{repo_name}"
    if repo_key not in REPOSITORY_REFS:
        return None

    # Add "refs/" prefix if ref does not start with it
    if not ref.startswith("refs/"):
        ref = f"refs/{ref}"

    if ref not in REPOSITORY_REFS[repo_key]:
        return None

    sha = update_data["sha"]
    # force = update_data.get("force", False)  # Unused variable

    # Check SHA existence (omitted in mock implementation)

    # Update reference
    REPOSITORY_REFS[repo_key][ref]["object"]["sha"] = sha

    return REPOSITORY_REFS[repo_key][ref]


def delete_ref(owner: str, repo_name: str, ref: str) -> bool:
    """Delete a reference"""
    repo_key = f"{owner}/{repo_name}"
    if repo_key not in REPOSITORY_REFS:
        return False

    # Add "refs/" prefix if ref does not start with it
    if not ref.startswith("refs/"):
        ref = f"refs/{ref}"

    if ref not in REPOSITORY_REFS[repo_key]:
        return False

    # Delete reference
    del REPOSITORY_REFS[repo_key][ref]
    return True


def generate_node_id(ref: str) -> str:
    """Generate node_id for reference"""
    import base64

    return base64.b64encode(f"REF:{ref}".encode()).decode()
