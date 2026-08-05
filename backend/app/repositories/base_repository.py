from typing import Generic, Optional, Type, TypeVar

from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType")


class BaseRepository(Generic[ModelType]):
    """
    Generic repository for CRUD operations.
    """

    def __init__(self, model: Type[ModelType], db: Session):
        self.model = model
        self.db = db

    def find_by_id(self, object_id: int) -> Optional[ModelType]:
        return (
            self.db.query(self.model)
            .filter(self.model.id == object_id)
            .first()
        )

    def get_all(self):
        return self.db.query(self.model).all()

    def save(self, obj: ModelType) -> ModelType:
        self.db.add(obj)
        return obj

    def remove(self, obj: ModelType):
        self.db.delete(obj)