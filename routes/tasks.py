from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth import AuthJWT
from fastapi_sqlalchemy import db

from entities.models import Task
from entities.schemas import TaskModel
from helpers.auth import require_jwt

task_router = APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)


@task_router.get("/task/all")
async def get_tasks(authorize: AuthJWT = Depends()):
    require_jwt(authorize)
    try:
        tasks = db.session.query(Task).filter(Task.user_id == authorize.get_jwt_subject()).all()
        return jsonable_encoder(tasks)
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong")


@task_router.post("/task/create", response_model=TaskModel)
async def post_task(model: TaskModel, authorize: AuthJWT = Depends()):
    require_jwt(authorize)
    try:
        task = Task(id=uuid4(), title=model.title, description=model.description, user_id=authorize.get_jwt_subject())
        db.session.add(task)
        db.session.commit()
        return task
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong")


@task_router.get("/task/get/{task_id}", response_model=TaskModel)
async def get_task(task_id: UUID, authorize: AuthJWT = Depends()):
    require_jwt(authorize)
    try:
        task = db.session.query(Task).filter(Task.id == task_id).first()
        if task is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="task not found")
        return task
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong")


@task_router.put("/task/update/{task_id}", response_model=TaskModel)
async def update_task(model: TaskModel, task_id: UUID, authorize: AuthJWT = Depends()):
    require_jwt(authorize)
    try:
        task = db.session.query(Task).filter(Task.id == task_id).first()
        if task is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="task not found")

        task.title = model.title
        task.description = model.description
        task.complete = model.complete
        db.session.commit()
        return task

    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong")


@task_router.put("/task/complete/{task_id}", response_model=TaskModel)
async def complete_task(task_id: UUID, authorize: AuthJWT = Depends()):
    require_jwt(authorize)
    try:
        task = db.session.query(Task).filter(Task.id == task_id).first()
        if task is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="task not found")

        task.complete = True
        db.session.commit()
        return task

    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong")


@task_router.delete("/task/delete/{task_id}")
async def delete_task(task_id: UUID, authorize: AuthJWT = Depends()):
    require_jwt(authorize)
    try:
        task = db.session.query(Task).filter(Task.id == task_id).first()
        if task is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="task not found")
        db.session.delete(task)
        db.session.commit()
        return {"message", "successfully deleted"}

    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong")
