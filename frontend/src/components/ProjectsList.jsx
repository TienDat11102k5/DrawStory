import React, { useState, useEffect } from 'react';
import { FolderOpen, Film, Trash2, Clock, Play, ArrowRight, Sparkles, AlertCircle } from 'lucide-react';
import { getProjects, deleteProject } from '../services/api';

export default function ProjectsList({ onOpenProject, onStartNew }) {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedVideo, setSelectedVideo] = useState(null);

  const fetchProjectsList = async () => {
    try {
      setLoading(true);
      const data = await getProjects();
      setProjects(data || []);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProjectsList();
  }, []);

  const handleDelete = async (e, projectId) => {
    e.stopPropagation();
    if (!window.confirm("Bạn có chắc chắn muốn xóa dự án này?")) return;
    try {
      await deleteProject(projectId);
      setProjects(projects.filter(p => p.project_id !== projectId));
    } catch (err) {
      alert("Lỗi khi xóa: " + err.message);
    }
  };

  return (
    <div style={{ maxWidth: '1080px', margin: '0 auto' }}>
      {/* Header */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '32px' }}>
        <div>
          <h2 style={{ fontSize: '28px', fontWeight: 800 }}>
            Dự Án Đã Lưu <span className="gradient-title">({projects.length})</span>
          </h2>
          <p style={{ fontSize: '14px', color: '#94a3b8' }}>
            Xem lại lịch sử kịch bản, mở lại để chỉnh sửa hoặc tải lại video đã hoàn thành.
          </p>
        </div>

        <button
          type="button"
          className="btn-primary"
          onClick={onStartNew}
          style={{ padding: '12px 24px', fontSize: '14px' }}
        >
          <Sparkles size={16} /> Tạo Dự Án Mới
        </button>
      </div>

      {/* Loading */}
      {loading && (
        <div style={{ textAlign: 'center', padding: '60px', color: '#94a3b8' }}>
          Đang tải danh sách dự án...
        </div>
      )}

      {/* Empty State */}
      {!loading && projects.length === 0 && (
        <div className="glass-panel" style={{ textAlign: 'center', padding: '60px 20px' }}>
          <FolderOpen size={48} color="#6366f1" style={{ margin: '0 auto 16px auto', opacity: 0.8 }} />
          <h3 style={{ fontSize: '18px', fontWeight: 700, marginBottom: '8px' }}>Chưa có dự án nào được lưu</h3>
          <p style={{ fontSize: '14px', color: '#94a3b8', marginBottom: '24px', maxWidth: '400px', margin: '0 auto 24px auto' }}>
            Mỗi khi bạn bấm tạo kịch bản hoặc render video, dự án sẽ tự động được lưu lại tại đây để chỉnh sửa bất kỳ lúc nào.
          </p>
          <button type="button" className="btn-primary" onClick={onStartNew}>
            Bắt đầu tạo kịch bản đầu tiên
          </button>
        </div>
      )}

      {/* Grid of Projects */}
      {!loading && projects.length > 0 && (
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))',
          gap: '24px'
        }}>
          {projects.map((proj) => {
            const hasVideo = !!proj.video_url;
            const fullVideoUrl = proj.video_url?.startsWith('http') 
              ? proj.video_url 
              : proj.video_url ? `http://127.0.0.1:8000${proj.video_url}` : '';

            const dateStr = proj.updated_at 
              ? new Date(proj.updated_at * 1000).toLocaleDateString('vi-VN', { hour: '2-digit', minute: '2-digit', day: '2-digit', month: '2-digit', year: 'numeric' })
              : 'Gần đây';

            return (
              <div
                key={proj.project_id}
                className="glass-panel"
                style={{
                  padding: '24px',
                  display: 'flex',
                  flexDirection: 'column',
                  justifyContent: 'space-between',
                  transition: 'all 0.2s ease',
                  cursor: 'pointer'
                }}
                onClick={() => onOpenProject(proj)}
              >
                <div>
                  {/* Status & Scenes Badge */}
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '14px' }}>
                    <span style={{
                      fontSize: '11px',
                      fontWeight: 700,
                      padding: '4px 10px',
                      borderRadius: '6px',
                      background: hasVideo ? 'rgba(16, 185, 129, 0.15)' : 'rgba(245, 158, 11, 0.15)',
                      color: hasVideo ? '#34d399' : '#fbbf24',
                      border: `1px solid ${hasVideo ? 'rgba(16, 185, 129, 0.3)' : 'rgba(245, 158, 11, 0.3)'}`
                    }}>
                      {hasVideo ? '🎬 Đã có video' : '📝 Bản nháp'}
                    </span>

                    <span style={{ fontSize: '12px', color: '#64748b' }}>
                      {proj.scenes?.length || proj.scenes_count || 0} phân cảnh
                    </span>
                  </div>

                  {/* Title */}
                  <h3 style={{ fontSize: '17px', fontWeight: 700, marginBottom: '8px', color: '#f8fafc', lineHeight: 1.4 }}>
                    {proj.title || 'Dự án không tên'}
                  </h3>

                  {/* Date */}
                  <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '12px', color: '#94a3b8', marginBottom: '16px' }}>
                    <Clock size={13} />
                    <span>{dateStr}</span>
                  </div>
                </div>

                {/* Bottom Actions */}
                <div style={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  paddingTop: '16px',
                  borderTop: '1px solid rgba(255, 255, 255, 0.06)'
                }}>
                  <div style={{ display: 'flex', gap: '8px' }}>
                    <button
                      type="button"
                      className="btn-primary"
                      onClick={(e) => {
                        e.stopPropagation();
                        onOpenProject(proj);
                      }}
                      style={{ padding: '8px 14px', fontSize: '12px' }}
                    >
                      Mở chỉnh sửa <ArrowRight size={13} />
                    </button>

                    {hasVideo && (
                      <button
                        type="button"
                        className="btn-secondary"
                        onClick={(e) => {
                          e.stopPropagation();
                          setSelectedVideo(fullVideoUrl);
                        }}
                        style={{ padding: '8px 12px', fontSize: '12px' }}
                        title="Xem video đã render"
                      >
                        <Play size={14} color="#818cf8" />
                      </button>
                    )}
                  </div>

                  <button
                    type="button"
                    onClick={(e) => handleDelete(e, proj.project_id)}
                    style={{
                      background: 'transparent',
                      border: 'none',
                      color: '#64748b',
                      cursor: 'pointer',
                      padding: '6px'
                    }}
                    title="Xóa dự án"
                  >
                    <Trash2 size={16} />
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* Modal Xem Nhanh Video */}
      {selectedVideo && (
        <div style={{
          position: 'fixed',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: 'rgba(0, 0, 0, 0.85)',
          backdropFilter: 'blur(8px)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          zIndex: 100
        }}>
          <div style={{ position: 'relative', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
            <button
              type="button"
              onClick={() => setSelectedVideo(null)}
              style={{
                position: 'absolute',
                top: '-40px',
                right: '0',
                background: 'transparent',
                border: 'none',
                color: '#fff',
                fontSize: '24px',
                cursor: 'pointer'
              }}
            >
              ✕ Đóng
            </button>
            <div className="shorts-frame">
              <video src={selectedVideo} controls autoPlay style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
