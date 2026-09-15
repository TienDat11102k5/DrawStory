"""
DrawStory AI - Pipeline Runner
Script điều phối chạy toàn bộ quy trình từ Ý tưởng -> Kịch bản -> TTS -> Ảnh -> Bút vẽ -> Video hoàn chỉnh.
"""

import os
import sys
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
import argparse
import time

# Đảm bảo import được các module trong package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core_pipeline.script_engine import generate_storyboard
from core_pipeline.audio_engine import synthesize_speech, get_audio_duration
from core_pipeline.image_engine import generate_sketch_image
from core_pipeline.sketch_animator import generate_sketch_video
from core_pipeline.compositor import assemble_full_video
from assets.generate_assets import create_hand_pen_asset

def run_pipeline(
    topic: str,
    scenes_count: int = 2,
    voice_id: str = "vi-VN-HoaiMyNeural",
    voice_rate: float = 1.0,
    output_filename: str = "drawstory_demo.mp4"
) -> str:
    start_time = time.time()
    print("=" * 65)
    print(f"🚀 BẮT ĐẦU QUY TRÌNH DRAWSTORY AI: '{topic}'")
    print("=" * 65)

    # 1. Khởi tạo thư mục và tài nguyên
    temp_dir = os.path.abspath("data/temp")
    output_dir = os.path.abspath("data/outputs")
    assets_dir = os.path.abspath("assets")
    os.makedirs(temp_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    hand_path = os.path.join(assets_dir, "hand_pen.png")
    if not os.path.exists(hand_path):
        create_hand_pen_asset(hand_path)

    # 2. Bước 1: Sinh kịch bản phân cảnh (LLM)
    print("\n[BƯỚC 1/4] Đang tạo kịch bản phân cảnh...")
    storyboard = generate_storyboard(topic, scenes_count=scenes_count)
    print(f"-> Tiêu đề: {storyboard.title}")
    print(f"-> Số phân cảnh: {len(storyboard.scenes)}")

    # 3. Bước 2 & 3: Xử lý từng phân cảnh (Audio + Image + Sketch Video)
    scene_pairs = []

    for i, scene in enumerate(storyboard.scenes):
        print(f"\n--- Đang xử lý Phân cảnh {scene.scene_id}/{len(storyboard.scenes)} ---")
        print(f"Lời thoại: \"{scene.narration}\"")
        
        # 3.1. Tạo Audio TTS
        audio_path = os.path.join(temp_dir, f"scene_{scene.scene_id}.mp3")
        synthesize_speech(scene.narration, audio_path, voice=voice_id, rate=voice_rate)
        duration = get_audio_duration(audio_path)
        print(f"-> Đã tạo Voice: {audio_path} (Thời lượng: {duration:.2f}s)")

        # 3.2. Tạo ảnh nét phác thảo AI
        image_path = os.path.join(temp_dir, f"scene_{scene.scene_id}.png")
        generate_sketch_image(scene.image_prompt, image_path, seed=100 + i)

        # 3.3. Sinh Video vẽ nét bút chì kèm bàn tay di chuyển và phụ đề
        video_clip_path = os.path.join(temp_dir, f"scene_{scene.scene_id}_draw.mp4")
        generate_sketch_video(
            image_path=image_path,
            audio_duration=duration,
            output_video_path=video_clip_path,
            narration=scene.narration,
            hand_img_path=hand_path,
            fps=30
        )

        scene_pairs.append({
            "video_path": video_clip_path,
            "audio_path": audio_path,
            "narration": scene.narration
        })

    # 4. Bước 4: Ghép nối các phân cảnh thành video hoàn chỉnh
    print("\n[BƯỚC 4/4] Đang ghép nối toàn bộ video...")
    final_output_path = os.path.join(output_dir, output_filename)
    assemble_full_video(scene_pairs, final_output_path)

    elapsed = time.time() - start_time
    print("=" * 65)
    print(f"🎉 THÀNH CÔNG! Video đã sẵn sàng tại:")
    print(f"📁 {final_output_path}")
    print(f"⏱️ Tổng thời gian thực hiện: {elapsed:.1f} giây")
    print("=" * 65)
    return final_output_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Chạy thử nghiệm DrawStory AI")
    parser.add_argument("--topic", type=str, default="Sự kiên trì của chú rùa nhỏ", help="Chủ đề video")
    parser.add_argument("--scenes", type=int, default=2, help="Số phân cảnh")
    parser.add_argument("--output", type=str, default="drawstory_demo.mp4", help="Tên file xuất")
    args = parser.parse_args()

    run_pipeline(args.topic, scenes_count=args.scenes, output_filename=args.output)
