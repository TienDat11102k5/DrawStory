"""
DrawStory AI - Task Manager Service
Quản lý hàng đợi và luồng xử lý render video ngầm.
"""

import os
import uuid
import threading
import time
from typing import Dict, Optional
from concurrent.futures import ThreadPoolExecutor

from backend.config import settings
from backend.schemas.task import TaskStatusEnum, TaskStatusResponse, VideoRenderRequest, VideoRenderResult
from core_pipeline.audio_engine import synthesize_speech, get_audio_duration
from core_pipeline.image_engine import generate_sketch_image
from core_pipeline.sketch_animator import generate_sketch_video
from core_pipeline.compositor import assemble_full_video

def slugify_title(text: str, max_words: int = 10) -> str:
    """Chuyển đổi tiêu đề video tiếng Việt thành slug tên file chuẩn, an toàn và dễ nhận diện."""
    if not text:
        return "drawstory_video"
    text = text.lower().strip()
    vn_map = {
        'à': 'a', 'á': 'a', 'ả': 'a', 'ã': 'a', 'ạ': 'a',
        'ă': 'a', 'ằ': 'a', 'ắ': 'a', 'ẳ': 'a', 'ẵ': 'a', 'ặ': 'a',
        'â': 'a', 'ầ': 'a', 'ấ': 'a', 'ẩ': 'a', 'ẫ': 'a', 'ậ': 'a',
        'đ': 'd',
        'è': 'e', 'é': 'e', 'ẻ': 'e', 'ẽ': 'e', 'ẹ': 'e',
        'ê': 'e', 'ề': 'e', 'ế': 'e', 'ể': 'e', 'ễ': 'e', 'ệ': 'e',
        'ì': 'i', 'í': 'i', 'ỉ': 'i', 'ĩ': 'i', 'ị': 'i',
        'ò': 'o', 'ó': 'o', 'ỏ': 'o', 'õ': 'o', 'ọ': 'o',
        'ô': 'o', 'ồ': 'o', 'ố': 'o', 'ổ': 'o', 'ỗ': 'o', 'ộ': 'o',
        'ơ': 'o', 'ờ': 'o', 'ớ': 'o', 'ở': 'o', 'ỡ': 'o', 'ợ': 'o',
        'ù': 'u', 'ú': 'u', 'ủ': 'u', 'ũ': 'u', 'ụ': 'u',
        'ư': 'u', 'ừ': 'u', 'ứ': 'u', 'ử': 'u', 'ữ': 'u', 'ự': 'u',
        'ỳ': 'y', 'ý': 'y', 'ỷ': 'y', 'ỹ': 'y', 'ỵ': 'y'
    }
    for k, v in vn_map.items():
        text = text.replace(k, v)
    import unicodedata
    import re
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    text = re.sub(r'[^a-zA-Z0-9\s_]', '', text)
    words = [w for w in text.split() if w][:max_words]
    slug = '_'.join(words)
    return slug or "drawstory_video"

