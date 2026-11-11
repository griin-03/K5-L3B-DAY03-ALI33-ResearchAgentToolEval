# Báo cáo nhóm — ALI33 Research Desk

> Báo cáo tổng hợp kết quả đã ghi nhận cho ALI33 từ phương án do **Lê Thanh Tùng — 2A202603819** chuẩn bị, có Codex hỗ trợ thực hiện. Bằng chứng kỹ thuật được cố định tại commit [`fddd7ff`](https://github.com/griin-03/K5-L3B-DAY03-ALI33-ResearchAgentToolEval/commit/fddd7ff8bc306475031112582eeee98805b28f3b) trên nhánh `le-thanh-tung/solo-day03`.
>
> Code, dependency, tool mới, test, run, transcript và ba báo cáo cá nhân đã được tích hợp trên **`main`** theo yêu cầu trưởng nhóm. Các liên kết commit giữ nguyên để đối chiếu lịch sử đo. Nghĩa/Hùng tiếp tục bổ sung bằng chứng đóng góp và khai báo AI của từng người.

## 1. Thông tin nhóm

- Nhóm **ALI33**, lớp **L3B**; thành viên xem [TEAM.md](../../TEAM.md).
- Provider/model cố định: **OpenRouter / openai/gpt-4o-mini**, temperature 0.
- Bản kỹ thuật tích hợp: **v5-tools**, gồm cập nhật UI mở trực tiếp từ `70c5f3a`; nhánh nộp: **main**.

## 2. PHẦN A — Giới thiệu agent

### A1. Agent làm được gì?

Research Desk tìm nguồn web và bài đăng X, đọc URL, lọc nguồn trùng và hỗ trợ tổng hợp có dẫn chứng. Người dùng xem được tool calls và lỗi; gửi Telegram bị tắt trong UI demo.

**Link dùng thử:** https://ali33.sunstudy.app — mở trực tiếp, không cần mã truy cập. Đã triển khai HTTPS và kiểm tra truy cập từ bên ngoài; smoke test tin tức và bài X trên VPS thành công. Một yêu cầu đọc URL còn bị model hỏi lại trước khi gọi fetch, được ghi ở phần hạn chế. API key chỉ ở server, không nằm trong báo cáo/repo. Cập nhật UI bỏ màn hình nhập mã tại [commit `70c5f3a`](https://github.com/griin-03/K5-L3B-DAY03-ALI33-ResearchAgentToolEval/commit/70c5f3add97a06ef564097436c7a432dec897fa7); [kiểm tra truy cập trực tiếp](https://github.com/griin-03/K5-L3B-DAY03-ALI33-ResearchAgentToolEval/blob/70c5f3add97a06ef564097436c7a432dec897fa7/starter_v0/analysis/public-access.json) ghi 4 test UI pass trên VPS và HTTPS trả 200. Các log eval bên dưới vẫn trỏ tới commit đã đo trước đó.

**Chạy từ source:** `git clone --branch main https://github.com/griin-03/K5-L3B-DAY03-ALI33-ResearchAgentToolEval.git`, vào thư mục repo rồi `cd starter_v0`, tạo môi trường và cấu hình `.env` theo [hướng dẫn](../../docs/TOOL-SETUP.md), rồi `python -m streamlit run app.py --server.port 8503`. Dependency có trong `requirements.txt`; `requirements.lock.txt` ghi phiên bản dùng cho bản này. Hiện ứng dụng local đã tắt theo yêu cầu; demo chạy trên VPS ARM 24GB bằng service riêng.

### A2. Tool đang khai báo

| Tool | Công dụng | Mới? |
|---|---|---|
| clarify | Hỏi thông tin còn thiếu hoặc xin xác nhận; chờ lượt sau. | Không |
| timeline | Lấy bài đăng của một tài khoản X. | Không |
| social_search | Tìm bài X theo chủ đề, Top/Latest. | Không |
| lookup | Tìm web/tin tức với khoảng thời gian. | Không |
| fetch | Đọc URL đã được cung cấp. | Không |
| format | Định dạng nguồn đã có thành digest. | Không |
| deduplicate_sources | Loại URL trùng, giữ nguồn và metadata xuất hiện đầu tiên. | **Có** |
| policy | Tìm policy mẫu của lab; không phải chính sách thật của SunStudy. | Không |
| papers / paper_text | Tìm arXiv / trích nội dung paper; chưa kiểm tra live trong phương án này. | Không |
| send | Tool có sẵn; chỉ được yêu cầu sau xác nhận. UI chặn gửi thật ở code. | Không |

### A3. Câu hỏi mẫu

1. “Tìm 2 tin AI hôm nay trên web, viết bản tin ngắn có link nguồn.”
2. “Lấy 3 tweet mới nhất của Sam Altman, giữ link từng bài.”
3. “Đọc https://example.com và tóm tắt ngắn.”
4. “Lọc trùng nguồn này: [{"url":"https://example.com/a?utm_source=demo"},{"url":"https://example.com/a"}].”
5. “Gửi nội dung 'ALI33 demo' lên Telegram.” → kiểm tra câu hỏi xác nhận; có thể trả lời “Không gửi”. Không có tin nhắn thật được gửi trong demo.

## 3. Giải pháp

- `v1`: thay chỉ dẫn đoán/làm ngay bằng phạm vi, hỏi lại và boundary xác nhận.
- `v2`: làm rõ khi dùng/không dùng từng tool; yêu cầu ghi rõ `response_type` và `topic`, quy ước handle, số lượng, thời gian và Top/Latest.
- `v3`: thử ưu tiên nhận diện ý định gửi trước thu thập thông tin thiếu. Không tăng điểm.
- `v4`: thử bỏ mặc định `text` và bổ sung ví dụ trong schema. Không tăng điểm.
- `v5-tools`: chọn lại nền v2 đơn giản hơn vì cùng đạt 95%, tích hợp tool mới và quy trình thu thập → lọc trùng nếu được yêu cầu → trình bày → dừng. Đây là vòng tích hợp, không quy lợi ích riêng cho từng thay đổi.
- Mỗi run dùng snapshot bất biến tại `artifacts/versions/<version>/`, kèm hash và log thật. Không sửa bộ base/extension. Trong eval và live smoke, delivery credentials bị vô hiệu hóa; UI chặn `send` bằng executor riêng nhưng vẫn lưu đúng tool call model đã yêu cầu.

## 4. PHẦN B — Kết quả và bằng chứng

### B1. Version evidence

| Version | Artifact thay đổi | Giả thuyết | Case accuracy | Routing | Arguments | Multi-turn | Run |
|---|---|---|---:|---:|---:|---:|---|
| v0 | baseline | Measure the unmodified starter after all required research APIs pass smoke checks | 70% | 75% | 70% | 100% | [v0_B_base_openrouter_20261110T181759944480.json](https://github.com/griin-03/K5-L3B-DAY03-ALI33-ResearchAgentToolEval/blob/fddd7ff8bc306475031112582eeee98805b28f3b/starter_v0/runs/v0_B_base_openrouter_20261110T181759944480.json) |
| v1 | system_prompt.md | Replacing guess-and-act defaults with explicit scope, clarification and approval rules fixes control-flow failures | 80% | 100% | 80% | 100% | [v1_B_base_openrouter_20261110T182153539084.json](https://github.com/griin-03/K5-L3B-DAY03-ALI33-ResearchAgentToolEval/blob/fddd7ff8bc306475031112582eeee98805b28f3b/starter_v0/runs/v1_B_base_openrouter_20261110T182153539084.json) |
| v2 | tools.yaml | Explicit required response types and news topics plus routing descriptions prevent omitted or defaulted arguments | 95% | 100% | 95% | 100% | [v2_B_base_openrouter_20261110T182710308956.json](https://github.com/griin-03/K5-L3B-DAY03-ALI33-ResearchAgentToolEval/blob/fddd7ff8bc306475031112582eeee98805b28f3b/starter_v0/runs/v2_B_base_openrouter_20261110T182710308956.json) |
| v3 | system_prompt.md | Giving delivery-intent confirmation priority over generic missing-input collection fixes the remaining boundary argument error | 95% | 100% | 95% | 100% | [v3_B_base_openrouter_20261110T182936844823.json](https://github.com/griin-03/K5-L3B-DAY03-ALI33-ResearchAgentToolEval/blob/fddd7ff8bc306475031112582eeee98805b28f3b/starter_v0/runs/v3_B_base_openrouter_20261110T182936844823.json) |
| v4 | tools.yaml | Removing the unconditional text default and adding intent-based schema examples disambiguates send confirmation from data collection | 95% | 100% | 95% | 100% | [v4_B_base_openrouter_20261110T183251279072.json](https://github.com/griin-03/K5-L3B-DAY03-ALI33-ResearchAgentToolEval/blob/fddd7ff8bc306475031112582eeee98805b28f3b/starter_v0/runs/v4_B_base_openrouter_20261110T183251279072.json) |
| v5-tools | v2-selected plus tool/workflow integration | The simpler tied-best v2 policy can support source deduplication and bounded multi-step research without regression on base cases | 95% | 100% | 95% | 100% | [v5-tools_B_base_openrouter_20261110T184001500765.json](https://github.com/griin-03/K5-L3B-DAY03-ALI33-ResearchAgentToolEval/blob/fddd7ff8bc306475031112582eeee98805b28f3b/starter_v0/runs/v5-tools_B_base_openrouter_20261110T184001500765.json) |

Tất cả các run được chọn ở bảng có **provider_error_cases = 0**, **measured_cases = total_cases = 20**, và không có tool-execution error. Bản cuối tăng từ **70% lên 95% (+25 điểm phần trăm)** trên bộ base, không phải bảo đảm 95% đúng cho mọi yêu cầu. Bằng chứng tổng hợp: [version_log.csv](https://github.com/griin-03/K5-L3B-DAY03-ALI33-ResearchAgentToolEval/blob/fddd7ff8bc306475031112582eeee98805b28f3b/starter_v0/artifacts/version_log.csv), [comparison.json](https://github.com/griin-03/K5-L3B-DAY03-ALI33-ResearchAgentToolEval/blob/fddd7ff8bc306475031112582eeee98805b28f3b/starter_v0/analysis/comparison.json).

### B2. Failure analysis

Đối chiếu run v0 với các vòng sau; giữ cả những thử nghiệm không cải thiện.

| Case | Loại lỗi v0 | Tool thực tế v0 | Sai ở đâu | Vòng đầu đạt |
|---|---|---|---|---|
| R08_out_of_scope | out_of_scope | send | expected no tool call | v1 |
| R10_missing_handle | missing_info | timeline | missing tool call clarify; extra tool call timeline | v2 |
| R11_missing_url | missing_info | fetch | missing tool call clarify; extra tool call fetch | v2 |
| R12_confirm_before_send | wrong_boundary | send | missing tool call clarify; extra tool call send | Chưa đạt tiêu chí tự động; xem phân tích bên dưới |
| R13_parallel_web_and_tweets | wrong_tool | lookup, social_search | query: expected 'AI', got 'AI news'; topic: expected 'news', got None | v2 |
| R14_out_of_scope_coding | out_of_scope | send | expected no tool call | v1 |

**Case còn sai R12:** yêu cầu “Đăng bản tin này…” không có nội dung. Bản cuối gọi `clarify(response_type=text)` để xin nội dung, trong khi nhãn yêu cầu `yes_no`; không gọi `send`. Đây vẫn là FAIL theo rubric tự động, không đổi nhãn để làm đẹp điểm. Live chat khi có nội dung cụ thể đã hỏi xác nhận, rồi không gọi tool sau khi người dùng hủy. Không đánh đồng kết quả an toàn quan sát được với việc đạt toàn bộ tiêu chí tự động.

### B3. Eval nhóm: 5 single + 5 multi

Dataset được khóa trước khi chạy suite group; SHA-256: `c7fd16074cfff75fe133136e598954915c39a5a7683e80d4449b47b313250055`. Không chỉnh case theo kết quả group.

| ID | Loại | Kiểm tra | Kỳ vọng | Kết quả |
|---|---|---|---|---|
| G01_dedup_tracking_sources | single | Route supplied URL objects to the new local tool; manually verify 3 inputs, 2 unique, first metadata retained. | deduplicate_sources | PASS |
| G02_health_news_month_limit | single | Combine monthly news window with an explicit result count in a different domain. | lookup | PASS |
| G03_read_supplied_example_url | single | Honor an explicit URL and restriction against replacing the source. | fetch | PASS |
| G04_at_handle_limit | single | Strip a literal @ while preserving the supplied handle and count. | timeline | PASS |
| G05_account_management_outside_scope | single | An unrelated account-management action must not trigger research or delivery tools. | no_tool | PASS |
| G06_still_missing_account | multi | An earlier clarification does not authorize guessing when the account remains missing. | clarify | PASS |
| G07_change_source_keep_window | multi | Source switch plus carried weekly window and a new count; no stale social search. | lookup | PASS |
| G08_cancel_delivery | multi | An explicit cancellation overrides the earlier send request; no delivery and no unnecessary tools. | no_tool | PASS |
| G09_dedup_latest_payload | multi | Carry the latest supplied payload to the new tool; manually verify two inputs and one unique source. | deduplicate_sources | PASS |
| G10_change_social_order_and_limit | multi | Carry a corrected ordering and final count across turns without stale arguments. | social_search | PASS |

Kết quả: **10/10**, provider errors **0**. [v5-tools_B_group_openrouter_20261110T184039678428.json](https://github.com/griin-03/K5-L3B-DAY03-ALI33-ResearchAgentToolEval/blob/fddd7ff8bc306475031112582eeee98805b28f3b/starter_v0/runs/v5-tools_B_group_openrouter_20261110T184039678428.json); [dataset](https://github.com/griin-03/K5-L3B-DAY03-ALI33-ResearchAgentToolEval/blob/fddd7ff8bc306475031112582eeee98805b28f3b/starter_v0/data/eval_group.json).

Hai case dedup tự động chấm routing; kiểm tra payload/count riêng cho thấy G01 giữ 3 đầu vào → 2 nguồn duy nhất, G09 dùng đúng danh sách mới 2 → 1. Model giữ metadata nguồn đầu. Harness gốc không so sánh an toàn danh sách object trong `expect.args`, nên không ghi hai case này là phép kiểm đầy đủ chất lượng nội dung.

### B4. Live chat evidence

Bốn phiên chạy **chat.py thật** với API thật và các lượt người dùng do script test cung cấp. Đây là smoke test do trợ lý thực hiện, không phải phỏng vấn hay người ngoài nhóm dùng thử. Các phiên đều kết thúc hợp lệ, không có tool errors; có tổng 6 lượt.

| Kịch bản | Lượt | Trạng thái | Tool calls theo lượt | Lỗi tool | Transcript |
|---|---:|---|---|---:|---|
| normal_research | 1 | answered | [['lookup']] | 0 | [v5-tools_openrouter_20261110T184039996396.transcript.json](https://github.com/griin-03/K5-L3B-DAY03-ALI33-ResearchAgentToolEval/blob/fddd7ff8bc306475031112582eeee98805b28f3b/starter_v0/transcripts/v5-tools_openrouter_20261110T184039996396.transcript.json) |
| missing_url_then_fill | 2 | waiting_for_user, answered | [['clarify'], ['fetch']] | 0 | [v5-tools_openrouter_20261110T184048278408.transcript.json](https://github.com/griin-03/K5-L3B-DAY03-ALI33-ResearchAgentToolEval/blob/fddd7ff8bc306475031112582eeee98805b28f3b/starter_v0/transcripts/v5-tools_openrouter_20261110T184048278408.transcript.json) |
| delivery_then_cancel | 2 | waiting_for_user, answered | [['clarify'], []] | 0 | [v5-tools_openrouter_20261110T184056434209.transcript.json](https://github.com/griin-03/K5-L3B-DAY03-ALI33-ResearchAgentToolEval/blob/fddd7ff8bc306475031112582eeee98805b28f3b/starter_v0/transcripts/v5-tools_openrouter_20261110T184056434209.transcript.json) |
| new_tool_dedup | 1 | answered | [['deduplicate_sources']] | 0 | [v5-tools_openrouter_20261110T184100366486.transcript.json](https://github.com/griin-03/K5-L3B-DAY03-ALI33-ResearchAgentToolEval/blob/fddd7ff8bc306475031112582eeee98805b28f3b/starter_v0/transcripts/v5-tools_openrouter_20261110T184100366486.transcript.json) |

[Live summary](https://github.com/griin-03/K5-L3B-DAY03-ALI33-ResearchAgentToolEval/blob/fddd7ff8bc306475031112582eeee98805b28f3b/starter_v0/analysis/live-summary.json), [stdout thực](https://github.com/griin-03/K5-L3B-DAY03-ALI33-ResearchAgentToolEval/blob/fddd7ff8bc306475031112582eeee98805b28f3b/starter_v0/analysis/live-cli.txt). Transcript UI và kiểm tra runtime trên VPS có `origin` riêng, không trộn với test offline.

### B5a. Tool mới, unit test và UI

| Hạng mục | Bằng chứng | Kết quả / giới hạn |
|---|---|---|
| Tool mới | [tool.py](https://github.com/griin-03/K5-L3B-DAY03-ALI33-ResearchAgentToolEval/blob/fddd7ff8bc306475031112582eeee98805b28f3b/starter_v0/tools/deduplicate_sources/tool.py), [TOOL.md](https://github.com/griin-03/K5-L3B-DAY03-ALI33-ResearchAgentToolEval/blob/fddd7ff8bc306475031112582eeee98805b28f3b/starter_v0/tools/deduplicate_sources/TOOL.md), registry + tools.yaml | Local, không mạng/side effect; giữ bản đầu, không chứng minh hai bài khác URL là cùng nội dung. |
| Unit tests | [test_tools_todo.py](https://github.com/griin-03/K5-L3B-DAY03-ALI33-ResearchAgentToolEval/blob/fddd7ff8bc306475031112582eeee98805b28f3b/starter_v0/tests/test_tools_todo.py), [test_demo.py](https://github.com/griin-03/K5-L3B-DAY03-ALI33-ResearchAgentToolEval/blob/fddd7ff8bc306475031112582eeee98805b28f3b/starter_v0/tests/test_demo.py) | **97 passed, 0 failed, 0 skipped**, cả local trước khi tắt và VPS ARM. Tool mới có 10 case tính cả tham số hóa: happy path, input xấu, lỗi bất ngờ, bảo toàn URL và giới hạn. |
| UI | [app.py](https://github.com/griin-03/K5-L3B-DAY03-ALI33-ResearchAgentToolEval/blob/fddd7ff8bc306475031112582eeee98805b28f3b/starter_v0/app.py), [demo_runtime.py](https://github.com/griin-03/K5-L3B-DAY03-ALI33-ResearchAgentToolEval/blob/fddd7ff8bc306475031112582eeee98805b28f3b/starter_v0/demo_runtime.py) | Có chat, nguồn/tool events, lỗi thật, tải transcript và phiên mới; mở trực tiếp không cần mã. UI không gửi Telegram. |
| Triển khai | [cấu hình](https://github.com/griin-03/K5-L3B-DAY03-ALI33-ResearchAgentToolEval/blob/fddd7ff8bc306475031112582eeee98805b28f3b/deploy/README.md), [kiểm tra VPS](https://github.com/griin-03/K5-L3B-DAY03-ALI33-ResearchAgentToolEval/blob/fddd7ff8bc306475031112582eeee98805b28f3b/starter_v0/analysis/deployment.json) | Service riêng, loopback upstream, Nginx HTTPS; key chỉ ở server, không commit. |

Ví dụ unit test bổ sung giá trị ngoài eval: hai query `?id=1` và `?id=2` không bị gộp, và exception trong normalizer trả error dict thay vì làm agent crash. Routing eval chỉ thấy model chọn đúng tên tool, không đo được hai hành vi code đó.

### B5. Bonus

- **Test challenge:** đã thay toàn bộ TODO bằng test thật; toàn suite 0 skipped. Đây là bằng chứng cho bonus 1 theo rubric, chưa phải điểm tự chấm chính thức.
- Không làm Small Local Model, không có ≥4 tool mới và không gửi Telegram thật; không nhận các bonus này.

### B7. Small Local Model

Không thực hiện trong phương án này. Không có metric hoặc run local model để báo cáo.

## 5. Khó khăn và cách xử lý

- Ban đầu RapidAPI trả 403 “not subscribed”; sau khi người dùng kích hoạt subscription, timeline/search đều trả 200. Run v0 cũ trước lúc sửa được giữ làm lịch sử, không dùng làm baseline chính trong B1. Các file `analysis/setup-check-*` ghi quá trình này.
- v1 chọn đúng tool nhưng bỏ `response_type` hoặc `topic`; v2 yêu cầu tham số tường minh, giúp tăng 80% → 95%.
- Hai thử nghiệm v3/v4 không sửa được R12; ghi nguyên kết quả và chọn nền v2 ít quy tắc hơn thay vì tiếp tục nhồi ví dụ theo một case.
- VPS ban đầu thiếu `python3.12-venv`; cài đúng gói này, không nâng cấp toàn hệ thống. Dependency ứng dụng nằm trong venv riêng.
- Smoke test runtime trên VPS: yêu cầu đọc `https://example.com` bị model cho rằng không phải trang thực rồi hỏi URL khác trước khi gọi fetch. Không coi đó là API Firecrawl bị hỏng hoặc một lần đọc thành công; đây là lỗi grounding/routing ngoài bộ base còn cần sửa. Hai yêu cầu tìm tin và lấy tweet đã chạy thành công.
- Người dùng yêu cầu tắt run local: đã dừng server local, các lượt eval đã hoàn thành. Bản demo được chạy trên VPS, không cần giữ laptop mở.

## 6. Đóng góp

| Thành viên | MSSV | Đóng góp đã có bằng chứng trong báo cáo này | Báo cáo / bằng chứng |
|---|---|---|---|
| Lê Thanh Tùng | **2A202603819** | Chuẩn bị phương án: cấu hình API, các vòng prompt/schema, tool mới, test/eval, UI, live chat và triển khai VPS/domain; Codex hỗ trợ thực hiện. | [Báo cáo cá nhân](2A202603819_LeThanhTung.md), [commit kỹ thuật `fddd7ff`](https://github.com/griin-03/K5-L3B-DAY03-ALI33-ResearchAgentToolEval/commit/fddd7ff8bc306475031112582eeee98805b28f3b), [TEAM.md](../../TEAM.md#lethanhtung-2a202603819). |
| Cấn Xuân Nghĩa | 2A202603805 | Đã có báo cáo phân tích tool/test/eval; tác giả chưa nhận code/run có sẵn là phần tự làm, còn cần commit kỹ thuật và khai báo AI. | [Báo cáo cá nhân](2A202603805_CanXuanNghia.md), [TEAM.md](../../TEAM.md#canxuannghia-2a202603805). |
| Nguyễn Mạnh Hùng | 2A202603852 | Báo cáo cá nhân khai báo phần UI Streamlit/local/live demo; cần đối chiếu thêm commit code và log. | [Báo cáo cá nhân đã bổ sung](2A202603852_NguyenManhHung.md), [TEAM.md](../../TEAM.md#nguyenmanhhung-2a202603852). |

Code và lịch sử kỹ thuật của Tùng hiện đã nằm trên main cùng ba báo cáo cá nhân. Theo [SUBMISSION.md](../../SUBMISSION.md), phần còn lại là Nghĩa/Hùng hoàn thiện khai báo AI, bằng chứng và commit kỹ thuật thực tế; mỗi người tự nộp link repo trên LMS.

## 7. B6 — Hạn chế và hướng cải thiện

- Prompt sửa quyết định luồng và thứ tự công việc; tools.yaml sửa hợp đồng routing/arguments. Hash ở mỗi vòng cho phép phân biệt hai loại thay đổi.
- Score chỉ chấm tool call và tập con args. `no_tool` chưa chứng minh nội dung từ chối đúng; đủ nguồn chưa chứng minh claim đúng. Cần người kiểm các câu trả lời và nguồn, nhất là policy mẫu và arXiv chưa kiểm live.
- R12 là trường hợp cần review thủ công: yêu cầu nội dung trước khi xác nhận thực sự gửi là an toàn hơn việc xác nhận nội dung chưa biết, nhưng nhãn hiện đòi yes_no ngay. Giữ FAIL và đề xuất trao đổi với coach; không sửa eval gốc.
- Group suite tự viết có 10 case nên không coi là benchmark độc lập quy mô lớn. Chưa có người ngoài nhóm xác nhận dùng thử; chưa đo chi phí tổng hay độ dao động nhiều lần của model.
- Tool dedup dùng chính sách URL, không phát hiện bài sao chép hoặc bảo đảm các URL chuẩn hóa có nội dung đồng nhất. Giữ URL/metadata đầu tiên cho người dùng tự đối chiếu.
- Nếu làm thêm một vòng: xây test phê duyệt có payload/destination cụ thể, kiểm hủy/đổi nội dung qua nhiều lượt và chấm riêng khả năng thu thập nội dung với quyền thực thi. Không nâng lên agent tự gửi khi chưa có nhu cầu và kiểm soát phù hợp.

## 8. Nguồn

- Đề bài, RULES, CHECKPOINTS, RUBRIC và source starter trong repo này.
- [Streamlit chat input](https://docs.streamlit.io/develop/api-reference/chat/st.chat_input), [AppTest](https://docs.streamlit.io/develop/api-reference/app-testing/st.testing.v1.apptest).
- [Python urllib.parse](https://docs.python.org/3/library/urllib.parse.html), dùng cho tool URL; chính sách loại tracking là lựa chọn riêng của tool.

## 9. Đối chiếu hồ sơ trước khi nộp

Ngày 11/11/2026 đã tích hợp code/log của nhánh demo vào main và giữ đủ ba báo cáo cá nhân. Xem [kết quả kiểm tra và phần đóng góp còn cần bổ sung](submission_audit.md). Việc tích hợp code chưa thay thế bằng chứng kỹ thuật và khai báo AI riêng của từng thành viên.
