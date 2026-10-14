"use client";

import {
  CheckCircle2,
  CircleAlert,
  Download,
  ExternalLink,
  Film,
  ImageIcon,
  LoaderCircle,
  Play,
  RotateCcw,
  Sparkles,
  Volume2,
} from "lucide-react";
import { FormEvent, useEffect, useState } from "react";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000";

type FlowStatus = {
  open: boolean;
  ready: boolean;
  url?: string;
  message: string;
};

type Scene = {
  order: number;
  narration: string;
  status: "pending" | "generating" | "completed" | "failed";
  image_path?: string;
  audio_path?: string;
};

type PipelineJob = {
  id: string;
  title: string;
  status: "pending" | "running" | "waiting_for_user" | "failed" | "completed";
  progress_percent: number;
  current_step: string;
  user_action_prompt?: string;
  error_message?: string;
  output_video_url?: string;
  scenes: Scene[];
};

async function requestJson<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, {
    ...init,
    headers: { "Content-Type": "application/json", ...init?.headers },
  });
  if (!response.ok) {
    const body = await response.json().catch(() => null);
    throw new Error(body?.detail ?? `API trả về lỗi ${response.status}`);
  }
  return response.json();
}

export default function Home() {
  const [flow, setFlow] = useState<FlowStatus>({
    open: false,
    ready: false,
    message: "Chưa kết nối Google Flow",
  });
  const [job, setJob] = useState<PipelineJob | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [topic, setTopic] = useState("Ý nghĩa tục dâng sớ Táo Quân của người Việt");
  const [sceneCount, setSceneCount] = useState(6);
  const [duration, setDuration] = useState(60);
  const [visualStyle, setVisualStyle] = useState(
    "Tranh sơn mài và thủy mặc truyền thống Việt Nam",
  );
  const [voice, setVoice] = useState("vi-VN-HoaiMyNeural");
  const [cta, setCta] = useState(
    "Liên hệ để được tư vấn phần mềm viết sớ và máy in sớ.",
  );

  useEffect(() => {
    let active = true;
    requestJson<FlowStatus>("/api/v1/flow/status")
      .then((status) => { if (active) setFlow(status); })
      .catch(() => {
        if (active) setFlow({ open: false, ready: false, message: "Backend chưa chạy" });
      });
    return () => { active = false; };
  }, []);

  useEffect(() => {
    if (!job || !["pending", "running"].includes(job.status)) return;
    const timer = window.setInterval(async () => {
      try {
        const latest = await requestJson<PipelineJob>(`/api/v1/pipeline/jobs/${job.id}`);
        setJob(latest);
      } catch (pollError) {
        setError(pollError instanceof Error ? pollError.message : "Không cập nhật được tác vụ");
      }
    }, 1800);
    return () => window.clearInterval(timer);
  }, [job]);

  async function openFlow() {
    setBusy(true);
    setError(null);
    try {
      setFlow(await requestJson<FlowStatus>("/api/v1/flow/open", { method: "POST" }));
    } catch (openError) {
      setError(openError instanceof Error ? openError.message : "Không mở được Flow");
    } finally {
      setBusy(false);
    }
  }

  async function start(event: FormEvent) {
    event.preventDefault();
    setBusy(true);
    setError(null);
    try {
      const created = await requestJson<PipelineJob>("/api/v1/pipeline/jobs", {
        method: "POST",
        body: JSON.stringify({
          topic,
          duration_target: duration,
          scene_count: sceneCount,
          visual_style: visualStyle,
          voice,
          cta_text: cta,
          generate_images: true,
          render_video: true,
        }),
      });
      setJob(created);
    } catch (startError) {
      setError(startError instanceof Error ? startError.message : "Không tạo được tác vụ");
    } finally {
      setBusy(false);
    }
  }

  async function resume() {
    if (!job) return;
    setBusy(true);
    setError(null);
    try {
      setJob(
        await requestJson<PipelineJob>(`/api/v1/pipeline/jobs/${job.id}/resume`, {
          method: "POST",
        }),
      );
    } catch (resumeError) {
      setError(resumeError instanceof Error ? resumeError.message : "Không thể tiếp tục");
    } finally {
      setBusy(false);
    }
  }

  const running = job && ["pending", "running"].includes(job.status);

  return (
    <main className="app-shell">
      <aside className="sidebar">
        <div className="brand-mark"><Sparkles size={22} /></div>
        <div>
          <p className="eyebrow">VIETCULTURE</p>
          <h1>AI Studio</h1>
        </div>
        <nav className="steps" aria-label="Quy trình">
          <Step icon={<Film size={18} />} label="Nội dung" active />
          <Step icon={<ImageIcon size={18} />} label="Google Flow" active={flow.ready} />
          <Step icon={<Volume2 size={18} />} label="Giọng đọc" active={Boolean(job?.scenes.some((scene) => scene.audio_path))} />
          <Step icon={<Play size={18} />} label="Xuất video" active={job?.status === "completed"} />
        </nav>
        <div className="sidebar-note">
          <span className="status-dot" data-ready={flow.ready} />
          <div>
            <strong>{flow.ready ? "Flow sẵn sàng" : "Flow chưa sẵn sàng"}</strong>
            <p>Ảnh được tạo trên Google, máy chỉ ghép video.</p>
          </div>
        </div>
      </aside>

      <section className="workspace">
        <header className="topbar">
          <div>
            <p className="eyebrow">XƯỞNG VIDEO VĂN HÓA</p>
            <h2>Tạo video mới</h2>
          </div>
          <button className={`flow-button ${flow.ready ? "ready" : ""}`} onClick={openFlow} disabled={busy}>
            <ExternalLink size={17} />
            {flow.ready ? "Mở lại Google Flow" : "Kết nối Google Flow"}
          </button>
        </header>

        <div className="content-grid">
          <form className="editor-card" onSubmit={start}>
            <div className="section-heading">
              <span>01</span>
              <div><h3>Chủ đề và kịch bản</h3><p>Hệ thống tự chia cảnh và viết prompt ảnh.</p></div>
            </div>

            <label>
              Chủ đề video
              <textarea value={topic} onChange={(event) => setTopic(event.target.value)} rows={3} required />
            </label>

            <div className="field-row">
              <label>
                Số cảnh
                <select value={sceneCount} onChange={(event) => setSceneCount(Number(event.target.value))}>
                  {[4, 5, 6, 7, 8, 9, 10].map((count) => <option key={count}>{count}</option>)}
                </select>
              </label>
              <label>
                Thời lượng mục tiêu
                <select value={duration} onChange={(event) => setDuration(Number(event.target.value))}>
                  {[30, 45, 60, 90, 120].map((seconds) => <option key={seconds} value={seconds}>{seconds} giây</option>)}
                </select>
              </label>
            </div>

            <label>
              Phong cách hình ảnh
              <input value={visualStyle} onChange={(event) => setVisualStyle(event.target.value)} />
            </label>

            <div className="field-row">
              <label>
                Giọng đọc
                <select value={voice} onChange={(event) => setVoice(event.target.value)}>
                  <option value="vi-VN-HoaiMyNeural">Hoài My — nữ</option>
                  <option value="vi-VN-NamMinhNeural">Nam Minh — nam</option>
                </select>
              </label>
              <label>
                Khung hình
                <input value="Dọc 9:16 · 1080 × 1920" disabled />
              </label>
            </div>

            <label>
              Lời kêu gọi cuối video
              <input value={cta} onChange={(event) => setCta(event.target.value)} />
            </label>

            {error && <div className="notice error"><CircleAlert size={18} />{error}</div>}
            {!flow.ready && <div className="notice"><CircleAlert size={18} />Mở Flow, đăng nhập và vào một project trước khi bắt đầu.</div>}

            <button className="primary-button" type="submit" disabled={busy || Boolean(running)}>
              {running ? <LoaderCircle className="spin" size={19} /> : <Sparkles size={19} />}
              {running ? "Đang xử lý…" : "Tạo ảnh và ghép video"}
            </button>
          </form>

          <aside className="job-card">
            <div className="section-heading compact">
              <span>02</span>
              <div><h3>Tiến trình</h3><p>Theo dõi từng cảnh trong thời gian thực.</p></div>
            </div>

            {!job ? (
              <div className="empty-state">
                <Film size={34} />
                <h4>Chưa có tác vụ</h4>
                <p>Kết nối Flow rồi bắt đầu dự án đầu tiên.</p>
              </div>
            ) : (
              <div className="job-content">
                <div className="job-title"><h4>{job.title}</h4><StatusBadge status={job.status} /></div>
                <div className="progress-track"><span style={{ width: `${job.progress_percent}%` }} /></div>
                <div className="progress-copy"><span>{job.current_step}</span><strong>{Math.round(job.progress_percent)}%</strong></div>

                {(job.user_action_prompt || job.error_message) && (
                  <div className={`notice ${job.error_message ? "error" : "warning"}`}>
                    <CircleAlert size={18} />
                    <div>
                      <p>{job.user_action_prompt ?? job.error_message}</p>
                      {["waiting_for_user", "failed"].includes(job.status) && (
                        <button type="button" className="text-button" onClick={resume} disabled={busy}>
                          <RotateCcw size={15} />
                          {job.status === "failed" ? "Thử lại tác vụ" : "Tôi đã xử lý, tiếp tục"}
                        </button>
                      )}
                    </div>
                  </div>
                )}

                <div className="scene-list">
                  {job.scenes.map((scene) => (
                    <div className="scene-row" key={scene.order}>
                      <span className="scene-number">{String(scene.order).padStart(2, "0")}</span>
                      <div><strong>Cảnh {scene.order}</strong><p>{scene.narration}</p></div>
                      {scene.status === "completed" ? <CheckCircle2 className="done" size={18} /> : scene.status === "generating" ? <LoaderCircle className="spin" size={18} /> : scene.status === "failed" ? <CircleAlert className="scene-error" size={18} /> : <span className="pending-dot" />}
                    </div>
                  ))}
                </div>

                {job.output_video_url && (
                  <a className="download-button" href={`${API_URL}${job.output_video_url}`} download>
                    <Download size={18} /> Tải video hoàn chỉnh
                  </a>
                )}
              </div>
            )}
          </aside>
        </div>
      </section>
    </main>
  );
}

function Step({ icon, label, active = false }: { icon: React.ReactNode; label: string; active?: boolean }) {
  return <div className={`step ${active ? "active" : ""}`}><span>{icon}</span>{label}</div>;
}

function StatusBadge({ status }: { status: PipelineJob["status"] }) {
  const labels: Record<PipelineJob["status"], string> = {
    pending: "Đang chờ",
    running: "Đang chạy",
    waiting_for_user: "Cần thao tác",
    failed: "Có lỗi",
    completed: "Hoàn tất",
  };
  return <span className={`status-badge ${status}`}>{labels[status]}</span>;
}
