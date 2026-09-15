import React, { useState } from 'react';
import { Sparkles, Volume2, Wand2, CheckCircle2, Play, Layers, Palette, Clock, Video, Minus, Plus } from 'lucide-react';
import { previewVoice } from '../services/api';

const SAMPLE_TOPICS = [
  "Sức mạnh của việc đọc sách 15 phút mỗi ngày",
  "Bài học về sự kiên trì từ câu chuyện Rùa và Thỏ",
  "Thế giới kỳ thú dưới lòng đại dương sâu thẳm",
  "Tại sao kỷ luật lại quan trọng hơn động lực?",
  "Bí quyết quản lý thời gian của những người thành công",
  "Nghệ thuật giao tiếp: Lắng nghe nhiều hơn nói"
];

export default function Step1_IdeaInput({
  topic,
  setTopic,
  scenesCount,
  setScenesCount,
  selectedVoice,
  setSelectedVoice,
  voiceRate = 1.0,
  setVoiceRate,
  voices,
  onGenerateStory,
  isLoading
}) {
  const [playingVoice, setPlayingVoice] = useState(false);
  const [audioEl, setAudioEl] = useState(null);

  const handlePreviewVoice = async (voiceId) => {
    try {
      setPlayingVoice(true);
      const res = await previewVoice("Xin chào! Đây là giọng đọc thuyết minh mẫu cho video của bạn.", voiceId, voiceRate);
      if (res.audio_url) {
        if (audioEl) audioEl.pause();
        const fullUrl = res.audio_url.startsWith("http") ? res.audio_url : `http://127.0.0.1:8000${res.audio_url}`;
        const newAudio = new Audio(fullUrl);
        setAudioEl(newAudio);
        newAudio.play();
        newAudio.onended = () => setPlayingVoice(false);
      }
    } catch (e) {
      console.error(e);
      alert("Không thể phát thử giọng đọc: " + e.message);
      setPlayingVoice(false);
    }
  };

  return (
    <div style={{
      display: 'grid',
      gridTemplateColumns: 'minmax(0, 1.4fr) minmax(0, 1fr)',
      gap: '28px',
      width: '100%',
      alignItems: 'start'
    }}>
      {/* CỘT TRÁI: FORM NHẬP Ý TƯỞNG & CẤU HÌNH */}
      <div className="glass-panel-glow" style={{ padding: '36px', display: 'flex', flexDirection: 'column', gap: '24px' }}>
        {/* Header Header */}
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', flexWrap: 'wrap', marginBottom: '12px' }}>
            <div style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: '8px',
              padding: '6px 14px',
              borderRadius: '999px',
              background: 'rgba(99, 102, 241, 0.12)',
              border: '1px solid rgba(99, 102, 241, 0.3)'
            }}>
              <Sparkles size={15} color="#818cf8" />
              <span style={{ fontSize: '13px', fontWeight: 600, color: '#c7d2fe' }}>
                Bước 1: Khởi Tạo Ý Tưởng & Kịch Bản
              </span>
            </div>

            {localStorage.getItem('gemini_api_key') ? (
              <div style={{
                display: 'inline-flex',
                alignItems: 'center',
                gap: '6px',
                padding: '6px 12px',
                borderRadius: '999px',
                background: 'rgba(16, 185, 129, 0.1)',
                border: '1px solid rgba(16, 185, 129, 0.3)',
                fontSize: '12px',
                color: '#34d399',
                fontWeight: 600
              }}>
                <CheckCircle2 size={13} color="#10b981" /> Đã kết nối Google Gemini
              </div>
            ) : (
              <div style={{
                display: 'inline-flex',
                alignItems: 'center',
                gap: '6px',
                padding: '6px 12px',
                borderRadius: '999px',
                background: 'rgba(255, 255, 255, 0.04)',
                border: '1px solid rgba(255, 255, 255, 0.1)',
                fontSize: '12px',
                color: '#94a3b8'
              }}>
                💡 Nhấn "Cài Gemini Key" góc trên để AI đạo diễn kịch bản đỉnh cao
              </div>
            )}
          </div>
          <h2 style={{ fontSize: '28px', fontWeight: 800, marginBottom: '6px' }}>
            Bạn muốn kể <span className="gradient-title">câu chuyện gì hôm nay?</span>
          </h2>
          <p style={{ fontSize: '14px', color: '#94a3b8' }}>
            Nhập ý tưởng ngắn, hệ thống AI sẽ tự động phân cảnh, viết câu thoại, tạo tranh vẽ và giọng đọc.
          </p>
        </div>

        {/* Input Topic */}
        <div>
          <label style={{ display: 'block', fontSize: '14px', fontWeight: 600, marginBottom: '8px', color: '#e2e8f0' }}>
            Chủ đề hoặc ý tưởng video của bạn:
          </label>
          <textarea
            rows={4}
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
            placeholder="Ví dụ: Tại sao người kỷ luật luôn đạt được mục tiêu dễ dàng hơn người chỉ dựa vào động lực..."
            style={{
              width: '100%',
              padding: '16px',
              borderRadius: '14px',
              background: 'rgba(9, 13, 22, 0.7)',
              border: '1px solid rgba(255, 255, 255, 0.12)',
              color: '#fff',
              fontSize: '15px',
              lineHeight: 1.5,
              resize: 'vertical',
              outline: 'none',
              fontFamily: 'inherit',
              transition: 'border 0.2s ease'
            }}
            onFocus={(e) => e.target.style.borderColor = '#6366f1'}
            onBlur={(e) => e.target.style.borderColor = 'rgba(255, 255, 255, 0.12)'}
          />

          {/* Quick Topics */}
          <div style={{ marginTop: '12px' }}>
            <span style={{ fontSize: '12px', color: '#64748b', display: 'block', marginBottom: '8px', fontWeight: 600 }}>
              GỢI Ý CHỦ ĐỀ NHANH:
            </span>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
              {SAMPLE_TOPICS.map((sample, idx) => (
                <button
                  key={idx}
                  type="button"
                  onClick={() => setTopic(sample)}
                  style={{
                    fontSize: '12px',
                    padding: '6px 12px',
                    borderRadius: '8px',
                    background: topic === sample ? 'rgba(99, 102, 241, 0.25)' : 'rgba(255, 255, 255, 0.04)',
                    border: topic === sample ? '1px solid #818cf8' : '1px solid rgba(255, 255, 255, 0.08)',
                    color: topic === sample ? '#fff' : '#cbd5e1',
                    cursor: 'pointer',
                    transition: 'all 0.15s ease'
                  }}
                >
                  {sample}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Giọng đọc thuyết minh */}
        <div>
          <label style={{ display: 'block', fontSize: '14px', fontWeight: 600, marginBottom: '8px', color: '#e2e8f0' }}>
            Giọng đọc thuyết minh:
          </label>
          <div style={{ display: 'flex', gap: '8px' }}>
            <select
              value={selectedVoice}
              onChange={(e) => setSelectedVoice(e.target.value)}
              style={{
                flex: 1,
                height: '46px',
                padding: '0 14px',
                borderRadius: '12px',
                background: 'rgba(9, 13, 22, 0.7)',
                border: '1px solid rgba(255, 255, 255, 0.12)',
                color: '#fff',
                fontSize: '14px',
                outline: 'none',
                cursor: 'pointer'
              }}
            >
              {voices.map((v) => (
                <option key={v.voice_id} value={v.voice_id} style={{ background: '#111827', color: '#fff' }}>
                  {v.name}
                </option>
              ))}
            </select>
            <button
              type="button"
              onClick={() => handlePreviewVoice(selectedVoice)}
              disabled={playingVoice}
              title="Nghe thử giọng đọc"
              className="btn-secondary"
              style={{ width: '46px', height: '46px', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: 0 }}
            >
              <Volume2 size={18} color="#818cf8" />
            </button>
          </div>
        </div>

        {/* Hàng chung: Số phân cảnh & Tốc độ đọc */}
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1.35fr', gap: '16px' }}>
          {/* Số phân cảnh */}
          <div>
            <label style={{ display: 'block', fontSize: '14px', fontWeight: 600, marginBottom: '8px', color: '#e2e8f0' }}>
              Số phân cảnh:
            </label>
            <div style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              height: '46px',
              background: 'rgba(9, 13, 22, 0.7)',
              border: '1px solid rgba(255, 255, 255, 0.12)',
              borderRadius: '12px',
              padding: '4px'
            }}>
              <button
                type="button"
                onClick={() => setScenesCount(Math.max(1, scenesCount - 1))}
                disabled={scenesCount <= 1}
                title="Giảm 1 cảnh"
                style={{
                  width: '38px',
                  height: '38px',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  borderRadius: '8px',
                  background: 'rgba(255, 255, 255, 0.06)',
                  border: 'none',
                  color: scenesCount <= 1 ? '#64748b' : '#fff',
                  cursor: scenesCount <= 1 ? 'not-allowed' : 'pointer'
                }}
              >
                <Minus size={16} />
              </button>
              
              <div style={{ flex: 1, textAlign: 'center' }}>
                <span style={{ fontSize: '15px', fontWeight: 700, color: '#818cf8' }}>
                  {scenesCount}
                </span>
                <span style={{ fontSize: '13px', color: '#94a3b8', marginLeft: '5px' }}>
                  cảnh
                </span>
              </div>

              <button
                type="button"
                onClick={() => setScenesCount(Math.min(10, scenesCount + 1))}
                disabled={scenesCount >= 10}
                title="Tăng 1 cảnh"
                style={{
                  width: '38px',
                  height: '38px',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  borderRadius: '8px',
                  background: 'rgba(255, 255, 255, 0.06)',
                  border: 'none',
                  color: scenesCount >= 10 ? '#64748b' : '#fff',
                  cursor: scenesCount >= 10 ? 'not-allowed' : 'pointer'
                }}
              >
                <Plus size={16} />
              </button>
            </div>
          </div>

          {/* Tốc độ đọc */}
          <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
              <label style={{ fontSize: '14px', fontWeight: 600, color: '#e2e8f0' }}>
                Tốc độ đọc:
              </label>
              <span style={{
                fontSize: '12px',
                fontWeight: 700,
                color: '#818cf8',
                background: 'rgba(99, 102, 241, 0.15)',
                padding: '1px 7px',
                borderRadius: '6px',
                border: '1px solid rgba(99, 102, 241, 0.3)'
              }}>
                {voiceRate}x
              </span>
            </div>

            <div style={{
              display: 'flex',
              alignItems: 'center',
              gap: '10px',
              height: '46px',
              background: 'rgba(9, 13, 22, 0.7)',
              border: '1px solid rgba(255, 255, 255, 0.12)',
              borderRadius: '12px',
              padding: '0 12px'
            }}>
              <input
                type="range"
                min="0.25"
                max="2.0"
                step="0.05"
                value={voiceRate}
                onChange={(e) => setVoiceRate(parseFloat(e.target.value))}
                style={{ flex: 1, accentColor: '#6366f1', cursor: 'pointer', height: '5px' }}
              />
              <div style={{ display: 'flex', gap: '4px' }}>
                {[0.75, 1.0, 1.25, 1.5].map((spd) => (
                  <button
                    key={spd}
                    type="button"
                    onClick={() => setVoiceRate(spd)}
                    style={{
                      padding: '3px 7px',
                      borderRadius: '6px',
                      fontSize: '11px',
                      fontWeight: voiceRate === spd ? 700 : 500,
                      background: voiceRate === spd ? '#6366f1' : 'rgba(255, 255, 255, 0.06)',
                      color: '#fff',
                      border: 'none',
                      cursor: 'pointer'
                    }}
                  >
                    {spd}x
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Submit Button */}
        <button
          type="button"
          className="btn-primary"
          onClick={onGenerateStory}
          disabled={isLoading || !topic.trim()}
          style={{ padding: '16px', fontSize: '16px', marginTop: '8px' }}
        >
          {isLoading ? (
            <>
              <span style={{
                width: '18px',
                height: '18px',
                border: '2px solid #fff',
                borderTopColor: 'transparent',
                borderRadius: '50%',
                display: 'inline-block',
                animation: 'spin 1s linear infinite'
              }}></span>
              AI đang phân tích & lên kịch bản...
            </>
          ) : (
            <>
              <Wand2 size={20} />
              Tạo Kịch Bản Phân Cảnh Bằng AI
            </>
          )}
        </button>
      </div>

      {/* CỘT PHẢI: SHOWCASE & TÍNH NĂNG NỔI BẬT */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
        {/* Banner Preview Phong cách Đồ Họa */}
        <div className="glass-panel" style={{ padding: '24px', borderLeft: '4px solid #a855f7' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '14px' }}>
            <div style={{
              width: '36px',
              height: '36px',
              borderRadius: '10px',
              background: 'linear-gradient(135deg, #a855f7, #ec4899)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center'
            }}>
              <Palette size={18} color="#fff" />
            </div>
            <div>
              <h3 style={{ fontSize: '16px', fontWeight: 700 }}>Phong Cách Bút Vẽ & Màu Nước</h3>
              <p style={{ fontSize: '12px', color: '#94a3b8' }}>Whiteboard Sketch & Watercolor Reveal</p>
            </div>
          </div>
          <p style={{ fontSize: '13px', color: '#cbd5e1', lineHeight: 1.6, marginBottom: '16px' }}>
            Video được dựng tự động với hiệu ứng bàn tay cầm bút vẽ từng nét viền phác thảo, sau đó quét cọ lan tỏa màu nước sống động, khớp hoàn hảo với nhịp giọng đọc.
          </p>

          <div style={{
            display: 'grid',
            gridTemplateColumns: '1fr 1fr',
            gap: '12px'
          }}>
            <div style={{
              background: 'rgba(255, 255, 255, 0.03)',
              padding: '12px',
              borderRadius: '10px',
              border: '1px solid rgba(255, 255, 255, 0.06)'
            }}>
              <span style={{ fontSize: '11px', color: '#818cf8', fontWeight: 700, display: 'block', marginBottom: '4px' }}>
                ✍️ NÉT VẼ PHÁC THẢO
              </span>
              <span style={{ fontSize: '12px', color: '#94a3b8' }}>
                Bút vẽ đường viền chi tiết sắc sảo
              </span>
            </div>

            <div style={{
              background: 'rgba(255, 255, 255, 0.03)',
              padding: '12px',
              borderRadius: '10px',
              border: '1px solid rgba(255, 255, 255, 0.06)'
            }}>
              <span style={{ fontSize: '11px', color: '#f59e0b', fontWeight: 700, display: 'block', marginBottom: '4px' }}>
                🎨 TÔ MÀU NƯỚC RỰC RỠ
              </span>
              <span style={{ fontSize: '12px', color: '#94a3b8' }}>
                Màu sắc lan tỏa lấp đầy bức tranh
              </span>
            </div>
          </div>
        </div>

        {/* Quy trình sản xuất tự động */}
        <div className="glass-panel" style={{ padding: '24px' }}>
          <h4 style={{ fontSize: '14px', fontWeight: 700, marginBottom: '14px', color: '#e2e8f0', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Layers size={16} color="#6366f1" /> Quy trình 100% tự động
          </h4>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            {[
              { step: '1', title: 'Phân tích kịch bản', desc: 'LLM tạo kịch bản phân cảnh xúc tích' },
              { step: '2', title: 'Lồng tiếng cảm xúc', desc: 'Giọng đọc Microsoft Neural chuẩn tiếng Việt' },
              { step: '3', title: 'Vẽ tranh & Tô màu', desc: 'Thuật toán Computer Vision mô phỏng bàn tay' },
              { step: '4', title: 'Xuất video Shorts 9:16', desc: 'Đồng bộ phụ đề và nhạc nền chất lượng cao' }
            ].map((item) => (
              <div key={item.step} style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                <span style={{
                  width: '24px',
                  height: '24px',
                  borderRadius: '50%',
                  background: '#4f46e5',
                  color: '#fff',
                  fontSize: '11px',
                  fontWeight: 800,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  flexShrink: 0
                }}>
                  {item.step}
                </span>
                <div>
                  <span style={{ fontSize: '13px', fontWeight: 600, color: '#f8fafc', display: 'block' }}>{item.title}</span>
                  <span style={{ fontSize: '11px', color: '#94a3b8' }}>{item.desc}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
