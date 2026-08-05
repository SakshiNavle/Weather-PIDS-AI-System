from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)
from app.core.jwt import create_access_token
from app.security.password import verify_password, hash_password
from app.models.user import User
from fastapi.security import OAuth2PasswordRequestForm
from app.security.password import verify_password
from sqlalchemy.orm import Session


from app.core.database import get_db

from app.models.user import User   # <-- ADD THIS

from app.schemas.user_schema import (
    UserRegister,
    Token,
    UserResponse
)

from app.services.auth_service import AuthService
from app.security.password import verify_password

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    user: UserRegister,
    db: Session = Depends(get_db),
):
    """
    Register a new user.
    """
    service = AuthService(db)

    return service.register(user)


@router.post(
    "/login",
    response_model=Token
)
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.username == form_data.username
    ).first()


    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )


    if not verify_password(
        form_data.password,
        user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )


    access_token = create_access_token(
        data={
            "sub": user.username,
            "user_id": user.id,
            "role": user.role
        }
    )


    return {
        "access_token": access_token,
        "token_type": "bearer"
    }