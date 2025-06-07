from fastapi import APIRouter, Depends, HTTPException

from auth import verify_admin, verify_token
from data import (
    ORGANIZATIONS,
    create_organization,
    get_organization_by_name,
    get_organizations_for_user,
)
from models.organizations import ApiGroup, CreateAGroup

router = APIRouter(tags=["Organizations"])


@router.get("/organizations", response_model=list[ApiGroup])
async def get_organizations():
    """Get list of all organizations"""
    return [ApiGroup(**org) for org in ORGANIZATIONS.values()]


@router.get("/orgs/{org_name}", response_model=ApiGroup)
async def get_organization(org_name: str):
    """Get specific organization information"""
    org = get_organization_by_name(org_name)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return ApiGroup(**org)


@router.get("/users/{username}/orgs", response_model=list[ApiGroup])
async def get_user_organizations(username: str):
    """Get organizations that a specific user belongs to"""
    orgs = get_organizations_for_user(username)
    return [ApiGroup(**org) for org in orgs]


@router.get("/user/orgs", response_model=list[ApiGroup])
async def get_authenticated_user_organizations(user: dict = Depends(verify_token)):
    """Get organizations that the authenticated user belongs to"""
    orgs = get_organizations_for_user(user["username"])
    return [ApiGroup(**org) for org in orgs]


@router.post("/admin/organizations", response_model=ApiGroup)
async def create_new_organization(
    org_data: CreateAGroup, admin: dict = Depends(verify_admin)
):
    """Create a new organization (admin only)"""
    if org_data.login in ORGANIZATIONS:
        raise HTTPException(status_code=400, detail="Organization already exists")

    # Create new organization
    new_org = create_organization(org_data.model_dump())
    if new_org is None:
        raise HTTPException(status_code=400, detail="Failed to create organization")
    return ApiGroup(**new_org)
