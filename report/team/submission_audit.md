# Đối chiếu hồ sơ ALI33 — 11/11/2026

Đối chiếu [SUBMISSION.md](../../SUBMISSION.md), [RULES.md](../../RULES.md) và [RUBRIC.md](../../RUBRIC.md) với main tại [`fe835ac`](https://github.com/griin-03/K5-L3B-DAY03-ALI33-ResearchAgentToolEval/commit/fe835ac25a5476497d24c618bf6ddc23fbef0b28) và nhánh demo tại [`70c5f3a`](https://github.com/griin-03/K5-L3B-DAY03-ALI33-ResearchAgentToolEval/commit/70c5f3add97a06ef564097436c7a432dec897fa7).

**Cập nhật sau yêu cầu tích hợp:** code và log của nhánh demo đã được đưa vào **main**, giữ ba báo cáo cá nhân và lịch sử commit. Phần kỹ thuật của Tùng đã nằm trên nhánh nộp; phần còn cần bổ sung là bằng chứng đóng góp, commit kỹ thuật và khai báo AI của Nghĩa/Hùng. Các SHA phía trên là mốc kiểm tra trước khi tích hợp.

## 1. Cá nhân và sự thống nhất trong TEAM.md

| Thành viên | Đã có | Còn cần hoàn thiện |
|---|---|---|
| Tùng — 2A202603819 | Báo cáo đúng tên, thông tin, khai báo Codex, link code/run/transcript và hạn chế. Commit kỹ thuật `fddd7ff`, `70c5f3a` đã được merge vào lịch sử main. | Đã tích hợp; commit chốt mã được ghi trong TEAM.md. |
| Nghĩa — 2A202603805 | Báo cáo được thêm qua `fe835ac`, phân tích tool/test/eval và số liệu phù hợp phương án v5-tools; ghi rõ phạm vi kế thừa và môi trường thiếu Streamlit. | Khai báo AI/công cụ đã dùng và cách kiểm tra; commit kỹ thuật, bằng chứng review/test do mình thực hiện. Báo cáo còn checklist chưa hoàn tất ở mục 10. |
| Hùng — 2A202603852 | Báo cáo được thêm qua `3265061`, `dfd2551`, khai báo phần UI/local/live demo. | Push hoặc liên kết commit chỉnh UI cùng log/transcript tương ứng; khai báo AI/công cụ đã dùng. Các commit hiện thấy của Hùng chỉ chứa báo cáo. |

- Tên, MSSV, email của ba người khớp danh sách nhóm.
- Nghĩa và Tùng thống nhất số liệu base 70% → 95%, group 10/10 và lỗi R12. Nghĩa dẫn kết quả 97 test từ tài liệu, không nhận đã chạy thành công trong môi trường của mình.
- Hùng mô tả UI local port 8502; demo VPS dùng 8503. Hai cổng có thể thuộc hai môi trường khác nhau, nhưng cần commit/log để đối chiếu phiên bản UI và tránh gán lẫn đóng góp.
- Nếu không dùng AI, thành viên cần tự ghi rõ điều đó; người tổng hợp không xác nhận thay. Không tạo commit dưới tên người khác để đáp ứng tiêu chí C8.

## 2. Bài nhóm và code thực tế

| Hạng mục bắt buộc | Main sau tích hợp | Nguồn đối chiếu |
|---|---|---|
| Báo cáo nhóm Phần A + B | Có, cập nhật lệnh chạy từ main. | Giữ báo cáo nhóm mới nhất. |
| Ba báo cáo cá nhân | Có đủ; giữ báo cáo của Nghĩa/Hùng. | Main trước tích hợp. |
| UI `starter_v0/app.py` | Có Streamlit và runtime, mở trực tiếp không cần mã. | `70c5f3a`. |
| Tool mới + tài liệu + đăng ký | Có đủ `deduplicate_sources`. | Nhánh nguồn của Tùng. |
| Version log v0–v3 trở lên | 6 dòng: v0–v5-tools. | Snapshot và run JSON. |
| Run JSON | 8 file: 6 run base được chọn, 1 group và 1 run chẩn đoán cũ. | Giữ nguyên log gốc. |
| Eval nhóm | Đúng 10: 5 single + 5 multi; metadata/expect đầy đủ, có route tới tool mới. | Dataset và run group. |
| Transcript live | 4 phiên, tổng 6 lượt; đủ các tình huống yêu cầu. | Transcript gốc của nhánh nguồn. |
| Commit kỹ thuật của mỗi người trên nhánh nộp | Đã có lịch sử kỹ thuật của Tùng; Nghĩa/Hùng còn thiếu bằng chứng tương ứng. | Không gán lại tác giả commit. |

Code, dependency, run, transcript và báo cáo hiện cùng nằm trên main. Việc merge giữ hai commit kỹ thuật của Tùng và các commit báo cáo của Nghĩa/Hùng. Người chấm có thể lấy source main và chạy theo mục A1 trong báo cáo nhóm; API key tự cấu hình theo hướng dẫn, không nằm trong repo.

## 3. Kiểm tra bằng chứng kỹ thuật

- Đối chiếu cả 6 run base với version log: mỗi run có `provider_error_cases = 0`, `measured_cases = total_cases = 20`; metric khớp CSV; SHA-256 prompt/tools khớp snapshot từng phiên bản.
- Prompt/tools đang dùng khớp snapshot v5-tools. Hai bộ base/extension giữ nguyên nội dung so với starter tại `32e7cda`.
- Đã chạy lại **toàn bộ unit test offline trên VPS đang demo**, không chạy model/eval trên laptop:

```text
cd /opt/ali33-research/current/starter_v0
sudo -u ali33-demo env PYTHONDONTWRITEBYTECODE=1 \
  /opt/ali33-research/.venv/bin/python -m pytest -q -p no:cacheprovider

97 passed in 1.09s
```

- Kiểm tra thêm đúng gói source sau merge: xuất Git index bằng `git archive`, giải nén vào thư mục tạm trên VPS rồi chạy toàn suite offline; kết quả **97 passed in 1.16s**. Không thay service và không chạy API/eval mới.
- Service `ali33-research` đang active; release `20261110-v5-tools-public`. Kết quả này xác nhận bản demo chung, không thay thế bằng chứng cá nhân của Nghĩa hoặc Hùng.
- Lỗi R12 và lần runtime hỏi lại URL trước khi gọi fetch vẫn là các hạn chế đã ghi nhận. Không đổi nhãn, không nâng metric và không chạy lại API để làm đẹp điểm.
- Không có `.env`, `.env.deploy` hoặc `.venv` trong danh sách file Git của hai nhánh được kiểm tra.

## 4. Sửa trong lần đối chiếu này và việc còn lại

Đã cập nhật trạng thái báo cáo Nghĩa trong TEAM.md/báo cáo nhóm; sửa ba liên kết bằng chứng đang trỏ nhầm bản mẫu trên main (`version_log.csv`, `eval_group.json`, `test_tools_todo.py`); sửa tiêu đề còn tên mẫu trong báo cáo Hùng. Nội dung tự khai, kết quả và tự đánh giá của hai bạn được giữ nguyên.

Các việc còn lại trước khi xác nhận đủ bài:

1. **Đã thực hiện:** chọn main làm nhánh tích hợp, đưa code và báo cáo về cùng nhánh và giữ lịch sử tác giả. Commit chốt mã ghi trong TEAM.md.
2. Nghĩa và Hùng bổ sung khai báo AI, phần việc kỹ thuật thực tế, commit và log tương ứng; cập nhật TEAM.md theo bằng chứng mới.
3. Mỗi thành viên tự nộp link repo trên LMS. Trạng thái LMS, thông báo gia hạn và khả năng tự giải thích bài không xác minh được bằng kiểm tra Git này.

Bonus Telegram gửi thật/local model/nhiều tool mới không phải phần bắt buộc còn thiếu; giữ đúng việc nhóm chưa thực hiện. Mọi bổ sung tiếp theo dùng commit mới, giữ đúng ngày và lịch sử theo RULES.md.
