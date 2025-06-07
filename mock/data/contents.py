import base64
import os
from typing import Dict, List, Optional, Union

# Repository content data (directory structure)
# Format: {repo_key: {path: {type: "file"|"dir", name: str, path: str, sha: str, content: str}}}
REPOSITORY_CONTENT_METADATA = {
    "admin/repo1": {
        "": {
            "type": "dir",
            "name": "",
            "path": "",
            "sha": "abcdef1234567890abcdef1234567890abcdef12",
            "contents": ["README.md", "file.txt"],
        },
        "README.md": {
            "type": "file",
            "name": "README.md",
            "path": "README.md",
            "sha": "1234567890abcdef1234567890abcdef12345678",
            "content": "# Repository 1\n\nThis is a test repository.",
        },
        "file.txt": {
            "type": "file",
            "name": "file.txt",
            "path": "file.txt",
            "sha": "2345678901abcdef2345678901abcdef23456789",
            "content": "This is a test file.",
        },
    },
    "user1/repo2": {
        "": {
            "type": "dir",
            "name": "",
            "path": "",
            "sha": "3456789012abcdef3456789012abcdef34567890",
            "contents": ["README.md"],
        },
        "README.md": {
            "type": "file",
            "name": "README.md",
            "path": "README.md",
            "sha": "4567890123abcdef4567890123abcdef45678901",
            "content": "# Repository 2\n\nThis is another test repository.",
        },
    },
    "org1/repo3": {
        "": {
            "type": "dir",
            "name": "",
            "path": "",
            "sha": "5678901234abcdef5678901234abcdef56789012",
            "contents": ["README.md", "src"],
        },
        "README.md": {
            "type": "file",
            "name": "README.md",
            "path": "README.md",
            "sha": "6789012345abcdef6789012345abcdef67890123",
            "content": "# Repository 3\n\nThis is an organization repository.",
        },
        "src": {
            "type": "dir",
            "name": "src",
            "path": "src",
            "sha": "7890123456abcdef7890123456abcdef78901234",
            "contents": ["main.py"],
        },
        "src/main.py": {
            "type": "file",
            "name": "main.py",
            "path": "src/main.py",
            "sha": "8901234567abcdef8901234567abcdef89012345",
            "content": "print('Hello, World!')",
        },
    },
}


def get_repository_readme(
    owner: str, repo_name: str, ref: Optional[str] = None
) -> Optional[Dict]:
    """Get repository README"""
    repo_key = f"{owner}/{repo_name}"
    if repo_key not in REPOSITORY_CONTENT_METADATA:
        return None

    # Search for README file
    readme_candidates = ["README.md", "README", "readme.md", "readme"]
    for candidate in readme_candidates:
        if candidate in REPOSITORY_CONTENT_METADATA[repo_key]:
            file_data = REPOSITORY_CONTENT_METADATA[repo_key][candidate]
            return format_file_response(owner, repo_name, file_data)

    return None


def get_contents(
    owner: str, repo_name: str, path: str = "", ref: Optional[str] = None
) -> Optional[Union[Dict, List[Dict]]]:
    """Get repository contents"""
    repo_key = f"{owner}/{repo_name}"
    if repo_key not in REPOSITORY_CONTENT_METADATA:
        return None

    # Path normalization
    path = path.strip("/")
    if path == "":
        # For root directory
        root_dir = REPOSITORY_CONTENT_METADATA[repo_key][""]
        contents = []
        for item_name in root_dir["contents"]:
            item_data = REPOSITORY_CONTENT_METADATA[repo_key][item_name]
            contents.append(
                format_content_response(
                    owner, repo_name, item_data, include_content=False
                )
            )
        return contents

    # For specific path
    if path not in REPOSITORY_CONTENT_METADATA[repo_key]:
        return None

    item_data = REPOSITORY_CONTENT_METADATA[repo_key][path]

    if item_data["type"] == "dir":
        # For directory
        contents = []
        for item_name in item_data["contents"]:
            full_path = f"{path}/{item_name}" if path else item_name
            if full_path in REPOSITORY_CONTENT_METADATA[repo_key]:
                sub_item_data = REPOSITORY_CONTENT_METADATA[repo_key][full_path]
                contents.append(
                    format_content_response(
                        owner, repo_name, sub_item_data, include_content=False
                    )
                )
        return contents
    else:
        # For files
        return format_file_response(owner, repo_name, item_data)


