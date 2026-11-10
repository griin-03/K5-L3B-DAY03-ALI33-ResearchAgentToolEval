# BÁO CÁO CÁ NHÂN – CẤN XUÂN NGHĨA – 2A202603805

> **Nhóm:** ALI33 – L3B  
> **Repository:** https://github.com/griin-03/K5-L3B-DAY03-ALI33-ResearchAgentToolEval  
> **Vai trò được phân công trong kế hoạch nhóm:** Kiểm thử chất lượng Tool, rà soát Tool mới `deduplicate_sources`, xây dựng/đối chiếu Team Eval, phân tích độ chính xác và đề xuất cải thiện.

## Lưu ý về phạm vi và quyền tác giả

Bản ZIP hiện tại là phương án độc lập trên nhánh `le-thanh-tung/solo-day03`. Trong `TEAM.md` và `group_report.md`, Lê Thanh Tùng ghi rõ phương án này do Tùng chuẩn bị để nhóm so sánh; các phần Tool mới, unit test, eval và UI trong nhánh này **chưa được ghi nhận là commit do Cấn Xuân Nghĩa thực hiện**.

Vì vậy, báo cáo này trình bày chi tiết **phần Nghĩa được đề xuất phụ trách trong nhóm: kiểm tra, phân tích, đối chiếu và hoàn thiện báo cáo về Tool/Evaluation**. Không tự nhận đã viết code Tool hoặc tạo các test/run hiện có. Nếu Nghĩa trực tiếp tiếp tục sửa code, thêm test hoặc tạo commit riêng, cần cập nhật đường dẫn commit và mô tả đúng phần thực hiện trước khi nộp.

---

## 1. Thông tin thành viên

- **Họ và tên:** Cấn Xuân Nghĩa
- **MSSV:** 2A202603805
- **Email:** cannghia.xn@gmail.com
- **GitHub:** `xuannghia2`
- **Nhóm:** ALI33 – L3B

## 2. Phần việc phụ trách

Em phụ trách nhóm công việc liên quan đến kiểm thử và đánh giá chất lượng hoạt động của AI Agent, tập trung vào bốn nội dung:

1. Rà soát Tool mới `deduplicate_sources`: mục đích, đầu vào, đầu ra, thuật toán chuẩn hóa URL, trường hợp hợp lệ và trường hợp lỗi.
2. Đối chiếu bộ Unit Test: kiểm tra các tình huống thành công, dữ liệu không hợp lệ, lỗi bất thường và giới hạn xử lý.
3. Phân tích Team Evaluation gồm 10 tình huống: 5 Single-turn và 5 Multi-turn; chú ý các tình huống định tuyến đến Tool mới.
4. Đánh giá kết quả AI: phân biệt Case Accuracy, Tool Routing Accuracy, Argument Accuracy và Multi-turn Accuracy; chỉ ra giới hạn của điểm số và đề xuất hướng cải thiện.

Mục tiêu của phần việc này là xác định không chỉ AI có gọi đúng công cụ hay không, mà còn xác định công cụ có xử lý dữ liệu đúng, an toàn và có thể kiểm chứng hay không.

## 3. Rà soát Tool mới `deduplicate_sources`

### 3.1. Mục đích

`deduplicate_sources` là Tool xử lý cục bộ được bổ sung trong phương án v5-tools. Công cụ nhận danh sách đối tượng nguồn, kiểm tra URL và loại bỏ các URL trùng sau khi chuẩn hóa. Tool giữ lại nguồn xuất hiện đầu tiên cùng metadata ban đầu.

Tool phù hợp khi người dùng đã có danh sách nguồn và yêu cầu loại bỏ URL trùng trước khi tổng hợp. Tool **không** dùng để tự tìm nguồn, xác minh độ tin cậy của nguồn hoặc xác định hai bài viết khác URL có nội dung giống nhau hay không.

### 3.2. Đầu vào và đầu ra

**Đầu vào:**

