"""
Story Schemas
"""

from typing import List, Optional
from pydantic import BaseModel, Field

class StoryGenerateRequest(BaseModel):
    topic: str = Field(..., description="Chủ đề hoặc ý tưởng của video", min_length=3)
    scenes_count: int = Field(default=2, ge=1, le=10, description="Số lượng phân cảnh")
    language: str = Field(default="vi", description="Ngôn ngữ thuyết minh ('vi' hoặc 'en')")
    tone: Optional[str] = Field(default="motivational", description="Giọng điệu (hài hước, triết lý, cảm động...)")
    api_key: Optional[str] = Field(default=None, description="Google Gemini API Key của người dùng")

class SceneItemSchema(BaseModel):
    scene_id: int
    narration: str
    image_prompt: str
    keywords: List[str] = []
    image_url: Optional[str] = None
    audio_url: Optional[str] = None
    audio_duration: Optional[float] = None

class StoryGenerateResponse(BaseModel):
    project_id: str
    title: str
    topic: str
    scenes: List[SceneItemSchema]
