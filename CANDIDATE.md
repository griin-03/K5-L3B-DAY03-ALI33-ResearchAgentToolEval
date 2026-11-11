# Phương án của Tùng — ALI33 Research Desk

Phương án được phát triển ở nhánh `le-thanh-tung/solo-day03` và đã tích hợp vào **main** theo yêu cầu trưởng nhóm ngày 11/11/2026. Code, log và ba báo cáo cá nhân nằm cùng nhánh; các tiêu chí so sánh bên dưới ghi lại cách đánh giá trước khi tích hợp.

- **Demo:** https://ali33.sunstudy.app — mở trực tiếp, không cần mã truy cập.
- **Báo cáo:** [Phần A + B](report/team/group_report.md), [báo cáo Tùng](report/team/2A202603819_LeThanhTung.md).
- **Bằng chứng:** [version log](starter_v0/artifacts/version_log.csv), [so sánh](starter_v0/analysis/comparison.json), [live chat](starter_v0/analysis/live-summary.json).
- **Mức đạt quan sát:** base 70% → 95%; group 10/10; 97 unit/contract/UI tests pass, 0 skipped. V3/V4 không tăng điểm và được giữ nguyên trong log.
- **Bản demo cuối:** v5-tools, có tool loại nguồn trùng; gửi Telegram thật bị tắt.

## Nhóm so sánh thế nào?

1. Chạy cùng 20 case base, cùng provider/model; chỉ dùng run đủ case và không có provider error.
2. So cả routing, arguments, multi-turn; đọc case sai và kiểm tra API tool thật, không chỉ nhìn phần trăm.
3. Kiểm tool mới bằng input xấu và nhánh lỗi; xác nhận bộ group đủ 5 single + 5 multi và có case route tới tool mới.
4. Tự thử UI: yêu cầu thường, thiếu thông tin rồi bổ sung, hủy gửi; xem lỗi và nguồn có rõ không.
5. Review giới hạn dữ liệu, quyền hành động và khả năng tự giải thích từng thay đổi trước khi chọn.

Không dùng điểm trên bộ group khác nhau để kết luận trực tiếp ai hơn ai. Mỗi
thành viên giữ bằng chứng và commit kỹ thuật thật; trên bản nộp main, mỗi người
tự hoàn thành bằng chứng đóng góp của mình, không tạo commit/báo cáo giả cho nhau.

## Tái lập kết quả

Tạo môi trường theo README, cài `starter_v0/requirements.lock.txt`, điền key trong
`.env`, chạy `pytest`. Muốn đo lại snapshot mà không ghi đè lịch sử:

```bash
cd starter_v0
python run_eval.py --provider openrouter --version replay-v0 --suite base \
  --system-prompt artifacts/versions/v0/system_prompt.md \
  --tools artifacts/versions/v0/tools.yaml --eval-cases data/eval_base.json
python run_eval.py --provider openrouter --version replay-v5 --suite base \
  --system-prompt artifacts/versions/v5-tools/system_prompt.md \
  --tools artifacts/versions/v5-tools/tools.yaml --eval-cases data/eval_base.json
python run_eval.py --provider openrouter --version replay-v5 --suite group \
  --eval-cases data/eval_group.json
```

Tắt delivery credentials khi chỉ đo routing/boundary. Để tái lập các phiên chat
thật mà không gửi tin, dùng `python scripts/live_smoke.py`. API calls tốn quota
thực; các test pytest được mock và chạy offline.
