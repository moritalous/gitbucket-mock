from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response, status

from auth import verify_token
from data import create_ref, delete_ref, get_all_refs, get_ref, update_ref
from models.git_refs import ApiRef, CreateARef, UpdateARef

router = APIRouter(tags=["GitReferences"])


@router.get("/repos/{owner}/{repository}/git/refs", response_model=List[ApiRef])
async def get_references(owner: str, repository: str):
    """Get all references for a repository"""
    refs = get_all_refs(owner, repository)
    if refs is None:
        raise HTTPException(status_code=404, detail="Repository not found")

    return [ApiRef(**ref) for ref in refs]


@router.get("/repos/{owner}/{repository}/git/refs/{ref:path}", response_model=ApiRef)
async def get_reference(owner: str, repository: str, ref: str):
    """Get a specific reference"""
    reference = get_ref(owner, repository, ref)
    if reference is None:
        raise HTTPException(status_code=404, detail="Reference or repository not found")

    return ApiRef(**reference)


@router.post("/repos/{owner}/{repository}/git/refs", response_model=ApiRef)
async def create_reference(
    owner: str,
    repository: str,
    ref_data: CreateARef,
    user: dict = Depends(verify_token),
):
    """Create a new reference"""
    new_ref = create_ref(owner, repository, ref_data.model_dump())
    if new_ref is None:
        raise HTTPException(
            status_code=422,
            detail="Reference already exists, repository not found, or invalid SHA",
        )

    return ApiRef(**new_ref)


@router.patch("/repos/{owner}/{repository}/git/refs/{ref:path}", response_model=ApiRef)
async def update_reference(
    owner: str,
    repository: str,
    ref: str,
    update_data: UpdateARef,
    user: dict = Depends(verify_token),
):
    """Update a reference"""
    updated_ref = update_ref(owner, repository, ref, update_data.model_dump())
    if updated_ref is None:
        raise HTTPException(
            status_code=422,
            detail="Reference doesn't exist, repository not found, or invalid SHA",
        )

    return ApiRef(**updated_ref)


@router.delete("/repos/{owner}/{repository}/git/refs/{ref:path}", status_code=204)
async def delete_reference(
    owner: str, repository: str, ref: str, user: dict = Depends(verify_token)
):
    """Delete a reference"""
    success = delete_ref(owner, repository, ref)
    if not success:
        raise HTTPException(
            status_code=422, detail="Reference doesn't exist or repository not found"
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)
