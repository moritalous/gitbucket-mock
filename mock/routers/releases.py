"""
GitBucket Release API Router

IMPORTANT: GitBucket's Release API differs significantly from GitHub's API:
- No Release ID concept: GitBucket uses tag names instead of release IDs
- Missing endpoint: GET /api/v3/repos/:owner/:repository/releases/:id is NOT implemented
- Tag-based operations: Update and delete operations use :tag instead of :release_id
- Asset handling: Asset operations require both tag name and file ID

ASSET UPLOAD LIMITATIONS:
- GitBucket's asset upload implementation has file system dependencies
- May fail with 500 Internal Server Error in restricted/containerized environments
- Uses request.inputStream.available() which can be unreliable
- Requires write permissions to release files directory

This implementation follows GitBucket's actual API behavior, including potential failures.
"""

from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path, Response, status
from fastapi.security import OAuth2PasswordBearer

from models.base import ApiPath
from models.releases import ApiRelease, ApiReleaseAsset, CreateARelease
from models.users import ApiUser

router = APIRouter(tags=["Releases"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get(
    "/repos/{owner}/{repository}/releases",
    response_model=List[ApiRelease],
    summary="List releases",
    description="Retrieves a list of releases for a repository.",
)
async def list_releases(
    owner: str = Path(..., description="The owner of the repository"),
    repository: str = Path(..., description="The name of the repository"),
    token: str = Depends(oauth2_scheme),
) -> List[ApiRelease]:
    """
    List releases for a repository.

    Args:
        owner: The owner of the repository
        repository: The name of the repository
        token: OAuth2 token

    Returns:
        List[ApiRelease]: List of releases

    Raises:
        HTTPException: If repository not found
    """
    # Return 404 if repository does not exist
    if owner == "nonexistent" or repository == "nonexistent":
        raise HTTPException(status_code=404, detail="Repository not found")

    # Return mock data
    return [
        ApiRelease(
            name="Release v1.0.0",
            tag_name="v1.0.0",
            body="Initial stable release",
            author=ApiUser(
                login="admin",
                id=1,
                email="admin@example.com",
                type="User",
                site_admin=True,
                created_at=datetime.now(),
                url=ApiPath("/api/v3/users/admin"),
                html_url=ApiPath("/admin"),
                avatar_url=ApiPath("/admin/avatar"),
            ),
            assets=[
                ApiReleaseAsset(
                    name="app-v1.0.0.zip",
                    size=1024,
                    label="app-v1.0.0.zip",
                    file_id="1",
                    browser_download_url=ApiPath(
                        f"/api/v3/repos/{owner}/{repository}/releases/v1.0.0/assets/1"
                    ),
                )
            ],
        ),
        ApiRelease(
            name="Beta Release",
            tag_name="v0.9.0",
            body="Beta release with new features",
            author=ApiUser(
                login="admin",
                id=1,
                email="admin@example.com",
                type="User",
                site_admin=True,
                created_at=datetime.now(),
                url=ApiPath("/api/v3/users/admin"),
                html_url=ApiPath("/admin"),
                avatar_url=ApiPath("/admin/avatar"),
            ),
            assets=[],
        ),
    ]


@router.get(
    "/repos/{owner}/{repository}/releases/latest",
    response_model=ApiRelease,
    summary="Get the latest release",
    description="Retrieves the latest release for a repository.",
)
async def get_latest_release(
    owner: str = Path(..., description="The owner of the repository"),
    repository: str = Path(..., description="The name of the repository"),
    token: str = Depends(oauth2_scheme),
) -> ApiRelease:
    """
    Get the latest release for a repository.

    Args:
        owner: The owner of the repository
        repository: The name of the repository
        token: OAuth2 token

    Returns:
        ApiRelease: Latest release information

    Raises:
        HTTPException: If repository not found or no releases exist
    """
    # Return 404 if repository does not exist
    if owner == "nonexistent" or repository == "nonexistent":
        raise HTTPException(status_code=404, detail="Repository not found")

    # Return mock data (latest release)
    return ApiRelease(
        name="Release v1.0.0",
        tag_name="v1.0.0",
        body="Initial stable release",
        author=ApiUser(
            login="admin",
            id=1,
            email="admin@example.com",
            type="User",
            site_admin=True,
            created_at=datetime.now(),
            url=ApiPath("/api/v3/users/admin"),
            html_url=ApiPath("/admin"),
            avatar_url=ApiPath("/admin/avatar"),
        ),
        assets=[
            ApiReleaseAsset(
                name="app-v1.0.0.zip",
                size=1024,
                label="app-v1.0.0.zip",
                file_id="1",
                browser_download_url=ApiPath(
                    f"/api/v3/repos/{owner}/{repository}/releases/v1.0.0/assets/1"
                ),
            )
        ],
    )


@router.get(
    "/repos/{owner}/{repository}/releases/tags/{tag}",
    response_model=ApiRelease,
    summary="Get a release by tag name",
    description="Retrieves a specific release by its tag name. This is the primary way to get a specific release in GitBucket since release IDs are not supported.",
)
async def get_release_by_tag(
    owner: str = Path(..., description="The owner of the repository"),
    repository: str = Path(..., description="The name of the repository"),
    tag: str = Path(..., description="The tag name of the release"),
    token: str = Depends(oauth2_scheme),
) -> ApiRelease:
    """
    Get a specific release by tag name.

    GitBucket Specific: This is the primary way to get a specific release in GitBucket
    since release IDs are not supported.

    Args:
        owner: The owner of the repository
        repository: The name of the repository
        tag: The tag name of the release
        token: OAuth2 token

    Returns:
        ApiRelease: Release information

    Raises:
        HTTPException: If repository or release not found
    """
    # Return 404 if repository does not exist
    if owner == "nonexistent" or repository == "nonexistent":
        raise HTTPException(status_code=404, detail="Repository not found")

    # Return 404 if release does not exist
    if tag not in ["v1.0.0", "v0.9.0"]:
        raise HTTPException(status_code=404, detail="Release not found")

    # Return mock data
    if tag == "v1.0.0":
        return ApiRelease(
            name="Release v1.0.0",
            tag_name="v1.0.0",
            body="Initial stable release",
            author=ApiUser(
                login="admin",
                id=1,
                email="admin@example.com",
                type="User",
                site_admin=True,
                created_at=datetime.now(),
                url=ApiPath("/api/v3/users/admin"),
                html_url=ApiPath("/admin"),
                avatar_url=ApiPath("/admin/avatar"),
            ),
            assets=[
                ApiReleaseAsset(
                    name="app-v1.0.0.zip",
                    size=1024,
                    label="app-v1.0.0.zip",
                    file_id="1",
                    browser_download_url=ApiPath(
                        f"/api/v3/repos/{owner}/{repository}/releases/v1.0.0/assets/1"
                    ),
                )
            ],
        )
    else:
        return ApiRelease(
            name="Beta Release",
            tag_name="v0.9.0",
            body="Beta release with new features",
            author=ApiUser(
                login="admin",
                id=1,
                email="admin@example.com",
                type="User",
                site_admin=True,
                created_at=datetime.now(),
                url=ApiPath("/api/v3/users/admin"),
                html_url=ApiPath("/admin"),
                avatar_url=ApiPath("/admin/avatar"),
            ),
            assets=[],
        )


@router.post(
    "/repos/{owner}/{repository}/releases",
    response_model=ApiRelease,
    summary="Create a release",
    description="Creates a new release in a repository.",
)
async def create_release(
    release: CreateARelease,
    owner: str = Path(..., description="The owner of the repository"),
    repository: str = Path(..., description="The name of the repository"),
    token: str = Depends(oauth2_scheme),
) -> ApiRelease:
    """
    Create a new release.

    Note: GitBucket ignores 'draft' and 'prerelease' fields as they are not implemented.

    Args:
        release: Release data
        owner: The owner of the repository
        repository: The name of the repository
        token: OAuth2 token

    Returns:
        ApiRelease: Created release information

    Raises:
        HTTPException: If repository not found or user not authorized
    """
    # Return 404 if repository does not exist
    if owner == "nonexistent" or repository == "nonexistent":
        raise HTTPException(status_code=404, detail="Repository not found")

    # Return mock data
    return ApiRelease(
        name=release.name or release.tag_name,
        tag_name=release.tag_name,
        body=release.body,
        author=ApiUser(
            login="admin",
            id=1,
            email="admin@example.com",
            type="User",
            site_admin=True,
            created_at=datetime.now(),
            url=ApiPath("/api/v3/users/admin"),
            html_url=ApiPath("/admin"),
            avatar_url=ApiPath("/admin/avatar"),
        ),
        assets=[],
    )


@router.patch(
    "/repos/{owner}/{repository}/releases/{tag}",
    response_model=ApiRelease,
    summary="Update a release",
    description="Updates an existing release. GitBucket Specific: Uses :tag parameter instead of :release_id like GitHub API.",
)
async def update_release(
    release: CreateARelease,
    owner: str = Path(..., description="The owner of the repository"),
    repository: str = Path(..., description="The name of the repository"),
    tag: str = Path(..., description="The tag name of the release to update"),
    token: str = Depends(oauth2_scheme),
) -> ApiRelease:
    """
    Update a release.

    GitBucket Specific: Uses :tag parameter instead of :release_id like GitHub API.
    Note: GitBucket ignores 'draft' and 'prerelease' fields as they are not implemented.

    Args:
        release: Updated release data
        owner: The owner of the repository
        repository: The name of the repository
        tag: The tag name of the release to update
        token: OAuth2 token

    Returns:
        ApiRelease: Updated release information

    Raises:
        HTTPException: If repository or release not found, or user not authorized
    """
    # Return 404 if repository does not exist
    if owner == "nonexistent" or repository == "nonexistent":
        raise HTTPException(status_code=404, detail="Repository not found")

    # Return 404 if release does not exist
    if tag not in ["v1.0.0", "v0.9.0"]:
        raise HTTPException(status_code=404, detail="Release not found")

    # Return mock data
    return ApiRelease(
        name=release.name or release.tag_name,
        tag_name=release.tag_name,
        body=release.body,
        author=ApiUser(
            login="admin",
            id=1,
            email="admin@example.com",
            type="User",
            site_admin=True,
            created_at=datetime.now(),
            url=ApiPath("/api/v3/users/admin"),
            html_url=ApiPath("/admin"),
            avatar_url=ApiPath("/admin/avatar"),
        ),
        assets=[
            ApiReleaseAsset(
                name="app-v1.0.0.zip",
                size=1024,
                label="app-v1.0.0.zip",
                file_id="1",
                browser_download_url=ApiPath(
                    f"/api/v3/repos/{owner}/{repository}/releases/{tag}/assets/1"
                ),
            )
        ]
        if tag == "v1.0.0"
        else [],
    )


@router.delete(
    "/repos/{owner}/{repository}/releases/{tag}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a release",
    description="Deletes a release from a repository. GitBucket Specific: Uses :tag parameter instead of :release_id like GitHub API.",
)
async def delete_release(
    owner: str = Path(..., description="The owner of the repository"),
    repository: str = Path(..., description="The name of the repository"),
    tag: str = Path(..., description="The tag name of the release to delete"),
    token: str = Depends(oauth2_scheme),
) -> Response:
    """
    Delete a release.

    GitBucket Specific: Uses :tag parameter instead of :release_id like GitHub API.

    Args:
        owner: The owner of the repository
        repository: The name of the repository
        tag: The tag name of the release to delete
        token: OAuth2 token

    Returns:
        Response: Empty response with 204 status code

    Raises:
        HTTPException: If repository or release not found, or user not authorized
    """
    # Return 404 if repository does not exist
    if owner == "nonexistent" or repository == "nonexistent":
        raise HTTPException(status_code=404, detail="Repository not found")

    # Return 404 if release does not exist
    if tag not in ["v1.0.0", "v0.9.0"]:
        raise HTTPException(status_code=404, detail="Release not found")

    # Return 204 No Content
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post(
    "/repos/{owner}/{repository}/releases/{tag}/assets",
    response_model=ApiReleaseAsset,
    summary="Upload a release asset",
    description="Uploads an asset to a release.",
)
async def upload_release_asset(
    owner: str = Path(..., description="The owner of the repository"),
    repository: str = Path(..., description="The name of the repository"),
    tag: str = Path(..., description="The tag name of the release"),
    name: str = Path(..., description="The name of the asset"),
    token: str = Depends(oauth2_scheme),
) -> ApiReleaseAsset:
    """
    Upload an asset to a release.

    IMPORTANT: GitBucket's actual implementation may encounter issues:
    - Uses request.inputStream.available() for file size detection
    - Requires write permissions to release files directory
    - May fail with 500 Internal Server Error in restricted environments
    - File system dependencies can cause failures in containerized environments

    This mock implementation simulates successful upload, but real GitBucket
    may return 500 errors due to environment constraints.

    Args:
        owner: The owner of the repository
        repository: The name of the repository
        tag: The tag name of the release
        name: The name of the asset
        token: OAuth2 token

    Returns:
        ApiReleaseAsset: Uploaded asset information

    Raises:
        HTTPException: If repository or release not found, or user not authorized
        HTTPException: 500 Internal Server Error (common in GitBucket due to file system issues)
    """
    # Return 404 if repository does not exist
    if owner == "nonexistent" or repository == "nonexistent":
        raise HTTPException(status_code=404, detail="Repository not found")

    # Return 404 if release does not exist
    if tag not in ["v1.0.0", "v0.9.0"]:
        raise HTTPException(status_code=404, detail="Release not found")

    # Simulate GitBucket's potential 500 error for certain conditions
    # In real GitBucket, this often happens due to file system constraints
    if name.startswith("error_"):
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error - File system operation failed",
        )

    # Return mock asset data
    return ApiReleaseAsset(
        name=name,
        size=2048,
        label=name,
        file_id="new_asset_id",
        browser_download_url=ApiPath(
            f"/api/v3/repos/{owner}/{repository}/releases/{tag}/assets/new_asset_id"
        ),
    )


@router.get(
    "/repos/{owner}/{repository}/releases/{tag}/assets/{file_id}",
    response_model=ApiReleaseAsset,
    summary="Get a release asset",
    description="Retrieves a specific release asset. GitBucket Specific: Requires both :tag and :file_id parameters, unlike GitHub which only needs :asset_id.",
)
async def get_release_asset(
    owner: str = Path(..., description="The owner of the repository"),
    repository: str = Path(..., description="The name of the repository"),
    tag: str = Path(..., description="The tag name of the release"),
    file_id: str = Path(..., description="The file ID of the asset"),
    token: str = Depends(oauth2_scheme),
) -> ApiReleaseAsset:
    """
    Get a specific release asset.

    GitBucket Specific: Requires both :tag and :file_id parameters, unlike GitHub
    which only needs :asset_id.

    Args:
        owner: The owner of the repository
        repository: The name of the repository
        tag: The tag name of the release
        file_id: The file ID of the asset
        token: OAuth2 token

    Returns:
        ApiReleaseAsset: Asset information

    Raises:
        HTTPException: If repository, release, or asset not found
    """
    # Return 404 if repository does not exist
    if owner == "nonexistent" or repository == "nonexistent":
        raise HTTPException(status_code=404, detail="Repository not found")

    # Return 404 if release does not exist
    if tag not in ["v1.0.0", "v0.9.0"]:
        raise HTTPException(status_code=404, detail="Release not found")

    # Return 404 if asset does not exist
    if file_id not in ["1", "new_asset_id"]:
        raise HTTPException(status_code=404, detail="Asset not found")

    # Return mock asset data
    return ApiReleaseAsset(
        name="app-v1.0.0.zip" if file_id == "1" else "uploaded-asset.zip",
        size=1024 if file_id == "1" else 2048,
        label="app-v1.0.0.zip" if file_id == "1" else "uploaded-asset.zip",
        file_id=file_id,
        browser_download_url=ApiPath(
            f"/api/v3/repos/{owner}/{repository}/releases/{tag}/assets/{file_id}"
        ),
    )
