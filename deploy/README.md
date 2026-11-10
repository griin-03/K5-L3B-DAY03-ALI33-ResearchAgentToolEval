# Demo VPS — ALI33 Research Desk

- URL: **https://ali33.sunstudy.app**.
- VPS: `161.33.136.24`, ARM, 4 OCPU / 24GB; alias SSH đã có trên máy chủ sở hữu: `vps-arm`.
- Service riêng: `ali33-research.service`, user `ali33-demo`, upstream `127.0.0.1:8503`.
- Root: `/opt/ali33-research`; source theo release dưới `releases/`, symlink `current` chọn bản đang phục vụ.
- `.venv` riêng; `.env`, transcript và PDF cache nằm trong `shared/`, quyền hạn chế. Không đặt API key vào Git. Web mở trực tiếp, không cần mã demo.
- Nginx chỉ thêm site `ali33-research`; không sửa các site SunStudy/StudyStream/VinAssess. HTTPS do Certbot webroot cấp, challenge ở `/var/www/ali33-acme`.
- Service giới hạn 1GB RAM, một CPU tương đương, chặn privilege escalation và chỉ cho ghi vào shared. Gửi Telegram bị tắt trong UI.

## Kiểm tra và vận hành

```bash
ssh vps-arm 'sudo systemctl status ali33-research --no-pager'
ssh vps-arm 'curl -fsS http://127.0.0.1:8503/_stcore/health'
ssh vps-arm 'sudo systemctl restart ali33-research'
```

Tắt riêng demo: `ssh vps-arm 'sudo systemctl stop ali33-research'`.
Không cần chạy server trên laptop để giữ demo hoạt động.

## Triển khai lại

`prepare_vps.sh` nhận release ID, dùng source archive `/tmp/ali33-release.tar.gz` và
file credentials `/tmp/ali33-demo.env` đã chuyển qua SSH. Không nhúng credentials
trong command, source archive hoặc báo cáo. Trên Ubuntu mới cần `python3.12-venv`.
Script dựng venv, cài lockfile, chạy test, tạo service và cấu hình HTTP challenge.
Sau đó cấp/kiểm certificate rồi cài `ali33-https.conf`, chạy `nginx -t` trước reload.

Không chạy script chuẩn bị lên site đang hoạt động chỉ để cập nhật tài liệu: nó
cài HTTP challenge tạm. Khi đổi source đã kiểm tra, tạo release mới và chuyển
symlink, restart riêng service; giữ cấu hình HTTPS hiện có.

## Phạm vi kiểm chứng

Xem `starter_v0/analysis/deployment.json`: test trên VPS, health HTTPS tại origin,
trạng thái probe ngoài và các yêu cầu gọi API thật trên máy chủ. Cloudflare có thể
áp dụng challenge theo client; HTTP thành công ở origin không thay thế kiểm tra
trình duyệt của người dùng. Bản này chưa có kiểm chứng người dùng ngoài nhóm.

## Truy cập trực tiếp

Đã bỏ màn hình nhập mã demo và xóa cấu hình `DEMO_ACCESS_CODE` trên VPS. Release `20261110-v5-tools-public` chạy giao diện mở trực tiếp; bốn test UI trên VPS đã pass. Xem [bằng chứng triển khai](../starter_v0/analysis/public-access.json). Các API key vẫn chỉ ở server.