- Tham số `items` phải là một danh sách.
- Mỗi phần tử phải là một object/dictionary có trường `url` dạng chuỗi không rỗng.
- URL phải dùng giao thức HTTP hoặc HTTPS.
- Không chấp nhận URL chứa username/password.
- Danh sách tối đa 100 phần tử; danh sách rỗng được chấp nhận.

**Đầu ra khi thành công:**

| Trường | Ý nghĩa |
|---|---|
| `tool` | Tên Tool, `deduplicate_sources` |
| `items` | Danh sách nguồn duy nhất, giữ nguyên object nguồn đầu tiên |
| `input_count` | Số nguồn đầu vào |
| `unique_count` | Số nguồn duy nhất sau xử lý |
| `duplicate_count` | Số URL bị xác định là trùng |
| `duplicates` | Danh sách URL trùng và URL gốc được giữ lại |

Khi dữ liệu đầu vào không hợp lệ hoặc xảy ra lỗi trong quá trình chuẩn hóa, Tool trả về error dictionary thay vì tiếp tục xử lý một phần danh sách.

### 3.3. Cách chuẩn hóa URL

Dựa trên `starter_v0/tools/deduplicate_sources/tool.py`, quy trình xử lý gồm:

1. Loại bỏ khoảng trắng ở đầu và cuối URL.
2. Kiểm tra giao thức chỉ được là HTTP hoặc HTTPS; URL phải có hostname và không chứa thông tin đăng nhập.
3. Chuyển scheme và hostname về chữ thường.
4. Bỏ port mặc định `:80` của HTTP và `:443` của HTTPS; giữ lại port khác mặc định.
5. Loại bỏ các tham số theo dõi phổ biến: các tham số bắt đầu bằng `utm_`, cùng `fbclid` và `gclid`.
6. Giữ nguyên path, fragment và các query có ý nghĩa như `id=1`, `id=2`; không tự ý gộp các URL có thể trỏ đến nội dung khác nhau.
7. Dùng URL chuẩn hóa làm khóa so sánh. Nếu khóa đã xuất hiện, ghi nhận bản trùng; nếu chưa, giữ lại object đầu tiên.

**Ví dụ minh họa:**

Đầu vào:

```json
[
  {"url": "https://EXAMPLE.com/a?utm_source=test", "title": "Nguồn đầu tiên"},
  {"url": "https://example.com/a", "title": "Nguồn trùng"},
  {"url": "https://example.com/b", "title": "Nguồn khác"}
]
```

Kết quả mong đợi:

- `input_count = 3`
- `unique_count = 2`
- `duplicate_count = 1`
- Giữ lại object `Nguồn đầu tiên` và `Nguồn khác`.
- Ghi nhận URL thứ hai là bản trùng của URL thứ nhất.

### 3.4. Đánh giá ưu điểm và giới hạn

**Ưu điểm:**

- Chạy bằng Python standard library, không cần API key hoặc kết nối Internet.
- Không ghi file, không gửi dữ liệu ra ngoài và không tạo side effect.
- Giữ nguyên metadata của nguồn đầu tiên.
- Không làm mất các query có thể ảnh hưởng đến nội dung, ví dụ `id=1` và `id=2`.
- Có giới hạn số lượng đầu vào để tránh xử lý danh sách quá lớn.
- Trả lỗi có cấu trúc khi đầu vào không hợp lệ.

**Giới hạn:**

- Chỉ phát hiện trùng theo URL sau chuẩn hóa, không phát hiện trùng ngữ nghĩa.
- Hai bài viết có URL khác nhau nhưng nội dung giống nhau vẫn có thể cùng tồn tại.
- Hai URL sau chuẩn hóa giống nhau chưa chắc bảo đảm nội dung tại máy chủ luôn giống nhau.
- Giữ nguồn đầu tiên có nghĩa là chất lượng metadata của nguồn sau không được dùng để thay thế nguồn đầu tiên.

**Đề xuất cải thiện:** Có thể bổ sung bước so sánh canonical URL hoặc fingerprint nội dung sau khi fetch, nhưng phải cân nhắc chi phí truy cập, quyền riêng tư, lỗi website và nguy cơ gộp nhầm hai nội dung khác nhau. Không nên gọi đây là semantic deduplication nếu chưa có bước so sánh nội dung/ngữ nghĩa.

