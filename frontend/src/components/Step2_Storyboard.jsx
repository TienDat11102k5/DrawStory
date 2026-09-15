import React, { useState, useEffect, useRef } from 'react';
import { 
  Film, Volume2, ArrowLeft, Plus, Trash2, Upload, 
  Sparkles, Save, Image as ImageIcon, CheckCircle, RefreshCw, X, Copy, Check 
} from 'lucide-react';
import { previewVoice, uploadCustomImage, saveProject } from '../services/api';

export default function Step2_Storyboard({
  storyData,
  scenes,
  setScenes,
  selectedVoice,
  voiceRate = 1.0,
  setVoiceRate,
  onBack,
  onStartRender,
  isSubmitting
}) {
  const [playingIdx, setPlayingIdx] = useState(null);
  const [uploadingIdx, setUploadingIdx] = useState(null);
  const [savingDraft, setSavingDraft] = useState(false);
  const [saveSuccess, setSaveSuccess] = useState(false);
  const [copiedIdx, setCopiedIdx] = useState(null);
  const [autoSaveStatus, setAutoSaveStatus] = useState('saved'); // 'saved' | 'saving' | 'idle'
  const isFirstMount = useRef(true);

  // Tự động lưu bản nháp mỗi khi người dùng chỉnh sửa lời thoại, ảnh, hoặc thêm/xóa cảnh
  useEffect(() => {
    if (isFirstMount.current) {
      isFirstMount.current = false;
      return;
    }
    if (!scenes || scenes.length === 0) return;

    setAutoSaveStatus('saving');
    const timer = setTimeout(async () => {
      try {
        const projId = storyData?.project_id || `proj_${Date.now()}`;
        await saveProject({
          project_id: projId,
          title: storyData?.title || scenes[0]?.narration?.slice(0, 30) || "Dự án mới",
          topic: storyData?.topic || "",
          voice_id: selectedVoice,
          voice_rate: voiceRate,
          scenes_count: scenes.length,
          scenes: scenes,
          status: "DRAFT"
        });
        setAutoSaveStatus('saved');
      } catch (e) {
        console.error("Lỗi tự động lưu nháp:", e);
        setAutoSaveStatus('idle');
      }
    }, 1200);

    return () => clearTimeout(timer);
  }, [scenes, selectedVoice, voiceRate]);

  const handleCopyPrompt = (index, promptText) => {
    if (!promptText) return;
    navigator.clipboard.writeText(promptText);
    setCopiedIdx(index);
    setTimeout(() => setCopiedIdx(null), 2500);
  };

  // 1. Chỉnh sửa trường của scene
  const handleSceneChange = (index, field, value) => {
    const updated = [...scenes];
    updated[index][field] = value;
    setScenes(updated);
  };

  // 2. Thêm phân cảnh mới
  const handleAddScene = () => {
    const nextId = scenes.length + 1;
    const newScene = {
      scene_id: nextId,
      narration: "Nhập lời thoại thuyết minh cho cảnh này...",
      image_prompt: "Vertical 9:16 portrait composition, vibrant storybook illustration of an inspiring moment, rich watercolor and pencil sketch, lively colors, clean white background --ar 9:16",
      keywords: ["mới"]
    };
    setScenes([...scenes, newScene]);
  };

  // 3. Xóa phân cảnh
  const handleDeleteScene = (index) => {
    if (scenes.length <= 1) {
      alert("Kịch bản cần có ít nhất 1 phân cảnh.");
      return;
    }
    const updated = scenes.filter((_, i) => i !== index).map((s, i) => ({
      ...s,
      scene_id: i + 1
    }));
    setScenes(updated);
  };

  // 4. Nghe thử giọng đọc câu thoại
  const handlePreviewSceneVoice = async (index, text) => {
    try {
      setPlayingIdx(index);
      const res = await previewVoice(text, selectedVoice, voiceRate);
      if (res.audio_url) {
        const fullUrl = res.audio_url.startsWith("http") ? res.audio_url : `http://127.0.0.1:8000${res.audio_url}`;
        const audio = new Audio(fullUrl);
        audio.play();
        audio.onended = () => setPlayingIdx(null);
      }
    } catch (e) {
      alert("Lỗi nghe thử: " + e.message);
      setPlayingIdx(null);
    }
  };

  // 5. Upload ảnh từ máy tính cho cảnh
  const handleImageUpload = async (index, file) => {
    if (!file) return;
    try {
      setUploadingIdx(index);
      const res = await uploadCustomImage(file);
      if (res.image_url) {
        handleSceneChange(index, 'image_url', res.image_url);
      }
    } catch (err) {
      alert("Lỗi tải ảnh lên: " + err.message);
    } finally {
      setUploadingIdx(null);
    }
  };

  // 6. Xóa ảnh upload, quay lại dùng AI
  const handleRemoveCustomImage = (index) => {
    handleSceneChange(index, 'image_url', null);
  };

  // 7. Lưu dự án nháp
  const handleSaveDraft = async () => {
    try {
      setSavingDraft(true);
      const projId = storyData?.project_id || `proj_${Date.now()}`;
      await saveProject({
        project_id: projId,
        title: storyData?.title || scenes[0]?.narration.slice(0, 30) || "Dự án mới",
        topic: storyData?.topic || "",
        voice_id: selectedVoice,
        voice_rate: voiceRate,
        scenes_count: scenes.length,
        scenes: scenes,
        status: "DRAFT"
      });
      setSaveSuccess(true);
      setTimeout(() => setSaveSuccess(false), 3000);
    } catch (err) {
      alert("Lỗi lưu dự án: " + err.message);
    } finally {
      setSavingDraft(false);
    }
  };

  return (
    <div style={{ width: '100%', maxWidth: '100%' }}>
      {/* Top Action Bar */}
      <div style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        flexWrap: 'wrap',
        gap: '16px',
        marginBottom: '28px'
      }}>
        <div>
          <button
            type="button"
            className="btn-secondary"
            onClick={onBack}
            style={{ marginBottom: '10px' }}
          >
            <ArrowLeft size={16} /> Đổi ý tưởng ban đầu
          </button>
          <h2 style={{ fontSize: '28px', fontWeight: 800 }}>
            Biên Tập Storyboard: <span className="gradient-title">{storyData?.title || 'Kịch bản phân cảnh'}</span>
          </h2>
          <p style={{ fontSize: '14px', color: '#94a3b8' }}>
            Tổng cộng: <strong>{scenes.length} phân cảnh</strong>. Bạn có thể tự tải ảnh lên, thêm/bớt cảnh hoặc chỉnh sửa lời thoại tùy ý.
          </p>
        </div>

        {/* Buttons: Auto Save Indicator, Save Draft & Start Render */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          {/* Voice Speed Adjuster */}
          {setVoiceRate && (
            <div style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: '6px',
              padding: '6px 12px',
              borderRadius: '10px',
              background: 'rgba(255, 255, 255, 0.05)',
              border: '1px solid rgba(255, 255, 255, 0.1)',
              fontSize: '12px'
            }}>
              <span style={{ color: '#94a3b8' }}>Tốc độ giọng:</span>
              <input
                type="range"
                min="0.25"
                max="2.0"
                step="0.05"
                value={voiceRate}
                onChange={(e) => setVoiceRate(parseFloat(e.target.value))}
                style={{ width: '70px', accentColor: '#6366f1', cursor: 'pointer' }}
                title="Kéo để chỉnh tốc độ đọc (0.25x - 2.0x)"
              />
              <span style={{ color: '#818cf8', fontWeight: 700, minWidth: '32px' }}>{voiceRate}x</span>
            </div>
          )}

          {/* Auto-Save Indicator Badge */}
          <div style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: '6px',
            padding: '8px 14px',
            borderRadius: '10px',
            background: autoSaveStatus === 'saving' ? 'rgba(234, 179, 8, 0.1)' : 'rgba(16, 185, 129, 0.1)',
            border: autoSaveStatus === 'saving' ? '1px solid rgba(234, 179, 8, 0.3)' : '1px solid rgba(16, 185, 129, 0.3)',
            color: autoSaveStatus === 'saving' ? '#fbbf24' : '#34d399',
            fontSize: '12px',
            fontWeight: 600
          }}>
            {autoSaveStatus === 'saving' ? (
              <>
                <RefreshCw size={13} style={{ animation: 'spin 1s linear infinite' }} />
                <span>Đang tự động lưu...</span>
              </>
            ) : (
              <>
                <CheckCircle size={13} color="#10b981" />
                <span>Tự động lưu nháp: Đã lưu</span>
              </>
            )}
          </div>

          <button
            type="button"
            className="btn-secondary"
            onClick={handleSaveDraft}
            disabled={savingDraft}
            style={{ padding: '12px 18px', fontSize: '14px' }}
          >
            {saveSuccess ? <CheckCircle size={16} color="#10b981" /> : <Save size={16} />}
            {saveSuccess ? 'Đã lưu!' : savingDraft ? 'Đang lưu...' : 'Lưu bản nháp'}
          </button>

          <button
            type="button"
            className="btn-primary"
            onClick={onStartRender}
            disabled={isSubmitting}
            style={{ padding: '12px 24px', fontSize: '15px' }}
          >
            <Film size={18} />
            Bắt Đầu Tạo Video Ngay
          </button>
        </div>
      </div>

      {/* List of Scene Cards: Widescreen Grid 2 Cột */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(460px, 1fr))',
        gap: '24px',
        marginBottom: '32px'
      }}>
        {scenes.map((scene, idx) => {
          const hasCustomImage = !!scene.image_url;
          const fullImgUrl = scene.image_url?.startsWith('http') 
            ? scene.image_url 
            : scene.image_url ? `http://127.0.0.1:8000${scene.image_url}` : '';

          return (
            <div
              key={scene.scene_id}
              className="glass-panel"
              style={{
                padding: '24px',
                borderLeft: '4px solid #6366f1',
                display: 'flex',
                flexDirection: 'column',
                gap: '18px'
              }}
            >
              {/* Card Header */}
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                  <span style={{
                    background: '#4f46e5',
                    color: '#fff',
                    padding: '4px 14px',
                    borderRadius: '8px',
                    fontSize: '13px',
                    fontWeight: 700
                  }}>
                    Phân cảnh #{scene.scene_id}
                  </span>
                  {hasCustomImage && (
                    <span style={{
                      fontSize: '11px',
                      background: 'rgba(16, 185, 129, 0.15)',
                      color: '#34d399',
                      padding: '3px 8px',
                      borderRadius: '6px',
                      border: '1px solid rgba(16, 185, 129, 0.3)'
                    }}>
                      Đã có ảnh tự tải lên
                    </span>
                  )}
                </div>

                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  {/* Preview Voice */}
                  <button
                    type="button"
                    className="btn-secondary"
                    onClick={() => handlePreviewSceneVoice(idx, scene.narration)}
                    disabled={playingIdx === idx}
                    style={{ padding: '6px 14px', fontSize: '13px' }}
                  >
                    <Volume2 size={14} color="#818cf8" />
                    {playingIdx === idx ? 'Đang đọc...' : 'Nghe thử câu này'}
                  </button>

                  {/* Delete Scene Button */}
                  <button
                    type="button"
                    onClick={() => handleDeleteScene(idx)}
                    style={{
                      background: 'rgba(239, 68, 68, 0.1)',
                      border: '1px solid rgba(239, 68, 68, 0.2)',
                      color: '#f87171',
                      borderRadius: '8px',
                      padding: '6px 10px',
                      cursor: 'pointer'
                    }}
                    title="Xóa phân cảnh này"
                  >
                    <Trash2 size={15} />
                  </button>
                </div>
              </div>

              {/* Narration Editor */}
              <div>
                <label style={{ display: 'block', fontSize: '13px', fontWeight: 600, color: '#cbd5e1', marginBottom: '6px' }}>
                  Lời thoại thuyết minh của cảnh:
                </label>
                <textarea
                  rows={2}
                  value={scene.narration}
                  onChange={(e) => handleSceneChange(idx, 'narration', e.target.value)}
                  style={{
                    width: '100%',
                    padding: '12px 16px',
                    borderRadius: '10px',
                    background: 'rgba(9, 13, 22, 0.6)',
                    border: '1px solid rgba(255, 255, 255, 0.1)',
                    color: '#fff',
                    fontSize: '14px',
                    fontFamily: 'inherit',
                    outline: 'none'
                  }}
                  placeholder="Nhập lời thoại..."
                />
              </div>

              {/* Image Source Selection: AI vs Custom Upload */}
              <div style={{
                background: 'rgba(255, 255, 255, 0.02)',
                padding: '16px',
                borderRadius: '12px',
                border: '1px solid rgba(255, 255, 255, 0.06)',
                display: 'flex',
                flexDirection: 'column',
                gap: '12px'
              }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '8px' }}>
                  <span style={{ fontSize: '13px', fontWeight: 600, color: '#cbd5e1', display: 'flex', alignItems: 'center', gap: '6px' }}>
                    <ImageIcon size={15} color="#818cf8" />
                    Hình ảnh cho phân cảnh:
                  </span>

                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    {/* Nút Copy Prompt */}
                    <button
                      type="button"
                      onClick={() => handleCopyPrompt(idx, scene.image_prompt)}
                      style={{
                        display: 'inline-flex',
                        alignItems: 'center',
                        gap: '6px',
                        padding: '6px 12px',
                        borderRadius: '8px',
                        fontSize: '12px',
                        fontWeight: 600,
                        background: copiedIdx === idx ? 'rgba(16, 185, 129, 0.2)' : 'rgba(99, 102, 241, 0.2)',
                        border: copiedIdx === idx ? '1px solid #10b981' : '1px solid #818cf8',
                        color: copiedIdx === idx ? '#34d399' : '#c7d2fe',
                        cursor: 'pointer',
                        transition: 'all 0.15s ease'
                      }}
                      title="Sao chép prompt để dán qua Midjourney / DALL-E / Gemini / Bing"
                    >
                      {copiedIdx === idx ? <Check size={13} color="#34d399" /> : <Copy size={13} />}
                      {copiedIdx === idx ? 'Đã copy prompt!' : '📋 Sao chép Prompt'}
                    </button>

                    {/* Upload button hidden input */}
                    <label style={{
                      display: 'inline-flex',
                      alignItems: 'center',
                      gap: '6px',
                      fontSize: '12px',
                      color: '#fff',
                      background: 'linear-gradient(135deg, #4f46e5, #7c3aed)',
                      padding: '6px 14px',
                      borderRadius: '8px',
                      cursor: 'pointer',
                      fontWeight: 600,
                      boxShadow: '0 2px 8px rgba(79, 70, 229, 0.3)'
                    }}>
                      <Upload size={13} />
                      {uploadingIdx === idx ? 'Đang tải...' : 'Tải ảnh từ máy'}
                      <input
                        type="file"
                        accept="image/*"
                        style={{ display: 'none' }}
                        disabled={uploadingIdx === idx}
                        onChange={(e) => {
                          if (e.target.files?.[0]) {
                            handleImageUpload(idx, e.target.files[0]);
                          }
                        }}
                      />
                    </label>
                  </div>
                </div>

                {/* If custom image uploaded -> Show Thumbnail preview */}
                {hasCustomImage ? (
                  <div style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '16px',
                    background: 'rgba(9, 13, 22, 0.85)',
                    padding: '12px',
                    borderRadius: '10px',
                    border: '1px solid rgba(16, 185, 129, 0.4)'
                  }}>
                    <img
                      src={fullImgUrl}
                      alt="Custom Preview"
                      style={{ width: '70px', height: '70px', objectFit: 'cover', borderRadius: '8px', border: '1px solid rgba(255,255,255,0.1)' }}
                    />
                    <div style={{ flex: 1 }}>
                      <span style={{ fontSize: '13px', fontWeight: 700, color: '#34d399', display: 'flex', alignItems: 'center', gap: '6px' }}>
                        <CheckCircle size={14} color="#34d399" /> Sử dụng ảnh bạn đã tải lên
                      </span>
                      <span style={{ fontSize: '12px', color: '#94a3b8', display: 'block', marginTop: '2px' }}>
                        Hệ thống sẽ vẽ lại chính xác bức ảnh này trên video (phác thảo chì & quét màu nước).
                      </span>
                    </div>
                    <button
                      type="button"
                      onClick={() => handleRemoveCustomImage(idx)}
                      style={{
                        background: 'rgba(239, 68, 68, 0.15)',
                        border: '1px solid rgba(239, 68, 68, 0.3)',
                        color: '#f87171',
                        padding: '6px 12px',
                        borderRadius: '6px',
                        cursor: 'pointer',
                        fontSize: '12px',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '4px'
                      }}
                      title="Gỡ ảnh này để dùng tranh AI"
                    >
                      <X size={14} /> Gỡ ảnh
                    </button>
                  </div>
                ) : (
                  /* Otherwise show AI Prompt Editor with guidance */
                  <div>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '6px' }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                        <label style={{ fontSize: '12px', color: '#cbd5e1', fontWeight: 600 }}>
                          Prompt tạo ảnh AI tiếng Anh:
                        </label>
                        <span style={{
                          fontSize: '11px',
                          color: '#818cf8',
                          fontWeight: 700,
                          background: 'rgba(99, 102, 241, 0.15)',
                          border: '1px solid rgba(99, 102, 241, 0.3)',
                          padding: '1px 8px',
                          borderRadius: '6px'
                        }}>
                          📱 Khổ dọc 9:16
                        </span>
                      </div>
                      <span style={{ fontSize: '11px', color: '#94a3b8' }}>
                        💡 Tối ưu chuẩn Shorts/Reels/TikTok
                      </span>
                    </div>
                    <textarea
                      rows={2}
                      value={scene.image_prompt || ''}
                      onChange={(e) => handleSceneChange(idx, 'image_prompt', e.target.value)}
                      placeholder="Vibrant watercolor illustration..."
                      style={{
                        width: '100%',
                        padding: '10px 12px',
                        borderRadius: '8px',
                        background: 'rgba(9, 13, 22, 0.6)',
                        border: '1px solid rgba(255, 255, 255, 0.08)',
                        color: '#cbd5e1',
                        fontSize: '13px',
                        lineHeight: 1.4,
                        fontFamily: 'inherit',
                        outline: 'none',
                        resize: 'vertical'
                      }}
                    />
                  </div>
                )}
              </div>

            </div>
          );
        })}
      </div>

      {/* Button: Add New Scene */}
      <div style={{ textAlign: 'center', marginBottom: '40px' }}>
        <button
          type="button"
          className="btn-secondary"
          onClick={handleAddScene}
          style={{
            padding: '12px 28px',
            fontSize: '14px',
            borderStyle: 'dashed',
            borderColor: 'rgba(99, 102, 241, 0.4)',
            color: '#c7d2fe'
          }}
        >
          <Plus size={16} /> + Thêm Phân Cảnh Mới
        </button>
      </div>
    </div>
  );
}