def create_or_update_file(
    owner: str, repo_name: str, path: str, file_data: Dict
) -> Optional[Dict]:
    """Create or update a file"""
    repo_key = f"{owner}/{repo_name}"
    if repo_key not in REPOSITORY_CONTENT_METADATA:
        return None

    # Path normalization
    path = path.strip("/")
    if not path:
        return None

    # Check and create directory structure
    dir_path = os.path.dirname(path)
    if dir_path:
        if dir_path not in REPOSITORY_CONTENT_METADATA[repo_key]:
            # Create parent directory if it does not exist
            parent_dir = os.path.dirname(dir_path) or ""
            if parent_dir not in REPOSITORY_CONTENT_METADATA[repo_key]:
                return None  # Fail if parent directory does not exist

            REPOSITORY_CONTENT_METADATA[repo_key][dir_path] = {
                "type": "dir",
                "name": os.path.basename(dir_path),
                "path": dir_path,
                "sha": generate_sha(),
                "contents": [],
            }

            # Add to parent directory contents
            REPOSITORY_CONTENT_METADATA[repo_key][parent_dir]["contents"].append(
                os.path.basename(dir_path)
            )

    # Decode file content
    try:
        content = base64.b64decode(file_data["content"]).decode("utf-8")
    except Exception:
        return None  # Fail if decode fails

    # Check SHA for updates
    is_update = path in REPOSITORY_CONTENT_METADATA[repo_key]
    if is_update and "sha" in file_data:
        if REPOSITORY_CONTENT_METADATA[repo_key][path]["sha"] != file_data["sha"]:
            return None  # Fail if SHA does not match

    # Generate new SHA
    new_sha = generate_sha()

    # Create or update file
    if not is_update:
        # Add to parent directory contents
        parent_dir = dir_path or ""
        if parent_dir not in REPOSITORY_CONTENT_METADATA[repo_key]:
            parent_dir = ""  # Root directory

        if (
            os.path.basename(path)
            not in REPOSITORY_CONTENT_METADATA[repo_key][parent_dir]["contents"]
        ):
            REPOSITORY_CONTENT_METADATA[repo_key][parent_dir]["contents"].append(
                os.path.basename(path)
            )

    # Update file data
    REPOSITORY_CONTENT_METADATA[repo_key][path] = {
        "type": "file",
        "name": os.path.basename(path),
        "path": path,
        "sha": new_sha,
        "content": content,
    }

    # Create response
    file_response = format_file_response(
        owner, repo_name, REPOSITORY_CONTENT_METADATA[repo_key][path]
    )

    # Create commit information
    commit = {
        "sha": generate_sha(),
        "url": f"/api/v3/repos/{owner}/{repo_name}/git/commits/{new_sha}",
        "html_url": f"/{owner}/{repo_name}/commit/{new_sha}",
        "author": {
            "name": file_data.get("author", {}).get("name", "User"),
            "email": file_data.get("author", {}).get("email", "user@example.com"),
        },
        "committer": {
            "name": file_data.get("committer", {}).get("name", "User"),
            "email": file_data.get("committer", {}).get("email", "user@example.com"),
        },
        "message": file_data["message"],
        "tree": {
            "sha": generate_sha(),
            "url": f"/api/v3/repos/{owner}/{repo_name}/git/trees/{new_sha}",
        },
        "parents": [],
    }

    # Add parent commit for updates
    if is_update:
        commit["parents"] = [
            {
                "sha": REPOSITORY_CONTENT_METADATA[repo_key][path]["sha"],
                "url": f"/api/v3/repos/{owner}/{repo_name}/git/commits/{REPOSITORY_CONTENT_METADATA[repo_key][path]['sha']}",
                "html_url": f"/{owner}/{repo_name}/commit/{REPOSITORY_CONTENT_METADATA[repo_key][path]['sha']}",
            }
        ]

    return {"content": file_response, "commit": commit}


def get_raw_content(owner: str, repo_name: str, path: str) -> Optional[str]:
    """Get raw file contents

    The path parameter should be in the format: {ref}/{file_path}
    where ref is the branch/commit/tag and file_path is the path to the file.
    For this mock implementation, we ignore the ref part and use the file_path.
    """
    repo_key = f"{owner}/{repo_name}"
    if repo_key not in REPOSITORY_CONTENT_METADATA:
        return None

    # Parse path to extract ref and file_path
    # Format: {ref}/{file_path}
    path_parts = path.strip("/").split("/", 1)
    if len(path_parts) < 2:
        # If no ref is provided, treat the entire path as file_path
        file_path = path.strip("/")
    else:
        # Extract ref and file_path
        # ref = path_parts[0]  # Currently ignored in mock implementation
        file_path = path_parts[1]

    if not file_path or file_path not in REPOSITORY_CONTENT_METADATA[repo_key]:
        return None

    item_data = REPOSITORY_CONTENT_METADATA[repo_key][file_path]
    if item_data["type"] != "file":
        return None

    return item_data["content"]


def format_file_response(owner: str, repo_name: str, file_data: Dict) -> Dict:
    """Format file response"""
    content = file_data["content"]
    encoded_content = base64.b64encode(content.encode("utf-8")).decode("utf-8")

    return {
        "type": "file",
        "name": file_data["name"],
        "path": file_data["path"],
        "sha": file_data["sha"],
        "content": encoded_content,
        "encoding": "base64",
        "download_url": f"/api/v3/repos/{owner}/{repo_name}/raw/{file_data['path']}",
    }


def format_content_response(
    owner: str, repo_name: str, item_data: Dict, include_content: bool = True
) -> Dict:
    """Format content response"""
    response = {
        "type": item_data["type"],
        "name": item_data["name"],
        "path": item_data["path"],
        "sha": item_data["sha"],
        "download_url": f"/api/v3/repos/{owner}/{repo_name}/raw/{item_data['path']}"
        if item_data["type"] == "file"
        else None,
    }

    if include_content and item_data["type"] == "file":
        content = item_data["content"]
        encoded_content = base64.b64encode(content.encode("utf-8")).decode("utf-8")
        response["content"] = encoded_content
        response["encoding"] = "base64"

    return response


def generate_sha() -> str:
    """Generate random SHA"""
    import random
    import string

    # Generate 40-character random hexadecimal
    return "".join(random.choice(string.hexdigits.lower()) for _ in range(40))
