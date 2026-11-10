# Báo cáo cá nhân — HoVaTen-MSSV

Đổi tên file theo quy tắc `MSSV_HoTen.md`.

Ví dụ: `20241234_NguyenVanAn.md`.

## 1. Thông tin thành viên

- Họ tên: Nguyễn Mạnh Hùng
- MSSV: 2A202603852
- Email: nguyenmanhhunglun@gmail.com

## 2. Phần việc phụ trách

- Phụ trách phần giao diện người dùng và trải nghiệm chat, đảm bảo app hiển thị phản hồi dạng chat bot thân thiện thay vì JSON thô.
- Xây dựng và kiểm tra triển khai local app bằng Streamlit, đảm bảo ứng dụng có thể demo trực tiếp trên localhost.
- Hỗ trợ live chat demo và tích hợp các mô-đun chính để trình bày sản phẩm cho người xem.
- Chuẩn bị và cập nhật tài liệu, báo cáo cá nhân và ghi chú liên quan đến quy trình triển khai.

## 3. Đóng góp cụ thể

- Thiết kế lại `starter_v0/app.py` theo hướng chat UI rõ ràng, chỉ hiển thị phản hồi cuối cùng cho người dùng và ẩn tool debug mặc định.
- Kiểm tra luồng chạy UI local, xử lý lỗi liên quan tới đường dẫn venv/Streamlit và đảm bảo ứng dụng khởi động được trên port `8502`.
- Hỗ trợ demo live bằng cách chạy app và làm rõ cách người dùng tương tác với agent qua giao diện chat.
- Ghi lại tài liệu, bằng chứng chạy và báo cáo cá nhân để hoàn thiện nội dung nộp nhóm.

## 4. Bằng chứng

- Đã chỉnh `starter_v0/app.py` từ chế độ hiển thị JSON/raw output sang giao diện chat bot thực tế, chỉ hiện câu trả lời cuối cùng cho người dùng.
- Kiểm tra kỹ thuật bằng lệnh `python -m py_compile app.py` và chạy local demo bằng Streamlit trên `localhost:8502` để đảm bảo app có thể mở và tương tác.
- Đã thực hiện demo live và kiểm nghiệm luồng chat: người dùng nhập câu hỏi như `AI news`, app hiển thị phản hồi dạng văn bản thay vì hiển thị file JSON thô.
- Cập nhật tài liệu và báo cáo cá nhân trong `report/team/2A202603852_NguyenManhHung.md` để thể hiện quá trình triển khai, demo và kiểm tra sản phẩm.

## 5. Tự đánh giá

- Mình đã hiểu rõ quy trình đánh giá agent, cách đọc lỗi từ run JSON và cách tối ưu prompt/tool theo evidence. Tự đánh giá đạt mức tốt.
