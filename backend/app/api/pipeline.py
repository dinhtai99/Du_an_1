from fastapi import APIRouter, HTTPException, Request, status

from app.schemas.pipeline import (
    FlowSessionStatus,
    PipelineJobResponse,
    PipelineStartRequest,
)
from app.workers.pipeline import PipelineWorker

router = APIRouter()


def worker_from(request: Request) -> PipelineWorker:
    return request.app.state.pipeline_worker


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@router.post("/flow/open", response_model=FlowSessionStatus)
async def open_flow(request: Request) -> FlowSessionStatus:
    try:
        return await worker_from(request).flow.open_session()
    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail=f"Không mở được trình duyệt Flow: {exc}",
        ) from exc


@router.get("/flow/status", response_model=FlowSessionStatus)
async def flow_status(request: Request) -> FlowSessionStatus:
    return await worker_from(request).flow.status()


@router.post(
    "/pipeline/jobs",
    response_model=PipelineJobResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
async def start_job(
    payload: PipelineStartRequest,
    request: Request,
) -> PipelineJobResponse:
    return await worker_from(request).start(payload)


@router.get("/pipeline/jobs", response_model=list[PipelineJobResponse])
async def list_jobs(request: Request) -> list[PipelineJobResponse]:
    return worker_from(request).list_recent()


@router.get("/pipeline/jobs/{job_id}", response_model=PipelineJobResponse)
async def get_job(job_id: str, request: Request) -> PipelineJobResponse:
    try:
        return worker_from(request).get(job_id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Không tìm thấy tác vụ.") from exc


@router.post("/pipeline/jobs/{job_id}/resume", response_model=PipelineJobResponse)
async def resume_job(job_id: str, request: Request) -> PipelineJobResponse:
    try:
        return await worker_from(request).resume(job_id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Không tìm thấy tác vụ.") from exc
