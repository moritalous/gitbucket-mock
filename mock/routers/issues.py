from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query

from auth import verify_token
from data import (
    create_comment,
    create_issue,
    delete_comment,
    get_comment,
    get_issue,
    get_issue_comments,
    get_repository_issues,
    update_comment,
    update_issue,
)
from models.issues import ApiComment, ApiIssue, CreateAComment, CreateAnIssue

router = APIRouter(tags=["Issues"])


@router.get("/repos/{owner}/{repository}/issues", response_model=List[ApiIssue])
async def get_issues(
    owner: str,
    repository: str,
    state: str = "open",
    page: int = Query(1, ge=1),
    per_page: int = Query(30, ge=1, le=100),
):
    """Get list of issues for a repository"""
    issues = get_repository_issues(owner, repository, state, page, per_page)
    if issues is None:
        raise HTTPException(status_code=404, detail="Repository not found")

    return [ApiIssue(**issue) for issue in issues]


@router.get(
    "/repos/{owner}/{repository}/issues/{issue_number}", response_model=ApiIssue
)
async def get_issue_info(owner: str, repository: str, issue_number: int):
    """Get a specific issue"""
    issue = get_issue(owner, repository, issue_number)
    if issue is None:
        raise HTTPException(status_code=404, detail="Issue or repository not found")

    return ApiIssue(**issue)


@router.post("/repos/{owner}/{repository}/issues", response_model=ApiIssue)
async def create_new_issue(
    owner: str,
    repository: str,
    issue_data: CreateAnIssue,
    user: dict = Depends(verify_token),
):
    """Create an issue"""
    new_issue = create_issue(
        owner, repository, issue_data.model_dump(), user["username"]
    )
    if new_issue is None:
        raise HTTPException(status_code=404, detail="Repository not found")

    return ApiIssue(**new_issue)


@router.patch(
    "/repos/{owner}/{repository}/issues/{issue_number}", response_model=ApiIssue
)
async def update_issue_info(
    owner: str,
    repository: str,
    issue_number: int,
    update_data: CreateAnIssue,
    user: dict = Depends(verify_token),
):
    """Update an issue"""
    updated_issue = update_issue(
        owner, repository, issue_number, update_data.model_dump()
    )
    if updated_issue is None:
        raise HTTPException(status_code=404, detail="Issue or repository not found")

    return ApiIssue(**updated_issue)


@router.get(
    "/repos/{owner}/{repository}/issues/{issue_number}/comments",
    response_model=List[ApiComment],
)
async def get_issue_comment_list(owner: str, repository: str, issue_number: int):
    """Get list of comments for an issue"""
    comments = get_issue_comments(owner, repository, issue_number)
    if comments is None:
        return []
    return [ApiComment(**comment) for comment in comments]


@router.get(
    "/repos/{owner}/{repository}/issues/comments/{comment_id}",
    response_model=ApiComment,
)
async def get_issue_comment(owner: str, repository: str, comment_id: int):
    """Get a specific comment"""
    comment = get_comment(comment_id)
    if comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")

    return ApiComment(**comment)


@router.post(
    "/repos/{owner}/{repository}/issues/{issue_number}/comments",
    response_model=ApiComment,
)
async def create_issue_comment(
    owner: str,
    repository: str,
    issue_number: int,
    comment_data: CreateAComment,
    user: dict = Depends(verify_token),
):
    """Create a comment"""
    new_comment = create_comment(
        owner, repository, issue_number, comment_data.model_dump(), user["username"]
    )
    if new_comment is None:
        raise HTTPException(status_code=404, detail="Issue or repository not found")

    return ApiComment(**new_comment)


@router.patch(
    "/repos/{owner}/{repository}/issues/comments/{comment_id}",
    response_model=ApiComment,
)
async def update_issue_comment(
    owner: str,
    repository: str,
    comment_id: int,
    comment_data: CreateAComment,
    user: dict = Depends(verify_token),
):
    """Update a comment"""
    # Permission check (omitted in mock implementation)

    updated_comment = update_comment(comment_id, comment_data.model_dump())
    if updated_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")

    return ApiComment(**updated_comment)


@router.delete(
    "/repos/{owner}/{repository}/issues/comments/{comment_id}", status_code=200
)
async def delete_issue_comment(
    owner: str, repository: str, comment_id: int, user: dict = Depends(verify_token)
):
    """Delete a comment"""
    # Permission check (omitted in mock implementation)

    success = delete_comment(comment_id)
    if not success:
        raise HTTPException(status_code=404, detail="Comment not found")

    return {"message": "Comment deleted successfully"}
