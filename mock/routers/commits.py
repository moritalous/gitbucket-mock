from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from auth import verify_token
from data import (
    create_commit_status,
    get_branches_for_head_commit,
    get_combined_status,
    get_commit,
    get_commit_statuses,
    get_repository_commits,
)
from models.branches import ApiBranchForHeadCommit
from models.commits import (
    ApiCombinedCommitStatus,
    ApiCommitListItem,
    ApiCommits,
    ApiCommitStatus,
    CreateAStatus,
)

router = APIRouter(tags=["Commits"])


@router.get(
    "/repos/{owner}/{repository}/commits", response_model=List[ApiCommitListItem]
)
async def get_commits(
    owner: str,
    repository: str,
    sha: Optional[str] = None,
    path: Optional[str] = None,
    author: Optional[str] = None,
    since: Optional[datetime] = None,
    until: Optional[datetime] = None,
    page: int = Query(1, ge=1),
    per_page: int = Query(30, ge=1, le=100),
):
    """Get list of commits for a repository"""
    commits = get_repository_commits(
        owner, repository, sha, path, author, since, until, page, per_page
    )
    if commits is None:
        raise HTTPException(status_code=404, detail="Repository not found")

    return [ApiCommitListItem(**commit) for commit in commits]


@router.get("/repos/{owner}/{repository}/commits/{sha}", response_model=ApiCommits)
async def get_commit_info(owner: str, repository: str, sha: str):
    """Get specific commit information"""
    commit = get_commit(owner, repository, sha)
    if commit is None:
        raise HTTPException(status_code=404, detail="Commit or repository not found")

    return ApiCommits(**commit)


@router.get(
    "/repos/{owner}/{repository}/commits/{sha}/branches-where-head",
    response_model=List[ApiBranchForHeadCommit],
)
async def get_branches_where_head(owner: str, repository: str, sha: str):
    """Get branches where specific commit is HEAD"""
    branches = get_branches_for_head_commit(owner, repository, sha)
    if branches is None:
        raise HTTPException(status_code=404, detail="Commit or repository not found")

    return [ApiBranchForHeadCommit(**branch) for branch in branches]


@router.get(
    "/repos/{owner}/{repository}/commits/{ref}/status",
    response_model=ApiCombinedCommitStatus,
)
async def get_combined_commit_status(owner: str, repository: str, ref: str):
    """Get combined status for a specific reference"""
    status = get_combined_status(owner, repository, ref)
    if status is None:
        raise HTTPException(status_code=404, detail="Reference or repository not found")

    return ApiCombinedCommitStatus(**status)


@router.get(
    "/repos/{owner}/{repository}/commits/{ref}/statuses",
    response_model=List[ApiCommitStatus],
)
async def get_commit_status_list(owner: str, repository: str, ref: str):
    """Get list of statuses for a specific reference"""
    statuses = get_commit_statuses(owner, repository, ref)
    if statuses is None:
        raise HTTPException(status_code=404, detail="Reference or repository not found")

    return [ApiCommitStatus(**status) for status in statuses]


@router.post(
    "/repos/{owner}/{repository}/statuses/{sha}", response_model=ApiCommitStatus
)
async def create_status(
    owner: str,
    repository: str,
    sha: str,
    status_data: CreateAStatus,
    user: dict = Depends(verify_token),
):
    """Create a commit status"""
    # Status data validation
    if not status_data.is_valid():
        raise HTTPException(status_code=400, detail="Invalid status data")

    status = create_commit_status(owner, repository, sha, status_data.model_dump())
    if status is None:
        raise HTTPException(status_code=404, detail="Commit or repository not found")

    return ApiCommitStatus(**status)
