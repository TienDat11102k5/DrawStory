"""
Audio Schemas
"""

from typing import Optional
from pydantic import BaseModel, Field

class VoiceInfo(BaseModel):
    voice_id: str
    name: str
    gender: str
    language: str

class AudioPreviewRequest(BaseModel):
    text: str = Field(..., description="Đoạn văn bản cần nghe thử")
    voice_id: str = Field(default="vi-VN-HoaiMyNeural", description="ID của giọng đọc")

class AudioPreviewResponse(BaseModel):
    audio_url: str
    duration_seconds: float
