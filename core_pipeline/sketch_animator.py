"""
DrawStory AI - Sketch & Color Animator
Module tạo hiệu ứng bàn tay vẽ nét phác thảo sau đó tô màu nước sống động (Sketch & Watercolor Reveal)
kết hợp chèn phụ đề tiếng Việt phong cách video ngắn (Shorts / Reels / TikTok).
"""

import os
import sys
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
import math
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from typing import Tuple, List, Optional

def overlay_alpha_image(
    canvas: np.ndarray,
    overlay_img_rgba: np.ndarray,
    x: int,
    y: int
) -> np.ndarray:
    """
    Hòa trộn ảnh có kênh Alpha (RGBA) lên canvas (BGR) tại vị trí (x, y).
    """
    h_canvas, w_canvas = canvas.shape[:2]
    h_overlay, w_overlay = overlay_img_rgba.shape[:2]

    # Kiểm tra ngoài viền màn hình
    if x >= w_canvas or y >= h_canvas or x + w_overlay <= 0 or y + h_overlay <= 0:
        return canvas

    x1 = max(0, x)
    y1 = max(0, y)
    x2 = min(w_canvas, x + w_overlay)
    y2 = min(h_canvas, y + h_overlay)

    overlay_x1 = max(0, -x)
    overlay_y1 = max(0, -y)
    overlay_x2 = overlay_x1 + (x2 - x1)
    overlay_y2 = overlay_y1 + (y2 - y1)

    overlay_crop = overlay_img_rgba[overlay_y1:overlay_y2, overlay_x1:overlay_x2]
    canvas_crop = canvas[y1:y2, x1:x2]

    alpha = overlay_crop[:, :, 3] / 255.0
    alpha = np.expand_dims(alpha, axis=-1)

    overlay_bgr = overlay_crop[:, :, :3]
    blended = (alpha * overlay_bgr + (1.0 - alpha) * canvas_crop).astype(np.uint8)
    canvas[y1:y2, x1:x2] = blended

    return canvas

def split_into_timed_subtitles(narration: str, total_frames: int) -> List[Tuple[int, int, str]]:
    """
    Chia đoạn thoại dài thành các cụm từ ngắn gọn gàng (3-5 từ một cụm)
    và phân bổ khung thời gian [start_frame, end_frame] tương ứng theo nhịp đọc.
    """
    if not narration or not narration.strip():
        return []

    # Tách đoạn văn thành các từ
    raw_words = narration.strip().split()
    if not raw_words:
        return []

    # Gom từ thành các cụm ngắn 3-5 từ, ưu tiên ngắt ở dấu câu
    chunks = []
    current_chunk = []

    for word in raw_words:
        current_chunk.append(word)
        has_punctuation = any(word.endswith(p) for p in [".", ",", "!", "?", ";", ":", "—"])
        if len(current_chunk) >= 4 or (len(current_chunk) >= 2 and has_punctuation):
            chunks.append(" ".join(current_chunk))
            current_chunk = []

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    # Phân bổ thời gian cho từng cụm dựa theo độ dài số từ
    total_words = len(raw_words)
    timed_subtitles = []
    current_frame = 0

    for idx, chunk in enumerate(chunks):
        chunk_words_count = len(chunk.split())
        # Tỉ lệ thời gian
        ratio = chunk_words_count / total_words
        chunk_duration_frames = int(ratio * total_frames)
        end_frame = current_frame + chunk_duration_frames if idx < len(chunks) - 1 else total_frames
        timed_subtitles.append((current_frame, end_frame, chunk))
        current_frame = end_frame

    return timed_subtitles

def draw_dynamic_subtitle(
    frame_bgr: np.ndarray,
    subtitle_chunk: str,
    pos_y: Optional[int] = None,
    font_size: int = 50
) -> np.ndarray:
    """
    Vẽ DUY NHẤT một cụm từ ngắn gọn gàng lên màn hình với phong cách TikTok/Shorts:
    Chữ to, màu vàng rực rỡ, viền đen sắc sảo và hộp badge ôm vừa khít cụm từ,
    đặt ở khoảng cách cân đối ngay dưới tranh vẽ.
    """
    if not subtitle_chunk:
        return frame_bgr

    h, w = frame_bgr.shape[:2]
    img_pil = Image.fromarray(cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img_pil)

    # Load font chữ đậm nét hỗ trợ tiếng Việt
    font = None
    for font_name in ["arialbd.ttf", "arial.ttf", "segoeui.ttf", "tahoma.ttf"]:
        try:
            font = ImageFont.truetype(font_name, font_size)
            break
        except Exception:
            continue

    if font is None:
        font = ImageFont.load_default()

    # Tính kích thước của cụm từ
    bbox = draw.textbbox((0, 0), subtitle_chunk, font=font, stroke_width=3)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    # Căn giữa theo chiều ngang
    pos_x = (w - text_w) // 2
    
    # Nếu không truyền pos_y, mặc định đặt ở 65% chiều cao
    if pos_y is None:
        pos_y = int(h * 0.65)

    # Đảm bảo hộp badge có chiều rộng tối thiểu đẹp mắt và bo góc mượt mà
    pad_x = 28
    pad_y = 14
    badge_w = max(text_w + pad_x * 2, 220)
    badge_left = (w - badge_w) // 2
    badge_right = badge_left + badge_w
    badge_rect = [
        badge_left,
        pos_y - pad_y,
        badge_right,
        pos_y + text_h + pad_y
    ]
    # Nền đen mờ cao cấp
    draw.rounded_rectangle(badge_rect, radius=22, fill=(15, 15, 20, 235), outline=(255, 255, 255, 50), width=1)

    # Vẽ chữ màu vàng chanh sáng với viền đen nổi bật
    draw.text(
        (pos_x, pos_y),
        subtitle_chunk,
        font=font,
        fill=(255, 230, 30), # Vàng chanh sáng
        stroke_width=2,
        stroke_fill=(0, 0, 0) # Viền đen rõ nét
    )

    return cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)

