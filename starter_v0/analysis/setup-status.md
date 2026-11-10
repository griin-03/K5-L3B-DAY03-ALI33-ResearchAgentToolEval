# Kiểm tra setup Day 03 — 10/11/2026 (GMT+7)

| Hạng mục | Kết quả thực tế |
|---|---|
| Unit/contract tests offline | 62 passed, 17 TODO skipped, 0 failed. |
| OpenRouter preflight | PASS; model `openai/gpt-4o-mini`, structured call `timeline(screenname="sama", limit=1)`. |
| Tavily / lookup | PASS; nhận 1 kết quả có nội dung. |
| Firecrawl / fetch | PASS; đọc `https://example.com`, nhận nội dung. |
| RapidAPI / timeline | PASS khi kiểm tra lại: HTTP 200, có nội dung. Lỗi subscription trước đó đã hết. |
| RapidAPI / social_search | PASS khi kiểm tra lại: HTTP 200, có nội dung. Lỗi subscription trước đó đã hết. |

## Cập nhật sau khi xử lý subscription

Cả timeline và social_search đã PASS bằng key đang lưu trong dự án tại 2026-11-10T18:07:41+07:00. OpenRouter, Tavily và Firecrawl đã PASS ở lượt kiểm tra trước.

Hướng dẫn dùng để xử lý lỗi trước đó: Đăng ký quyền sử dụng **Twitter API45** cho đúng tài khoản/app tương ứng với `RAPIDAPI_KEY` đang cấu hình tại https://rapidapi.com/alexanderxbx/api/twitter-api45. Nếu đã đăng ký trên tài khoản/app khác, kiểm tra lại key thuộc app đã có subscription. Hướng dẫn của đề: `../../docs/TOOL-SETUP.md`, mục 4.

Đã kiểm tra lại timeline và social_search thành công. Run baseline cũ bên dưới là kết quả trước khi lỗi subscription được xử lý; chưa chạy lại trong lượt xác nhận này. Không khởi chạy thêm base eval trong đợt kiểm tra API này; không sửa prompt, tools.yaml hoặc bộ eval; không push thay đổi.

Telegram là bonus, chưa có key/chat ID và không gửi tin nhắn trong đợt kiểm tra. Hai tool arXiv chưa được kiểm tra live trong đợt kiểm tra key này.

## Bằng chứng

- `setup-check-provider.json`: preflight thật.
- `setup-check-tools.json`: kết quả gọi tool thật.
- `setup-check-rapidapi-diagnostic.json`: phản hồi HTTP và thông báo của RapidAPI khi thử riêng từng endpoint.

Các báo cáo không lưu giá trị API key.

## Run baseline đã có trong workspace khi kiểm tra

- File: `runs/v0_B_base_openrouter_20261110T180101858976.json`.
- Routing/args eval: 14/20 case pass; case accuracy 70%, routing 75%, argument 70%; provider errors 0.
- Có 9 lượt thực thi tool trả error; trong run này các lỗi đều ở timeline/social_search. Điểm routing/args không có nghĩa API tool đã chạy thành công.
- Hash prompt/tools trùng bản hiện tại: True. Run này được đọc để đối chiếu, không được chạy lại hoặc chỉnh sửa trong đợt kiểm tra API.

- Bằng chứng kiểm tra lại thành công: `setup-check-rapidapi-recheck.json`.
