from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import datetime
from app.db.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 5000
    ) -> List[ModelType]:
        return (
            db.query(self.model).order_by(self.model.id).offset(skip).limit(limit).all()
        )

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        # print(type(obj_in_data['time']))
        # if 'time' in obj_in_data:
        obj_in_data['start_time'] = datetime.now()
        obj_in_data['finish_time'] = datetime.now()
        obj_in_data['task_finished'] = 0
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        # db.delete(db_obj)
        obj_data = jsonable_encoder(db_obj)

        # print(obj_data)
        # print(obj_in)
        if obj_in.type == 0:
            obj_data['start_time'] = datetime.now()
            obj_data['finish_time'] = datetime.now()
            obj_data['task_finished'] = 0
            to_update = ['start_time', 'finish_time', 'task_finished']
        else:
            obj_data['finish_time'] = datetime.now()
            obj_data['task_finished'] = 1
            to_update = ['finish_time', 'task_finished']

        # print(obj_data)
        for field in to_update:
            setattr(db_obj, field, obj_data[field])

        # print(db_obj.task_finished)
        db.add(db_obj)
        db.commit()
        # print(db_obj.task_finished)
        db.refresh(db_obj)
        # print(db_obj.task_finished)
        return db_obj

    def remove(self, db: Session, *, id: int) -> ModelType:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj
