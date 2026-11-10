# Team — ALI33

## Thông tin nhóm

- Tên nhóm: **ALI33**.
- Lớp: **L3B**, khóa K5, Day 03 — Research Agent Tool Eval.
- Repo nhóm: [K5-L3B-DAY03-ALI33-ResearchAgentToolEval](https://github.com/griin-03/K5-L3B-DAY03-ALI33-ResearchAgentToolEval).
- Báo cáo chính: [report/team/group_report.md](report/team/group_report.md).
- Nhánh chứa báo cáo được bổ sung: `main`.
- Nhánh chứa phương án kỹ thuật đã triển khai: [`le-thanh-tung/solo-day03`](https://github.com/griin-03/K5-L3B-DAY03-ALI33-ResearchAgentToolEval/tree/le-thanh-tung/solo-day03).
- Commit kỹ thuật dùng làm bằng chứng: [`fddd7ff8bc306475031112582eeee98805b28f3b`](https://github.com/griin-03/K5-L3B-DAY03-ALI33-ResearchAgentToolEval/commit/fddd7ff8bc306475031112582eeee98805b28f3b).
- Nhánh/commit nộp cuối: nhóm cần thống nhất sau khi so sánh hoặc tích hợp các phương án. Việc bổ sung báo cáo trên `main` chưa thay thế bước này.

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
|---:|---|---|---|---|---|
| 1 | Lê Thanh Tùng | **2A202603819** | lethanhtung6803@gmail.com | griin-03 | Trưởng nhóm |
| 2 | Cấn Xuân Nghĩa | 2A202603805 | cannghia.xn@gmail.com | xuannghia2 | Thành viên |
| 3 | Nguyễn Mạnh Hùng | 2A202603852 | nguyenmanhhunglun@gmail.com | HungLunnn | Thành viên |

## Trạng thái báo cáo cá nhân

| Thành viên | Báo cáo | Trạng thái đóng góp và bằng chứng |
|---|---|---|
| Lê Thanh Tùng — 2A202603819 | [2A202603819_LeThanhTung.md](report/team/2A202603819_LeThanhTung.md) | Đã có phần việc, bằng chứng, khai báo AI và đối chiếu kết quả. |
| Cấn Xuân Nghĩa — 2A202603805 | Tên file cần tạo: `report/team/2A202603805_CanXuanNghia.md` | Chưa có báo cáo/commit cá nhân được ghi nhận trong phạm vi cập nhật này; thành viên bổ sung theo công việc thật. |
| Nguyễn Mạnh Hùng — 2A202603852 | Tên file cần tạo: `report/team/2A202603852_NguyenManhHung.md` | Chưa có báo cáo/commit cá nhân được ghi nhận trong phạm vi cập nhật này; thành viên bổ sung theo công việc thật. |

## LeThanhTung-2A202603819

### Phần việc phụ trách

Chuẩn bị một phương án để nhóm so sánh: setup API, đo baseline, tối ưu prompt/tool declaration, bổ sung tool, kiểm thử, eval nhóm, UI, live chat và triển khai demo trên VPS.

### Đóng góp cụ thể

- Cấu hình key và xử lý subscription RapidAPI; yêu cầu kiểm tra bằng API thật.
- Chuẩn bị sáu phiên bản `v0`–`v5-tools`, giữ cả các vòng không cải thiện. Case accuracy trên base tăng từ 70% lên 95%; còn một case không đạt.
- Bổ sung `deduplicate_sources`, khai báo tool và tài liệu; bộ eval nhóm có đúng 10 case, gồm 5 single turn và 5 multi turn.
- Có kết quả 97 unit test pass, không failed/skipped; bốn phiên live CLI với tổng sáu lượt; UI Streamlit hiển thị tool calls và cho tải transcript.
- Triển khai demo tại https://ali33.sunstudy.app trên VPS ARM 24GB, service riêng và HTTPS; dừng server local theo yêu cầu. UI chặn gửi Telegram thật.
- Codex hỗ trợ viết code/test, chạy lệnh, phân tích log, soạn tài liệu và triển khai theo yêu cầu. Không quy các phần này thành code tự viết hoàn toàn hoặc đóng góp của thành viên khác.

### Bằng chứng

- [Báo cáo cá nhân](report/team/2A202603819_LeThanhTung.md) và [báo cáo nhóm Phần A + B](report/team/group_report.md).
- [Commit kỹ thuật fddd7ff](https://github.com/griin-03/K5-L3B-DAY03-ALI33-ResearchAgentToolEval/commit/fddd7ff8bc306475031112582eeee98805b28f3b).
- [Version log](https://github.com/griin-03/K5-L3B-DAY03-ALI33-ResearchAgentToolEval/blob/fddd7ff8bc306475031112582eeee98805b28f3b/starter_v0/artifacts/version_log.csv), [kết quả so sánh](https://github.com/griin-03/K5-L3B-DAY03-ALI33-ResearchAgentToolEval/blob/fddd7ff8bc306475031112582eeee98805b28f3b/starter_v0/analysis/comparison.json), [live summary](https://github.com/griin-03/K5-L3B-DAY03-ALI33-ResearchAgentToolEval/blob/fddd7ff8bc306475031112582eeee98805b28f3b/starter_v0/analysis/live-summary.json).
- [Hướng dẫn triển khai](https://github.com/griin-03/K5-L3B-DAY03-ALI33-ResearchAgentToolEval/blob/fddd7ff8bc306475031112582eeee98805b28f3b/deploy/README.md) và [kết quả kiểm tra VPS](https://github.com/griin-03/K5-L3B-DAY03-ALI33-ResearchAgentToolEval/blob/fddd7ff8bc306475031112582eeee98805b28f3b/starter_v0/analysis/deployment.json).

## CanXuanNghia-2A202603805

### Phần việc phụ trách

Thành viên bổ sung phần việc đã thực hiện khi nhóm so sánh hoặc tích hợp phương án.

### Đóng góp cụ thể

Chưa có thông tin đóng góp cá nhân được xác nhận trong phạm vi cập nhật này.

### Bằng chứng

Thành viên bổ sung báo cáo `report/team/2A202603805_CanXuanNghia.md` và liên kết file/commit/PR thực tế; khai báo AI và cách kiểm tra kết quả theo [mẫu báo cáo](report/team/MSSV_HoTen.md).

## NguyenManhHung-2A202603852

### Phần việc phụ trách

Thành viên bổ sung phần việc đã thực hiện khi nhóm so sánh hoặc tích hợp phương án.

### Đóng góp cụ thể

Chưa có thông tin đóng góp cá nhân được xác nhận trong phạm vi cập nhật này.

### Bằng chứng

Thành viên bổ sung báo cáo `report/team/2A202603852_NguyenManhHung.md` và liên kết file/commit/PR thực tế; khai báo AI và cách kiểm tra kết quả theo [mẫu báo cáo](report/team/MSSV_HoTen.md).
