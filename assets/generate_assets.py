"""
Script khởi tạo tài nguyên đồ họa ban đầu:
- Ảnh bàn tay cầm bút có nền trong suốt (RGBA): assets/hand_pen.png
"""
import os
import sys
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
from PIL import Image, ImageDraw

def create_hand_pen_asset(output_path="assets/hand_pen.png", size=(400, 400)):
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    
    # Tạo canvas trong suốt
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Tọa độ đầu ngòi bút nằm ở góc trên-trái (ví dụ: x=20, y=20)
    # Thân bút vẽ chéo từ (20, 20) xuống (220, 220)
    # Bàn tay ôm quanh thân bút từ (160, 160) đến (350, 350)
    
    # 1. Vẽ ngòi bút kim loại
    draw.polygon([(20, 20), (35, 10), (10, 35)], fill=(80, 80, 80, 255))
    draw.polygon([(20, 20), (45, 15), (60, 60), (15, 45)], fill=(180, 180, 190, 255))
    # Đầu ngòi bi cực nhỏ
    draw.ellipse([(17, 17), (23, 23)], fill=(20, 20, 20, 255))
    
    # 2. Thân bút chì / bút máy (màu vàng gỗ hoặc xanh than)
    draw.polygon([(45, 15), (180, 150), (150, 180), (15, 45)], fill=(220, 170, 70, 255))
    # Đường chỉ sọc trên thân bút
    draw.line([(30, 30), (165, 165)], fill=(180, 130, 40, 255), width=3)
    
    # 3. Vẽ bàn tay (ngón cái, ngón trỏ, mu bàn tay) - màu da ấm
    skin_color = (245, 215, 190, 255)
    skin_shadow = (220, 185, 160, 255)
    skin_outline = (190, 150, 130, 255)
    
    # Ngón trỏ tì lên bút
    draw.ellipse([(90, 90), (190, 160)], fill=skin_color, outline=skin_outline, width=2)
    # Ngón cái kẹp đối diện
    draw.ellipse([(120, 120), (220, 210)], fill=skin_shadow, outline=skin_outline, width=2)
    # Mu bàn tay và cổ tay nghiêng xuống góc dưới phải
    draw.polygon([(150, 160), (280, 190), (380, 360), (240, 380), (140, 230)], fill=skin_color, outline=skin_outline, width=2)
    
    # Nếp gấp khớp ngón tay
    draw.arc([(120, 105), (150, 135)], start=30, end=150, fill=skin_outline, width=2)
    draw.arc([(150, 140), (180, 170)], start=30, end=150, fill=skin_outline, width=2)
    
    img.save(output_path, "PNG")
    print(f"[Assets] Đã tạo thành công ảnh bàn tay cầm bút tại: {output_path} (Ngòi bút tại x=20, y=20)")

if __name__ == "__main__":
    create_hand_pen_asset()
