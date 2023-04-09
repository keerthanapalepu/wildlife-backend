from fastapi import APIRouter, Body, Depends, HTTPException, Response, status
from fastapi_jwt_auth import AuthJWT
from pydantic import EmailStr

from myserver.models.user import User, UserAuth, UserOut
from myserver.util.current_user import current_user

router = APIRouter(prefix="/register", tags=["Register"])


@router.post("", response_model=UserOut)
async def user_registration(
    user_auth: UserAuth,
    user: User = Depends(current_user)
):
    """Creates a new user"""
    # Check if user making the request is an admin
    is_admin = user.is_admin
    if not is_admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Only admins can register new users")
    
    user = await User.by_email(user_auth.email)
    if user is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail = "User with that email already exists")
    # hashed = hash_password(user_auth.password)?
    user = User(email=user_auth.email, password=user_auth.password)
    await user.create()
    return user

@router.post("/admin", response_model=UserOut)
async def user_registration(
    user_auth: UserAuth
):    
    user = User(email=user_auth.email, password=user_auth.password, is_admin=True)
    await user.create()
    return user