from typing import Union

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.task import Task
from app.models.user import User
from app.schemas.task import TaskCreate, TaskUpdateRestricted, TaskUpdate


class CRUDTask(CRUDBase[Task, TaskCreate, TaskUpdate]):
    def update(
        self,
        db: Session,
        *,
        db_obj: User,
        obj_in: Union[TaskUpdate, TaskUpdateRestricted]
    ) -> Task:
        db_obj = super().update(db, db_obj=db_obj, obj_in=obj_in)
        return db_obj


task = CRUDTask(Task)