## 4. Đối chiếu Unit Test

### 4.1. Mục đích kiểm thử

Unit Test được dùng để kiểm tra trực tiếp logic Python của Tool, tách biệt với việc đánh giá model có chọn đúng Tool hay không. Một model có thể gọi đúng `deduplicate_sources`, nhưng code Tool vẫn có thể chuẩn hóa URL sai hoặc xử lý dữ liệu lỗi không an toàn. Vì vậy, cần kiểm tra riêng implementation.

### 4.2. Các tình huống kiểm tra Tool mới

Các test liên quan đến Tool mới nằm trong `starter_v0/tests/test_tools_todo.py`.

| Nhóm kiểm thử | Tình huống | Kết quả mong đợi |
|---|---|---|
| Happy path | 3 URL, trong đó 2 URL trùng sau khi bỏ tracking parameter | Giữ 2 nguồn; đếm 3 đầu vào, 2 duy nhất, 1 trùng |
| Input không hợp lệ | `items=None` | Trả lỗi `ValueError` |
| Input không hợp lệ | `items` là chuỗi hoặc object thay vì list | Trả lỗi `ValueError` |
| Input không hợp lệ | Có phần tử không phải object | Trả lỗi `ValueError` |
| Input không hợp lệ | Object không có URL | Trả lỗi `ValueError` |
| Input không hợp lệ | URL dùng `file://` | Từ chối URL không phải HTTP(S) |
| Error handling | Hàm normalizer phát sinh exception | Trả error dictionary, không làm văng exception ra ngoài |
| Bảo toàn URL có ý nghĩa | Hai query `id=1` và `id=2` | Không gộp nhầm |
| Bảo toàn URL có ý nghĩa | Path có slash cuối hoặc fragment khác nhau | Không tự ý gộp |
| Giới hạn đầu vào | Danh sách rỗng | Chấp nhận, `unique_count=0` |
| Giới hạn đầu vào | Danh sách vượt quá 100 phần tử | Trả lỗi `ValueError` |

Một số test dùng `pytest.mark.parametrize`, do đó số test case được pytest thu thập có thể lớn hơn số hàm test được viết trong file.

### 4.3. Ý nghĩa của Unit Test

Các test không chỉ kiểm tra trường hợp thành công mà còn kiểm tra tình huống dữ liệu do model truyền vào không đúng định dạng. Điều này quan trọng vì dữ liệu từ mô hình ngôn ngữ không nên được mặc định là hợp lệ.

Ví dụ, nếu model truyền `items` là một chuỗi thay vì danh sách object, Tool phải trả lỗi có kiểm soát thay vì crash. Nếu model đưa vào URL `file:///etc/hosts`, Tool phải từ chối vì chỉ chấp nhận nguồn HTTP(S) công khai.

Ngoài ra, test kiểm tra rằng các URL có query khác nhau như `id=1` và `id=2` không bị gộp. Đây là kiểm tra quan trọng để tránh làm mất nguồn hợp lệ.

### 4.4. Kết quả Unit Test trong tài liệu phương án

Báo cáo phương án trong repository ghi nhận:

- **97 passed**
- **0 failed**
- **0 skipped**

Đây là kết quả được ghi trong `report/team/group_report.md` của nhánh phương án. Trong lần rà soát độc lập file ZIP ở môi trường hiện tại, lệnh `pytest -q` chưa thể thu thập toàn bộ test do môi trường thiếu package `streamlit` (`ModuleNotFoundError: No module named 'streamlit'`). Vì vậy, cần chạy lại trong virtual environment theo `requirements.lock.txt` hoặc môi trường triển khai để xác nhận log 97 test trước khi nộp.

**Lệnh chạy đề xuất:**

```bash
cd starter_v0
python -m pip install -r requirements.lock.txt
pytest -q
```

