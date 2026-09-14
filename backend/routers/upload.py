"""
Upload API Router
Tiếp nhận file ảnh tùy chỉnh từ người dùng cho từng phân cảnh.
"""

import os
import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException
from backend.config import settings

router = APIRouter(prefix="/upload", tags=["Upload Tài Nguyên"])

UPLOADS_DIR = os.path.join(settings.DATA_DIR, "uploads")
os.makedirs(UPLOADS_DIR, exist_ok=True)

ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}

@router.post("/image")
async def upload_custom_image(file: UploadFile = File(...)):
    """
    Tải ảnh từ máy tính lên để dùng làm ảnh vẽ cho một phân cảnh cụ thể.
    """
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Định dạng ảnh không hợp lệ. Chỉ chấp nhận: {', '.join(ALLOWED_EXTENSIONS)}"
        )

    unique_filename = f"user_img_{uuid.uuid4().hex[:10]}{ext}"
    saved_path = os.path.join(UPLOADS_DIR, unique_filename)

    try:
        content = await file.read()
        with open(saved_path, "wb") as f:
            f.write(content)

        # Trả về URL tĩnh để hiển thị trên web và truyền vào render
        return {
            "image_url": f"/static/uploads/{unique_filename}",
            "filename": unique_filename,
            "size_bytes": len(content)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi khi lưu ảnh: {str(e)}")
