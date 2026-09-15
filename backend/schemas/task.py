"""
Task & Video Rendering Schemas
"""

from typing import List, Optional, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field

class TaskStatusEnum(str, Enum):
    QUEUED = "QUEUED"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class SceneRenderInput(BaseModel):
    scene_id: int
    narration: str
    image_prompt: Optional[str] = None
    image_url: Optional[str] = None

class VideoRenderRequest(BaseModel):
    project_id: Optional[str] = None
    title: Optional[str] = Field(default=None, description="Tiêu đề của video/kịch bản")
    scenes: List[SceneRenderInput] = Field(..., description="Danh sách các phân cảnh kịch bản")
    voice_id: str = Field(default="vi-VN-HoaiMyNeural", description="Giọng đọc")
    voice_rate: float = Field(default=1.0, ge=0.25, le=2.0, description="Tốc độ giọng đọc (0.25x - 2.0x)")
    aspect_ratio: str = Field(default="9:16")
    enable_hand_drawing: bool = Field(default=True)
    enable_subtitles: bool = Field(default=True)

class VideoRenderResult(BaseModel):
    video_url: str
    duration_seconds: float
    file_size_bytes: int

class TaskStatusResponse(BaseModel):
    task_id: str
    status: TaskStatusEnum
    progress_percentage: int
    current_step: str
    error_message: Optional[str] = None
    result: Optional[VideoRenderResult] = None
