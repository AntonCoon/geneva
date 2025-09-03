from contextlib import asynccontextmanager
from pathlib import Path
from typing import Optional

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from .model import (
    create_tables,
    create_user,
    get_user_by_name,
    get_user_queries,
    save_user_query,
)
from .services.openrouter import OpenRouterService
from .services.opentarget import OpenTargetService
from .utils import error, success


class LoginRequest(BaseModel):
    username: str
    api_key: Optional[str] = None


class GeneDiseaseRequest(BaseModel):
    username: str
    gene: str
    disease: str


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield


app = FastAPI(lifespan=lifespan)


static_path = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=static_path), name="static")


@app.get("/")
async def root():
    return success("GenEvA is running!")


@app.get("/app")
def serve_frontend():
    index_file = static_path / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    return {"message": "Frontend not found"}


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

    target_service = OpenTargetService()
    try:
        service_response = target_service.fetch_association(
            request.gene, request.disease
        )
    except Exception as e:
        return error(f"OpenTargetService error: {str(e)}", status_code=500)

    llm_service = OpenRouterService(api_key=user.api_key)
    try:
        llm_response = llm_service.summarize_gene_disease(service_response)
    except Exception as e:
        llm_response = {
            "summary_text": f"LLM error: {str(e)}",
            "key_findings": [],
            "confidence": None,
        }

    saved = save_user_query(
        user_id=user.id,
        gene=request.gene,
        disease=request.disease,
        service_response=service_response,
        llm_response=llm_response,
    )

    return success(
        "Query executed successfully",
        {
            "id": saved.id,
            "gene": saved.gene,
            "disease": saved.disease,
            "service_response": service_response,
            "llm_response": llm_response,
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
                "service_response": q.service_response,
                "llm_response": q.llm_response,
                "created_at": q.created_at.isoformat(),
            }
            for q in queries
        ],
    )
