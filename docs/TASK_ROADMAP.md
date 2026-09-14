# KẾ HOẠCH PHÁT TRIỂN & DANH MỤC CÔNG VIỆC (TASK ROADMAP)
## DỰ ÁN: DRAWSTORY AI

---

## 📅 1. LỘ TRÌNH TỔNG THỂ (PHASE OVERVIEW)

```
[ Phase 1: Core Rendering Pipeline ]  ──►  Kiểm chứng thuật toán vẽ bút & TTS
             │
             ▼
[ Phase 2: Backend API & Task Queue ] ──►  Xây dựng FastAPI + Asynchronous Worker
             │
             ▼
[ Phase 3: Frontend Web Studio ]      ──►  Giao diện Next.js tương tác trực quan
             │
             ▼
[ Phase 4: Tối ưu & Đóng gói Docker ] ──►  Triển khai và hoàn thiện báo cáo đồ án
```

---

## 🎯 2. CHI TIẾT TỪNG GIAI ĐOẠN & CHECKLIST THỰC HIỆN

### GIAI ĐOẠN 1: CORE RENDERING PIPELINE (TRÁI TIM HỆ THỐNG)
> **Mục tiêu**: Viết các module Python độc lập, chạy thành công kịch bản thử nghiệm từ dòng lệnh `python -m core_pipeline.runner`.

- [ ] **Task 1.1: Thiết lập môi trường dự án**
  - Khởi tạo thư mục mã nguồn: `core_pipeline/`, `backend/`, `frontend/`.
  - Khởi tạo `requirements.txt` với: `opencv-python`, `numpy`, `edge-tts`, `moviepy`, `google-genai`, `requests`.
  - Chuẩn bị tài nguyên mẫu trong `assets/`: ảnh bàn tay cầm bút `hand_pen.png`, nhạc nền `bgm_sample.mp3`, font chữ `Inter-Bold.ttf`.
- [ ] **Task 1.2: Module Kịch bản (`core_pipeline/script_engine.py`)**
  - Viết hàm gọi Google Gemini API với structured output JSON (Pydantic schema).
  - Tự động chuẩn hóa prompt sinh ảnh sang phong cách: *clean minimal line art, black and white sketch, white background*.
- [ ] **Task 1.3: Module Giọng đọc (`core_pipeline/audio_engine.py`)**
  - Viết hàm async gọi `edge-tts` chuyển văn bản kịch bản thành file audio `.mp3`.
  - Viết hàm trích xuất chính xác thời lượng audio (`duration`) bằng thư viện `mutagen` hoặc `moviepy`.
- [ ] **Task 1.4: Module Tạo ảnh (`core_pipeline/image_engine.py`)**
  - Tích hợp API tạo ảnh miễn phí (Pollinations AI / HuggingFace) hoặc lưu cache ảnh.
- [ ] **Task 1.5: Module Thuật toán Bút vẽ (`core_pipeline/sketch_animator.py`)**
  - Triển khai bộ lọc Canny Edge Detection & Contour Ordering.
  - Viết hàm nội suy khung hình khớp chính xác với thời lượng $T_{audio}$.
  - Viết thuật toán hòa trộn Alpha Blending đặt bàn tay cầm bút di chuyển theo nét vẽ.
- [ ] **Task 1.6: Module Ghép Video (`core_pipeline/compositor.py`)**
  - Sử dụng MoviePy / FFmpeg ghép các clip từng cảnh lại thành 1 video duy nhất.
  - Ghép track giọng đọc thuyết minh và track nhạc nền lofi (có ducking âm lượng).
  - Tự động chèn phụ đề chữ nổi bật giữa màn hình.

---

### GIAI ĐOẠN 2: BACKEND API & ASYNC QUEUE
> **Mục tiêu**: Đóng gói Core Pipeline thành dịch vụ Web API có khả năng xử lý ngầm không chặn luồng (Non-blocking).

- [ ] **Task 2.1: Cấu hình FastAPI (`backend/main.py`)**
  - Thiết lập CORS cho phép kết nối từ Frontend Next.js.
  - Cấu hình phục vụ file tĩnh (`/static/videos`, `/static/images`).
- [ ] **Task 2.2: Định nghĩa Models & Schemas (`backend/schemas/`)**
  - Pydantic models cho `StoryRequest`, `StoryResponse`, `RenderRequest`, `TaskStatus`.
- [ ] **Task 2.3: Bộ điều phối tác vụ ngầm (`backend/services/task_manager.py`)**
  - Triển khai hàng đợi tác vụ nền lưu tiến độ % vào bộ nhớ (Memory/SQLite).
  - Cung cấp API `GET /api/v1/video/status/{task_id}` để Frontend kiểm tra trạng thái.
- [ ] **Task 2.4: Viết API Endpoints (`backend/routers/`)**
  - `routers/story.py`: Sinh kịch bản và phân cảnh.
  - `routers/audio.py`: Nghe thử giọng đọc.
  - `routers/video.py`: Bấm nút render và kiểm tra tiến độ.

---

### GIAI ĐOẠN 3: FRONTEND WEB STUDIO (GIAO DIỆN NGƯỜI DÙNG)
> **Mục tiêu**: Xây dựng Web App tương tác hiện đại, trực quan, dễ dùng cho bất kỳ ai.

- [ ] **Task 3.1: Khởi tạo dự án Next.js & UI Components**
  - Setup Next.js 14 + TailwindCSS + Lucide Icons + Radix UI.
  - Thiết kế tông màu hiện đại (Modern Slate & Indigo Accent).
- [ ] **Task 3.2: Màn hình 1 - Nhập Ý Tưởng (Prompt Workspace)**
  - Ô nhập chủ đề video, lựa chọn tone giọng, lựa chọn ngôn ngữ và số lượng phân cảnh.
  - Nút bấm *"Tạo Kịch Bản Bằng AI"* với hiệu ứng loading đẹp mắt.
- [ ] **Task 3.3: Màn hình 2 - Storyboard Studio (Biên tập từng cảnh)**
  - Danh sách các thẻ (Card) phân cảnh:
    * Khung hiển thị ảnh minh họa (kèm nút đổi ảnh khác).
    * Ô soạn thảo văn bản thoại (cho phép sửa lời).
    * Trình phát nghe thử giọng đọc của cảnh đó.
- [ ] **Task 3.4: Màn hình 3 - Render & Xuất Bản (Export Center)**
  - Thanh tiến trình hiển thị trực quan từng bước: `% Tiến độ`, thông báo: *"Đang vẽ phân cảnh 2/3..."*.
  - Trình phát video chuẩn kích thước 9:16 (Shorts/TikTok Player).
  - Nút bấm Tải xuống (Download MP4).

---

### GIAI ĐOẠN 4: THỬ NGHIỆM, TỐI ƯU & ĐÓNG GÓI
- [ ] **Task 4.1: Kiểm thử tải và tối ưu render**
  - Đo đạc thời gian render trên các độ dài kịch bản khác nhau (30s, 60s).
  - Tinh chỉnh tốc độ thuật toán OpenCV để giảm thiểu thời gian xử lý.
- [ ] **Task 4.2: Đóng gói Docker Compose (`docker-compose.yml`)**
  - Container 1: Frontend (Next.js).
  - Container 2: Backend & Worker (FastAPI + OpenCV + FFmpeg).
- [ ] **Task 4.3: Chuẩn bị tài liệu báo cáo đồ án**
  - Xuất Slide thuyết trình, Video demo thực tế và file Báo cáo kỹ thuật tổng kết.
