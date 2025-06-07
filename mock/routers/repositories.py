from typing import List

from fastapi import APIRouter, Depends, HTTPException

from auth import verify_token
from data import (
    create_repository,
    get_all_public_repositories,
    get_organization_repositories,
    get_repository,
    get_repository_tags,
    get_user_repositories,
)
from models.repositories import ApiRepository, ApiTag, CreateARepository

router = APIRouter(tags=["Repositories"])


@router.get("/repositories", response_model=List[ApiRepository])
async def get_repositories():
    """Get all public repositories"""
    return [ApiRepository(**repo) for repo in get_all_public_repositories()]


@router.get("/user/repos", response_model=List[ApiRepository])
async def get_authenticated_user_repositories(user: dict = Depends(verify_token)):
    """Get repositories for authenticated user"""
    repos = get_user_repositories(user["username"])
    return [ApiRepository(**repo) for repo in repos]


@router.get("/users/{username}/repos", response_model=List[ApiRepository])
async def get_user_repos(username: str):
    """Get repositories for a specific user"""
    repos = get_user_repositories(username)
    return [ApiRepository(**repo) for repo in repos]


@router.get("/orgs/{org_name}/repos", response_model=List[ApiRepository])
async def get_organization_repos(org_name: str):
    """Get repositories for an organization"""
    repos = get_organization_repositories(org_name)
    return [ApiRepository(**repo) for repo in repos]


@router.get("/repos/{owner}/{repository}", response_model=ApiRepository)
async def get_repo(owner: str, repository: str):
    """Get specific repository information"""
    repo = get_repository(owner, repository)
    if not repo:
        raise HTTPException(status_code=404, detail="Repository not found")
    return ApiRepository(**repo)


@router.post("/user/repos", response_model=ApiRepository)
async def create_user_repository(
    repo_data: CreateARepository, user: dict = Depends(verify_token)
):
    """Create a repository for authenticated user"""
    new_repo = create_repository(user["username"], repo_data.model_dump())
    if not new_repo:
        raise HTTPException(status_code=400, detail="Repository already exists")
    return ApiRepository(**new_repo)


@router.post("/orgs/{org_name}/repos", response_model=ApiRepository)
async def create_organization_repository(
    org_name: str, repo_data: CreateARepository, user: dict = Depends(verify_token)
):
    """Create a repository for an organization"""
    # Organization existence check and permission check omitted (for mock implementation)
    new_repo = create_repository(org_name, repo_data.model_dump())
    if not new_repo:
        raise HTTPException(
            status_code=400,
            detail="Repository already exists or organization not found",
        )
    return ApiRepository(**new_repo)


@router.get("/repos/{owner}/{repository}/tags", response_model=List[ApiTag])
async def get_repo_tags(owner: str, repository: str):
    """Get tags for a repository"""
    tags = get_repository_tags(owner, repository)
    if tags is None:
        raise HTTPException(status_code=404, detail="Repository not found")
    return [ApiTag(**tag) for tag in tags]
