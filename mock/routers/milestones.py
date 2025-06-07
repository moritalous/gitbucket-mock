from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response, status

from auth import verify_token
from data import (
    create_milestone,
    delete_milestone,
    get_milestone,
    get_repository_milestones,
    update_milestone,
)
from models.issues import ApiMilestone
from models.milestones import CreateAMilestone

router = APIRouter(tags=["Milestones"])


@router.get("/repos/{owner}/{repository}/milestones", response_model=List[ApiMilestone])
async def get_milestones(owner: str, repository: str, state: str = "all"):
    """Get list of milestones for a repository"""
    # State parameter validation
    if state not in ["open", "closed", "all"]:
        raise HTTPException(status_code=404, detail="Invalid state parameter")

    milestones = get_repository_milestones(owner, repository, state)
    if milestones is None:
        raise HTTPException(status_code=404, detail="Repository not found")

    return [ApiMilestone(**milestone) for milestone in milestones]


@router.get(
    "/repos/{owner}/{repository}/milestones/{milestone_number}",
    response_model=ApiMilestone,
)
async def get_milestone_info(owner: str, repository: str, milestone_number: int):
    """Get a specific milestone"""
    milestone = get_milestone(owner, repository, milestone_number)
    if milestone is None:
        raise HTTPException(status_code=404, detail="Milestone or repository not found")

    return ApiMilestone(**milestone)


@router.post("/repos/{owner}/{repository}/milestones", response_model=ApiMilestone)
async def create_new_milestone(
    owner: str,
    repository: str,
    milestone_data: CreateAMilestone,
    user: dict = Depends(verify_token),
):
    """Create a milestone

    Note: GitBucket has strict validation for milestone titles:
    - Maximum 100 characters
    - Only alphanumeric characters, hyphens, plus signs, underscores, and periods allowed
    - No spaces, Japanese characters, or other symbols permitted
    - Pattern: [a-zA-Z0-9\\-\\+_.]+
    """
    # Milestone validation (GitBucket's strict isValid check)
    if not milestone_data.is_valid():
        raise HTTPException(status_code=404, detail="Invalid milestone data")

    new_milestone = create_milestone(owner, repository, milestone_data.model_dump())
    if new_milestone is None:
        raise HTTPException(status_code=404, detail="Repository not found")

    return ApiMilestone(**new_milestone)


@router.patch(
    "/repos/{owner}/{repository}/milestones/{milestone_number}",
    response_model=ApiMilestone,
)
async def update_milestone_info(
    owner: str,
    repository: str,
    milestone_number: int,
    milestone_data: CreateAMilestone,
    user: dict = Depends(verify_token),
):
    """Update a milestone

    Note: GitBucket has strict validation for milestone titles:
    - Maximum 100 characters
    - Only alphanumeric characters, hyphens, plus signs, underscores, and periods allowed
    - No spaces, Japanese characters, or other symbols permitted
    - Pattern: [a-zA-Z0-9\\-\\+_.]+
    """
    # Milestone validation (GitBucket's strict isValid check)
    if not milestone_data.is_valid():
        raise HTTPException(status_code=404, detail="Invalid milestone data")

    updated_milestone = update_milestone(
        owner, repository, milestone_number, milestone_data.model_dump()
    )
    if updated_milestone is None:
        raise HTTPException(status_code=404, detail="Milestone or repository not found")

    return ApiMilestone(**updated_milestone)


@router.delete(
    "/repos/{owner}/{repository}/milestones/{milestone_number}", status_code=204
)
async def delete_milestone_info(
    owner: str,
    repository: str,
    milestone_number: int,
    user: dict = Depends(verify_token),
):
    """Delete a milestone"""
    success = delete_milestone(owner, repository, milestone_number)
    if not success:
        raise HTTPException(status_code=404, detail="Milestone or repository not found")

    return Response(status_code=status.HTTP_204_NO_CONTENT)
