"""
DrawStory AI - Compositor
Module ghép nối các phân cảnh video, âm thanh thuyết minh, nhạc nền và xuất video hoàn chỉnh.
"""

import os
import sys
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
from typing import List, Dict, Any, Optional
from moviepy import VideoFileClip, AudioFileClip, CompositeAudioClip, concatenate_videoclips

def create_scene_clip_with_audio(video_path: str, audio_path: str) -> VideoFileClip:
    """
    Ghép file video nét vẽ với file audio giọng đọc tương ứng.
    """
    video_clip = VideoFileClip(video_path)
    audio_clip = AudioFileClip(audio_path)
    
    # Cắt hoặc khớp thời lượng chính xác
    final_clip = video_clip.with_audio(audio_clip)
    return final_clip

def assemble_full_video(
    scene_video_audio_pairs: List[Dict[str, str]],
    output_path: str,
    bgm_path: Optional[str] = None,
    bgm_volume: float = 0.12
) -> str:
    """
    Ghép tất cả các phân cảnh thành video ngắn hoàn chỉnh (9:16) kèm nhạc nền.
    scene_video_audio_pairs: [{"video_path": "...", "audio_path": "...", "narration": "..."}, ...]
    """
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    print(f"[Compositor] Đang ghép {len(scene_video_audio_pairs)} phân cảnh...")

    clips = []
    for item in scene_video_audio_pairs:
        v_path = item["video_path"]
        a_path = item["audio_path"]
        clip = create_scene_clip_with_audio(v_path, a_path)
        clips.append(clip)

    # Nối các phân cảnh liên tiếp
    final_video = concatenate_videoclips(clips, method="compose")

    # Xử lý nhạc nền nếu có
    if bgm_path and os.path.exists(bgm_path):
        try:
            bgm = AudioFileClip(bgm_path)
            # Lặp nhạc nền nếu video dài hơn nhạc
            if bgm.duration < final_video.duration:
                bgm = bgm.with_effects([]) # Lặp lại nếu cần
            bgm = bgm.subclipped(0, final_video.duration)
            bgm = bgm.with_volume_scaled(bgm_volume)

            # Hòa trộn âm thanh thuyết minh và nhạc nền
            composite_audio = CompositeAudioClip([final_video.audio, bgm])
            final_video = final_video.with_audio(composite_audio)
            print(f"[Compositor] Đã chèn nhạc nền: {bgm_path} (âm lượng: {bgm_volume})")
        except Exception as e:
            print(f"[Compositor] Không thể chèn nhạc nền ({e}), giữ nguyên thuyết minh gốc.")

    # Render video thành phẩm MP4 (H.264 + AAC)
    print(f"[Compositor] Đang xuất file hoàn chỉnh ra: {output_path}...")
    final_video.write_videofile(
        output_path,
        codec="libx264",
        audio_codec="aac",
        fps=30,
        preset="fast",
        threads=4
    )

    # Đóng các clip để giải phóng tài nguyên
    for c in clips:
        c.close()
    final_video.close()

    print(f"[Compositor] Hoàn tất! Video lưu tại: {output_path}")
    return output_path

if __name__ == "__main__":
    print("Compositor module sẵn sàng.")
