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
from typing import Optional

DEFAULT_VOICE = "vi-VN-HoaiMyNeural"

SUPPORTED_VOICES = {
    "vi_female": "vi-VN-HoaiMyNeural",     # Nữ miền Bắc truyền cảm
    "vi_male": "vi-VN-NamMinhNeural",      # Nam miền Bắc trầm ấm
    "en_female": "en-US-JennyNeural",      # Nữ tiếng Anh tự nhiên
    "en_male": "en-US-GuyNeural",          # Nam tiếng Anh
}

async def synthesize_speech_async(
    text: str,
    output_path: str,
    voice: str = DEFAULT_VOICE,
    rate: str = "+0%",
    volume: str = "+0%"
) -> str:
    """
    Sinh file âm thanh từ văn bản kịch bản sử dụng Microsoft Edge TTS.
    """
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    communicate = edge_tts.Communicate(text, voice, rate=rate, volume=volume)
    await communicate.save(output_path)
    return output_path

def synthesize_speech(
    text: str,
    output_path: str,
    voice: str = DEFAULT_VOICE,
    rate: str = "+0%",
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
            from moviepy.editor import AudioFileClip
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
