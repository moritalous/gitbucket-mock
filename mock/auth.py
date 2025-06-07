from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

# Use HTTPBearer to get token from Authorization header
security = HTTPBearer()


# Token verification function
async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    # Check fixed tokens
    if token == "admin-token":
        return {"username": "admin", "is_admin": True}
    elif token == "user1-token":
        return {"username": "user1", "is_admin": False}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


# Admin permission check
async def verify_admin(credentials: HTTPAuthorizationCredentials = Depends(security)):
    user = await verify_token(credentials)
    if not user["is_admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    return user
