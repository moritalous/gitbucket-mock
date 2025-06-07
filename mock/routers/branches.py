from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response, status

from auth import verify_token
from data import (
    delete_branch_protection,
    get_branch,
    get_branch_protection,
    get_repository_branches,
    get_required_status_check_contexts,
    get_required_status_checks,
    update_branch_protection,
)
from models.branches import (
    ApiBranch,
    ApiBranchForList,
    ApiBranchProtection,
    ApiBranchProtectionStatus,
    ApiBranchProtectionUpdate,
)

router = APIRouter(tags=["Branches"])


@router.get(
    "/repos/{owner}/{repository}/branches", response_model=List[ApiBranchForList]
)
async def get_branches(owner: str, repository: str):
    """Get list of branches for a repository"""
    branches = get_repository_branches(owner, repository)
    if branches is None:
        raise HTTPException(status_code=404, detail="Repository not found")
    return [ApiBranchForList(**branch) for branch in branches]


@router.get("/repos/{owner}/{repository}/branches/{branch}", response_model=ApiBranch)
async def get_branch_info(owner: str, repository: str, branch: str):
    """Get specific branch information"""
    branch_data = get_branch(owner, repository, branch)
    if branch_data is None:
        raise HTTPException(status_code=404, detail="Branch or repository not found")
    return ApiBranch(**branch_data)


@router.get(
    "/repos/{owner}/{repository}/branches/{branch}/protection",
    response_model=ApiBranchProtection,
)
async def get_branch_protection_info(owner: str, repository: str, branch: str):
    """Get branch protection settings"""
    protection = get_branch_protection(owner, repository, branch)
    if protection is None:
        raise HTTPException(status_code=404, detail="Branch or repository not found")
    return ApiBranchProtection(**protection)


@router.get(
    "/repos/{owner}/{repository}/branches/{branch}/protection/required_status_checks",
    response_model=ApiBranchProtectionStatus,
)
async def get_branch_required_status_checks(owner: str, repository: str, branch: str):
    """Get required status checks for a branch"""
    status_checks = get_required_status_checks(owner, repository, branch)
    if status_checks is None:
        raise HTTPException(
            status_code=404,
            detail="Branch or repository not found, or branch protection not enabled",
        )
    return ApiBranchProtectionStatus(**status_checks)


@router.get(
    "/repos/{owner}/{repository}/branches/{branch}/protection/required_status_checks/contexts",
    response_model=List[str],
)
async def get_branch_required_status_check_contexts(
    owner: str, repository: str, branch: str
):
    """Get required status check contexts for a branch"""
    contexts = get_required_status_check_contexts(owner, repository, branch)
    if contexts is None:
        raise HTTPException(
            status_code=404,
            detail="Branch or repository not found, or branch protection not enabled",
        )
    return contexts


@router.patch("/repos/{owner}/{repository}/branches/{branch}", response_model=ApiBranch)
async def update_branch_protection_settings(
    owner: str,
    repository: str,
    branch: str,
    protection_data: ApiBranchProtectionUpdate,
    user: dict = Depends(verify_token),
):
    """Update branch protection settings"""
    # Permission check (omitted in mock implementation)
    # In actual implementation, need to check if user is repository owner

    updated_branch = update_branch_protection(
        owner, repository, branch, protection_data.model_dump()
    )
    if updated_branch is None:
        raise HTTPException(status_code=404, detail="Branch or repository not found")

    return ApiBranch(**updated_branch)


@router.delete(
    "/repos/{owner}/{repository}/branches/{branch}/protection", status_code=204
)
async def delete_branch_protection_settings(
    owner: str, repository: str, branch: str, user: dict = Depends(verify_token)
):
    """Delete branch protection settings"""
    # Permission check (omitted in mock implementation)
    # In actual implementation, need to check if user is repository owner

    success = delete_branch_protection(owner, repository, branch)
    if not success:
        raise HTTPException(status_code=404, detail="Branch or repository not found")

    return Response(status_code=status.HTTP_204_NO_CONTENT)
