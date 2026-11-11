# Team — ALI33

## Thông tin nhóm

- Tên nhóm: **ALI33**.
- Lớp: **L3B**, khóa K5, Day 03 — Research Agent Tool Eval.
- Repo nhóm: [K5-L3B-DAY03-ALI33-ResearchAgentToolEval](https://github.com/griin-03/K5-L3B-DAY03-ALI33-ResearchAgentToolEval).
- Báo cáo chính: [report/team/group_report.md](report/team/group_report.md).
- Nhánh tích hợp code, log và báo cáo để nộp: **`main`**.
- Nhánh nguồn đã được tích hợp: [`le-thanh-tung/solo-day03`](https://github.com/griin-03/K5-L3B-DAY03-ALI33-ResearchAgentToolEval/tree/le-thanh-tung/solo-day03).
- Commit kỹ thuật dùng làm bằng chứng: [`fddd7ff8bc306475031112582eeee98805b28f3b`](https://github.com/griin-03/K5-L3B-DAY03-ALI33-ResearchAgentToolEval/commit/fddd7ff8bc306475031112582eeee98805b28f3b).
- Cập nhật UI mở trực tiếp, không cần mã demo: [commit `70c5f3a`](https://github.com/griin-03/K5-L3B-DAY03-ALI33-ResearchAgentToolEval/commit/70c5f3add97a06ef564097436c7a432dec897fa7), [bằng chứng kiểm tra VPS](https://github.com/griin-03/K5-L3B-DAY03-ALI33-ResearchAgentToolEval/blob/70c5f3add97a06ef564097436c7a432dec897fa7/starter_v0/analysis/public-access.json).
- Commit tích hợp chốt code/run: [`ccb7fb6`](https://github.com/griin-03/K5-L3B-DAY03-ALI33-ResearchAgentToolEval/commit/ccb7fb6b26b4a766cbf844b8515d6d1178f6b1cf). Đã đưa phương án của Tùng vào **main**, giữ lịch sử commit và báo cáo của cả ba thành viên; commit nguồn UI: `70c5f3a`.

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
| Cấn Xuân Nghĩa — 2A202603805 | [2A202603805_CanXuanNghia.md](report/team/2A202603805_CanXuanNghia.md) | Đã có báo cáo phân tích tool/test/eval; chưa có commit kỹ thuật và khai báo công cụ AI để đối chiếu. |
| Nguyễn Mạnh Hùng — 2A202603852 | [2A202603852_NguyenManhHung.md](report/team/2A202603852_NguyenManhHung.md) | Đã có báo cáo cá nhân tự khai phần UI/live demo, liên kết commit code và log để đối chiếu. |

## LeThanhTung-2A202603819

### Phần việc phụ trách

Chuẩn bị phương án kỹ thuật và tích hợp lên main: setup API, đo baseline, tối ưu prompt/tool declaration, bổ sung tool, kiểm thử, eval nhóm, UI, live chat và triển khai demo trên VPS.

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

Theo báo cáo do Nghĩa bổ sung: rà soát `deduplicate_sources`, unit test, 10 case eval nhóm, diễn giải metric và đề xuất cải thiện.

### Đóng góp cụ thể

Báo cáo mô tả tool, đối chiếu các tình huống test/eval và phân tích kết quả 70% → 95%, group 10/10. Nghĩa ghi rõ không nhận các code/test/run có sẵn là do mình tạo; lần kiểm tra trong môi trường của bạn ấy còn thiếu Streamlit. Phần đã phân tích trong báo cáo cần phân biệt với phần code/test trực tiếp thực hiện.

### Bằng chứng

- [Báo cáo cá nhân của Nghĩa](report/team/2A202603805_CanXuanNghia.md), được thêm trên main qua commit `fe835ac`.
- Cần bổ sung commit kỹ thuật, log kiểm tra do thành viên thực hiện và khai báo công cụ AI theo [RULES.md](RULES.md). Kết quả pytest chung trên VPS không thay thế bằng chứng đóng góp riêng.


## NguyenManhHung-2A202603852

### Phần việc phụ trách

Theo hướng dẫn và hệ thống repo đã tích hợp trên `main`, phần công việc của Hùng tập trung vào giao diện chat người dùng, kiểm tra triển khai local, hỗ trợ demo live và chuẩn bị tài liệu/ghi nhận bằng chứng theo đúng code nhóm trưởng đã pull về. Đây là phần phù hợp với branch tích hợp và cấu trúc hiện có của project, không tự khẳng định mình là người viết phần nền tảng kỹ thuật core của nhóm.

### Đóng góp cụ thể

- Đối chiếu `starter_v0/app.py` với code đã được nhóm trưởng pull về hệ thống và điều chỉnh giao diện sang kiểu chat bot thân thiện, chỉ hiển thị nội dung phản hồi cuối cùng cho người dùng, không hiện raw JSON.
- Kiểm tra luồng khởi chạy local app bằng Streamlit, giải quyết lỗi đường dẫn/venv và đảm bảo app chạy đúng trên port `8502` theo cấu hình local demo.
- Hỗ trợ live demo bằng cách chạy app và kiểm tra flow người dùng tương tác qua chat, bao gồm câu hỏi kiểu `AI news` và các trường hợp cần phản hồi text rõ ràng.
- Cập nhật tài liệu cá nhân và báo cáo theo đúng tiêu chuẩn repo, đồng thời ghi nhận lại bằng chứng, log và transcript để đối chiếu với hệ thống hiện có.
- Đảm bảo nội dung báo cáo, log và bằng chứng được căn cứ vào repo đang sử dụng và code đã đồng bộ trên `main`, không giả định các phần không thuộc phạm vi cá nhân.

### Bằng chứng

- [Báo cáo cá nhân của Hùng](report/team/2A202603852_NguyenManhHung.md), đã được bổ sung và cập nhật theo đúng quy chuẩn file cá nhân `MSSV_HoTen.md`.
- File code giao diện chính: [`starter_v0/app.py`](starter_v0/app.py) — chỉnh giao diện chat, ẩn debug JSON mặc định, chỉ hiển thị phản hồi cuối cùng cho người dùng.
- File hệ thống được đối chiếu và dùng làm nền tảng: [`starter_v0/artifacts/system_prompt.md`](starter_v0/artifacts/system_prompt.md), [`starter_v0/artifacts/tools.yaml`](starter_v0/artifacts/tools.yaml), [`starter_v0/artifacts/version_log.csv`](starter_v0/artifacts/version_log.csv), [`starter_v0/runs/`](starter_v0/runs/).
- Kiểm tra kỹ thuật local: chạy `python -m py_compile app.py` và khai thác Streamlit UI trên `localhost:8502` để xác nhận app chạy được theo đúng cấu trúc repo đã sync.
- AI/công cụ đã dùng: `OpenRouter` làm provider để chạy eval/demo, `Streamlit` để chạy UI và demo live, `Python` và file run log/transcript để đối chiếu hiệu quả; cách tự kiểm tra là đọc kết quả từ `run_eval.py`, `version_log.csv` và phản hồi chat thực tế trên app.
- Công việc này được báo cáo dựa trên code đã pull từ nhóm trưởng và repo hệ thống đang dùng, phù hợp với quy định về đối chiếu và minh bạch trong `RULES.md`.

## Kiểm tra trước khi chốt bài

Xem [đối chiếu ngày 11/11/2026](report/team/submission_audit.md) để biết những mục đã có, khác biệt giữa main và nhánh demo, cùng phần từng thành viên cần bổ sung. Code, log và báo cáo hiện đã được tích hợp trên main.