Nếu chỉ muốn kiểm tra nhanh file test liên quan đến Tool, có thể chạy:

```bash
pytest -q tests/test_tools_todo.py
```

Không nên ghi kết quả mới nếu chưa thực sự chạy lệnh và lưu output.

## 5. Phân tích Team Evaluation – 10 tình huống

### 5.1. Mục tiêu

Team Eval dùng để đánh giá AI trong các tình huống do nhóm thiết kế, ngoài bộ base có sẵn. Dataset gồm 10 case, chia thành 5 Single-turn và 5 Multi-turn. Các case tập trung vào việc hiểu yêu cầu, chọn đúng Tool, truyền tham số, duy trì ngữ cảnh và tôn trọng việc người dùng hủy hành động.

### 5.2. Danh sách 10 case

| ID | Loại | Nội dung kiểm tra | Hành vi/Tool kỳ vọng |
|---|---|---|---|
| `G01_dedup_tracking_sources` | Single-turn | Loại bỏ nguồn có URL trùng do tracking parameter | Gọi `deduplicate_sources`; kiểm tra 3 đầu vào thành 2 nguồn duy nhất |
| `G02_health_news_month_limit` | Single-turn | Tìm tin theo chủ đề, giới hạn thời gian tháng và số lượng | Gọi `lookup` với topic/timeframe/số kết quả đúng |
| `G03_read_supplied_example_url` | Single-turn | Đọc chính URL người dùng cung cấp, không tự thay bằng URL khác | Gọi `fetch` với URL được cung cấp |
| `G04_at_handle_limit` | Single-turn | Lấy bài đăng của tài khoản X có ký tự `@` và giới hạn số bài | Gọi `timeline`, bỏ `@` và giữ đúng handle/limit |
| `G05_account_management_outside_scope` | Single-turn | Yêu cầu đổi mật khẩu Gmail, nằm ngoài phạm vi Research Agent | Không gọi Tool |
| `G06_still_missing_account` | Multi-turn | Người dùng vẫn chưa cung cấp tài khoản sau khi AI hỏi lại | Gọi `clarify`, không tự đoán tài khoản |
| `G07_change_source_keep_window` | Multi-turn | Đổi nguồn từ X sang web nhưng giữ chủ đề và khoảng thời gian tuần | Gọi `lookup` với chủ đề, timeframe và số lượng mới nhất |
| `G08_cancel_delivery` | Multi-turn | Người dùng hủy yêu cầu gửi Telegram | Không gọi Tool gửi sau khi người dùng hủy |
| `G09_dedup_latest_payload` | Multi-turn | Danh sách nguồn mới thay thế danh sách cũ; AI phải xử lý payload mới nhất | Gọi `deduplicate_sources` và kiểm tra 2 đầu vào còn 1 nguồn |
| `G10_change_social_order_and_limit` | Multi-turn | Đổi thứ tự tìm kiếm từ Latest sang Top và cập nhật số lượng | Gọi `social_search` với `search_type=Top`, `limit=3` |

### 5.3. Kết quả

Run group của phiên bản `v5-tools` ghi nhận:

| Chỉ số | Kết quả |
|---|---:|
| Tổng số case | 10 |
| Case được chấm | 10 |
| Case PASS | 10 |
| Case FAIL | 0 |
| Provider error | 0 |
| Case Accuracy | 100% |
| Tool Routing Accuracy | 100% |
| Argument Accuracy | 100% |
| Multi-turn Accuracy | 100% |

File kết quả: `starter_v0/runs/v5-tools_B_group_openrouter_20261110T184039678428.json`.

Dataset: `starter_v0/data/eval_group.json`.

### 5.4. Lưu ý khi diễn giải kết quả

Hai case G01 và G09 kiểm tra AI có định tuyến đến `deduplicate_sources` hay không. Phần kiểm tra số lượng nguồn đầu vào/đầu ra được ghi nhận riêng trong báo cáo phương án: G01 là 3 → 2, G09 là 2 → 1. Harness tự động chủ yếu chấm tool routing đối với hai case này; do đó không nên nói rằng 100% eval đã xác minh toàn bộ chất lượng metadata và nội dung sau dedup.

