# ĐẶC TẢ YÊU CẦU PHẦN MỀM (SRS - SOFTWARE REQUIREMENTS SPECIFICATION)
## DỰ ÁN: DRAWSTORY AI (SKETCHSHORTS GENERATOR)

---

## 1. GIỚI THIỆU (INTRODUCTION)

### 1.1. Mục đích (Purpose)
Tài liệu này định nghĩa chi tiết các yêu cầu chức năng (Functional Requirements) và yêu cầu phi chức năng (Non-functional Requirements) cho hệ thống **DrawStory AI**. Hệ thống hướng đến tự động hóa toàn diện quy trình sản xuất video dạng vẽ tranh bảng trắng (Whiteboard / Sketch Animation) kết hợp lồng tiếng thuyết minh và phụ đề dành cho các nền tảng video ngắn (TikTok, YouTube Shorts, Reels).

### 1.2. Bối cảnh & Phạm vi sản phẩm (Product Scope)
* **Bối cảnh**: Nhu cầu sáng tạo nội dung dạng giáo dục, tóm tắt sách, truyện ngắn, bài học cuộc sống theo phong cách vẽ tay (whiteboard) rất lớn nhưng quy trình sản xuất thủ công đòi hỏi kỹ năng đồ họa phức tạp và tốn nhiều giờ biên tập.
* **Phạm vi**: Ứng dụng cung cấp giao diện Web cho phép người dùng:
  * Nhập ý tưởng/chủ đề -> Sinh kịch bản phân cảnh tự động bằng LLM.
  * Tinh chỉnh nội dung từng phân cảnh (lời thoại, hình ảnh).
  * Tự động sinh giọng đọc AI (TTS) và hình ảnh phác thảo nét vẽ.
  * Áp dụng thuật toán dựng video mô phỏng bàn tay cầm bút vẽ lại tranh theo thời gian thực của giọng đọc.
  * Xuất video hoàn chỉnh độ phân giải Full HD (1080x1920) tỉ lệ 9:16.

### 1.3. Đối tượng sử dụng (Target Audience)
* Nhà sáng tạo nội dung (Content Creators, YouTubers, TikTokers).
* Giáo viên, người làm nội dung giáo dục trực tuyến (EdTech).
* Marketers muốn sản xuất video minh họa giải thích sản phẩm (Explainer videos).

---

## 2. MÔ TẢ TỔNG QUAN HỆ THỐNG (OVERALL DESCRIPTION)

### 2.1. Phân loại tác nhân (Actors)
* **Khách / Người dùng (User)**: Người thao tác nhập ý tưởng, biên tập kịch bản và yêu cầu xuất video.
* **Hệ thống AI Ngoại vi (External AI Services)**:
  * Google Gemini API (Sinh kịch bản & prompt).
  * Text-to-Speech Engine (Edge-TTS hoặc ElevenLabs).
  * Image Generation API (Flux / SD / Pollinations).
* **Worker xử lý nền (Video Processing Worker)**: Tiến trình chạy ngầm nhận lệnh từ hàng đợi để render video.

### 2.2. Sơ đồ Use Case tổng thể (Use Case Diagram)

```mermaid
usecaseDiagram
    actor "Content Creator" as User
    actor "Gemini LLM" as LLM
    actor "Edge TTS" as TTS
    actor "Image Engine" as ImgGen
    actor "Video Worker" as Worker

    package "DrawStory AI System" {
        usecase "UC-01: Nhập ý tưởng & Cấu hình" as UC1
        usecase "UC-02: Tạo kịch bản phân cảnh" as UC2
        usecase "UC-03: Biên tập Storyboard (Thoại & Ảnh)" as UC3
        usecase "UC-04: Nghe thử Voice & Xem trước ảnh" as UC4
        usecase "UC-05: Yêu cầu Render Video" as UC5
        usecase "UC-06: Theo dõi tiến độ Render" as UC6
        usecase "UC-07: Xem & Tải video thành phẩm" as UC7
    }

    User --> UC1
    UC1 ..> UC2 : <<include>>
    UC2 --> LLM
    User --> UC3
    UC3 --> UC4
    UC4 --> TTS
    UC4 --> ImgGen
    User --> UC5
    UC5 --> Worker
    User --> UC6
    Worker --> UC6
    User --> UC7
```

---

## 3. YÊU CẦU CHỨC NĂNG (FUNCTIONAL REQUIREMENTS)

### 3.1. Phân hệ Kịch bản (Scripting & Storyboard Module)
* **FR-01 (Generate Script)**: Người dùng nhập vào chủ đề (Topic), chọn tone giọng (Hài hước, Kể chuyện, Giáo dục), thời lượng mong muốn (30s, 60s). Hệ thống trả về cấu trúc JSON gồm danh sách các phân cảnh (`scenes`).
* **FR-02 (Scene Properties)**: Mỗi cảnh phải gồm:
  * `scene_index`: Số thứ tự cảnh (1, 2, 3...).
  * `narration`: Đoạn lời thoại thuyết minh (tiếng Việt hoặc tiếng Anh).
  * `image_prompt`: Câu lệnh tiếng Anh mô tả tranh vẽ nét chì đen trắng.
  * `keywords`: Từ khóa chính để phục vụ làm phụ đề nổi bật.
