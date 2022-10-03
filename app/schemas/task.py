from pydantic import BaseModel, HttpUrl
from datetime import datetime, date
from typing import Sequence


class TaskBase(BaseModel):
    label: str
    source: str
    url: HttpUrl
    start_time: datetime
    finish_time: datetime
    task_finished: int


class TaskCreate(BaseModel):
    label: str
    source: str
    url: HttpUrl
    submitter_id: int


class TaskUpdate(TaskBase):
    id: int


class TaskUpdateRestricted(BaseModel):
    id: int
    type: int


# Properties shared by models stored in DB
class TaskInDBBase(TaskBase):
    id: int
    submitter_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Task(TaskInDBBase):
    pass


# Properties properties stored in DB
class TaskInDB(TaskInDBBase):
    pass


class TaskSearchResults(BaseModel):
    results: Sequence[Task]
