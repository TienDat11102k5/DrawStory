# ĐẶC TẢ GIAO DIỆN LẬP TRÌNH ỨNG DỤNG (API SPECIFICATION)
## DỰ ÁN: DRAWSTORY AI (FASTAPI RESTFUL ENDPOINTS)

---

## 1. TIÊU CHUẨN CHUNG (CONVENTIONS)
* **Base URL**: `http://localhost:8000/api/v1`
* **Content-Type**: `application/json`
* **Xác thực (Authentication)**: Bản MVP mở nội bộ, phiên bản thương mại hỗ trợ Bearer Token (`Authorization: Bearer <token>`).
* **Định dạng thời gian**: ISO 8601 (`YYYY-MM-DDTHH:mm:ssZ`).

---

## 2. DANH SÁCH CÁC ENDPOINTS

| Nhóm chức năng | Phương thức | Endpoint | Mô tả ngắn |
| :--- | :--- | :--- | :--- |
| **Kịch bản** | `POST` | `/story/generate` | Tạo kịch bản phân cảnh từ ý tưởng |
| **Âm thanh** | `GET` | `/audio/voices` | Lấy danh sách giọng đọc hỗ trợ |
| **Âm thanh** | `POST` | `/audio/preview` | Tạo & nghe thử audio 1 câu thoại |
| **Hình ảnh** | `POST` | `/image/generate` | Tạo ảnh nét vẽ minh họa cho 1 cảnh |
| **Render Video** | `POST` | `/video/render` | Bắt đầu tác vụ render toàn bộ video |
| **Render Video** | `GET` | `/video/status/{task_id}` | Kiểm tra % tiến độ render |
| **Dự án** | `GET` | `/projects/{project_id}` | Lấy chi tiết thông tin dự án |

---

## 3. CHI TIẾT CÁC ENDPOINTS

### 3.1. `POST /api/v1/story/generate`
Tự động gọi Google Gemini LLM để sinh danh sách các phân cảnh kịch bản dựa trên ý tưởng của người dùng.

#### Request Body:
```json
{
  "topic": "Tại sao dậy sớm lúc 5h sáng giúp thay đổi cuộc sống",
  "language": "vi",
  "tone": "motivational", 
  "target_duration_seconds": 45,
  "scenes_count": 3
}
```

#### Response Success (`200 OK`):
```json
{
  "project_id": "proj_9a7d2b1f",
  "title": "Sức mạnh của việc thức dậy 5h sáng",
  "scenes": [
    {
      "scene_id": 1,
      "narration": "Khi cả thế giới đang say ngủ lúc 5 giờ sáng, một thế giới tĩnh lặng bắt đầu mở ra trước mắt bạn.",
      "image_prompt": "Minimalist pencil sketch, a serene quiet city before sunrise, an open window with a steaming cup of coffee, clean black and white lines, white background",
      "keywords": ["5 giờ sáng", "tĩnh lặng", "thay đổi"]
    },
    {
      "scene_id": 2,
      "narration": "Đó không chỉ là thời gian, đó là khoảnh khắc bạn hoàn toàn làm chủ chính mình trước khi ngày mới bắt đầu.",
      "image_prompt": "Minimal line art sketch, a person writing in a journal under a warm desk lamp, clean geometric lines, sketch style",
      "keywords": ["làm chủ", "thời gian", "mục tiêu"]
    }
  ]
}
```

---

### 3.2. `GET /api/v1/audio/voices`
Lấy danh sách các giọng đọc TTS được hỗ trợ (qua `edge-tts`).

#### Response Success (`200 OK`):
```json
[
  {
    "voice_id": "vi-VN-HoaiMyNeural",
    "name": "Hoài My (Nữ - Miền Bắc)",
    "gender": "Female",
    "language": "vi-VN"
  },
  {
    "voice_id": "vi-VN-NamMinhNeural",
    "name": "Nam Minh (Nam - Miền Bắc)",
    "gender": "Male",
    "language": "vi-VN"
  }
]
```

---

### 3.3. `POST /api/v1/image/generate`
Tạo lại hoặc sinh mới hình ảnh phác thảo cho một phân cảnh cụ thể.

#### Request Body:
```json
{
  "prompt": "Minimalist sketch of a runner crossing the finish line, clean lines, black ink on white background",
  "aspect_ratio": "9:16"
}
```

#### Response Success (`200 OK`):
```json
{
  "image_url": "/static/images/img_4c2e88a1.png",
  "cached": false
}
```

---

### 3.4. `POST /api/v1/video/render`
Gửi toàn bộ kịch bản đã được người dùng chỉnh sửa vào hàng đợi xử lý render video.

#### Request Body:
```json
{
  "project_id": "proj_9a7d2b1f",
  "voice_id": "vi-VN-HoaiMyNeural",
  "bgm_id": "lofi_peaceful_01",
  "aspect_ratio": "9:16",
  "enable_hand_drawing": true,
  "enable_subtitles": true,
  "scenes": [
    {
      "scene_id": 1,
      "narration": "Khi cả thế giới đang say ngủ lúc 5 giờ sáng...",
      "image_url": "/static/images/img_4c2e88a1.png"
    }
  ]
}
```

#### Response Success (`202 Accepted`):
```json
{
  "task_id": "task_render_890a3c",
  "status": "QUEUED",
  "message": "Video rendering task has been successfully scheduled."
}
```

---

### 3.5. `GET /api/v1/video/status/{task_id}`
Thăm dò tiến độ render video theo thời gian thực.

#### Response In Progress (`200 OK`):
```json
{
  "task_id": "task_render_890a3c",
  "status": "PROCESSING",
  "progress_percentage": 65,
  "current_step": "Synthesizing pencil sketch animation for Scene 2/3",
  "estimated_remaining_seconds": 15
}
```

#### Response Completed (`200 OK`):
```json
{
  "task_id": "task_render_890a3c",
  "status": "COMPLETED",
  "progress_percentage": 100,
  "current_step": "Rendering finished successfully.",
  "result": {
    "video_url": "/static/videos/final_proj_9a7d2b1f.mp4",
    "duration_seconds": 46.2,
    "file_size_mb": 14.8
  }
}
```
