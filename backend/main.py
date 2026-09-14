"""
DrawStory AI - Main Application Server
"""

import sys
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.config import settings
from backend.routers import story, audio, video, projects, upload

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Hệ thống RESTful API tạo video ngắn phong cách vẽ tranh bảng trắng (Whiteboard Animation) bằng AI.",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 1. Cấu hình CORS mở để Frontend kết nối thuận tiện
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Phục vụ file tĩnh (Static Files)
UPLOADS_DIR = os.path.join(settings.DATA_DIR, "uploads")
os.makedirs(UPLOADS_DIR, exist_ok=True)

app.mount("/static/outputs", StaticFiles(directory=settings.OUTPUTS_DIR), name="outputs")
app.mount("/static/temp", StaticFiles(directory=settings.TEMP_DIR), name="temp")
app.mount("/static/uploads", StaticFiles(directory=UPLOADS_DIR), name="uploads")

# 3. Đăng ký các API Routers
API_PREFIX = "/api/v1"
app.include_router(story.router, prefix=API_PREFIX)
app.include_router(audio.router, prefix=API_PREFIX)
app.include_router(video.router, prefix=API_PREFIX)
app.include_router(projects.router, prefix=API_PREFIX)
app.include_router(upload.router, prefix=API_PREFIX)

@app.get("/", tags=["Hệ thống"])
async def root():
    return {
        "status": "ONLINE",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs_url": "/docs",
        "endpoints": {
            "story": f"{API_PREFIX}/story/generate",
            "voices": f"{API_PREFIX}/audio/voices",
            "preview_voice": f"{API_PREFIX}/audio/preview",
            "render_video": f"{API_PREFIX}/video/render",
            "video_status": f"{API_PREFIX}/video/status/{{task_id}}"
        }
    }

if __name__ == "__main__":
    uvicorn.run(
        "backend.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG
    )
