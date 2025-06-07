from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response, status

from auth import verify_token
from data import (
    add_collaborator,
    check_collaborator,
    get_collaborator_permission,
    get_repository_collaborators,
    remove_collaborator,
)
from models.collaborators import AddACollaborator, ApiRepositoryCollaborator
from models.users import ApiUser

router = APIRouter(tags=["Collaborators"])


@router.get("/repos/{owner}/{repository}/collaborators", response_model=List[ApiUser])
async def get_collaborators(owner: str, repository: str):
    """Get collaborators for a repository"""
    collaborators = get_repository_collaborators(owner, repository)
    if collaborators is None:
        raise HTTPException(status_code=404, detail="Repository not found")
    return [ApiUser(**user) for user in collaborators]


@router.get("/repos/{owner}/{repository}/collaborators/{username}")
async def check_user_is_collaborator(owner: str, repository: str, username: str):
    """Check if user is a repository collaborator"""
    is_collaborator = check_collaborator(owner, repository, username)
    if not is_collaborator:
        raise HTTPException(
            status_code=404, detail="User is not a collaborator or repository not found"
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    "/repos/{owner}/{repository}/collaborators/{username}/permission",
    response_model=ApiRepositoryCollaborator,
)
async def get_user_permission(owner: str, repository: str, username: str):
    """Get collaborator permissions"""
    result = get_collaborator_permission(owner, repository, username)
    if result is None:
        raise HTTPException(
            status_code=404, detail="User is not a collaborator or repository not found"
        )

    permission, user = result
    return ApiRepositoryCollaborator(permission=permission, user=ApiUser(**user))


@router.put("/repos/{owner}/{repository}/collaborators/{username}", status_code=204)
async def add_repository_collaborator(
    owner: str,
    repository: str,
    username: str,
    collaborator_data: AddACollaborator,
    user: dict = Depends(verify_token),
):
    """Add a collaborator"""
    # Permission check (omitted in mock implementation)
    # In actual implementation, need to check if user is repository owner

    success = add_collaborator(owner, repository, username, collaborator_data.role)
    if not success:
        raise HTTPException(status_code=404, detail="Repository or user not found")

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("/repos/{owner}/{repository}/collaborators/{username}", status_code=204)
async def remove_repository_collaborator(
    owner: str, repository: str, username: str, user: dict = Depends(verify_token)
):
    """Remove a collaborator"""
    # Permission check (omitted in mock implementation)
    # In actual implementation, need to check if user is repository owner

    success = remove_collaborator(owner, repository, username)
    if not success:
        raise HTTPException(
            status_code=404, detail="Repository not found or user is not a collaborator"
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)
