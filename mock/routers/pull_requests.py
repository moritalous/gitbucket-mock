"""
GitBucket Pull Requests API Router

IMPORTANT: GitBucket's Pull Request API has implementation issues that differ from GitHub:

1. Merge Status Check Issue:
   - GitBucket's checkConflict() checks merge POSSIBILITY, not merge STATUS
   - Returns 204 for mergeable, conflicted, AND actually merged PRs
   - Cannot reliably determine if a PR is actually merged

2. This affects the GET /pulls/:id/merge endpoint behavior significantly.

This implementation follows GitBucket's actual (flawed) API behavior.
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status

from auth import verify_token
from data import (
    create_pull_request,
    get_pull_request,
    get_pull_request_commits,
    get_repository_pull_requests,
    is_pull_request_merged,
    merge_pull_request,
    update_pull_request,
)
from models.commits import ApiCommitListItem
from models.pull_requests import (
    ApiPullRequest,
    CreateAPullRequest,
    MergeAPullRequest,
    SuccessToMergePrResponse,
    UpdateAPullRequest,
)

router = APIRouter(tags=["PullRequests"])


@router.get("/repos/{owner}/{repository}/pulls", response_model=List[ApiPullRequest])
async def get_pull_requests(
    owner: str,
    repository: str,
    state: str = "open",
    page: int = Query(1, ge=1),
    per_page: int = Query(30, ge=1, le=100),
):
    """Get list of pull requests for a repository"""
    pull_requests = get_repository_pull_requests(
        owner, repository, state, page, per_page
    )
    if pull_requests is None:
        raise HTTPException(status_code=404, detail="Repository not found")

    return [ApiPullRequest(**pr) for pr in pull_requests]


@router.get(
    "/repos/{owner}/{repository}/pulls/{pr_number}", response_model=ApiPullRequest
)
async def get_pull_request_info(owner: str, repository: str, pr_number: int):
    """Get a specific pull request"""
    pr = get_pull_request(owner, repository, pr_number)
    if pr is None:
        raise HTTPException(
            status_code=404, detail="Pull request or repository not found"
        )

    return ApiPullRequest(**pr)


@router.post("/repos/{owner}/{repository}/pulls", response_model=ApiPullRequest)
async def create_new_pull_request(
    owner: str,
    repository: str,
    pr_data: CreateAPullRequest,
    user: dict = Depends(verify_token),
):
    """Create a pull request"""
    new_pr = create_pull_request(
        owner, repository, pr_data.model_dump(), user["username"]
    )
    if new_pr is None:
        raise HTTPException(
            status_code=404, detail="Repository not found or invalid parameters"
        )

    return ApiPullRequest(**new_pr)


@router.patch(
    "/repos/{owner}/{repository}/pulls/{pr_number}", response_model=ApiPullRequest
)
async def update_pull_request_info(
    owner: str,
    repository: str,
    pr_number: int,
    pr_data: UpdateAPullRequest,
    user: dict = Depends(verify_token),
):
    """Update a pull request"""
    updated_pr = update_pull_request(
        owner, repository, pr_number, pr_data.model_dump(exclude_unset=True)
    )
    if updated_pr is None:
        raise HTTPException(
            status_code=404, detail="Pull request or repository not found"
        )

    return ApiPullRequest(**updated_pr)


@router.get(
    "/repos/{owner}/{repository}/pulls/{pr_number}/commits",
    response_model=List[ApiCommitListItem],
)
async def get_pull_request_commit_list(owner: str, repository: str, pr_number: int):
    """Get list of commits for a pull request"""
    commits = get_pull_request_commits(owner, repository, pr_number)
    if commits is None:
        raise HTTPException(
            status_code=404, detail="Pull request or repository not found"
        )

    return [ApiCommitListItem(**commit) for commit in commits]


@router.get("/repos/{owner}/{repository}/pulls/{pr_number}/merge")
async def check_pull_request_merged(owner: str, repository: str, pr_number: int):
    """Check if a pull request is merged

    IMPORTANT: GitBucket's implementation has logical issues and differs from GitHub API.

    GitBucket's checkConflict() function checks merge POSSIBILITY, not merge STATUS:
    - Returns 204 when: PR is mergeable OR has conflicts OR is actually merged
    - Returns 404 when: Merge status is unknown/uncached

    This means GitBucket incorrectly returns 204 for:
    1. ✅ Actually merged pull requests (correct)
    2. ❌ Unmerged but mergeable pull requests (wrong)
    3. ❌ Unmerged pull requests with conflicts (wrong)

    GitHub API behavior:
    - 204: Pull request IS merged
    - 404: Pull request is NOT merged

    GitBucket API behavior:
    - 204: Pull request is mergeable, has conflicts, OR is merged
    - 404: Merge status unknown or PR/repo not found

    Due to this implementation issue, you cannot reliably determine if a PR is
    actually merged using this endpoint in GitBucket.
    """
    merged = is_pull_request_merged(owner, repository, pr_number)
    if not merged:
        raise HTTPException(
            status_code=404,
            detail="Pull request has not been merged or pull request/repository not found",
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put(
    "/repos/{owner}/{repository}/pulls/{pr_number}/merge",
    response_model=SuccessToMergePrResponse,
)
async def merge_pull_request_endpoint(
    owner: str,
    repository: str,
    pr_number: int,
    merge_data: MergeAPullRequest,
    user: dict = Depends(verify_token),
):
    """Merge a pull request"""
    result = merge_pull_request(
        owner, repository, pr_number, merge_data.model_dump(), user["username"]
    )
    if result is None:
        raise HTTPException(
            status_code=404, detail="Pull request or repository not found"
        )

    # In case of error
    if isinstance(result, tuple):
        status_code, error_data = result
        raise HTTPException(status_code=status_code, detail=error_data["message"])

    return SuccessToMergePrResponse(**result)
