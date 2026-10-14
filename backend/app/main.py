from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.pipeline import router as pipeline_router
from app.core.config import settings
from app.database.session import Base, engine
from app.models import entities  # noqa: F401 - register SQLAlchemy tables
from app.workers.pipeline import PipelineWorker


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    app.state.pipeline_worker = PipelineWorker()
    yield
    await app.state.pipeline_worker.close()


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.CORS_ORIGINS.split(",")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(pipeline_router, prefix=settings.API_V1_STR)
app.mount("/media", StaticFiles(directory=settings.EXPORTS_DIR), name="media")


@app.get("/")
async def root() -> dict[str, str]:
    return {
        "name": settings.PROJECT_NAME,
        "docs": "/docs",
        "health": f"{settings.API_V1_STR}/health",
    }
