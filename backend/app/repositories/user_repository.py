from typing import Optional

from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:
    """
    Repository responsible only for database operations
    related to the User model.

    NOTE:
    - No business logic
    - No HTTPExceptions
    - No password hashing
    - No JWT
    - No commit/rollback
    """

    def __init__(self, db: Session):
        self.db = db

    def find_by_id(self, user_id: int) -> Optional[User]:
        return (
            self.db.query(User)
            .filter(User.id == user_id)
            .first()
        )

    def find_by_username(self, username: str) -> Optional[User]:
        return (
            self.db.query(User)
            .filter(User.username == username)
            .first()
        )

    def find_by_email(self, email: str) -> Optional[User]:
        return (
            self.db.query(User)
            .filter(User.email == email)
            .first()
        )

    def save(self, user: User) -> User:
        """
        Stage a new user for persistence.
        Commit is handled by the service layer.
        """
        self.db.add(user)
        return user

    def remove(self, user: User) -> None:
        """
        Stage a user for deletion.
        Commit is handled by the service layer.
        """
        self.db.delete(user)