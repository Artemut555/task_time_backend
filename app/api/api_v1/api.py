from fastapi import APIRouter

from app.api.api_v1.endpoints import task, auth


api_router = APIRouter()
api_router.include_router(task.router, prefix="/tasks", tags=["tasks"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
