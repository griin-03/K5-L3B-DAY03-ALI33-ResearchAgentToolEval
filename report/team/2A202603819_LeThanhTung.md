# Báo cáo cá nhân — Lê Thanh Tùng — 2A202603819

## 1. Thông tin thành viên

- Họ tên: Lê Thanh Tùng; MSSV: 2A202603819; nhóm ALI33, L3B.
- GitHub: griin-03; nhánh phương án: `le-thanh-tung/solo-day03`.

## 2. Phần việc phụ trách

Chuẩn bị một phương án hoàn chỉnh để nhóm so sánh: setup, baseline, prompt/tool declaration, tool mới, unit tests, eval nhóm, UI, live chat và triển khai VPS. Đây chưa phải xác nhận nhóm đã chọn phương án này.

## 3. Đóng góp cụ thể

- Yêu cầu kiểm tra toàn bộ key; xử lý subscription RapidAPI sau khi kiểm tra báo lỗi 403.
- Yêu cầu làm một phương án riêng để so sánh, triển khai lên VPS ARM 24GB và domain `ali33.sunstudy.app`; yêu cầu tắt run trên laptop.
- Có 6 phiên bản được đo thật: v0 70%, v1 80%, v2–v5-tools 95%; các thử nghiệm không tăng điểm vẫn được giữ.
- Phương án có tool deduplicate_sources, đúng 10 case nhóm (5 single/5 multi, đạt 10/10), 97 test offline pass không skip, bốn phiên chat.py thật gồm sáu lượt và UI Streamlit.
- Dùng user/service riêng trên VPS, upstream loopback, HTTPS; giao diện mở trực tiếp không cần mã demo. Không gửi Telegram thật.

## 4. Bằng chứng và AI đã dùng

- [Báo cáo nhóm của phương án](group_report.md); [version_log](../../starter_v0/artifacts/version_log.csv); [comparison](../../starter_v0/analysis/comparison.json); [live summary](../../starter_v0/analysis/live-summary.json).
- Code tool/test/UI, snapshots, run JSON và transcript đi kèm repo; key không nằm trong Git.
- Tôi dùng Codex để đọc đề, viết code/test, chạy API/eval, phân tích log, viết tài liệu và thao tác triển khai theo yêu cầu. Các số đo do chương trình thực sự chạy tạo ra; không dùng số giả, không gán phần việc hoặc commit cho thành viên khác.
- Cách kiểm: pytest, contract tests, đối chiếu input/output tool, so hash, đọc run lỗi và transcript, kiểm API/HTTPS trên VPS. Tôi cần tự giải thích được từng thay đổi khi coach hỏi; việc có AI hỗ trợ không thay thế yêu cầu hiểu bài.

## 5. Tự đánh giá theo bằng chứng

Phương án đã có code và log cho các phần bắt buộc, nhưng chưa đạt hoàn hảo: base vẫn sai R12 theo tiêu chí tự động; hai vòng v3/v4 không cải thiện. Điểm 95% chỉ là kết quả trên 20 case cố định, không chứng minh mọi câu trả lời đúng. Trong kịch bản gửi có nội dung cụ thể, agent đã hỏi xác nhận và dừng khi hủy; UI còn chặn gửi ở code. Nhóm cần tự dùng thử, review nguồn và chọn phương án trước khi chốt nộp. Tôi không có bằng chứng để ghi cảm nhận hoặc đóng góp của Nghĩa/Hùng thay cho hai bạn.
