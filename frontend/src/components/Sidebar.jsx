import React, { useState } from 'react';
import { 
  Film, FolderClock, ChevronRight, ChevronLeft, 
  Key, Sparkles 
} from 'lucide-react';

export default function Sidebar({ 
  activeTab, 
  onChangeTab, 
  onOpenKeyModal,
  hasApiKey
}) {
  const [isExpanded, setIsExpanded] = useState(false);

  return (
    <aside style={{
      position: 'fixed',
      top: '71px', // Ngay dưới Navbar
      left: 0,     // Nằm ở bên TRÁI
      bottom: 0,
      width: isExpanded ? '240px' : '58px',
      background: 'rgba(9, 13, 22, 0.96)',
      backdropFilter: 'blur(20px)',
      borderRight: '1px solid rgba(255, 255, 255, 0.08)',
      zIndex: 45,
      display: 'flex',
      flexDirection: 'column',
      transition: 'width 0.22s cubic-bezier(0.4, 0, 0.2, 1)',
      boxShadow: isExpanded ? '12px 0 35px rgba(0, 0, 0, 0.6)' : 'none',
      overflow: 'hidden'
    }}>
      {/* Nút Toggle mở rộng / thu gọn */}
      <div style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: isExpanded ? 'space-between' : 'center',
        padding: '14px 12px',
        borderBottom: '1px solid rgba(255, 255, 255, 0.06)'
      }}>
        {isExpanded && (
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Sparkles size={15} color="#818cf8" />
            <span style={{ fontSize: '12px', fontWeight: 700, color: '#e2e8f0', letterSpacing: '0.4px' }}>
              BẢNG ĐIỀU HƯỚNG
            </span>
          </div>
        )}
        <button
          type="button"
          onClick={() => setIsExpanded(!isExpanded)}
          title={isExpanded ? "Thu gọn thanh bên" : "Mở rộng thanh bên"}
          style={{
            width: '32px',
            height: '32px',
            borderRadius: '8px',
            background: 'rgba(255, 255, 255, 0.06)',
            border: '1px solid rgba(255, 255, 255, 0.1)',
            color: '#94a3b8',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            cursor: 'pointer',
            transition: 'all 0.15s'
          }}
        >
          {isExpanded ? <ChevronLeft size={18} /> : <ChevronRight size={18} />}
        </button>
      </div>

      {/* Danh sách các tab chức năng */}
      <div style={{ padding: '12px 8px', display: 'flex', flexDirection: 'column', gap: '8px', flex: 1 }}>
        {/* Tab 1: Studio Tạo Mới */}
        <button
          type="button"
          onClick={() => onChangeTab('studio')}
          title="Studio Tạo Mới"
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '12px',
            padding: '12px',
            borderRadius: '12px',
            border: activeTab === 'studio' ? '1px solid rgba(99, 102, 241, 0.5)' : '1px solid transparent',
            background: activeTab === 'studio' ? 'linear-gradient(135deg, rgba(79, 70, 229, 0.35), rgba(124, 58, 237, 0.35))' : 'transparent',
            color: activeTab === 'studio' ? '#fff' : '#94a3b8',
            cursor: 'pointer',
            textAlign: 'left',
            width: '100%',
            transition: 'all 0.15s',
            justifyContent: isExpanded ? 'flex-start' : 'center'
          }}
        >
          <div style={{
            minWidth: '22px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: activeTab === 'studio' ? '#818cf8' : '#94a3b8'
          }}>
            <Film size={20} />
          </div>
          {isExpanded && (
            <div style={{ overflow: 'hidden', whiteSpace: 'nowrap' }}>
              <div style={{ fontSize: '13px', fontWeight: 600 }}>Studio Tạo Mới</div>
              <div style={{ fontSize: '11px', color: '#64748b' }}>Tạo video phác thảo</div>
            </div>
          )}
        </button>

        {/* Tab 2: Dự Án Đã Lưu */}
        <button
          type="button"
          onClick={() => onChangeTab('projects')}
          title="Dự Án Đã Lưu (Lịch Sử)"
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '12px',
            padding: '12px',
            borderRadius: '12px',
            border: activeTab === 'projects' ? '1px solid rgba(99, 102, 241, 0.5)' : '1px solid transparent',
            background: activeTab === 'projects' ? 'linear-gradient(135deg, rgba(79, 70, 229, 0.35), rgba(124, 58, 237, 0.35))' : 'transparent',
            color: activeTab === 'projects' ? '#fff' : '#94a3b8',
            cursor: 'pointer',
            textAlign: 'left',
            width: '100%',
            transition: 'all 0.15s',
            justifyContent: isExpanded ? 'flex-start' : 'center'
          }}
        >
          <div style={{
            minWidth: '22px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: activeTab === 'projects' ? '#818cf8' : '#94a3b8'
          }}>
            <FolderClock size={20} />
          </div>
          {isExpanded && (
            <div style={{ overflow: 'hidden', whiteSpace: 'nowrap' }}>
              <div style={{ fontSize: '13px', fontWeight: 600 }}>Dự Án Đã Lưu</div>
              <div style={{ fontSize: '11px', color: '#64748b' }}>Lịch sử & Video</div>
            </div>
          )}
        </button>
      </div>

      {/* Footer Phím tắt */}
      <div style={{
        padding: '10px 8px',
        borderTop: '1px solid rgba(255, 255, 255, 0.06)',
        display: 'flex',
        flexDirection: 'column',
        gap: '6px'
      }}>
        {onOpenKeyModal && (
          <button
            type="button"
            onClick={onOpenKeyModal}
            title="Cài đặt Google Gemini API Key"
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '12px',
              padding: '10px',
              borderRadius: '10px',
              border: 'none',
              background: 'rgba(255, 255, 255, 0.04)',
              color: hasApiKey ? '#34d399' : '#94a3b8',
              cursor: 'pointer',
              textAlign: 'left',
              width: '100%',
              justifyContent: isExpanded ? 'flex-start' : 'center'
            }}
          >
            <Key size={18} color={hasApiKey ? '#10b981' : '#818cf8'} />
            {isExpanded && (
              <span style={{ fontSize: '12px', fontWeight: 600 }}>
                {hasApiKey ? 'Gemini: Đã kết nối' : 'Cài Gemini Key'}
              </span>
            )}
          </button>
        )}
      </div>
    </aside>
  );
}
