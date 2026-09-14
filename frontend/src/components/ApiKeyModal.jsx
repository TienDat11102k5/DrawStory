import React, { useState, useEffect } from 'react';
import { Key, ExternalLink, Check, Eye, EyeOff, Trash2, X, Sparkles, ShieldCheck } from 'lucide-react';

export default function ApiKeyModal({ isOpen, onClose, onKeySaved }) {
  const [apiKey, setApiKey] = useState('');
  const [showKey, setShowKey] = useState(false);
  const [savedSuccess, setSavedSuccess] = useState(false);

  useEffect(() => {
    if (isOpen) {
      const existing = localStorage.getItem('gemini_api_key') || '';
      setApiKey(existing);
      setSavedSuccess(false);
    }
  }, [isOpen]);

  if (!isOpen) return null;

  const handleSave = () => {
    const trimmed = apiKey.trim();
    if (!trimmed) {
      alert('Vui lòng nhập API Key trước khi lưu!');
      return;
    }
    localStorage.setItem('gemini_api_key', trimmed);
    setSavedSuccess(true);
    if (typeof onKeySaved === 'function') {
      onKeySaved(trimmed);
    }
    setTimeout(() => {
      setSavedSuccess(false);
      onClose();
    }, 1000);
  };

  const handleClear = () => {
    localStorage.removeItem('gemini_api_key');
    setApiKey('');
    if (typeof onKeySaved === 'function') {
      onKeySaved('');
    }
    alert('Đã gỡ bỏ Gemini API Key khỏi trình duyệt!');
  };

  const hasKey = !!apiKey.trim();

  return (
    <div style={{
      position: 'fixed',
      inset: 0,
      background: 'rgba(5, 7, 13, 0.85)',
      backdropFilter: 'blur(12px)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 100,
      padding: '20px'
    }}>
      <div 
        className="glass-panel-glow" 
        style={{
          width: '100%',
          maxWidth: '560px',
          background: 'rgba(15, 23, 42, 0.95)',
          borderRadius: '20px',
          padding: '32px',
          border: '1px solid rgba(99, 102, 241, 0.3)',
          boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.7)',
          position: 'relative',
          display: 'flex',
          flexDirection: 'column',
          gap: '20px'
        }}
      >
        {/* Close Button */}
        <button
          type="button"
          onClick={onClose}
          style={{
            position: 'absolute',
            top: '20px',
            right: '20px',
            background: 'rgba(255, 255, 255, 0.06)',
            border: 'none',
            color: '#94a3b8',
            borderRadius: '50%',
            width: '32px',
            height: '32px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            cursor: 'pointer'
          }}
        >
          <X size={18} />
        </button>

        {/* Modal Header */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
          <div style={{
            width: '44px',
            height: '44px',
            borderRadius: '12px',
            background: 'linear-gradient(135deg, #6366f1, #a855f7)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            boxShadow: '0 0 15px rgba(99, 102, 241, 0.4)'
          }}>
            <Key size={22} color="#fff" />
          </div>
          <div>
            <h3 style={{ fontSize: '20px', fontWeight: 800 }}>
              Cài Đặt <span className="gradient-title">Google Gemini API Key</span>
            </h3>
            <p style={{ fontSize: '13px', color: '#94a3b8', marginTop: '2px' }}>
              Tự động hóa kịch bản chuẩn đạo diễn và tạo prompt vẽ tranh chất lượng cao
            </p>
          </div>
        </div>

        {/* Free Guide Banner */}
        <div style={{
          background: 'rgba(99, 102, 241, 0.08)',
          border: '1px solid rgba(99, 102, 241, 0.25)',
          borderRadius: '12px',
          padding: '16px',
          fontSize: '13px',
          color: '#cbd5e1',
          lineHeight: 1.6
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: '#818cf8', fontWeight: 700, marginBottom: '6px' }}>
            <Sparkles size={16} />
            <span>Cách lấy API Key MIỄN PHÍ từ Google (Chỉ mất 30 giây):</span>
          </div>
          <ol style={{ paddingLeft: '20px', margin: 0 }}>
            <li>Vào Google AI Studio và đăng nhập tài khoản Gmail.</li>
            <li>Bấm nút <strong>"Create API key"</strong> &gt; Chọn tạo trong dự án mới.</li>
            <li>Copy chuỗi khóa bí mật (dạng <code>AIzaSy...</code>) và dán vào ô bên dưới.</li>
          </ol>
          <a
            href="https://aistudio.google.com/app/apikey"
            target="_blank"
            rel="noreferrer"
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: '6px',
              marginTop: '10px',
              color: '#38bdf8',
              fontWeight: 700,
              textDecoration: 'none',
              fontSize: '13px'
            }}
          >
            👉 Mở Google AI Studio để lấy Key ngay <ExternalLink size={14} />
          </a>
        </div>

        {/* Input Field */}
        <div>
          <label style={{ display: 'block', fontSize: '13px', fontWeight: 600, color: '#e2e8f0', marginBottom: '8px' }}>
            Nhập Gemini API Key của bạn:
          </label>
          <div style={{ position: 'relative' }}>
            <input
              type={showKey ? 'text' : 'password'}
              value={apiKey}
              onChange={(e) => setApiKey(e.target.value)}
              placeholder="AIzaSy..."
              style={{
                width: '100%',
                padding: '14px 44px 14px 16px',
                borderRadius: '12px',
                background: 'rgba(9, 13, 22, 0.8)',
                border: '1px solid rgba(255, 255, 255, 0.15)',
                color: '#fff',
                fontSize: '14px',
                outline: 'none',
                fontFamily: 'monospace'
              }}
            />
            <button
              type="button"
              onClick={() => setShowKey(!showKey)}
              style={{
                position: 'absolute',
                right: '12px',
                top: '50%',
                transform: 'translateY(-50%)',
                background: 'transparent',
                border: 'none',
                color: '#94a3b8',
                cursor: 'pointer'
              }}
              title={showKey ? 'Ẩn key' : 'Hiện key'}
            >
              {showKey ? <EyeOff size={18} /> : <Eye size={18} />}
            </button>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', marginTop: '8px' }}>
            <ShieldCheck size={14} color="#10b981" />
            <span style={{ fontSize: '11px', color: '#94a3b8' }}>
              Key được lưu trực tiếp trên trình duyệt của riêng bạn (LocalStorage), an toàn và bảo mật tuyệt đối.
            </span>
          </div>
        </div>

        {/* Modal Actions */}
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginTop: '8px' }}>
          <div>
            {hasKey && (
              <button
                type="button"
                onClick={handleClear}
                style={{
                  background: 'rgba(239, 68, 68, 0.1)',
                  border: '1px solid rgba(239, 68, 68, 0.2)',
                  color: '#f87171',
                  padding: '10px 16px',
                  borderRadius: '10px',
                  fontSize: '13px',
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '6px'
                }}
              >
                <Trash2 size={14} /> Xóa Key
              </button>
            )}
          </div>

          <div style={{ display: 'flex', gap: '10px' }}>
            <button
              type="button"
              className="btn-secondary"
              onClick={onClose}
              style={{ padding: '10px 18px', fontSize: '13px' }}
            >
              Đóng
            </button>
            <button
              type="button"
              className="btn-primary"
              onClick={handleSave}
              style={{ padding: '10px 22px', fontSize: '13px' }}
            >
              {savedSuccess ? (
                <>
                  <Check size={16} color="#fff" /> Đã lưu thành công!
                </>
              ) : (
                <>
                  <Key size={16} /> Lưu & Áp Dụng
                </>
              )}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
