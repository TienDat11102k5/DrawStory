"""
DrawStory AI - Project Manager Service
Quản lý và lưu trữ lịch sử các dự án (kịch bản, phân cảnh, video hoàn thành).
"""

import os
import json
import time
import uuid
from typing import List, Dict, Optional, Any
from backend.config import settings

PROJECTS_FILE = os.path.join(settings.DATA_DIR, "projects.json")

class ProjectManager:
    def __init__(self, storage_path: str = PROJECTS_FILE):
        self.storage_path = storage_path
        self._ensure_storage()

    def _ensure_storage(self):
        os.makedirs(os.path.dirname(os.path.abspath(self.storage_path)), exist_ok=True)
        if not os.path.exists(self.storage_path):
            with open(self.storage_path, "w", encoding="utf-8") as f:
                json.dump({}, f, ensure_ascii=False, indent=2)

    def _read_all(self) -> Dict[str, Any]:
        try:
            with open(self.storage_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}

    def _write_all(self, data: Dict[str, Any]):
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def get_all_projects(self) -> List[Dict[str, Any]]:
        """Lấy danh sách tất cả các dự án, sắp xếp theo thời gian mới nhất."""
        data = self._read_all()
        projects = list(data.values())
        projects.sort(key=lambda p: p.get("updated_at", p.get("created_at", 0)), reverse=True)
        return projects

    def get_project(self, project_id: str) -> Optional[Dict[str, Any]]:
        """Lấy thông tin chi tiết một dự án theo ID."""
        data = self._read_all()
        return data.get(project_id)

    def save_project(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Tạo mới hoặc cập nhật một dự án."""
        data = self._read_all()
        
        project_id = project_data.get("project_id") or f"proj_{uuid.uuid4().hex[:8]}"
        project_data["project_id"] = project_id
        
        now = time.time()
        if project_id in data:
            # Cập nhật
            data[project_id].update(project_data)
            data[project_id]["updated_at"] = now
        else:
            # Tạo mới
            project_data["created_at"] = now
            project_data["updated_at"] = now
            data[project_id] = project_data

        self._write_all(data)
        return data[project_id]

    def delete_project(self, project_id: str) -> bool:
        """Xóa một dự án khỏi danh sách."""
        data = self._read_all()
        if project_id in data:
            del data[project_id]
            self._write_all(data)
            return True
        return False

project_manager = ProjectManager()
