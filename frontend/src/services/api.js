/**
 * DrawStory AI - API Client Service
 */

const API_BASE_URL = "http://127.0.0.1:8000/api/v1";

export async function checkBackendHealth() {
  try {
    const res = await fetch("http://127.0.0.1:8000/");
    if (res.ok) {
      const data = await res.json();
      return { online: true, data };
    }
    return { online: false };
  } catch (error) {
    return { online: false, error: error.message };
  }
}

export async function getVoices() {
  const res = await fetch(`${API_BASE_URL}/audio/voices`);
  if (!res.ok) throw new Error("Không thể tải danh sách giọng đọc");
  return res.json();
}

export async function previewVoice(text, voiceId) {
  const res = await fetch(`${API_BASE_URL}/audio/preview`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text, voice_id: voiceId }),
  });
  if (!res.ok) throw new Error("Lỗi khi tạo audio nghe thử");
  return res.json();
}

export async function generateStory({ topic, scenesCount = 2, language = "vi", tone = "motivational", apiKey = null }) {
  const finalApiKey = apiKey || localStorage.getItem("gemini_api_key") || null;
  const res = await fetch(`${API_BASE_URL}/story/generate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      topic,
      scenes_count: scenesCount,
      language,
      tone,
      api_key: finalApiKey,
    }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || "Không thể sinh kịch bản");
  }
  return res.json();
}

export async function startVideoRender({ scenes, voiceId, projectId = null, title = null, enableHand = true, enableSubtitles = true }) {
  const res = await fetch(`${API_BASE_URL}/video/render`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      project_id: projectId,
      title: title,
      scenes: scenes.map((s) => ({
        scene_id: s.scene_id,
        narration: s.narration,
        image_prompt: s.image_prompt,
        image_url: s.image_url || null, // BẮT BUỘC TRUYỀN IMAGE_URL CỦA NGƯỜI DÙNG
      })),
      voice_id: voiceId,
      aspect_ratio: "9:16",
      enable_hand_drawing: enableHand,
      enable_subtitles: enableSubtitles,
    }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || "Lỗi khi bắt đầu render video");
  }
  return res.json();
}

export async function getTaskStatus(taskId) {
  const res = await fetch(`${API_BASE_URL}/video/status/${taskId}`);
  if (!res.ok) throw new Error("Không thể kiểm tra trạng thái tác vụ");
  return res.json();
}

// ---------------- PROJECTS & HISTORY ----------------
export async function getProjects() {
  const res = await fetch(`${API_BASE_URL}/projects`);
  if (!res.ok) throw new Error("Không thể tải danh sách dự án");
  return res.json();
}

export async function getProject(projectId) {
  const res = await fetch(`${API_BASE_URL}/projects/${projectId}`);
  if (!res.ok) throw new Error("Không thể tải chi tiết dự án");
  return res.json();
}

export async function saveProject(projectData) {
  const res = await fetch(`${API_BASE_URL}/projects/save`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(projectData),
  });
  if (!res.ok) throw new Error("Không thể lưu dự án");
  return res.json();
}

export async function deleteProject(projectId) {
  const res = await fetch(`${API_BASE_URL}/projects/${projectId}`, {
    method: "DELETE",
  });
  if (!res.ok) throw new Error("Không thể xóa dự án");
  return res.json();
}

// ---------------- UPLOAD IMAGE ----------------
export async function uploadCustomImage(file) {
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(`${API_BASE_URL}/upload/image`, {
    method: "POST",
    body: formData,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || "Không thể tải ảnh lên");
  }
  return res.json();
}
