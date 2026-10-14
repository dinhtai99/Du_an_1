# VietCulture AI Studio

Ứng dụng tạo video dọc về văn hóa Việt Nam. Google Flow tạo hình ảnh trên cloud;
máy chỉ giữ phiên trình duyệt, tạo giọng đọc/phụ đề và ghép video bằng FFmpeg.

## Luồng xử lý

1. Nhập chủ đề, số cảnh, phong cách và giọng đọc.
2. Backend tự chia cảnh và soạn prompt 9:16.
3. Playwright điền từng prompt vào Google Flow và tải ảnh về.
4. Edge TTS tạo giọng đọc cùng phụ đề cho từng cảnh.
5. FFmpeg ghép ảnh, âm thanh và phụ đề thành MP4 1080 × 1920.
6. Nếu Flow yêu cầu đăng nhập, credit hoặc CAPTCHA, tác vụ chuyển sang trạng thái
   `waiting_for_user` và có thể tiếp tục sau khi người dùng xử lý.

## Chạy dự án

Yêu cầu: Node.js 20+, Python 3.11+ và FFmpeg.

Lần đầu chạy trên máy mới:

```bash
cd backend
python3 -m venv .venv
./.venv/bin/pip install -r requirements.txt
./.venv/bin/playwright install chromium

cd ../frontend
npm ci
cd ..
```

Khởi động cả frontend và backend:

```bash
chmod +x scripts/run-dev.sh
./scripts/run-dev.sh
```

Mở http://localhost:3000, chọn **Kết nối Google Flow**, đăng nhập Google và mở
một Flow project. Để cửa sổ Flow mở, quay lại ứng dụng và bắt đầu tạo video.

Backend API: http://127.0.0.1:8000/docs

## Lưu trữ

- Trạng thái và tài nguyên từng dự án: `storage/projects/<job-id>/`
- Video hoàn chỉnh: `storage/exports/<job-id>.mp4`
- Phiên đăng nhập Flow: `storage/flow_browser_profile/`

Thư mục `storage/` bị loại khỏi Git để không tải phiên đăng nhập và dữ liệu người
dùng lên repository.
