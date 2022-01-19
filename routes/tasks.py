from fastapi import APIRouter, Depends, HTTPException, status

task_router = APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)


@task_router.get("/task/all")
async def get_tasks():
    return {"tasks": [
        {"title": "task1"},
        {"title": "task2"},
    ]}

@task_router.post("/task")
async def post_task():
    pass


@task_router.get("task/{task_id}")
async def get_task(task_id:str):
    pass