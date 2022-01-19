from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi_sqlalchemy import DBSessionMiddleware, db
from fastapi_jwt_auth import AuthJWT
from entities.schemas import RegisterModel, LoginModel
from dotenv import load_dotenv

from entities.models import User
from werkzeug.security import generate_password_hash, check_password_hash

from settings import Settings

auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@AuthJWT.load_config
def get_config():
    return Settings()


@auth_router.post("/register")
async def register(model: RegisterModel):
    try:
        user = db.session.query(User).filter(User.email == model.email).first()
        if user is not None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user with that email exists")

        # Register User
        new_user = User(email=model.email, full_name=model.full_name, password=generate_password_hash(model.password))
        db.session.add(new_user)
        db.session.commit()
        return jsonable_encoder(new_user)

    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="something went wrong")


@auth_router.post("/login")
async def login(model: LoginModel, authorize: AuthJWT = Depends()):
    user = db.session.query(User).filter(User.email == model.email).first()

    if user and check_password_hash(user.password, model.password):
        access_token = authorize.create_access_token(subject=str(user.id))
        refresh_token = authorize.create_refresh_token(subject=str(user.id))

        return jsonable_encoder({
            "access_token": access_token,
            "refresh_token": refresh_token
        })

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="authentication failed")


@auth_router.get('/users')
async def users():
    sys_users = db.session.query(User).all()
    return jsonable_encoder(sys_users)
