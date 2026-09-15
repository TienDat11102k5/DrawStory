"""
DrawStory AI - Centralized Logging System
Ghi log đồng thời ra console và file xoay vòng (rotating log file) chuẩn UTF-8.
"""

import os
import sys
import logging
from logging.handlers import RotatingFileHandler
from backend.config import settings

# Đảm bảo console Windows hỗ trợ UTF-8 không bị lỗi charmap
if sys.platform == "win32":
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

def setup_logging():
    """Khởi tạo cấu hình logging toàn cục cho DrawStory AI."""
    os.makedirs(settings.LOGS_DIR, exist_ok=True)
    
    log_format = "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter(log_format, datefmt=date_format)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    # Tránh gắn handler trùng lặp khi reload
    if not any(isinstance(h, RotatingFileHandler) for h in root_logger.handlers):
        file_handler = RotatingFileHandler(
            settings.LOG_FILE,
            maxBytes=5 * 1024 * 1024,  # 5MB per file
            backupCount=3,
            encoding="utf-8"
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.INFO)
        root_logger.addHandler(file_handler)

    if not any(isinstance(h, logging.StreamHandler) and not isinstance(h, RotatingFileHandler) for h in root_logger.handlers):
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        console_handler.setLevel(logging.INFO)
        root_logger.addHandler(console_handler)

    # Điều hướng log của uvicorn và fastapi vào root logger chung
    for logger_name in ("uvicorn", "uvicorn.error", "uvicorn.access", "fastapi"):
        l = logging.getLogger(logger_name)
        l.handlers = []
        l.propagate = True

    return logging.getLogger("DrawStory")

logger = setup_logging()
