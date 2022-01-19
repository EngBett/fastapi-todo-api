from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_jwt_auth import AuthJWT
from fastapi_sqlalchemy import db

from entities.models import Task

task_router = APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)


@task_router.get("/task/all")
async def get_tasks(authorize: AuthJWT = Depends()):


    try:
        tasks = db.session.query(Task).filter(Task.user_id == authorize.get_jwt_subject()).all()
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong")


@task_router.post("/task")
async def post_task():
    try:
        pass
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong")


@task_router.get("task/{task_id}")
async def get_task(task_id: str):
    try:
        pass
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong")
