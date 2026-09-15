"""
DrawStory AI - Audio Engine
Module xử lý Text-to-Speech (TTS) bằng edge-tts và đo thời lượng âm thanh.
"""

import asyncio
import os
import sys
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
import edge_tts
from typing import Optional, Union

def _format_rate(rate: Union[str, float]) -> str:
    if isinstance(rate, (int, float)):
        pct = int(round((float(rate) - 1.0) * 100))
        return f"+{pct}%" if pct >= 0 else f"{pct}%"
    return str(rate)

VOICE_PROFILES = {
    # 6 Phong cách giọng tiếng Việt ổn định 100%
    "vi-VN-HoaiMyNeural": {"voice": "vi-VN-HoaiMyNeural", "rate_offset": 0},
    "vi-VN-HoaiMy-Deep": {"voice": "vi-VN-HoaiMyNeural", "rate_offset": -8},
    "vi-VN-HoaiMy-Lively": {"voice": "vi-VN-HoaiMyNeural", "rate_offset": 8},
    "vi-VN-NamMinhNeural": {"voice": "vi-VN-NamMinhNeural", "rate_offset": 0},
    "vi-VN-NamMinh-Deep": {"voice": "vi-VN-NamMinhNeural", "rate_offset": -8},
    "vi-VN-NamMinh-Youth": {"voice": "vi-VN-NamMinhNeural", "rate_offset": 8},
}

DEFAULT_VOICE = "vi-VN-HoaiMyNeural"

SUPPORTED_VOICES = {
    "vi_female": "vi-VN-HoaiMyNeural",     # Nữ miền Bắc truyền cảm
    "vi_female_deep": "vi-VN-HoaiMy-Deep", # Nữ trầm lắng kể chuyện
    "vi_female_lively": "vi-VN-HoaiMy-Lively", # Nữ tươi trẻ hoạt hình
    "vi_male": "vi-VN-NamMinhNeural",      # Nam miền Bắc trầm ấm
    "vi_male_deep": "vi-VN-NamMinh-Deep",  # Nam sâu lắng tài liệu
    "vi_male_youth": "vi-VN-NamMinh-Youth",# Nam trẻ trung review
    "en_female": "en-US-JennyNeural",      # Nữ tiếng Anh tự nhiên
    "en_male": "en-US-GuyNeural",          # Nam tiếng Anh
}

async def synthesize_speech_async(
    text: str,
    output_path: str,
    voice: str = DEFAULT_VOICE,
    rate: Union[str, float] = 1.0,
    volume: str = "+0%"
) -> str:
    """
    Sinh file âm thanh từ văn bản kịch bản sử dụng Microsoft Edge TTS.
    """
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    
    clean_text = text.replace("DrawStory", "Draw Story")
    profile = VOICE_PROFILES.get(voice, {"voice": voice, "rate_offset": 0})
    actual_voice = profile.get("voice", voice)
    rate_offset = profile.get("rate_offset", 0)

    if isinstance(rate, (int, float)):
        final_rate = max(0.25, min(2.0, rate + (rate_offset / 100.0)))
    else:
        final_rate = rate
    rate_str = _format_rate(final_rate)

    for attempt in range(2):
        try:
            communicate = edge_tts.Communicate(clean_text, actual_voice, rate=rate_str, volume=volume)
            await communicate.save(output_path)
            return output_path
        except Exception as e:
            if attempt == 0:
                await asyncio.sleep(0.3)
                rate_str = "+0%"
            else:
                raise e
    return output_path

def synthesize_speech(
    text: str,
    output_path: str,
    voice: str = DEFAULT_VOICE,
    rate: Union[str, float] = 1.0,
    volume: str = "+0%"
) -> str:
    """Wrapper đồng bộ cho synthesize_speech_async"""
    return asyncio.run(synthesize_speech_async(text, output_path, voice, rate, volume))

def get_audio_duration(audio_path: str) -> float:
    """
    Trích xuất thời lượng chính xác của file âm thanh (tính theo giây).
    Sử dụng mutagen hoặc fallback đọc qua moviepy/wave.
    """
    try:
        from mutagen.mp3 import MP3
        audio = MP3(audio_path)
        return float(audio.info.length)
    except Exception:
        try:
            try:
                from moviepy import AudioFileClip
            except (ImportError, AttributeError):
                import importlib
                AudioFileClip = importlib.import_module("moviepy.editor").AudioFileClip
            with AudioFileClip(audio_path) as clip:
                return float(clip.duration)
        except Exception as e:
            # Fallback tính toán ước tính nếu không đọc được header (khoảng 3.5 từ/giây)
            print(f"[Warning] Không thể đọc metadata audio: {e}. Sử dụng thời lượng mặc định 5.0s.")
            return 5.0

if __name__ == "__main__":
    test_text = "Xin chào các bạn, đây là thử nghiệm giọng đọc tự nhiên cho dự án DrawStory AI."
    out_file = "data/temp/test_voice.mp3"
    print(f"Đang tạo giọng đọc mẫu: '{test_text}'...")
    synthesize_speech(test_text, out_file)
    dur = get_audio_duration(out_file)
    print(f"Thành công! File lưu tại: {out_file} (Thời lượng: {dur:.2f}s)")
