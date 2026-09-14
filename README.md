# DrawStory AI (SketchShorts AI) 🎨✍️
> **Hệ thống tự động tạo video ngắn phong cách vẽ phác thảo (Whiteboard Animation) từ ý tưởng kịch bản bằng Generative AI**

---

## 📌 1. Giới thiệu dự án
**DrawStory AI** là một nền tảng tạo video tự động (Automated Video Generation Platform). Người dùng chỉ cần nhập một ý tưởng nội dung ngắn (prompt/chủ đề), hệ thống sẽ:
1. Sử dụng Large Language Model (LLM - Google Gemini) phân tích và sinh kịch bản chi tiết theo từng phân cảnh (Storyboard).
2. Tạo hình ảnh minh họa màu sắc rực rỡ phong cách truyện tranh / màu nước (Vibrant Storybook Art) bằng AI.
3. Chuyển đổi văn bản thuyết minh thành giọng đọc tự nhiên (Text-to-Speech) qua `edge-tts`.
4. Áp dụng thuật toán Computer Vision mô phỏng bàn tay cầm bút vẽ nét viền, sau đó quét cọ lan tỏa hiệu ứng tô màu nước sống động (Watercolor Reveal).
5. Tự động ghép nối video, phụ đề động phong cách TikTok/Shorts và nhạc nền thành video ngắn hoàn chỉnh định dạng dọc (9:16).

---

## 🎬 Video Demo Trực Tiếp (Live Demo)

Người xem trên GitHub có thể xem trực tiếp video được tạo tự động bởi hệ thống dưới đây:

<div align="center">
  <table>
    <tr>
      <th align="center">🎞️ Ảnh động xem nhanh (Autoplay)</th>
      <th align="center">🔊 Video hoàn chỉnh có âm thanh & phụ đề</th>
    </tr>
    <tr>
      <td align="center" width="50%">
        <img src="assets/demo_preview.gif" alt="Whiteboard Drawing & Watercolor Animation Demo" width="280" style="border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.3);" />
      </td>
      <td align="center" width="50%">
        <video src="assets/demo_video.mp4" controls="controls" width="280" style="border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.3);"></video>
        <br />
        <a href="assets/demo_video.mp4"><b>▶ Bấm vào đây để tải / mở video gốc chất lượng cao</b></a>
      </td>
    </tr>
  </table>
</div>

---

## 🏗️ 2. Cấu trúc thư mục tài liệu dự án

Tài liệu kỹ thuật của dự án được tổ chức chi tiết trong thư mục `docs/`:

* 📄 [`docs/SRS.md`](docs/SRS.md): **Đặc tả yêu cầu phần mềm (Software Requirements Specification - Chuẩn IEEE 830)**.
* 🏛️ [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md): **Thiết kế kiến trúc hệ thống, sơ đồ tuần tự và luồng dữ liệu (C4 Model & Dataflow)**.
* ⚙️ [`docs/CORE_ALGORITHM_DESIGN.md`](docs/CORE_ALGORITHM_DESIGN.md): **Thiết kế thuật toán tạo hiệu ứng nét bút vẽ (Computer Vision, Vectorizer & Hand Sync)**.
* 🔌 [`docs/API_SPECIFICATION.md`](docs/API_SPECIFICATION.md): **Đặc tả chi tiết các RESTful API endpoints**.
* 📋 [`docs/TASK_ROADMAP.md`](docs/TASK_ROADMAP.md): **Lộ trình phân kỳ phát triển & Checklist thực hiện từng giai đoạn**.

---

## 💻 3. Công nghệ chủ đạo (Tech Stack)

| Thành phần | Công nghệ lựa chọn | Lý do sử dụng |
| :--- | :--- | :--- |
| **Frontend** | React (Vite) + Glassmorphism Dark UI | Giao diện Studio hiện đại, tự động lưu nháp thời gian thực, xem preview video mượt mà. |
| **Backend API** | Python (FastAPI) | Hiệu năng cao (Async), chuẩn hóa API RESTful, tích hợp hoàn hảo với thư viện AI. |
| **Queue / Worker** | Python BackgroundTasks / ThreadPool | Xử lý các tác vụ render video nặng ngầm không làm nghẽn server. |
| **LLM Engine** | Google Gemini (hỗ trợ nhập API Key) | Phản hồi siêu tốc, kịch bản điện ảnh sâu sắc, hook trực diện không lan man. |
| **TTS Engine** | `edge-tts` (Microsoft Neural Voices) | Giọng đọc tiếng Việt tự nhiên chuẩn cảm xúc, hoàn toàn miễn phí, tốc độ cao. |
| **Image Gen** | Pollinations AI / Flux / Midjourney 9:16 | Tự động tạo ảnh phác thảo + màu nước khung dọc 9:16 và hỗ trợ upload ảnh cá nhân. |
| **Animation Engine**| OpenCV + MoviePy / PIL | Tách contour đường nét, mô phỏng bàn tay vẽ chân thực và hiệu ứng loang màu nước. |

---

## 🚀 4. Hướng dẫn khởi động nhanh (Quick Start)

### Cách 1: Khởi động tự động bằng 1-Click (Khuyên dùng trên Windows)
Chỉ cần nhấp đúp chuột vào file:
```bash
run_app.bat
```
*(Hệ thống sẽ tự động khởi động đồng thời Backend FastAPI port 8000 và Frontend Studio port 3000)*

---

### Cách 2: Khởi động thủ công qua Terminal

#### 1. Chạy Backend (FastAPI):
```bash
# Kích hoạt môi trường ảo
.\venv\Scripts\activate

# Khởi động Backend API Server
uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```

#### 2. Chạy Frontend Studio (Vite):
```bash
cd frontend
npm install
npm run dev
```
Mở trình duyệt tại: **`http://localhost:3000`** để bắt đầu sáng tạo video ngắn!
