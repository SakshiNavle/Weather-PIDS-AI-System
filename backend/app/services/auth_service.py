from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.security.jwt_handler import create_access_token
from app.security.password import hash_password, verify_password
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserLogin, UserRegister
from app.core.jwt import create_access_token

class AuthService:
    """
    Service layer responsible for authentication and
    user management business logic.
    """

    def __init__(self, db: Session):
        self.db = db
        self.user_repository = UserRepository(db)

    def register(self, user_data: UserRegister) -> User:
        """
        Register a new user.
        """

        # Check username
        if self.user_repository.find_by_username(user_data.username):
            raise ValueError("Username already exists")

        # Check email
        if self.user_repository.find_by_email(user_data.email):
            raise ValueError("Email already exists")

        new_user = User(
            username=user_data.username,
            email=user_data.email,
            password_hash=hash_password(user_data.password),
        )

        try:
            self.user_repository.save(new_user)

            self.db.commit()
            self.db.refresh(new_user)

            return new_user

        except IntegrityError:
            self.db.rollback()
            raise ValueError("User already exists")

        except Exception:
            self.db.rollback()
            raise

    def login(self, credentials: UserLogin) -> dict:
        """
        Authenticate user and return JWT token.
        """

        user = self.user_repository.find_by_username(
            credentials.username
        )

        if not user:
            raise ValueError("Invalid username or password")

        if not verify_password(
            credentials.password,
            user.password_hash,
        ):
            raise ValueError("Invalid username or password")

        access_token = create_access_token(
            data={
                "sub": user.username,
                "user_id": user.id,
                "role": user.role,
            }
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
        }