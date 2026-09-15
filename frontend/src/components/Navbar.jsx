import React, { useState, useEffect } from 'react';
import { Sparkles, Palette, Activity, Key } from 'lucide-react';
import ApiKeyModal from './ApiKeyModal';

export default function Navbar({ backendOnline, activeTab = 'studio', onChangeTab = () => {} }) {
  const [isKeyModalOpen, setIsKeyModalOpen] = useState(false);
  const [hasApiKey, setHasApiKey] = useState(false);
  const [logoError, setLogoError] = useState(false);

  useEffect(() => {
    const key = localStorage.getItem('gemini_api_key');
    setHasApiKey(!!(key && key.trim()));
  }, []);

  const handleTabClick = (tab) => {
    if (typeof onChangeTab === 'function') {
      onChangeTab(tab);
    }
  };

  const handleKeySaved = (newKey) => {
    setHasApiKey(!!(newKey && newKey.trim()));
  };

  return (
    <>
      <header style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        padding: '16px 32px',
        borderBottom: '1px solid rgba(255, 255, 255, 0.08)',
        backdropFilter: 'blur(16px)',
        position: 'sticky',
        top: 0,
        zIndex: 50,
        background: 'rgba(9, 13, 22, 0.9)',
        width: '100%'
      }}>
        {/* Brand Logo - Bấm vào để về Trang Chủ */}
        <div 
          onClick={() => onChangeTab('studio')} 
          title="Về Trang Chủ (Studio)"
          style={{ display: 'flex', alignItems: 'center', gap: '12px', cursor: 'pointer', userSelect: 'none' }}
        >
          <div style={{
            width: '38px',
            height: '38px',
            borderRadius: '10px',
            background: 'linear-gradient(135deg, #6366f1, #a855f7)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            boxShadow: '0 0 20px rgba(99, 102, 241, 0.4)',
            overflow: 'hidden'
          }}>
            {!logoError ? (
              <img 
                src="/logo.png" 
                alt="Logo" 
                onError={(e) => {
                  if (!e.target.dataset.triedJpg) {
                    e.target.dataset.triedJpg = 'true';
                    e.target.src = '/logo.jpg';
                  } else {
                    setLogoError(true);
                  }
                }}
                style={{ width: '100%', height: '100%', objectFit: 'cover' }} 
              />
            ) : (
              <Palette size={22} color="#fff" />
            )}
          </div>

          <div>
            <h1 style={{ fontSize: '18px', fontWeight: 800, letterSpacing: '-0.5px' }}>
              DrawStory <span style={{ color: '#818cf8' }}>AI</span>
            </h1>
            <p style={{ fontSize: '11px', color: '#94a3b8', fontWeight: 500 }}>
              Whiteboard & Color Sketch Video Studio
            </p>
          </div>
        </div>



        {/* Right Tools: Gemini Key & Backend Status */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
          {/* Gemini API Key Button */}
          <button
            type="button"
            onClick={() => setIsKeyModalOpen(true)}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '8px',
              padding: '7px 14px',
              borderRadius: '10px',
              fontSize: '12px',
              fontWeight: 600,
              cursor: 'pointer',
              transition: 'all 0.2s ease',
              background: hasApiKey ? 'rgba(16, 185, 129, 0.12)' : 'rgba(99, 102, 241, 0.15)',
              border: `1px solid ${hasApiKey ? 'rgba(16, 185, 129, 0.4)' : 'rgba(99, 102, 241, 0.35)'}`,
              color: hasApiKey ? '#34d399' : '#c7d2fe'
            }}
            title="Cài đặt Google Gemini API Key để tạo kịch bản chuyên nghiệp"
          >
            <Key size={14} color={hasApiKey ? '#10b981' : '#818cf8'} />
            {hasApiKey ? 'Gemini: Đã kết nối' : 'Cài Gemini Key'}
          </button>

          {/* Backend Status Indicator */}
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
            padding: '6px 14px',
            borderRadius: '999px',
            background: backendOnline ? 'rgba(16, 185, 129, 0.12)' : 'rgba(239, 68, 68, 0.12)',
            border: `1px solid ${backendOnline ? 'rgba(16, 185, 129, 0.3)' : 'rgba(239, 68, 68, 0.3)'}`
          }}>
            <span style={{
              width: '8px',
              height: '8px',
              borderRadius: '50%',
              background: backendOnline ? '#10b981' : '#ef4444',
              boxShadow: `0 0 8px ${backendOnline ? '#10b981' : '#ef4444'}`
            }}></span>
            <span style={{ fontSize: '12px', fontWeight: 600, color: backendOnline ? '#34d399' : '#f87171' }}>
              {backendOnline ? 'ONLINE' : 'OFFLINE'}
            </span>
          </div>

          <a 
            href="http://127.0.0.1:8000/docs" 
            target="_blank" 
            rel="noreferrer"
            style={{
              fontSize: '12px',
              color: '#94a3b8',
              textDecoration: 'none',
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
              padding: '6px 12px',
              borderRadius: '8px',
              border: '1px solid rgba(255, 255, 255, 0.08)',
              background: 'rgba(255, 255, 255, 0.03)'
            }}
          >
            <Activity size={14} /> Swagger API
          </a>
        </div>
      </header>

      {/* API Key Modal */}
      <ApiKeyModal
        isOpen={isKeyModalOpen}
        onClose={() => setIsKeyModalOpen(false)}
        onKeySaved={handleKeySaved}
      />
    </>
  );
}
