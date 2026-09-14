"""
DrawStory AI - Image Engine
Module tạo ảnh phác thảo nét chì (Line art / Minimalist Sketch) bằng AI Image API.
Mặc định sử dụng Pollinations AI (miễn phí, nhanh, không yêu cầu API key).
"""

import os
import sys
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
import urllib.parse
import requests
from PIL import Image, ImageDraw

def enhance_sketch_prompt(base_prompt: str) -> str:
    """
    Bổ sung các từ khóa để mô hình AI luôn luôn tạo ra bức tranh khổ dọc 9:16,
    màu sắc rực rỡ, đường viền nét vẽ rõ ràng trên nền sáng để tối ưu cho video ngắn Shorts/Reels.
    """
    prompt_clean = (base_prompt or "").strip()
    
    # Đảm bảo phần đầu có chỉ thị khung dọc 9:16
    if "vertical" not in prompt_clean.lower() and "9:16" not in prompt_clean.lower():
        prompt_clean = f"Vertical 9:16 portrait composition, {prompt_clean}"
        
    style_modifiers = (
        "vibrant storybook illustration, clear ink outlines, rich watercolor coloring, "
        "lively vibrant colors, clean light background, beautiful artistic texture, "
        "high aesthetic, digital art, vertical orientation, full vertical view, 9:16 aspect ratio --ar 9:16"
    )
    return f"{prompt_clean}, {style_modifiers}"

def generate_sketch_image(
    prompt: str,
    output_path: str,
    width: int = 720,
    height: int = 1280,
    seed: int = 42
) -> str:
    """
    Gọi API để sinh ảnh nét vẽ khổ dọc 9:16 (mặc định 720x1280) và lưu về đĩa.
    """
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    enhanced_prompt = enhance_sketch_prompt(prompt)
    encoded_prompt = urllib.parse.quote(enhanced_prompt)
    
    # URL gọi Pollinations AI với tỉ lệ 9:16
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}&nologo=true&seed={seed}&model=flux"
    
    print(f"[ImageEngine] Đang sinh ảnh dọc 9:16 ({width}x{height}): '{prompt}'...")
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            with open(output_path, "wb") as f:
                f.write(response.content)
            print(f"[ImageEngine] Đã tải ảnh thành công về: {output_path}")
            return output_path
        else:
            print(f"[ImageEngine] Lỗi HTTP {response.status_code}, chuyển sang chế độ tạo ảnh phác thảo dự phòng.")
            return generate_fallback_sketch(prompt, output_path, width, height)
    except Exception as e:
        print(f"[ImageEngine] Lỗi kết nối API ({e}), chuyển sang chế độ tạo ảnh phác thảo dự phòng.")
        return generate_fallback_sketch(prompt, output_path, width, height)

def generate_fallback_sketch(prompt: str, output_path: str, width: int = 720, height: int = 1280) -> str:
    """
    Tạo ảnh minh họa màu sắc rực rỡ khổ dọc 9:16 nếu không có kết nối mạng (dự phòng).
    """
    img = Image.new("RGB", (width, height), (250, 252, 255))
    draw = ImageDraw.Draw(img)
    
    center_x = width // 2
    center_y = int(height * 0.44)
    
    # 1. Vẽ vầng hào quang màu vàng cam rực rỡ phía sau
    draw.ellipse([(center_x - 180, center_y - 240), (center_x + 180, center_y + 120)], fill=(255, 245, 180), outline=(255, 210, 80), width=4)
    # Bóng đèn ý tưởng màu vàng chanh sáng
    draw.arc([(center_x - 100, center_y - 160), (center_x + 100, center_y)], start=180, end=0, fill=(255, 160, 0), width=6)
    draw.polygon([(center_x - 35, center_y), (center_x + 35, center_y), (center_x + 20, center_y + 40), (center_x - 20, center_y + 40)], fill=(200, 200, 210), outline=(50, 50, 60), width=4)
    
    # 2. Cuốn sách màu xanh ngọc bích nổi bật
    draw.polygon([(center_x, center_y + 130), (center_x - 180, center_y + 90), (center_x - 180, center_y + 200), (center_x, center_y + 240)], fill=(60, 180, 220), outline=(20, 80, 120), width=5)
    draw.polygon([(center_x, center_y + 130), (center_x + 180, center_y + 90), (center_x + 180, center_y + 200), (center_x, center_y + 240)], fill=(80, 200, 240), outline=(20, 80, 120), width=5)
    
    # Các trang sách màu trắng kem bên trong
    draw.polygon([(center_x, center_y + 120), (center_x - 160, center_y + 85), (center_x - 160, center_y + 185), (center_x, center_y + 225)], fill=(255, 255, 240), outline=(100, 150, 180), width=3)
    draw.polygon([(center_x, center_y + 120), (center_x + 160, center_y + 85), (center_x + 160, center_y + 185), (center_x, center_y + 225)], fill=(255, 255, 240), outline=(100, 150, 180), width=3)

    img.save(output_path, "PNG")
    print(f"[ImageEngine] Đã tạo ảnh minh họa màu sắc rực rỡ dự phòng 9:16 tại: {output_path}")
    return output_path

if __name__ == "__main__":
    generate_sketch_image("A cute little turtle reading a book under a tree", "data/temp/test_image.png")
