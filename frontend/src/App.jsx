import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import Step1_IdeaInput from './components/Step1_IdeaInput';
import Step2_Storyboard from './components/Step2_Storyboard';
import Step3_RenderPlayer from './components/Step3_RenderPlayer';
import ProjectsList from './components/ProjectsList';
import Sidebar from './components/Sidebar';
import { checkBackendHealth, getVoices, generateStory, startVideoRender, getTaskStatus, saveProject } from './services/api';

export default function App() {
  const [activeTab, setActiveTab] = useState('studio'); // 'studio' | 'projects'
  const [currentStep, setCurrentStep] = useState(1);
  const [backendOnline, setBackendOnline] = useState(false);
  
  // Form State
  const [topic, setTopic] = useState("Lợi ích của sự tập trung sâu trong công việc");
  const [scenesCount, setScenesCount] = useState(3);
  const [selectedVoice, setSelectedVoice] = useState("vi-VN-HoaiMyNeural");
  const [voiceRate, setVoiceRate] = useState(1.0);
  const [voices, setVoices] = useState([
    { voice_id: "vi-VN-HoaiMyNeural", name: "Hoài My (Truyền cảm - Chuẩn)" },
    { voice_id: "vi-VN-HoaiMy-Deep", name: "Hoài My (Trầm lắng - Kể chuyện)" },
    { voice_id: "vi-VN-HoaiMy-Lively", name: "Hoài My (Tươi trẻ - Hoạt hình)" },
    { voice_id: "vi-VN-NamMinhNeural", name: "Nam Minh (Trầm ấm - Chuẩn)" },
    { voice_id: "vi-VN-NamMinh-Deep", name: "Nam Minh (Sâu lắng - Tài liệu)" },
    { voice_id: "vi-VN-NamMinh-Youth", name: "Nam Minh (Năng động - Review)" }
  ]);

  // Data State
  const [isGeneratingStory, setIsGeneratingStory] = useState(false);
  const [storyData, setStoryData] = useState(null);
  const [scenes, setScenes] = useState([]);

  // Render & Task State
  const [isStartingRender, setIsStartingRender] = useState(false);
  const [taskId, setTaskId] = useState(null);
  const [taskStatus, setTaskStatus] = useState(null);
  const [videoUrl, setVideoUrl] = useState(null);

  // 1. Kiểm tra kết nối Backend & Lấy danh sách giọng đọc
  useEffect(() => {
    const initApp = async () => {
      const health = await checkBackendHealth();
      setBackendOnline(health.online);
      if (health.online) {
        try {
          const vList = await getVoices();
          if (vList && vList.length > 0) {
            setVoices(vList);
            setSelectedVoice(vList[0].voice_id);
          }
        } catch (err) {
          console.error("Không thể tải danh sách voices:", err);
        }
      }
    };
    initApp();
  }, []);

  // 2. Xử lý Sinh Kịch Bản (Step 1 -> Step 2) và TỰ ĐỘNG LƯU BẢN NHÁP NGAY
  const handleGenerateStory = async () => {
    if (!topic.trim()) return;
    try {
      setIsGeneratingStory(true);
      const res = await generateStory({
        topic,
        scenesCount,
        language: "vi"
      });
      setStoryData(res);
      setScenes(res.scenes);
      setCurrentStep(2);

      // TỰ ĐỘNG LƯU DỰ ÁN NHÁP NGAY VÀO LỊCH SỬ (Tránh người dùng thoát hoặc mất dữ liệu)
      try {
        await saveProject({
          project_id: res.project_id,
          title: res.title,
          topic: res.topic || topic,
          voice_id: selectedVoice,
          voice_rate: voiceRate,
          scenes_count: res.scenes.length,
          scenes: res.scenes,
          status: "DRAFT"
        });
        console.log("[App] Đã tự động lưu bản nháp ban đầu:", res.project_id);
      } catch (saveErr) {
        console.warn("Lỗi lưu nháp ban đầu:", saveErr);
      }
    } catch (err) {
      alert("Lỗi tạo kịch bản: " + err.message);
    } finally {
      setIsGeneratingStory(false);
    }
  };

  // 3. Xử lý Bắt đầu Render (Step 2 -> Step 3)
  const handleStartRender = async () => {
    if (!scenes || scenes.length === 0) {
      alert("Cần có ít nhất 1 phân cảnh để tạo video.");
      return;
    }
    try {
      setIsStartingRender(true);
      const res = await startVideoRender({
        scenes,
        voiceId: selectedVoice,
        voiceRate: voiceRate,
        projectId: storyData?.project_id,
        title: storyData?.title || topic,
        enableHand: true,
        enableSubtitles: true
      });
      if (res.task_id) {
        setTaskId(res.task_id);
        setCurrentStep(3);
      }
    } catch (err) {
      alert("Lỗi kích hoạt render: " + err.message);
    } finally {
      setIsStartingRender(false);
    }
  };

  // 4. Polling trạng thái tiến độ Render khi ở Step 3
  useEffect(() => {
    if (currentStep !== 3 || !taskId) return;

    let intervalId = setInterval(async () => {
      try {
        const status = await getTaskStatus(taskId);
        setTaskStatus(status);
        if (status.status === 'COMPLETED') {
          clearInterval(intervalId);
          if (status.result?.video_url) {
            setVideoUrl(status.result.video_url);
          }
        } else if (status.status === 'FAILED') {
          clearInterval(intervalId);
        }
      } catch (e) {
        console.error("Lỗi polling task status:", e);
      }
    }, 2500);

    return () => clearInterval(intervalId);
  }, [currentStep, taskId]);

  // 5. Mở lại một dự án cũ từ History để tiếp tục chỉnh sửa
  const handleOpenProjectFromHistory = (proj) => {
    setStoryData(proj);
    setScenes(proj.scenes || []);
    if (proj.voice_id) setSelectedVoice(proj.voice_id);
    if (proj.voice_rate) setVoiceRate(proj.voice_rate);
    if (proj.topic) setTopic(proj.topic);
    
    // LUÔN LUÔN VÀO STEP 2 (Storyboard Editor) để người dùng xem và chỉnh sửa kịch bản & ảnh
    setCurrentStep(2);
    setActiveTab('studio');
  };

  const handleReset = () => {
    setCurrentStep(1);
    setTaskId(null);
    setTaskStatus(null);
    setVideoUrl(null);
  };

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      <Navbar 
        backendOnline={backendOnline} 
        activeTab={activeTab} 
        onChangeTab={(tab) => setActiveTab(tab)} 
      />

      <Sidebar 
        activeTab={activeTab}
        onChangeTab={(tab) => setActiveTab(tab)}
      />

      <main style={{ 
        flex: 1, 
        padding: '28px 32px', 
        paddingLeft: '80px',
        width: '100%', 
        maxWidth: '100%', 
        margin: '0 auto',
        boxSizing: 'border-box'
      }}>
        {/* TAB 1: STUDIO TẠO MỚI */}
        {activeTab === 'studio' && (
          <>
            {currentStep === 1 && (
              <Step1_IdeaInput
                topic={topic}
                setTopic={setTopic}
                scenesCount={scenesCount}
                setScenesCount={setScenesCount}
                selectedVoice={selectedVoice}
                setSelectedVoice={setSelectedVoice}
                voiceRate={voiceRate}
                setVoiceRate={setVoiceRate}
                voices={voices}
                onGenerateStory={handleGenerateStory}
                isLoading={isGeneratingStory}
              />
            )}

            {currentStep === 2 && (
              <Step2_Storyboard
                storyData={storyData}
                scenes={scenes}
                setScenes={setScenes}
                selectedVoice={selectedVoice}
                voiceRate={voiceRate}
                setVoiceRate={setVoiceRate}
                onBack={() => setCurrentStep(1)}
                onStartRender={handleStartRender}
                isSubmitting={isStartingRender}
              />
            )}

            {currentStep === 3 && (
              <Step3_RenderPlayer
                taskStatus={taskStatus}
                videoUrl={videoUrl}
                videoTitle={storyData?.title || topic}
                onReset={handleReset}
              />
            )}
          </>
        )}

        {/* TAB 2: QUẢN LÝ DỰ ÁN & LỊCH SỬ */}
        {activeTab === 'projects' && (
          <ProjectsList
            onOpenProject={handleOpenProjectFromHistory}
            onStartNew={() => {
              handleReset();
              setActiveTab('studio');
            }}
          />
        )}
      </main>

      <footer style={{
        textAlign: 'center',
        padding: '24px',
        color: '#64748b',
        fontSize: '12px',
        borderTop: '1px solid rgba(255, 255, 255, 0.05)'
      }}>
        DrawStory AI © 2026 - Tự động hóa video bảng trắng & màu nước bằng Generative AI
      </footer>
    </div>
  );
}
