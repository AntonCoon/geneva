from contextlib import asynccontextmanager

from fastapi import FastAPI
from pydantic import BaseModel

from .model import create_tables
from .model import create_user as save_user
from .model import get_user_by_name as get_user
from .utils import error, success


class LoginRequest(BaseModel):
    username: str
    api_key: str | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return success("GenEvA is running!")


@app.post("/login")
def login(request: LoginRequest):
    user = get_user(request.username)

    if request.api_key:
        if user:
            return error("Username already taken", status_code=409)
        save_user(request.username, request.api_key)
        return success(
            "User registered and logged in", {"username": request.username}
        )

    if not user:
        return error("User not found, registration required", status_code=404)
    return success("User logged in successfully", {"username": user.username})


@app.get("/user/{username}")
def get_user_info(username: str):
    user = get_user(username)
    if not user:
        return error("User not found", status_code=404)
    return success(
        "User info retrieved",
        {"username": user.username, "has_api_key": bool(user.api_key)},
    )
