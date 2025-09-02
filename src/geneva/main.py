from contextlib import asynccontextmanager

from fastapi import FastAPI
from pydantic import BaseModel

from .model import (
    create_tables,
    create_user,
    get_user_by_name,
    get_user_queries,
    save_user_query,
)
from .services.opentarget import OpenTargetService
from .utils import error, success


class LoginRequest(BaseModel):
    username: str
    api_key: str | None = None


class GeneDiseaseRequest(BaseModel):
    username: str
    gene: str
    disease: str


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
    user = get_user_by_name(request.username)

    if request.api_key:
        if user:
            return error("Username already taken", status_code=409)
        create_user(request.username, request.api_key)
        return success(
            "User registered and logged in", {"username": request.username}
        )

    if not user:
        return error("User not found, registration required", status_code=404)
    return success("User logged in successfully", {"username": user.username})


@app.get("/user/{username}")
def get_user_info(username: str):
    user = get_user_by_name(username)
    if not user:
        return error("User not found", status_code=404)
    return success(
        "User info retrieved",
        {"username": user.username, "has_api_key": bool(user.api_key)},
    )


@app.post("/query")
def run_gene_disease_query(request: GeneDiseaseRequest):
    user = get_user_by_name(request.username)
    if not user:
        return error("User not found", status_code=404)
    service = OpenTargetService()
    try:
        response = service.fetch_association(request.gene, request.disease)
    except Exception as e:
        return error(f"Service error: {str(e)}", status_code=500)
    saved = save_user_query(
        user_id=user.id,
        gene=request.gene,
        disease=request.disease,
        response=response,
    )
    return success(
        "Query executed successfully",
        {
            "id": saved.id,
            "gene": saved.gene,
            "disease": saved.disease,
            "response": response,
            "created_at": saved.created_at.isoformat(),
        },
    )


@app.get("/queries/{username}")
def list_user_queries(username: str):
    user = get_user_by_name(username)
    if not user:
        return error("User not found", status_code=404)
    queries = get_user_queries(user.id)
    return success(
        "User queries retrieved",
        [
            {
                "id": q.id,
                "gene": q.gene,
                "disease": q.disease,
                "response": q.service_response,
                "created_at": q.created_at.isoformat(),
            }
            for q in queries
        ],
    )
