import React, { useEffect } from 'react';
import { Download, RefreshCw, CheckCircle2, AlertCircle, Sparkles, Share2, Film, Check, ExternalLink } from 'lucide-react';
import confetti from 'canvas-confetti';

export default function Step3_RenderPlayer({
  taskStatus,
  videoUrl,
  videoTitle,
  onReset
}) {
  const isCompleted = taskStatus?.status === 'COMPLETED';
  const isFailed = taskStatus?.status === 'FAILED';
  const progress = taskStatus?.progress_percentage || 0;
  const currentStep = taskStatus?.current_step || 'Đang chuẩn bị...';

  useEffect(() => {
    if (isCompleted) {
      confetti({
        particleCount: 100,
        spread: 80,
        origin: { y: 0.6 }
      });
    }
  }, [isCompleted]);

  const fullVideoUrl = videoUrl?.startsWith('http') 
    ? videoUrl 
    : videoUrl ? `http://127.0.0.1:8000${videoUrl}` : '';

  const downloadName = videoUrl 
    ? videoUrl.split('/').pop().split('?')[0]
    : 'drawstory_video.mp4';

  return (
    <div style={{ width: '100%', maxWidth: '100%', boxSizing: 'border-box' }}>
      {/* Top Header */}
      <div style={{ textAlign: 'center', marginBottom: '32px' }}>
        <div style={{
          display: 'inline-flex',
          alignItems: 'center',
          gap: '8px',
          padding: '6px 16px',
          borderRadius: '999px',
          background: isCompleted ? 'rgba(16, 185, 129, 0.15)' : 'rgba(99, 102, 241, 0.15)',
          border: `1px solid ${isCompleted ? '#10b981' : '#818cf8'}`,
          marginBottom: '14px'
        }}>
          {isCompleted ? <CheckCircle2 size={16} color="#10b981" /> : <Sparkles size={16} color="#818cf8" />}
          <span style={{ fontSize: '13px', fontWeight: 700, color: isCompleted ? '#34d399' : '#c7d2fe' }}>
            {isCompleted ? 'Sản Xuất Video Hoàn Thành!' : 'Đang Tự Động Vẽ & Render Video...'}
          </span>
        </div>

        <h2 style={{ fontSize: '32px', fontWeight: 800, marginBottom: '8px' }}>
          {isCompleted ? (
            <>Tác phẩm của bạn đã <span className="gradient-title">Sẵn Sàng Xuất Bản!</span></>
          ) : (
            <>Hệ thống đang <span className="gradient-title">vẽ nét bút & tô màu nước</span></>
          )}
        </h2>
        <p style={{ fontSize: '15px', color: '#94a3b8' }}>
          {isCompleted 
            ? 'Video ngắn chuẩn kích thước dọc 9:16 sắc nét, tối ưu cho TikTok, YouTube Shorts và Facebook Reels.'
            : 'Tiến trình render đang chạy ngầm trên máy chủ bằng OpenCV & MoviePy, vui lòng đợi trong giây lát...'}
        </p>
      </div>

      {/* Progress Bar khi đang chạy */}
      {!isCompleted && !isFailed && (
        <div className="glass-panel-glow" style={{ padding: '36px', maxWidth: '880px', margin: '0 auto', textAlign: 'left' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '14px' }}>
            <span style={{ fontSize: '16px', fontWeight: 600, color: '#f8fafc', display: 'flex', alignItems: 'center', gap: '8px' }}>
              <span style={{
                width: '10px',
                height: '10px',
                borderRadius: '50%',
                background: '#818cf8',
                display: 'inline-block',
                animation: 'pulse 1.5s infinite'
              }}></span>
              {currentStep}
            </span>
            <span style={{ fontSize: '18px', fontWeight: 800, color: '#818cf8' }}>{progress}%</span>
          </div>

          <div style={{
            width: '100%',
            height: '12px',
            borderRadius: '999px',
            background: 'rgba(255, 255, 255, 0.08)',
            overflow: 'hidden',
            marginBottom: '24px'
          }}>
            <div
              className="progress-bar-glow"
              style={{
                width: `${progress}%`,
                height: '100%',
                borderRadius: '999px',
                transition: 'width 0.4s ease'
              }}
            ></div>
          </div>

          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(3, 1fr)',
            gap: '16px',
            paddingTop: '16px',
            borderTop: '1px solid rgba(255, 255, 255, 0.06)'
          }}>
            <div style={{ textAlign: 'center' }}>
              <span style={{ fontSize: '11px', color: '#64748b', display: 'block', fontWeight: 700 }}>ĐỘ PHÂN GIẢI</span>
              <span style={{ fontSize: '13px', color: '#cbd5e1', fontWeight: 600 }}>1080 x 1920 (9:16)</span>
            </div>
            <div style={{ textAlign: 'center' }}>
              <span style={{ fontSize: '11px', color: '#64748b', display: 'block', fontWeight: 700 }}>TỐC ĐỘ KHUNG HÌNH</span>
              <span style={{ fontSize: '13px', color: '#cbd5e1', fontWeight: 600 }}>30 FPS (Mượt mà)</span>
            </div>
            <div style={{ textAlign: 'center' }}>
              <span style={{ fontSize: '11px', color: '#64748b', display: 'block', fontWeight: 700 }}>HIỆU ỨNG ĐỒ HỌA</span>
              <span style={{ fontSize: '13px', color: '#cbd5e1', fontWeight: 600 }}>Sketch & Watercolor</span>
            </div>
          </div>
        </div>
      )}

      {/* Error View */}
      {isFailed && (
        <div className="glass-panel" style={{ padding: '32px', maxWidth: '720px', margin: '0 auto', borderColor: '#ef4444', textAlign: 'center' }}>
          <AlertCircle size={40} color="#ef4444" style={{ margin: '0 auto 14px auto' }} />
          <h3 style={{ fontSize: '18px', fontWeight: 700, color: '#f87171', marginBottom: '8px' }}>Đã xảy ra lỗi khi render</h3>
          <p style={{ fontSize: '14px', color: '#94a3b8', marginBottom: '20px' }}>{taskStatus?.error_message || 'Vui lòng kiểm tra lại kết nối máy chủ.'}</p>
          <button type="button" className="btn-secondary" onClick={onReset}>Quay lại chỉnh sửa</button>
        </div>
      )}

      {/* Video Thành Phẩm: Bố Cục Widescreen 2 Cột */}
      {isCompleted && fullVideoUrl && (
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'minmax(320px, 380px) minmax(0, 1fr)',
          gap: '40px',
          maxWidth: '1100px',
          margin: '0 auto',
          alignItems: 'center'
        }}>
          {/* CỘT TRÁI: KHUNG ĐIỆN THOẠI SHORTS PLAYER */}
          <div style={{ display: 'flex', justifyContent: 'center' }}>
            <div className="shorts-frame" style={{ width: '340px', height: '604px' }}>
              <video
                src={fullVideoUrl}
                controls
                autoPlay
                loop
                playsInline
                style={{
                  width: '100%',
                  height: '100%',
                  objectFit: 'cover'
                }}
              />
            </div>
          </div>

          {/* CỘT PHẢI: BẢNG ĐIỀU KHIỂN & XUẤT XƯỞNG */}
          <div className="glass-panel-glow" style={{ padding: '36px', display: 'flex', flexDirection: 'column', gap: '24px' }}>
            <div>
              <span style={{ fontSize: '12px', color: '#34d399', fontWeight: 700, display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '8px' }}>
                <CheckCircle2 size={16} /> XUẤT XƯỞNG THÀNH CÔNG
              </span>
              <h3 style={{ fontSize: '24px', fontWeight: 800, marginBottom: '8px' }}>Video ngắn đã sẵn sàng</h3>
              <p style={{ fontSize: '14px', color: '#94a3b8', lineHeight: 1.6 }}>
                File MP4 chuẩn codec H.264 và âm thanh AAC chất lượng cao đã được tối ưu hóa dung lượng để đăng tải ngay lên TikTok, Shorts hoặc Reels mà không bị giảm chất lượng.
              </p>
            </div>

            {/* Thông số kỹ thuật */}
            <div style={{
              display: 'grid',
              gridTemplateColumns: '1fr 1fr',
              gap: '12px',
              background: 'rgba(255, 255, 255, 0.03)',
              padding: '16px',
              borderRadius: '12px',
              border: '1px solid rgba(255, 255, 255, 0.06)'
            }}>
              <div>
                <span style={{ fontSize: '11px', color: '#64748b', display: 'block', fontWeight: 600 }}>TÊN FILE XUẤT</span>
                <span style={{ fontSize: '13px', fontWeight: 700, color: '#38bdf8', wordBreak: 'break-all' }}>
                  {downloadName}
                </span>
              </div>
              <div>
                <span style={{ fontSize: '11px', color: '#64748b', display: 'block', fontWeight: 600 }}>TỔNG THỜI LƯỢNG</span>
                <span style={{ fontSize: '14px', fontWeight: 700, color: '#f8fafc' }}>
                  {taskStatus?.result?.duration_seconds ? `${taskStatus.result.duration_seconds}s` : 'Chuẩn Shorts'}
                </span>
              </div>
              <div>
                <span style={{ fontSize: '11px', color: '#64748b', display: 'block', fontWeight: 600 }}>ĐỊNH DẠNG</span>
                <span style={{ fontSize: '14px', fontWeight: 700, color: '#f8fafc' }}>MP4 (9:16 Dọc)</span>
              </div>
              <div>
                <span style={{ fontSize: '11px', color: '#64748b', display: 'block', fontWeight: 600 }}>DUNG LƯỢNG FILE</span>
                <span style={{ fontSize: '14px', fontWeight: 700, color: '#f8fafc' }}>
                  {taskStatus?.result?.file_size_bytes ? `${(taskStatus.result.file_size_bytes / 1024 / 1024).toFixed(1)} MB` : '~2 MB'}
                </span>
              </div>
            </div>

            {/* Action Buttons */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
              <a
                href={fullVideoUrl}
                download={downloadName}
                className="btn-primary"
                style={{ textDecoration: 'none', padding: '16px', fontSize: '16px', textAlign: 'center' }}
              >
                <Download size={18} />
                Tải Video MP4 Về Máy Tính
              </a>

              <div style={{ display: 'flex', gap: '12px' }}>
                <a
                  href={fullVideoUrl}
                  target="_blank"
                  rel="noreferrer"
                  className="btn-secondary"
                  style={{ flex: 1, textDecoration: 'none', justifyContent: 'center', padding: '12px', fontSize: '14px' }}
                >
                  <ExternalLink size={15} /> Mở tab mới
                </a>

                <button
                  type="button"
                  className="btn-secondary"
                  onClick={onReset}
                  style={{ flex: 1, justifyContent: 'center', padding: '12px', fontSize: '14px' }}
                >
                  <RefreshCw size={15} /> Làm video mới
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
