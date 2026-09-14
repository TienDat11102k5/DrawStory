"""
Projects API Router
Quản lý lịch sử các dự án (kịch bản, trạng thái video, chỉnh sửa lại).
"""

from typing import List, Dict, Any
from fastapi import APIRouter, HTTPException
from backend.services.project_manager import project_manager

router = APIRouter(prefix="/projects", tags=["Quản Lý Dự Án (Projects)"])

@router.get("")
async def list_projects():
    """Lấy danh sách tất cả các dự án đã tạo hoặc đã lưu."""
    return project_manager.get_all_projects()

@router.get("/{project_id}")
async def get_project_detail(project_id: str):
    """Lấy chi tiết một dự án để tiếp tục chỉnh sửa hoặc xem lại kịch bản."""
    proj = project_manager.get_project(project_id)
    if not proj:
        raise HTTPException(status_code=404, detail=f"Không tìm thấy dự án với mã: {project_id}")
    return proj

@router.post("/save")
async def save_project_data(project_data: Dict[str, Any]):
    """Lưu mới hoặc cập nhật một dự án kịch bản."""
    saved = project_manager.save_project(project_data)
    return {
        "success": True,
        "message": "Dự án đã được lưu thành công.",
        "project": saved
    }

@router.delete("/{project_id}")
async def delete_project_by_id(project_id: str):
    """Xóa một dự án khỏi danh sách."""
    deleted = project_manager.delete_project(project_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Dự án không tồn tại.")
    return {"success": True, "message": "Đã xóa dự án."}
