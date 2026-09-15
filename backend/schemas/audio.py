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
    rate: float = Field(default=1.0, ge=0.25, le=2.0, description="Tốc độ giọng đọc (0.25x - 2.0x)")

class AudioPreviewResponse(BaseModel):
    audio_url: str
    duration_seconds: float
