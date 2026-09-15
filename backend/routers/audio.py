"""
Audio API Router
"""

import os
import uuid
from typing import List
from fastapi import APIRouter, HTTPException

from backend.config import settings
from backend.schemas.audio import VoiceInfo, AudioPreviewRequest, AudioPreviewResponse
from core_pipeline.audio_engine import synthesize_speech_async, get_audio_duration

router = APIRouter(prefix="/audio", tags=["Âm thanh (Audio & TTS)"])

VOICE_LIST = [
    VoiceInfo(
        voice_id="vi-VN-HoaiMyNeural",
        name="Hoài My (Truyền cảm - Chuẩn)",
        gender="Female",
        language="vi-VN"
    ),
    VoiceInfo(
        voice_id="vi-VN-HoaiMy-Deep",
        name="Hoài My (Trầm lắng - Kể chuyện)",
        gender="Female",
        language="vi-VN"
    ),
    VoiceInfo(
        voice_id="vi-VN-HoaiMy-Lively",
        name="Hoài My (Tươi trẻ - Hoạt hình)",
        gender="Female",
        language="vi-VN"
    ),
    VoiceInfo(
        voice_id="vi-VN-NamMinhNeural",
        name="Nam Minh (Trầm ấm - Chuẩn)",
        gender="Male",
        language="vi-VN"
    ),
    VoiceInfo(
        voice_id="vi-VN-NamMinh-Deep",
        name="Nam Minh (Sâu lắng - Tài liệu)",
        gender="Male",
        language="vi-VN"
    ),
    VoiceInfo(
        voice_id="vi-VN-NamMinh-Youth",
        name="Nam Minh (Năng động - Review)",
        gender="Male",
        language="vi-VN"
    ),
    VoiceInfo(
        voice_id="en-US-JennyNeural",
        name="Jenny (Nữ - Tiếng Anh)",
        gender="Female",
        language="en-US"
    ),
    VoiceInfo(
        voice_id="en-US-GuyNeural",
        name="Guy (Nam - Tiếng Anh)",
        gender="Male",
        language="en-US"
    ),
]

@router.get("/voices", response_model=List[VoiceInfo])
async def get_available_voices():
    """Lấy danh sách các giọng đọc AI được hỗ trợ."""
    return VOICE_LIST

@router.post("/preview", response_model=AudioPreviewResponse)
async def preview_voice(req: AudioPreviewRequest):
    """
    Sinh file âm thanh nghe thử cho một câu thoại ngắn.
    """
    try:
        preview_id = f"prev_{uuid.uuid4().hex[:8]}.mp3"
        preview_path = os.path.join(settings.TEMP_DIR, preview_id)
        
        await synthesize_speech_async(
            text=req.text,
            output_path=preview_path,
            voice=req.voice_id,
            rate=req.rate
        )
        duration = get_audio_duration(preview_path)
        
        return AudioPreviewResponse(
            audio_url=f"/static/temp/{preview_id}",
            duration_seconds=round(duration, 2)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi khi tạo audio nghe thử: {str(e)}")
