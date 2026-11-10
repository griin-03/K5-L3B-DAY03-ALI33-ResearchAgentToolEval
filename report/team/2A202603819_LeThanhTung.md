# Báo cáo cá nhân — Lê Thanh Tùng — 2A202603819

## 1. Thông tin thành viên

- Họ tên: **Lê Thanh Tùng**.
- MSSV: **2A202603819**.
- Email: lethanhtung6803@gmail.com.
- GitHub: [griin-03](https://github.com/griin-03).
- Nhóm: **ALI33**; lớp **L3B**, khóa K5.
- Bài lab: Day 03 — Research Agent Tool Eval.
- Nhánh kỹ thuật: `le-thanh-tung/solo-day03`; commit bằng chứng: [`fddd7ff`](https://github.com/griin-03/K5-L3B-DAY03-ALI33-ResearchAgentToolEval/commit/fddd7ff8bc306475031112582eeee98805b28f3b).

## 2. Phần việc phụ trách

Tôi chuẩn bị một phương án để nhóm so sánh trước khi chọn hoặc tích hợp bản nộp: setup môi trường và API, đo baseline, tối ưu prompt/tool declaration, thêm tool, kiểm thử, xây eval nhóm, làm UI, lưu live chat và triển khai demo trên VPS. Code và thao tác kỹ thuật có Codex hỗ trợ; phần dưới ghi rõ sản phẩm và bằng chứng kiểm tra.

## 3. Đóng góp cụ thể

| Hạng mục | Công việc và kết quả ghi nhận |
|---|---|
| Setup | Cấu hình các key cần thiết; xử lý subscription RapidAPI sau lỗi 403. Sau khi kích hoạt, timeline và search trả dữ liệu thật. |
| Baseline và tối ưu | Có sáu phiên bản `v0`, `v1`, `v2`, `v3`, `v4`, `v5-tools`; case accuracy lần lượt là 70%, 80%, 95%, 95%, 95%, 95% trên 20 case base. Các run được chọn có đủ 20 case đo và 0 provider error. |
| Prompt và tool declaration | v1 làm rõ phạm vi, hỏi lại và xác nhận; v2 làm rõ tham số bắt buộc và cách chọn tool; v3/v4 thử xử lý case còn sai nhưng không tăng điểm. v5-tools chọn lại nền v2 và tích hợp tool mới. |
| Tool mới | `deduplicate_sources` loại URL trùng theo quy tắc chuẩn hóa, giữ metadata của nguồn xuất hiện đầu tiên; có `TOOL.md`, đăng ký và khai báo schema. |
| Unit test và eval nhóm | Kết quả đã chạy: 97 passed, 0 failed, 0 skipped. Bộ nhóm đúng 10 case, gồm 5 single và 5 multi, kết quả 10/10; hai case dedup có kiểm tra payload/count riêng ngoài routing. |
| UI và live chat | UI Streamlit có hội thoại, tool calls, lỗi và tải transcript; bốn phiên CLI dùng API thật với tổng sáu lượt, gồm yêu cầu thường, bổ sung thông tin thiếu, xác nhận rồi hủy và tool mới. |
| Triển khai | Demo tại https://ali33.sunstudy.app trên VPS ARM 24GB, chạy service riêng với Nginx/HTTPS. Key ở phía server; giao diện mở trực tiếp không cần mã truy cập. Server local đã dừng theo yêu cầu. |
| Báo cáo | Tổng hợp kết quả, phân tích lỗi còn lại, liên kết log và khai báo đóng góp trong báo cáo nhóm và TEAM.md. |

## 4. Bằng chứng

Các liên kết kỹ thuật dưới đây trỏ tới commit cố định đã push để đối chiếu được kết quả, dù nhóm chưa chọn nhánh nộp cuối.

- File/commit/PR: [commit kỹ thuật fddd7ff](https://github.com/griin-03/K5-L3B-DAY03-ALI33-ResearchAgentToolEval/commit/fddd7ff8bc306475031112582eeee98805b28f3b), [báo cáo nhóm Phần A + B](group_report.md), [khai báo đóng góp trong TEAM.md](../../TEAM.md#lethanhtung-2a202603819).
- Các vòng thử nghiệm: [version_log.csv](https://github.com/griin-03/K5-L3B-DAY03-ALI33-ResearchAgentToolEval/blob/fddd7ff8bc306475031112582eeee98805b28f3b/starter_v0/artifacts/version_log.csv), [comparison.json](https://github.com/griin-03/K5-L3B-DAY03-ALI33-ResearchAgentToolEval/blob/fddd7ff8bc306475031112582eeee98805b28f3b/starter_v0/analysis/comparison.json), các run cụ thể tại mục B1 của báo cáo nhóm.
- Tool mới: [tool.py](https://github.com/griin-03/K5-L3B-DAY03-ALI33-ResearchAgentToolEval/blob/fddd7ff8bc306475031112582eeee98805b28f3b/starter_v0/tools/deduplicate_sources/tool.py), [TOOL.md](https://github.com/griin-03/K5-L3B-DAY03-ALI33-ResearchAgentToolEval/blob/fddd7ff8bc306475031112582eeee98805b28f3b/starter_v0/tools/deduplicate_sources/TOOL.md).
- Kiểm thử: [test_tools_todo.py](https://github.com/griin-03/K5-L3B-DAY03-ALI33-ResearchAgentToolEval/blob/fddd7ff8bc306475031112582eeee98805b28f3b/starter_v0/tests/test_tools_todo.py), [test_demo.py](https://github.com/griin-03/K5-L3B-DAY03-ALI33-ResearchAgentToolEval/blob/fddd7ff8bc306475031112582eeee98805b28f3b/starter_v0/tests/test_demo.py), [kết quả kiểm tra VPS](https://github.com/griin-03/K5-L3B-DAY03-ALI33-ResearchAgentToolEval/blob/fddd7ff8bc306475031112582eeee98805b28f3b/starter_v0/analysis/deployment.json).
- Eval nhóm và live chat: [eval_group.json](https://github.com/griin-03/K5-L3B-DAY03-ALI33-ResearchAgentToolEval/blob/fddd7ff8bc306475031112582eeee98805b28f3b/starter_v0/data/eval_group.json), [live summary](https://github.com/griin-03/K5-L3B-DAY03-ALI33-ResearchAgentToolEval/blob/fddd7ff8bc306475031112582eeee98805b28f3b/starter_v0/analysis/live-summary.json); run và transcript gốc được liên kết ở mục B3–B4 của báo cáo nhóm.
- UI/triển khai: [app.py](https://github.com/griin-03/K5-L3B-DAY03-ALI33-ResearchAgentToolEval/blob/fddd7ff8bc306475031112582eeee98805b28f3b/starter_v0/app.py), [hướng dẫn và cấu hình VPS](https://github.com/griin-03/K5-L3B-DAY03-ALI33-ResearchAgentToolEval/blob/fddd7ff8bc306475031112582eeee98805b28f3b/deploy/README.md).

**AI/công cụ đã dùng và cách kiểm tra kết quả:** Tôi dùng Codex để đọc đề, hỗ trợ viết code/test, thực thi API/eval, phân tích log, soạn tài liệu và triển khai theo yêu cầu. Việc kiểm tra trong quá trình làm gồm pytest, kiểm hợp đồng tool, đối chiếu input/output và transcript, kiểm hash snapshot, đọc run lỗi và kiểm API/HTTPS trên VPS. Các số liệu lấy từ lần chạy thật; tôi không ghi toàn bộ code là tự gõ hoặc gán phần của phương án này cho thành viên khác.

- Cập nhật giao diện mở trực tiếp: [commit `70c5f3a`](https://github.com/griin-03/K5-L3B-DAY03-ALI33-ResearchAgentToolEval/commit/70c5f3add97a06ef564097436c7a432dec897fa7), [bằng chứng 4 test UI pass và HTTPS 200](https://github.com/griin-03/K5-L3B-DAY03-ALI33-ResearchAgentToolEval/blob/70c5f3add97a06ef564097436c7a432dec897fa7/starter_v0/analysis/public-access.json). Thay đổi này chỉ bỏ mã truy cập, không thay prompt/tool hay số liệu eval đã báo cáo.

## 5. Tự đánh giá dựa trên bằng chứng

Phương án có code và bằng chứng cho các hạng mục kỹ thuật đã liệt kê; base tăng 25 điểm phần trăm so với baseline. Kết quả 95% chỉ phản ánh 19/20 case base, còn 10/10 là trên bộ case nhóm tự xây dựng; hai con số này chưa chứng minh mọi câu trả lời đều đúng.

Case R12 vẫn không đạt tiêu chí tự động: agent hỏi nội dung bằng `clarify(response_type=text)` trong khi nhãn đòi `yes_no`. Ngoài ra, một yêu cầu đọc `example.com` trên runtime VPS bị model hỏi lại trước khi gọi fetch. Cả hai hạn chế được giữ trong báo cáo. Các vòng v3/v4 không cải thiện cũng được giữ nguyên để đối chiếu. UI chặn gửi Telegram thật; chưa có bằng chứng gửi thật, local model hoặc người ngoài nhóm dùng thử.

Bước tiếp theo là review nguồn và câu trả lời, thử giả thuyết xử lý yêu cầu gửi khi thiếu nội dung, sửa hành vi đánh giá URL trước khi đọc và để nhóm so sánh/chọn phương án. Tôi cần tự đọc, dùng thử và giải thích được các thay đổi khi được hỏi; việc có log và AI hỗ trợ không thay thế yêu cầu hiểu bài. Báo cáo này không xác nhận thay phần việc, commit hoặc tự đánh giá của thành viên khác.