* **FR-03 (Edit Scene)**: Cho phép người dùng chỉnh sửa nội dung văn bản thoại, thêm cảnh mới hoặc xóa cảnh không mong muốn.
* **FR-04 (Regenerate Image)**: Cho phép người dùng tạo lại hình ảnh cho 1 cảnh cụ thể nếu ảnh ban đầu chưa ưng ý.

### 3.2. Phân hệ Âm thanh (Audio & TTS Module)
* **FR-05 (Voice Selection)**: Cung cấp danh sách các giọng đọc (ví dụ: Nữ miền Bắc - Hoài My, Nam miền Bắc - Nam Minh, Nữ miền Nam...).
* **FR-06 (Audio Synthesis)**: Tạo file âm thanh `.wav`/`.mp3` tương ứng với đoạn thoại của từng cảnh.
* **FR-07 (Audio Duration Extraction)**: Trích xuất chính xác độ dài thời gian của audio từng cảnh (độ chính xác đến mili-giây) để truyền vào module animation.
* **FR-08 (Background Music)**: Cho phép chọn nhạc nền lofi/nhẹ nhàng, tự động áp dụng hiệu ứng Audio Ducking (giảm âm lượng nhạc nền 80% khi có giọng đọc).

### 3.3. Phân hệ Xử lý hình ảnh & Hiệu ứng Bút vẽ (Animation Engine)
* **FR-09 (Sketch Preprocessing)**: Chuyển đổi ảnh AI màu sang định dạng phác thảo nét vẽ đơn sắc (Monochrome Sketch / Line Art) với nền trắng.
* **FR-10 (Vectorization / Contour Extraction)**: Trích xuất các đường nét chính của hình ảnh theo thứ tự hợp lý (từ nét viền lớn đến chi tiết nhỏ).
* **FR-11 (Stroke Progressive Reveal)**: Tạo video hiển thị nét vẽ xuất hiện dần dần từ 0% đến 100% hình ảnh trong đúng khoảng thời gian $T_{audio}$.
* **FR-12 (Hand Overlay Movement)**: Chèn hình ảnh bàn tay cầm bút (PNG trong suốt) di chuyển theo tọa độ $(x, y)$ của đầu nét vẽ đang được tạo ra.

### 3.4. Phân hệ Biên tập & Xuất Video (Video Assembly & Export)
* **FR-13 (Aspect Ratio & Resolution)**: Xuất chuẩn kích thước 1080x1920 pixels, khung hình dọc 9:16, tốc độ 30fps.
* **FR-14 (Dynamic Subtitle)**: Tự động chèn phụ đề chữ lớn ở trung tâm màn hình, có hiệu ứng highlight từ ngữ theo nhịp giọng đọc.
* **FR-15 (Transition Effects)**: Chèn hiệu ứng chuyển cảnh mượt mà giữa các phân cảnh (như hiệu ứng lật trang giấy hoặc xóa bảng).
* **FR-16 (Download & Preview)**: Cho phép xem trước video trực tiếp trên trình duyệt qua HTML5 Player và tải file `.mp4` về máy.

---

## 4. YÊU CẦU PHI CHỨC NĂNG (NON-FUNCTIONAL REQUIREMENTS)

### 4.1. Hiệu năng & Tốc độ (Performance)
* **NFR-01 (Script Latency)**: Thời gian sinh kịch bản ban đầu bằng Gemini không vượt quá 5 giây cho video 60 giây.
* **NFR-02 (Render Speed)**: Thời gian render toàn bộ video không vượt quá 2 lần thời lượng video thực tế (video 60s render trong khoảng < 120s trên cấu hình tiêu chuẩn).
* **NFR-03 (Asynchronous Queue)**: Quá trình render video bắt buộc phải thực thi bất đồng bộ thông qua Task Queue (Redis + Celery/ARQ), trả về task ID để client thăm dò (polling) hoặc nhận thông báo qua WebSocket/SSE.

### 4.2. Khả năng mở rộng (Scalability)
* **NFR-04 (Decoupled Design)**: Tách biệt hoàn toàn giữa Frontend, Backend API và Rendering Worker. Khi tải tăng, có thể scale nhiều Worker nodes độc lập.

### 4.3. Tính khả dụng & Trải nghiệm người dùng (Usability & UI/UX)
* **NFR-05 (Modern UI)**: Giao diện trực quan, hỗ trợ Dark Mode, thiết kế theo hệ thống thẻ (Card-based Storyboard) dễ theo dõi.
* **NFR-06 (Progress Feedback)**: Hiển thị thanh tiến trình chi tiết theo từng bước: Đang sinh kịch bản -> Đang tạo giọng đọc -> Đang vẽ nét tranh -> Đang ghép video hoàn tất.

---

## 5. RÀNG BUỘC & TIÊU CHUẨN THỰC HIỆN (CONSTRAINTS)
* Định dạng video xuất xưởng: MP4 (H.264 video codec, AAC audio codec) để đảm bảo tương thích tuyệt đối khi đăng lên TikTok, YouTube, Facebook.
* API Secret Keys: Lưu trữ an toàn qua biến môi trường (`.env`), tuyệt đối không lưu cứng trong mã nguồn.
