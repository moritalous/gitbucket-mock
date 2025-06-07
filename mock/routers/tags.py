from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path
from fastapi.security import OAuth2PasswordBearer

from models.base import ApiPath
from models.repositories import ApiTag, ApiTagCommit

router = APIRouter(tags=["Tags"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get(
    "/repos/{owner}/{repository}/tags",
    response_model=List[ApiTag],
    summary="List repository tags",
    description="Retrieves a list of tags for a repository.",
)
async def list_repository_tags(
    owner: str = Path(..., description="The owner of the repository"),
    repository: str = Path(..., description="The name of the repository"),
    token: str = Depends(oauth2_scheme),
) -> List[ApiTag]:
    """
    List repository tags.

    Args:
        owner: The owner of the repository
        repository: The name of the repository
        token: OAuth2 token

    Returns:
        List[ApiTag]: List of repository tags

    Raises:
        HTTPException: If repository not found
    """
    # This mock returns a fixed list of tags
    # In actual implementation, check repository existence and retrieve tags

    # Return 404 if repository does not exist
    if owner == "nonexistent" or repository == "nonexistent":
        raise HTTPException(status_code=404, detail="Repository not found")

    # Return mock data
    return [
        ApiTag(
            name="v1.0.0",
            commit=ApiTagCommit(
                sha="6dcb09b5b57875f334f61aebed695e2e4193db5e",
                url=ApiPath(
                    f"/api/v3/repos/{owner}/{repository}/commits/6dcb09b5b57875f334f61aebed695e2e4193db5e"
                ),
            ),
            zipball_url=ApiPath(f"/api/v3/repos/{owner}/{repository}/zipball/v1.0.0"),
            tarball_url=ApiPath(f"/api/v3/repos/{owner}/{repository}/tarball/v1.0.0"),
        ),
        ApiTag(
            name="v0.9.0",
            commit=ApiTagCommit(
                sha="6dcb09b5b57875f334f61aebed695e2e4193db5f",
                url=ApiPath(
                    f"/api/v3/repos/{owner}/{repository}/commits/6dcb09b5b57875f334f61aebed695e2e4193db5f"
                ),
            ),
            zipball_url=ApiPath(f"/api/v3/repos/{owner}/{repository}/zipball/v0.9.0"),
            tarball_url=ApiPath(f"/api/v3/repos/{owner}/{repository}/tarball/v0.9.0"),
        ),
    ]
