from typing import List, Optional, Union

from fastapi import APIRouter, Depends, HTTPException, Path, Query, Response

from auth import verify_token
from data import (
    create_or_update_file,
    get_contents,
    get_raw_content,
    get_repository_readme,
)
from models.contents import ApiCommit, ApiContents, CreateAFile

router = APIRouter(tags=["Contents"])


@router.get("/repos/{owner}/{repository}/readme", response_model=ApiContents)
async def get_readme(owner: str, repository: str, ref: Optional[str] = None):
    """Get repository README"""
    readme = get_repository_readme(owner, repository, ref)
    if readme is None:
        raise HTTPException(status_code=404, detail="Repository or README not found")

    return ApiContents(**readme)


@router.get(
    "/repos/{owner}/{repository}/contents/{path:path}",
    response_model=Union[ApiContents, List[ApiContents]],
)
async def get_repository_contents(
    owner: str,
    repository: str,
    path: str = Path(...),
    ref: Optional[str] = None,
    large_file: bool = Query(False),
):
    """Get repository contents"""
    contents = get_contents(owner, repository, path, ref)
    if contents is None:
        raise HTTPException(
            status_code=404, detail="File, directory, or repository not found"
        )

    if isinstance(contents, list):
        return [ApiContents(**item) for item in contents]
    else:
        return ApiContents(**contents)


@router.put("/repos/{owner}/{repository}/contents/{path:path}", response_model=dict)
async def create_update_file(
    owner: str,
    repository: str,
    path: str,
    file_data: CreateAFile,
    user: dict = Depends(verify_token),
):
    """Create or update a file"""
    result = create_or_update_file(owner, repository, path, file_data.model_dump())
    if result is None:
        raise HTTPException(
            status_code=404, detail="Repository not found or SHA mismatch"
        )

    # Format response structure
    response = {
        "content": ApiContents(**result["content"]),
        "commit": ApiCommit(**result["commit"]),
    }

    return response


@router.get("/repos/{owner}/{repository}/raw/{path:path}")
async def get_raw_file_content(owner: str, repository: str, path: str):
    """Get raw file contents

    The path parameter should be in the format: {ref}/{file_path}
    where ref is the branch/commit/tag and file_path is the path to the file.
    Example: /api/v3/repos/owner/repo/raw/main/src/file.txt
    """
    content = get_raw_content(owner, repository, path)
    if content is None:
        raise HTTPException(status_code=404, detail="File not found")

    return Response(content=content, media_type="text/plain")