def extract_sketch_points_and_color(
    img_bgr: np.ndarray,
    target_size: Tuple[int, int] = (1080, 1920)
):
    """
    Tiền xử lý ảnh, phóng to và căn chỉnh tranh vẽ cân đối ở trung tâm thị giác của video 9:16,
    trích xuất đường nét và chuẩn bị canvas màu hoàn chỉnh.
    """
    target_w, target_h = target_size
    h, w = img_bgr.shape[:2]

    # Phóng to tranh vẽ chiếm tới 90% bề ngang hoặc 68% chiều cao màn hình (tối ưu thị giác Shorts dọc 9:16)
    scale = min((target_w * 0.90) / w, (target_h * 0.68) / h)
    new_w, new_h = int(w * scale), int(h * scale)
    resized_color = cv2.resize(img_bgr, (new_w, new_h), interpolation=cv2.INTER_AREA)

    offset_x = (target_w - new_w) // 2
    # Căn trung tâm thị giác của bức tranh ở 44% chiều cao màn hình (cân đối, không bị đẩy lên quá cao)
    visual_center_y = int(target_h * 0.44)
    offset_y = max(int(target_h * 0.08), visual_center_y - (new_h // 2))

    # Tạo canvas màu đầy đủ đặt trên nền trắng tinh tế
    color_canvas = np.ones((target_h, target_w, 3), dtype=np.uint8) * 255
    color_canvas[offset_y:offset_y + new_h, offset_x:offset_x + new_w] = resized_color

    # Chuyển grayscale & phát hiện nét
    gray = cv2.cvtColor(resized_color, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    edges = cv2.Canny(blur, 50, 140)

    contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    contours = sorted(contours, key=lambda c: cv2.arcLength(c, False), reverse=True)

    points_with_color = []
    for c in contours:
        for pt in c:
            lx, ly = int(pt[0][0]), int(pt[0][1])
            gx, gy = lx + offset_x, ly + offset_y
            # Lấy màu gốc của pixel nhưng tăng độ tương phản để nét vẽ sắc sảo
            orig_color = resized_color[ly, lx].astype(np.float32)
            ink_color = (orig_color * 0.55).astype(np.uint8) # Làm đậm 45% để tạo nét bút rõ nét
            points_with_color.append(((gx, gy), tuple(int(v) for v in ink_color)))

    return resized_color, points_with_color, color_canvas, (offset_x, offset_y, new_w, new_h)

def generate_sketch_video(
    image_path: str,
    audio_duration: float,
    output_video_path: str,
    narration: str = "",
    hand_img_path: str = "assets/hand_pen.png",
    fps: int = 30,
    canvas_size: Tuple[int, int] = (1080, 1920),
    tip_offset: Tuple[int, int] = (20, 20)
) -> str:
    """
    Render video 3 giai đoạn:
    1. 0% -> 45%: Bàn tay vẽ nét phác thảo (Sketch lines có màu tương ứng).
    2. 45% -> 80%: Bàn tay tô màu nước sống động (Watercolor Color Fill).
    3. 80% -> 100%: Bàn tay rút ra, chiêm ngưỡng bức tranh màu sắc rực rỡ 100% kèm phụ đề.
    """
    os.makedirs(os.path.dirname(os.path.abspath(output_video_path)), exist_ok=True)

    img_bgr = cv2.imread(image_path)
    if img_bgr is None:
        raise FileNotFoundError(f"Không tìm thấy ảnh tại: {image_path}")

    if not os.path.exists(hand_img_path):
        from assets.generate_assets import create_hand_pen_asset
        create_hand_pen_asset(hand_img_path)

    hand_pil = Image.open(hand_img_path).convert("RGBA")
    hand_pil = hand_pil.resize((350, 350), Image.Resampling.LANCZOS)
    hand_rgba = np.array(hand_pil)
    hand_bgra = cv2.cvtColor(hand_rgba, cv2.COLOR_RGBA2BGRA)

    tip_x, tip_y = int(tip_offset[0] * (350 / 400)), int(tip_offset[1] * (350 / 400))

    w_canvas, h_canvas = canvas_size
    _, points_color, color_canvas, rect = extract_sketch_points_and_color(img_bgr, target_size=canvas_size)
    offset_x, offset_y, img_w, img_h = rect

    total_frames = max(1, int(audio_duration * fps))

    # Chia tỉ lệ 3 giai đoạn
    sketch_frames = int(total_frames * 0.45)
    color_frames = int(total_frames * 0.35)
    pause_frames = total_frames - sketch_frames - color_frames

    total_points = len(points_color)
    pts_per_frame = max(1, total_points // max(1, sketch_frames))

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(output_video_path, fourcc, fps, (w_canvas, h_canvas))

    # Canvas giấy trắng ban đầu
    sketch_canvas = np.ones((h_canvas, w_canvas, 3), dtype=np.uint8) * 255

    # Chuẩn bị phụ đề động từng cụm 3-5 từ theo thời gian thực
    timed_subtitles = split_into_timed_subtitles(narration, total_frames)

    # Đặt phụ đề ngay sát bên dưới tranh vẽ (cách chân tranh 55-65px), xóa bỏ khoảng trống mênh mông
    subtitle_pos_y = min(int(h_canvas * 0.82), offset_y + img_h + 65)

    def get_subtitle_at_frame(f_idx: int) -> str:
        if not timed_subtitles:
            return ""
        for start_f, end_f, chunk in timed_subtitles:
            if start_f <= f_idx < end_f:
                return chunk
        return timed_subtitles[-1][2]

    # ==========================================
    # GIAI ĐOẠN 1: BÀN TAY VẼ NÉT PHÁC THẢO (SKETCH)
    # ==========================================
    for f in range(sketch_frames):
        start_idx = f * pts_per_frame
        end_idx = min((f + 1) * pts_per_frame, total_points)

        for idx in range(start_idx, end_idx):
            pt, color = points_color[idx]
            cv2.circle(sketch_canvas, pt, 2, color, -1)

        frame = sketch_canvas.copy()

        if end_idx > 0 and end_idx < total_points:
            cur_tip, _ = points_color[end_idx - 1]
            hand_x = cur_tip[0] - tip_x
            hand_y = cur_tip[1] - tip_y
            frame = overlay_alpha_image(frame, hand_bgra, hand_x, hand_y)

        # Vẽ cụm phụ đề ngắn ngay dưới chân tranh
        sub_chunk = get_subtitle_at_frame(f)
        frame = draw_dynamic_subtitle(frame, sub_chunk, pos_y=subtitle_pos_y)

        writer.write(frame)

    # ==========================================
    # GIAI ĐOẠN 2: BÀN TAY TÔ MÀU NƯỚC (COLOR REVEAL)
    # ==========================================
    base_sketch_canvas = sketch_canvas.copy()

    for f in range(color_frames):
        alpha = (f + 1) / color_frames
        blended_art = cv2.addWeighted(color_canvas, alpha, base_sketch_canvas, 1.0 - alpha, 0)
        frame = blended_art.copy()

        time_ratio = f / color_frames
        brush_x = int(offset_x + img_w * 0.5 + (img_w * 0.35) * math.sin(time_ratio * math.pi * 5))
        brush_y = int(offset_y + img_h * (0.2 + 0.6 * time_ratio))

        hand_x = brush_x - tip_x
        hand_y = brush_y - tip_y
        frame = overlay_alpha_image(frame, hand_bgra, hand_x, hand_y)

        global_f = sketch_frames + f
        sub_chunk = get_subtitle_at_frame(global_f)
        frame = draw_dynamic_subtitle(frame, sub_chunk, pos_y=subtitle_pos_y)

        writer.write(frame)

    # ==========================================
    # GIAI ĐOẠN 3: BỨC TRANH MÀU HOÀN HẢO (PAUSE & ADMIRE)
    # ==========================================
    for f in range(pause_frames):
        frame = color_canvas.copy()
        global_f = sketch_frames + color_frames + f
        sub_chunk = get_subtitle_at_frame(global_f)
        frame = draw_dynamic_subtitle(frame, sub_chunk, pos_y=subtitle_pos_y)
        writer.write(frame)

    writer.release()
    print(f"[SketchAnimator] Video vẽ nét và tô màu đã render xong: {output_video_path} ({total_frames} frames, {audio_duration:.2f}s)")
    return output_video_path
