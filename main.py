import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi_sqlalchemy import DBSessionMiddleware

from routes.auth import auth_router
from routes.tasks import task_router

load_dotenv(".env")
app = FastAPI()

app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])

app.include_router(auth_router)
app.include_router(task_router)


@app.get("/")
async def home():
    return {"Message": "works well"}