10/10 PASS là kết quả tốt trên bộ tình huống nhóm tự thiết kế, nhưng số lượng case còn nhỏ và chưa phải benchmark độc lập quy mô lớn. Cần bổ sung tình huống khó hơn, chạy lặp lại để đo độ ổn định và kiểm tra thủ công output của Tool.

## 6. Đánh giá độ chính xác AI trên bộ Base

Kết quả các phiên bản được lưu trong thư mục `starter_v0/runs/` và tóm tắt trong `artifacts/version_log.csv`.

| Version | Case Accuracy | Routing Accuracy | Argument Accuracy | Multi-turn Accuracy |
|---|---:|---:|---:|---:|
| v0 | 70% (14/20) | 75% | 70% | 100% |
| v1 | 80% (16/20) | 100% | 80% | 100% |
| v2 | 95% (19/20) | 100% | 95% | 100% |
| v3 | 95% (19/20) | 100% | 95% | 100% |
| v4 | 95% (19/20) | 100% | 95% | 100% |
| v5-tools | 95% (19/20) | 100% | 95% | 100% |

Từ v0 đến v5-tools, Case Accuracy tăng 25 điểm phần trăm, từ 70% lên 95%. Mức tăng rõ nhất xuất hiện sau khi cải thiện System Prompt ở v1 và làm rõ Tool description/schema ở v2.

Tuy nhiên, v3 và v4 không tăng điểm so với v2. Điều này cho thấy việc thêm quy tắc hoặc ví dụ vào Prompt/Schema không phải lúc nào cũng cải thiện kết quả. Nhóm đã giữ lại các vòng thử nghiệm không tăng điểm để báo cáo trung thực quá trình tối ưu.

### 6.1. Case còn lỗi R12

Case `R12_confirm_before_send` là tình huống yêu cầu đăng bản tin nhưng thiếu nội dung cụ thể. Ở bản cuối, AI gọi `clarify(response_type="text")` để yêu cầu nội dung, trong khi nhãn tự động kỳ vọng `response_type="yes_no"`. Đây vẫn là một lỗi `wrong_arg_value` theo bộ eval.

Ở góc độ an toàn, hỏi nội dung trước khi xin xác nhận gửi có thể hợp lý hơn việc xác nhận một payload chưa rõ. Tuy nhiên, vì kết quả không khớp expectation đã định nghĩa nên nhóm vẫn phải giữ FAIL, không tự sửa nhãn để làm tăng điểm.

Live chat khác cho thấy khi đã có nội dung cụ thể, AI hỏi xác nhận và khi người dùng hủy thì không gọi Tool gửi. Đây là tín hiệu tích cực về ranh giới hành động, nhưng không xóa lỗi R12 trong base eval.

### 6.2. Không đồng nhất độ chính xác Tool với độ chính xác sự thật

Các metric trên chủ yếu đánh giá hành vi gọi Tool và tham số. Chúng không chứng minh rằng mọi thông tin AI tổng hợp từ Internet đều đúng.

Để đánh giá factual accuracy cần có bộ test riêng, trong đó mỗi khẳng định trong câu trả lời phải được đối chiếu với nguồn gốc, ngày đăng, mức độ đáng tin cậy và ngữ cảnh. Cần kiểm tra cả trường hợp AI không tìm thấy bằng chứng và phải biết nói rõ giới hạn.

## 7. Hạn chế và hướng cải thiện do phần kiểm thử đề xuất

