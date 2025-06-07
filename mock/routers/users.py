from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException

from auth import verify_admin, verify_token
from data import USERS, create_user, get_user_by_username, update_user
from models.users import ApiUser, CreateAUser, UpdateAUser

router = APIRouter(tags=["Users"])


@router.get("/users", response_model=list[ApiUser])
async def get_users():
    """Get list of all users"""
    return [ApiUser(**user) for user in USERS.values()]


@router.get("/users/{username}", response_model=ApiUser)
async def get_user(username: str):
    """Get specific user information"""
    user = get_user_by_username(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return ApiUser(**user)


@router.get("/user", response_model=ApiUser)
async def get_authenticated_user(user: dict = Depends(verify_token)):
    """Get authenticated user information"""
    return ApiUser(**USERS[user["username"]])


@router.patch("/user", response_model=ApiUser)
async def update_authenticated_user(
    user_data: UpdateAUser, user: dict = Depends(verify_token)
):
    """Update authenticated user information"""
    # Process updatable fields
    update_fields = user_data.model_dump(exclude_unset=True)
    updated_user = update_user(user["username"], update_fields)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return ApiUser(**updated_user)


@router.post("/admin/users", response_model=ApiUser)
async def create_new_user(user_data: CreateAUser, admin: dict = Depends(verify_admin)):
    """Create a new user (admin only)"""
    if user_data.login in USERS:
        raise HTTPException(status_code=400, detail="User already exists")

    # Create new user
    new_user = {
        "login": user_data.login,
        "id": len(USERS) + 1,
        "email": user_data.email,
        "type": "User",
        "site_admin": user_data.isAdmin or False,
        "created_at": datetime.now(),
        "url": f"/api/v3/users/{user_data.login}",
        "html_url": f"/{user_data.login}",
        "avatar_url": f"/{user_data.login}/avatar",
    }

    created_user = create_user(new_user)
    if created_user is None:
        raise HTTPException(status_code=400, detail="User already exists")
    return ApiUser(**created_user)


@router.put("/users/{username}/suspended", status_code=204)
async def suspend_user(username: str, admin: dict = Depends(verify_admin)):
    """Suspend user account (admin only)"""
    if username not in USERS:
        raise HTTPException(status_code=404, detail="User not found")

    # In actual application, change user status
    # Do nothing in mock implementation
    return None


@router.delete("/users/{username}/suspended", status_code=204)
async def unsuspend_user(username: str, admin: dict = Depends(verify_admin)):
    """Unsuspend user account (admin only)"""
    if username not in USERS:
        raise HTTPException(status_code=404, detail="User not found")

    # In actual application, change user status
    # Do nothing in mock implementation
    return None
