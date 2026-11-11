# Đối chiếu hồ sơ ALI33 — 11/11/2026

Đối chiếu [SUBMISSION.md](../../SUBMISSION.md), [RULES.md](../../RULES.md) và [RUBRIC.md](../../RUBRIC.md) với main tại [`fe835ac`](https://github.com/griin-03/K5-L3B-DAY03-ALI33-ResearchAgentToolEval/commit/fe835ac25a5476497d24c618bf6ddc23fbef0b28) và nhánh demo tại [`70c5f3a`](https://github.com/griin-03/K5-L3B-DAY03-ALI33-ResearchAgentToolEval/commit/70c5f3add97a06ef564097436c7a432dec897fa7).

**Kết luận:** đủ ba file báo cáo cá nhân; bản demo có code và bằng chứng kỹ thuật, nhưng hồ sơ nhóm chưa hoàn tất vì chưa chốt/tích hợp nhánh nộp và chưa có đủ bằng chứng đóng góp cá nhân. Không suy ra một thành viên chưa làm việc chỉ vì bằng chứng chưa được push.

## 1. Cá nhân và sự thống nhất trong TEAM.md

| Thành viên | Đã có | Còn cần hoàn thiện |
|---|---|---|
| Tùng — 2A202603819 | Báo cáo đúng tên, thông tin, khai báo Codex, link code/run/transcript và hạn chế. Có commit kỹ thuật `fddd7ff`, `70c5f3a` trên nhánh riêng. | Đưa phần kỹ thuật vào lịch sử nhánh nhóm chọn nộp và chốt commit; hiện các commit này chưa nằm trên main. |
| Nghĩa — 2A202603805 | Báo cáo được thêm qua `fe835ac`, phân tích tool/test/eval và số liệu phù hợp phương án v5-tools; ghi rõ phạm vi kế thừa và môi trường thiếu Streamlit. | Khai báo AI/công cụ đã dùng và cách kiểm tra; commit kỹ thuật, bằng chứng review/test do mình thực hiện. Báo cáo còn checklist chưa hoàn tất ở mục 10. |
| Hùng — 2A202603852 | Báo cáo được thêm qua `3265061`, `dfd2551`, khai báo phần UI/local/live demo. | Push hoặc liên kết commit chỉnh UI cùng log/transcript tương ứng; khai báo AI/công cụ đã dùng. Các commit hiện thấy của Hùng chỉ chứa báo cáo. |

- Tên, MSSV, email của ba người khớp danh sách nhóm.
- Nghĩa và Tùng thống nhất số liệu base 70% → 95%, group 10/10 và lỗi R12. Nghĩa dẫn kết quả 97 test từ tài liệu, không nhận đã chạy thành công trong môi trường của mình.
- Hùng mô tả UI local port 8502; demo VPS dùng 8503. Hai cổng có thể thuộc hai môi trường khác nhau, nhưng cần commit/log để đối chiếu phiên bản UI và tránh gán lẫn đóng góp.
- Nếu không dùng AI, thành viên cần tự ghi rõ điều đó; người tổng hợp không xác nhận thay. Không tạo commit dưới tên người khác để đáp ứng tiêu chí C8.

## 2. Bài nhóm và code thực tế

| Hạng mục bắt buộc | Main tại thời điểm kiểm tra | Nhánh demo `70c5f3a` |
|---|---|---|
| Báo cáo nhóm Phần A + B | Có; ghi rõ đây là phương án chờ nhóm lựa chọn. | Có báo cáo phương án. |
| Ba báo cáo cá nhân | Có đủ. | Chỉ có báo cáo Tùng; chưa nhận báo cáo hai bạn từ main. |
| UI `starter_v0/app.py` | Chưa có. | Có Streamlit và runtime. |
| Tool mới + tài liệu + đăng ký | Chưa có `deduplicate_sources`. | Có đủ. |
| Version log v0–v3 trở lên | 0 dòng dữ liệu. | 6 dòng: v0–v5-tools. |
| Run JSON | 0. | 8, gồm 6 run base được chọn, 1 group và 1 run chẩn đoán cũ. |
| Eval nhóm | 0 case. | Đúng 10: 5 single + 5 multi, metadata/expect đầy đủ, có route tới tool mới. |
| Transcript live | 0. | 4 phiên, tổng 6 lượt, có tra cứu thường, hỏi thiếu thông tin rồi bổ sung, yêu cầu gửi rồi hủy. |
| Commit kỹ thuật của mỗi người trên nhánh nộp | Chưa đáp ứng. | Hiện mới có bằng chứng commit kỹ thuật của Tùng. |

Vì vậy, clone main rồi làm theo lệnh chạy UI sẽ chưa tái lập được bản demo. Khi nhóm quyết định chọn/tích hợp phương án, cần đưa code, dependency, run, transcript và báo cáo về cùng nhánh nộp, giữ lịch sử tác giả thật và điền commit chốt trong TEAM.md. Chưa thực hiện bước chọn/merge phương án trong lần kiểm tra này.

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

- Service `ali33-research` đang active; release `20261110-v5-tools-public`. Kết quả này xác nhận bản demo chung, không thay thế bằng chứng cá nhân của Nghĩa hoặc Hùng.
- Lỗi R12 và lần runtime hỏi lại URL trước khi gọi fetch vẫn là các hạn chế đã ghi nhận. Không đổi nhãn, không nâng metric và không chạy lại API để làm đẹp điểm.
- Không có `.env`, `.env.deploy` hoặc `.venv` trong danh sách file Git của hai nhánh được kiểm tra.

## 4. Sửa trong lần đối chiếu này và việc còn lại

Đã cập nhật trạng thái báo cáo Nghĩa trong TEAM.md/báo cáo nhóm; sửa ba liên kết bằng chứng đang trỏ nhầm bản mẫu trên main (`version_log.csv`, `eval_group.json`, `test_tools_todo.py`); sửa tiêu đề còn tên mẫu trong báo cáo Hùng. Nội dung tự khai, kết quả và tự đánh giá của hai bạn được giữ nguyên.

Các việc còn lại trước khi xác nhận đủ bài:

1. Nhóm chốt phương án và nhánh/commit nộp, tích hợp code và báo cáo để người chấm kiểm được trong cùng nhánh.
2. Nghĩa và Hùng bổ sung khai báo AI, phần việc kỹ thuật thực tế, commit và log tương ứng; cập nhật TEAM.md theo bằng chứng mới.
3. Mỗi thành viên tự nộp link repo trên LMS. Trạng thái LMS, thông báo gia hạn và khả năng tự giải thích bài không xác minh được bằng kiểm tra Git này.

Bonus Telegram gửi thật/local model/nhiều tool mới không phải phần bắt buộc còn thiếu; giữ đúng việc nhóm chưa thực hiện. Mọi bổ sung tiếp theo dùng commit mới, giữ đúng ngày và lịch sử theo RULES.md.
