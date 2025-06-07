from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response, status

from auth import verify_token
from data import (
    add_labels_to_issue,
    create_label,
    delete_label,
    get_issue_labels,
    get_label,
    get_repository_labels,
    remove_all_labels,
    remove_label_from_issue,
    replace_all_labels,
    update_label,
)
from models.issues import ApiLabel
from models.labels import AddLabelsToAnIssue, CreateALabel

router = APIRouter(tags=["Labels"])


@router.get("/repos/{owner}/{repository}/labels", response_model=List[ApiLabel])
async def get_labels(owner: str, repository: str):
    """Get list of labels for a repository"""
    labels = get_repository_labels(owner, repository)
    if labels is None:
        raise HTTPException(status_code=404, detail="Repository not found")

    return [ApiLabel(**label) for label in labels]


@router.get("/repos/{owner}/{repository}/labels/{label_name}", response_model=ApiLabel)
async def get_label_info(owner: str, repository: str, label_name: str):
    """Get a specific label"""
    label = get_label(owner, repository, label_name)
    if label is None:
        raise HTTPException(status_code=404, detail="Label or repository not found")

    return ApiLabel(**label)


@router.post(
    "/repos/{owner}/{repository}/labels", response_model=ApiLabel, status_code=201
)
async def create_new_label(
    owner: str,
    repository: str,
    label_data: CreateALabel,
    user: dict = Depends(verify_token),
):
    """Create a label"""
    # Label validation
    if not label_data.is_valid():
        raise HTTPException(status_code=422, detail="Invalid label data")

    new_label = create_label(owner, repository, label_data.model_dump())
    if new_label is None:
        raise HTTPException(
            status_code=422, detail="Label already exists or repository not found"
        )

    return ApiLabel(**new_label)


@router.patch(
    "/repos/{owner}/{repository}/labels/{label_name}", response_model=ApiLabel
)
async def update_label_info(
    owner: str,
    repository: str,
    label_name: str,
    label_data: CreateALabel,
    user: dict = Depends(verify_token),
):
    """Update a label"""
    # Label validation
    if not label_data.is_valid():
        raise HTTPException(status_code=422, detail="Invalid label data")

    updated_label = update_label(owner, repository, label_name, label_data.model_dump())
    if updated_label is None:
        raise HTTPException(status_code=404, detail="Label or repository not found")

    return ApiLabel(**updated_label)


@router.delete("/repos/{owner}/{repository}/labels/{label_name}", status_code=204)
async def delete_label_info(
    owner: str, repository: str, label_name: str, user: dict = Depends(verify_token)
):
    """Delete a label"""
    success = delete_label(owner, repository, label_name)
    if not success:
        raise HTTPException(status_code=404, detail="Label or repository not found")

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    "/repos/{owner}/{repository}/issues/{issue_number}/labels",
    response_model=List[ApiLabel],
)
async def get_issue_label_list(owner: str, repository: str, issue_number: int):
    """Get list of labels for an issue"""
    labels = get_issue_labels(owner, repository, issue_number)
    if labels is None:
        raise HTTPException(status_code=404, detail="Repository not found")

    return [ApiLabel(**label) for label in labels]


@router.post(
    "/repos/{owner}/{repository}/issues/{issue_number}/labels",
    response_model=List[ApiLabel],
)
async def add_labels_to_issue_endpoint(
    owner: str,
    repository: str,
    issue_number: int,
    label_data: AddLabelsToAnIssue,
    user: dict = Depends(verify_token),
):
    """Add labels to an issue"""
    labels = add_labels_to_issue(owner, repository, issue_number, label_data.labels)
    if labels is None:
        raise HTTPException(status_code=404, detail="Issue or repository not found")

    return [ApiLabel(**label) for label in labels]


@router.delete(
    "/repos/{owner}/{repository}/issues/{issue_number}/labels/{label_name}",
    response_model=List[ApiLabel],
)
async def remove_label_from_issue_endpoint(
    owner: str,
    repository: str,
    issue_number: int,
    label_name: str,
    user: dict = Depends(verify_token),
):
    """Remove a label from an issue"""
    labels = remove_label_from_issue(owner, repository, issue_number, label_name)
    if labels is None:
        raise HTTPException(
            status_code=404, detail="Label, issue, or repository not found"
        )

    return [ApiLabel(**label) for label in labels]


@router.put(
    "/repos/{owner}/{repository}/issues/{issue_number}/labels",
    response_model=List[ApiLabel],
)
async def replace_all_labels_endpoint(
    owner: str,
    repository: str,
    issue_number: int,
    label_data: AddLabelsToAnIssue,
    user: dict = Depends(verify_token),
):
    """Replace all labels for an issue"""
    labels = replace_all_labels(owner, repository, issue_number, label_data.labels)
    if labels is None:
        raise HTTPException(status_code=404, detail="Issue or repository not found")

    return [ApiLabel(**label) for label in labels]


@router.delete(
    "/repos/{owner}/{repository}/issues/{issue_number}/labels", status_code=204
)
async def remove_all_labels_endpoint(
    owner: str, repository: str, issue_number: int, user: dict = Depends(verify_token)
):
    """Remove all labels from an issue"""
    success = remove_all_labels(owner, repository, issue_number)
    if not success:
        raise HTTPException(status_code=404, detail="Issue or repository not found")

    return Response(status_code=status.HTTP_204_NO_CONTENT)
