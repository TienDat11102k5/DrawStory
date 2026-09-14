"""
Video Rendering API Router
"""

from fastapi import APIRouter, HTTPException, status
from backend.schemas.task import VideoRenderRequest, TaskStatusResponse
from backend.services.task_manager import task_manager

router = APIRouter(prefix="/video", tags=["Xuất Video (Video Render)"])

@router.post("/render", status_code=status.HTTP_202_ACCEPTED)
async def start_render_video(req: VideoRenderRequest):
    """
    Tiếp nhận yêu cầu render video và đẩy vào hàng đợi xử lý ngầm (Non-blocking).
    Trả về mã task_id để client theo dõi tiến độ %.
    """
    if not req.scenes:
        raise HTTPException(status_code=400, detail="Danh sách phân cảnh không được rỗng.")

    task_id = task_manager.create_task(req)
    return {
        "task_id": task_id,
        "status": "QUEUED",
        "message": "Tác vụ tạo video đã được đưa vào hàng đợi thành công."
    }

@router.get("/status/{task_id}", response_model=TaskStatusResponse)
async def check_task_status(task_id: str):
    """
    Thăm dò trạng thái và tiến độ % của tác vụ render video theo task_id.
    """
    status_resp = task_manager.get_task_status(task_id)
    if not status_resp:
        raise HTTPException(status_code=404, detail=f"Không tìm thấy tác vụ với mã: {task_id}")
    return status_resp
