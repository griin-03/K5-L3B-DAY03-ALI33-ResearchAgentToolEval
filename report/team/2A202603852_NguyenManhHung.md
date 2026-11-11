# Báo cáo cá nhân — HoVaTen-MSSV

Đổi tên file theo quy tắc `MSSV_HoTen.md`.

Ví dụ: `20241234_NguyenVanAn.md`.

## 1. Thông tin thành viên

- Họ tên: Nguyễn Mạnh Hùng
- MSSV: 2A202603852
- Email: nguyenmanhhunglun@gmail.com

## 2. Phần việc phụ trách

- Phụ trách phần giao diện người dùng và trải nghiệm chat dựa trên code gốc đã được nhóm trưởng pull về hệ thống, đảm bảo app hiển thị phản hồi dạng chat bot thân thiện thay vì JSON thô.
- Kiểm tra và đối chiếu luồng triển khai local app với cấu trúc hệ thống hiện có, đảm bảo ứng dụng demo hoạt động đúng với code chính của nhóm.
- Hỗ trợ live chat demo, tích hợp và trình bày giao diện theo mô-đun hiện có để người dùng dễ tương tác.
- Chuẩn bị và cập nhật tài liệu, báo cáo cá nhân và ghi chú theo đúng tiến độ của hệ thống và code đã được đồng bộ.

## 3. Đóng góp cụ thể

- Đối chiếu `starter_v0/app.py` với code nhóm trưởng đã pull về, sau đó chỉnh sửa theo hướng chat UI rõ ràng, chỉ hiển thị phản hồi cuối cùng cho người dùng và ẩn debug tool mặc định.
- Kiểm tra luồng chạy UI local với cấu trúc hệ thống hiện có, xử lý lỗi liên quan tới đường dẫn venv/Streamlit và đảm bảo ứng dụng khởi động trên port `8502`.
- Hỗ trợ demo live theo code chuẩn của nhóm, đảm bảo trải nghiệm người dùng tương ứng với phiên bản đã đồng bộ.
- Ghi lại tài liệu, bằng chứng chạy và báo cáo cá nhân dựa trên hệ thống và artifact đã được cập nhật trong repo.

## 4. Bằng chứng

- Đối chiếu với hệ thống và code đã pull từ nhóm trưởng, các thay đổi UI được thực hiện trên `starter_v0/app.py` nhằm chuyển từ raw JSON sang giao diện chat bot thân thiện cho người dùng.
- Kiểm tra kỹ thuật bằng lệnh `python -m py_compile app.py` và chạy local demo bằng Streamlit trên `localhost:8502` để xác nhận app khởi động theo đúng cấu trúc hệ thống đã đồng bộ.
- Đã thực hiện demo live qua giao diện chat và đối chiếu với luồng hoạt động của agent trên code nhóm trưởng: người dùng nhập câu hỏi như `AI news`, app hiển thị phản hồi dạng văn bản thay vì hiển thị file JSON thô.
- Đã đối chiếu log/transcript và kết quả đánh giá qua `starter_v0/runs/...json` cùng `starter_v0/artifacts/version_log.csv` để theo dõi phiên bản `v0` và `v1` trước/sau khi tối ưu prompt và UI.
- AI/công cụ được khai báo sử dụng: `OpenRouter` làm provider, `Python` + `Streamlit` cho demo, `run_eval.py` để đánh giá chất lượng, `system_prompt.md` và `tools.yaml` để điều chỉnh tool routing và output.
- File/commit chính liên quan: `starter_v0/app.py`, `starter_v0/artifacts/system_prompt.md`, `starter_v0/artifacts/tools.yaml`, `starter_v0/artifacts/version_log.csv`, `starter_v0/runs/`.
- Tất cả nội dung báo cáo và bằng chứng đều được đối chiếu với code nhóm trưởng đã pull về và hệ thống repo đang dùng.

## 5. Tự đánh giá

- Mình đã hiểu rõ quy trình đánh giá agent, cách đọc lỗi từ run JSON và cách tối ưu prompt/tool theo evidence. Tự đánh giá đạt mức tốt.
