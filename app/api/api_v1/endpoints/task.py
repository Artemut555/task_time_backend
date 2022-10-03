import asyncio
from typing import Any, Optional

import httpx
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import crud
from app.api import deps
from app.clients.reddit import RedditClient
from app.schemas.task import (
    Task,
    TaskCreate,
    TaskSearchResults,
    TaskUpdateRestricted,
)
from app.models.user import User

router = APIRouter()
RECIPE_SUBREDDITS = ["tasks", "easytasks", "TopSecretTasks"]


@router.get("/{task_id}", status_code=200, response_model=Task)
def fetch_task(
    *,
    task_id: int,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Fetch a single task by ID
    """
    result = crud.task.get(db=db, id=task_id)
    if not result:
        # the exception is raised, not returned - you will get a validation
        # error otherwise.
        raise HTTPException(
            status_code=404, detail=f"Task with ID {task_id} not found"
        )

    return result


@router.get("/my-tasks/", status_code=200, response_model=TaskSearchResults)
def fetch_user_tasks(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Fetch all tasks for a user
    """
    tasks = current_user.tasks
    print(tasks)
    if not tasks:
        return {"results": list()}

    return {"results": list(tasks)}


@router.get("/search/", status_code=200, response_model=TaskSearchResults)
def search_tasks(
    *,
    keyword: str = Query(None, min_length=3, example="chicken"),
    max_results: Optional[int] = 10,
    db: Session = Depends(deps.get_db),
) -> dict:
    """
    Search for tasks based on label keyword
    """
    tasks = crud.task.get_multi(db=db, limit=max_results)
    results = filter(lambda task: keyword.lower() in task.label.lower(), tasks)

    return {"results": list(results)}


@router.post("/", status_code=201, response_model=Task)
def create_task(
    *,
    task_in: TaskCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> dict:
    """
    Create a new task in the database.
    """
    print("In")
    if task_in.submitter_id != current_user.id:
        raise HTTPException(
            status_code=403, detail=f"You can only submit tasks as yourself"
        )
    task = crud.task.create(db=db, obj_in=task_in)

    return task


@router.put("/", status_code=201, response_model=Task)
def update_task(
    *,
    task_in: TaskUpdateRestricted,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> dict:
    """
    Update task in the database.
    """
    task = crud.task.get(db, id=task_in.id)
    if not task:
        raise HTTPException(
            status_code=400, detail=f"Task with ID: {task_in.id} not found."
        )

    if task.submitter_id != current_user.id:
        raise HTTPException(
            status_code=403, detail=f"You can only update your tasks."
        )

    updated_task = crud.task.update(db=db, db_obj=task, obj_in=task_in)
    return updated_task