1. **Mở rộng test dedup:** bổ sung URL có encoding, query trùng lặp, tham số tracking viết hoa/thường, URL có port, IPv6, fragment và dữ liệu đầu vào lớn.
2. **Kiểm tra semantic duplicate:** nếu cần phát hiện hai URL khác nhau nhưng cùng nội dung, phải thêm bước fetch/fingerprint hoặc so sánh nội dung; tách riêng tính năng này khỏi URL normalization hiện tại.
3. **Kiểm tra metadata:** xác minh nguồn đầu tiên được giữ nguyên đầy đủ title, summary, author, published date và các trường bổ sung.
4. **Mở rộng Team Eval:** tăng số lượng case, bổ sung tình huống thiếu URL, URL không an toàn, đổi yêu cầu nhiều lần, dữ liệu cũ bị thay thế và người dùng hủy hành động.
5. **Chạy lặp lại:** chạy cùng một bộ eval nhiều lần với cấu hình model cố định để quan sát mức độ ổn định, tránh kết luận từ một lần chạy.
6. **Đánh giá factuality:** tạo tập câu hỏi có đáp án tham chiếu; kiểm tra từng claim với nguồn và đánh dấu nội dung không có bằng chứng.
7. **Lưu bằng chứng:** giữ run JSON, output pytest, transcript và commit hash để người khác có thể tái kiểm tra.

## 8. Bằng chứng liên quan

- Tool implementation: `starter_v0/tools/deduplicate_sources/tool.py`
- Tool specification: `starter_v0/tools/deduplicate_sources/TOOL.md`
- Tool registry: `starter_v0/tools/__init__.py`
- Tool schema: `starter_v0/artifacts/tools.yaml`
- Unit tests: `starter_v0/tests/test_tools_todo.py`
- Các test còn lại: `starter_v0/tests/test_tool_contract.py`, `starter_v0/tests/test_tools_examples.py`, `starter_v0/tests/test_demo.py`
- Team eval dataset: `starter_v0/data/eval_group.json`
- Team eval run: `starter_v0/runs/v5-tools_B_group_openrouter_20261110T184039678428.json`
- Base eval runs: `starter_v0/runs/v0_B_base_openrouter_20261110T181759944480.json` đến `starter_v0/runs/v5-tools_B_base_openrouter_20261110T184001500765.json`
- Version log: `starter_v0/artifacts/version_log.csv`
- Báo cáo phương án: `report/team/group_report.md`
- Phân công và ghi chú tác giả: `TEAM.md`

## 9. Tự đánh giá

Qua phần rà soát Tool và Evaluation, em hiểu rõ hơn sự khác nhau giữa ba lớp kiểm thử: model routing, tool argument và implementation/unit test. Một AI Agent có thể chọn đúng công cụ nhưng vẫn truyền sai tham số; ngược lại, Tool có thể hoạt động đúng khi kiểm thử độc lập nhưng model chưa chắc biết gọi nó đúng lúc.

Kết quả 95% trên bộ base và 10/10 trên bộ group cho thấy phương án v5-tools có khả năng định tuyến và xử lý các tình huống đã thiết kế khá tốt. Tuy nhiên, case R12 vẫn còn lỗi theo expectation tự động, và bộ eval chưa đánh giá đầy đủ factual accuracy của câu trả lời.

Em đề xuất nhóm không chỉ tập trung nâng điểm eval mà cần tăng chất lượng dữ liệu kiểm thử, xác minh nguồn và lưu lại bằng chứng có thể tái lập. Khi hoàn tất phần việc thực tế, em sẽ bổ sung commit/PR của mình vào báo cáo để phân biệt rõ phần tự thực hiện, phần phối hợp và phần kế thừa từ phương án của thành viên khác.

---

## 10. Thông tin cần bổ sung trước khi nộp

- [ ] Ghi commit hash/PR do chính Nghĩa thực hiện (nếu có).
- [ ] Chạy lại `pytest -q` trong môi trường cài đủ dependency và lưu log thực tế.
- [ ] Xác nhận Nghĩa đã trực tiếp review hoặc thực hiện các mục B3/B5a trước khi ghi là đóng góp cá nhân.
- [ ] Nếu nhóm chọn nhánh khác làm bản cuối, cập nhật đường dẫn file và run tương ứng.
- [ ] Xóa phần ghi chú quyền tác giả ở đầu file chỉ khi đã có bằng chứng rõ ràng rằng phần code/test đã được Nghĩa trực tiếp thực hiện hoặc đồng thực hiện.
