from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel

class JobEventResponse(BaseModel):
    id: str
    job_id: str
    event_type: str
    message: str
    details_json: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class JobResponse(BaseModel):
    id: str
    project_id: str
    job_type: str
    status: str
    progress_percent: float
    current_step: str
    current_scene_order: int
    total_scenes: int
    credit_budget: int
    credits_used: int
    error_message: Optional[str] = None
    requires_user_action: bool = False
    user_action_prompt: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    events: List[JobEventResponse] = []

    class Config:
        from_attributes = True

class JobActionRequest(BaseModel):
    action: str # "pause", "resume", "retry", "cancel"