class TaskManager:
    def __init__(self, max_workers: int = 2):
        self._tasks: Dict[str, Dict] = {}
        self._lock = threading.Lock()
        self._executor = ThreadPoolExecutor(max_workers=max_workers)

    def create_task(self, render_request: VideoRenderRequest) -> str:
        task_id = f"task_{uuid.uuid4().hex[:10]}"
        with self._lock:
            self._tasks[task_id] = {
                "task_id": task_id,
                "status": TaskStatusEnum.QUEUED,
                "progress_percentage": 0,
                "current_step": "Đang chờ trong hàng đợi...",
                "error_message": None,
                "result": None,
                "created_at": time.time()
            }
        
        # Đẩy vào ThreadPool chạy ngầm
        self._executor.submit(self._execute_render_task, task_id, render_request)
        return task_id

    def get_task_status(self, task_id: str) -> Optional[TaskStatusResponse]:
        with self._lock:
            task = self._tasks.get(task_id)
            if not task:
                return None
            return TaskStatusResponse(**task)

    def _update_task(self, task_id: str, status: TaskStatusEnum, progress: int, step: str, error: str = None, result: Dict = None):
        with self._lock:
            if task_id in self._tasks:
                self._tasks[task_id]["status"] = status
                self._tasks[task_id]["progress_percentage"] = progress
                self._tasks[task_id]["current_step"] = step
                if error:
                    self._tasks[task_id]["error_message"] = error
                if result:
                    self._tasks[task_id]["result"] = result

    def _execute_render_task(self, task_id: str, req: VideoRenderRequest):
        try:
            self._update_task(task_id, TaskStatusEnum.PROCESSING, 5, "Khởi tạo môi trường xử lý...")
            
            project_id = req.project_id or f"proj_{uuid.uuid4().hex[:8]}"
            task_temp_dir = os.path.join(settings.TEMP_DIR, task_id)
            os.makedirs(task_temp_dir, exist_ok=True)
            
            hand_path = os.path.join(settings.ASSETS_DIR, "hand_pen.png")
            total_scenes = len(req.scenes)
            scene_pairs = []

            # 1. Xử lý từng phân cảnh
            for idx, scene in enumerate(req.scenes):
                scene_num = idx + 1
                base_pct = 10 + int((idx / total_scenes) * 70)

                # 1.1 Voice TTS
                self._update_task(
                    task_id, TaskStatusEnum.PROCESSING, base_pct,
                    f"Cảnh {scene_num}/{total_scenes}: Đang tạo giọng đọc thuyết minh..."
                )
                audio_path = os.path.join(task_temp_dir, f"scene_{scene_num}.mp3")
                synthesize_speech(scene.narration, audio_path, voice=req.voice_id, rate=req.voice_rate)
                duration = get_audio_duration(audio_path)

                # 1.2 Ảnh minh họa
                self._update_task(
                    task_id, TaskStatusEnum.PROCESSING, base_pct + int(35 / total_scenes),
                    f"Cảnh {scene_num}/{total_scenes}: Đang xử lý hình ảnh..."
                )
                image_path = os.path.join(task_temp_dir, f"scene_{scene_num}.png")
                
                # Ưu tiên số 1: Nếu người dùng đã tải ảnh lên hoặc cung cấp image_url
                if scene.image_url and str(scene.image_url).strip():
                    img_url_str = str(scene.image_url).strip()
                    if "/static/uploads/" in img_url_str:
                        fname = img_url_str.split("/static/uploads/")[-1].split("?")[0]
                        local_upload = os.path.join(settings.DATA_DIR, "uploads", fname)
                        if os.path.exists(local_upload):
                            image_path = local_upload
                            print(f"[TaskManager] ✅ Cảnh {scene_num}: Dùng ảnh người dùng upload tại: {image_path}")
                        else:
                            print(f"[TaskManager] ⚠️ Không tìm thấy file upload: {local_upload}, chuyển sang tạo ảnh AI")
                            prompt = scene.image_prompt or scene.narration
                            generate_sketch_image(prompt, image_path, seed=100 + idx)
                    elif os.path.exists(img_url_str):
                        image_path = img_url_str
                        print(f"[TaskManager] ✅ Cảnh {scene_num}: Dùng ảnh đường dẫn cục bộ: {image_path}")
                    else:
                        prompt = scene.image_prompt or scene.narration
                        generate_sketch_image(prompt, image_path, seed=100 + idx)
                else:
                    # Người dùng không upload ảnh -> Dùng prompt do người dùng nhập hoặc AI sinh
                    prompt = scene.image_prompt or scene.narration
                    print(f"[TaskManager] 🎨 Cảnh {scene_num}: Sinh ảnh AI theo prompt: '{prompt}'")
                    generate_sketch_image(prompt, image_path, seed=100 + idx)

                # 1.3 Nét bút vẽ & Bàn tay
                self._update_task(
                    task_id, TaskStatusEnum.PROCESSING, base_pct + int(50 / total_scenes),
                    f"Cảnh {scene_num}/{total_scenes}: Đang vẽ nét bút và chèn phụ đề..."
                )
                video_clip_path = os.path.join(task_temp_dir, f"scene_{scene_num}_draw.mp4")
                generate_sketch_video(
                    image_path=image_path,
                    audio_duration=duration,
                    output_video_path=video_clip_path,
                    narration=scene.narration if req.enable_subtitles else "",
                    hand_img_path=hand_path,
                    fps=settings.DEFAULT_FPS
                )

                scene_pairs.append({
                    "video_path": video_clip_path,
                    "audio_path": audio_path,
                    "narration": scene.narration
                })

            # 2. Ghép nối thành video hoàn chỉnh
            self._update_task(task_id, TaskStatusEnum.PROCESSING, 85, "Đang ghép nối các phân cảnh và tối ưu âm thanh...")
            
            # Lấy tiêu đề dự án để đặt tên file video chuẩn hóa theo yêu cầu
            raw_title = (req.title or "").strip()
            if not raw_title:
                try:
                    from backend.services.project_manager import project_manager
                    proj = project_manager.get_project(project_id)
                    if proj and proj.get("title"):
                        raw_title = proj.get("title")
                except Exception:
                    pass
            if not raw_title and req.scenes:
                raw_title = req.scenes[0].narration

            slug = slugify_title(raw_title)
            output_filename = f"{slug}.mp4"
            final_output_path = os.path.join(settings.OUTPUTS_DIR, output_filename)
            
            # Nếu trùng tên file đã có, thêm hậu tố ngắn để không ghi đè
            if os.path.exists(final_output_path):
                short_suffix = project_id.replace("proj_", "")[:6]
                output_filename = f"{slug}_{short_suffix}.mp4"
                final_output_path = os.path.join(settings.OUTPUTS_DIR, output_filename)
            
            assemble_full_video(scene_pairs, final_output_path)

            # Lấy thông tin video xuất xưởng
            file_size = os.path.getsize(final_output_path)
            total_duration = sum(get_audio_duration(p["audio_path"]) for p in scene_pairs)
            video_url = f"/static/outputs/{output_filename}"

            result = VideoRenderResult(
                video_url=video_url,
                duration_seconds=round(total_duration, 2),
                file_size_bytes=file_size
            )

            self._update_task(
                task_id, TaskStatusEnum.COMPLETED, 100,
                "Hoàn tất tạo video!",
                result=result.model_dump()
            )

            # Tự động lưu hoặc cập nhật dự án vào Project Manager
            try:
                from backend.services.project_manager import project_manager
                project_manager.save_project({
                    "project_id": project_id,
                    "title": raw_title[:60] if raw_title else "Dự án mới",
                    "voice_id": req.voice_id,
                    "voice_rate": req.voice_rate,
                    "scenes_count": len(req.scenes),
                    "scenes": [s.model_dump() for s in req.scenes],
                    "video_url": video_url,
                    "duration": round(total_duration, 1),
                    "status": "COMPLETED"
                })
            except Exception as pe:
                print(f"[Warning] Không thể lưu lịch sử dự án: {pe}")

        except Exception as e:
            import traceback
            traceback.print_exc()
            self._update_task(
                task_id, TaskStatusEnum.FAILED, 0,
                "Đã xảy ra lỗi trong quá trình tạo video.",
                error=str(e)
            )

task_manager = TaskManager()
