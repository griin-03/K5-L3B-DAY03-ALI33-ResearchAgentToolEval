"""Build candidate documentation from recorded runs; no API calls or invented results."""
from pathlib import Path
import csv
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'))


def cell(value):
    return str(value).replace('|', '\\|').replace('\n', ' ')


def link(path):
    return f'[{Path(path).name}](../../starter_v0/{path})'


def main():
    with (ROOT/'artifacts/version_log.csv').open(newline='',encoding='utf-8') as file:
        versions = list(csv.DictReader(file))
    selected = [(row,read_json(ROOT/row['run_file'])) for row in versions]
    final = selected[-1][1]
    group = read_json(sorted((ROOT/'runs').glob('v5-tools_B_group_*.json'))[-1])
    live = read_json(ROOT/'analysis/live-summary.json')
    deployment_path = ROOT/'analysis/deployment.json'
    deployment = read_json(deployment_path) if deployment_path.exists() else {}
    compare = [{'version': row['version'], 'hypothesis': row['hypothesis'], 'run_file':row['run_file'], **run['summary']}
               for row,run in selected]
    (ROOT/'analysis/comparison.json').write_text(json.dumps(compare,ensure_ascii=False,indent=2),encoding='utf-8')
    table = '\n'.join(f"| {row['version']} | {cell(row['changed_artifact'])} | {cell(row['hypothesis'])} | {run['summary']['case_accuracy']:.0%} | {run['summary']['tool_routing_accuracy']:.0%} | {run['summary']['argument_accuracy']:.0%} | {run['summary']['multiturn_accuracy']:.0%} | {link(row['run_file'])} |" for row,run in selected)
    failures = []
    for case in selected[0][1]['results']:
        if case['result']['passed']:
            continue
        resolved = next((row['version'] for row,run in selected[1:]
                         if next(c for c in run['results'] if c['id']==case['id'])['result']['passed']),None)
        failures.append(f"| {case['id']} | {case['result']['failure_type']} | {cell(', '.join(c['name'] for c in case['result']['actual_tool_calls']))} | {cell('; '.join(case['result']['failures']))} | {resolved or 'Chưa đạt tiêu chí tự động; xem phân tích bên dưới'} |")
    group_table = '\n'.join(f"| {case['id']} | {'multi' if case['is_multiturn'] else 'single'} | {cell(case['metadata']['what_it_tests'])} | {cell(', '.join(c['name'] for c in case['expect'].get('tool_calls',[])) or 'no_tool')} | {'PASS' if case['result']['passed'] else 'FAIL'} |" for case in group['results'])
    live_table = '\n'.join(f"| {row['scenario']} | {row['turns']} | {cell(', '.join(row['statuses']))} | {cell(str(row['tool_calls']))} | {row['tool_errors']} | {link(row['file'])} |" for row in live)
    group_file = 'runs/'+group['run_id']+'.json'
    deployed = deployment.get('origin_https_health') == 200 and deployment.get('external_http_probe', {}).get('root_status') == 200
    deploy_state = 'Đã triển khai HTTPS và kiểm tra truy cập từ bên ngoài; smoke test tin tức và bài X trên VPS thành công. Một yêu cầu đọc URL còn bị model hỏi lại trước khi gọi fetch, được ghi ở phần hạn chế.' if deployed else 'Đang hoàn tất kiểm tra triển khai; chưa xác nhận toàn bộ đường truy cập.'
    report = f'''# Báo cáo phương án độc lập — ALI33 Research Desk

> Phương án của **Lê Thanh Tùng — 2A202603819**, nhánh `le-thanh-tung/solo-day03`, chuẩn bị để nhóm so sánh rồi lựa chọn. Có AI hỗ trợ code, test, phân tích và soạn báo cáo. Không ghi nhận phần của Nghĩa/Hùng là do Tùng thực hiện hoặc ngược lại; báo cáo/commit cá nhân của mỗi người cần dựa vào công việc thật.

## 1. Thông tin nhóm

- Nhóm **ALI33**, lớp **L3B**; thành viên xem [TEAM.md](../../TEAM.md).
- Provider/model cố định: **OpenRouter / openai/gpt-4o-mini**, temperature 0.
- Bản tích hợp cuối: **v5-tools**. Đây là ứng viên, chưa phải quyết định chung chọn bản nộp.

## 2. PHẦN A — Giới thiệu agent

### A1. Agent làm được gì?

Research Desk tìm nguồn web và bài đăng X, đọc URL, lọc nguồn trùng và hỗ trợ tổng hợp có dẫn chứng. Người dùng xem được tool calls và lỗi; gửi Telegram bị tắt trong UI demo.

**Link dùng thử:** https://ali33.sunstudy.app — có mã truy cập do người vận hành cung cấp. {deploy_state} Mã demo và API key không nằm trong báo cáo/repo.

**Chạy từ source:** `cd starter_v0`, tạo môi trường và cấu hình `.env` theo [hướng dẫn](../../docs/TOOL-SETUP.md), rồi `python -m streamlit run app.py --server.port 8503`. Dependency có trong `requirements.txt`; `requirements.lock.txt` ghi phiên bản dùng cho bản này. Hiện ứng dụng local đã tắt theo yêu cầu; demo chạy trên VPS ARM 24GB bằng service riêng.

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
4. “Lọc trùng nguồn này: [{{\"url\":\"https://example.com/a?utm_source=demo\"}},{{\"url\":\"https://example.com/a\"}}].”
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
{table}

Tất cả các run được chọn ở bảng có **provider_error_cases = 0**, **measured_cases = total_cases = 20**, và không có tool-execution error. Bản cuối tăng từ **70% lên 95% (+25 điểm phần trăm)** trên bộ base, không phải bảo đảm 95% đúng cho mọi yêu cầu. Bằng chứng tổng hợp: [version_log.csv](../../starter_v0/artifacts/version_log.csv), [comparison.json](../../starter_v0/analysis/comparison.json).

### B2. Failure analysis

Đối chiếu run v0 với các vòng sau; giữ cả những thử nghiệm không cải thiện.

| Case | Loại lỗi v0 | Tool thực tế v0 | Sai ở đâu | Vòng đầu đạt |
|---|---|---|---|---|
{chr(10).join(failures)}

**Case còn sai R12:** yêu cầu “Đăng bản tin này…” không có nội dung. Bản cuối gọi `clarify(response_type=text)` để xin nội dung, trong khi nhãn yêu cầu `yes_no`; không gọi `send`. Đây vẫn là FAIL theo rubric tự động, không đổi nhãn để làm đẹp điểm. Live chat khi có nội dung cụ thể đã hỏi xác nhận, rồi không gọi tool sau khi người dùng hủy. Không đánh đồng kết quả an toàn quan sát được với việc đạt toàn bộ tiêu chí tự động.

### B3. Eval nhóm: 5 single + 5 multi

Dataset được khóa trước khi chạy suite group; SHA-256: `{hashlib.sha256((ROOT/'data/eval_group.json').read_bytes()).hexdigest()}`. Không chỉnh case theo kết quả group.

| ID | Loại | Kiểm tra | Kỳ vọng | Kết quả |
|---|---|---|---|---|
{group_table}

Kết quả: **{group['summary']['passed_cases']}/{group['summary']['total_cases']}**, provider errors **{group['summary']['provider_error_cases']}**. {link(group_file)}; [dataset](../../starter_v0/data/eval_group.json).

Hai case dedup tự động chấm routing; kiểm tra payload/count riêng cho thấy G01 giữ 3 đầu vào → 2 nguồn duy nhất, G09 dùng đúng danh sách mới 2 → 1. Model giữ metadata nguồn đầu. Harness gốc không so sánh an toàn danh sách object trong `expect.args`, nên không ghi hai case này là phép kiểm đầy đủ chất lượng nội dung.

### B4. Live chat evidence

Bốn phiên chạy **chat.py thật** với API thật và các lượt người dùng do script test cung cấp. Đây là smoke test do trợ lý thực hiện, không phải phỏng vấn hay người ngoài nhóm dùng thử. Các phiên đều kết thúc hợp lệ, không có tool errors; có tổng 6 lượt.

| Kịch bản | Lượt | Trạng thái | Tool calls theo lượt | Lỗi tool | Transcript |
|---|---:|---|---|---:|---|
{live_table}

[Live summary](../../starter_v0/analysis/live-summary.json), [stdout thực](../../starter_v0/analysis/live-cli.txt). Transcript UI và kiểm tra runtime trên VPS có `origin` riêng, không trộn với test offline.

### B5a. Tool mới, unit test và UI

| Hạng mục | Bằng chứng | Kết quả / giới hạn |
|---|---|---|
| Tool mới | [tool.py](../../starter_v0/tools/deduplicate_sources/tool.py), [TOOL.md](../../starter_v0/tools/deduplicate_sources/TOOL.md), registry + tools.yaml | Local, không mạng/side effect; giữ bản đầu, không chứng minh hai bài khác URL là cùng nội dung. |
| Unit tests | [test_tools_todo.py](../../starter_v0/tests/test_tools_todo.py), [test_demo.py](../../starter_v0/tests/test_demo.py) | **97 passed, 0 failed, 0 skipped**, cả local trước khi tắt và VPS ARM. Tool mới có 10 case tính cả tham số hóa: happy path, input xấu, lỗi bất ngờ, bảo toàn URL và giới hạn. |
| UI | [app.py](../../starter_v0/app.py), [demo_runtime.py](../../starter_v0/demo_runtime.py) | Có chat, nguồn/tool events, lỗi thật, tải transcript, phiên mới và mã truy cập. UI không gửi Telegram. |
| Triển khai | [cấu hình](../../deploy/README.md), [kiểm tra VPS](../../starter_v0/analysis/deployment.json) | Service riêng, loopback upstream, Nginx HTTPS; key chỉ ở server, không commit. |

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

Tùng phụ trách phương án độc lập này: yêu cầu triển khai, kiểm soát phạm vi, provider/eval, prompt/schema, tool mới, test, UI, bằng chứng và triển khai VPS/domain. AI hỗ trợ thực hiện code và phân tích; không ghi đây là code Tùng tự gõ toàn bộ. Xem [báo cáo cá nhân](2A202603819_LeThanhTung.md). Nghĩa/Hùng tự bổ sung đóng góp và báo cáo thật khi nhóm chọn hoặc tích hợp các phương án; chưa gán commit cho họ.

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
'''
    (REPO/'report/team/group_report.md').write_text(report,encoding='utf-8')
    personal=f'''# Báo cáo cá nhân — Lê Thanh Tùng — 2A202603819

## 1. Thông tin thành viên

- Họ tên: Lê Thanh Tùng; MSSV: 2A202603819; nhóm ALI33, L3B.
- GitHub: griin-03; nhánh phương án: `le-thanh-tung/solo-day03`.

## 2. Phần việc phụ trách

Chuẩn bị một phương án hoàn chỉnh để nhóm so sánh: setup, baseline, prompt/tool declaration, tool mới, unit tests, eval nhóm, UI, live chat và triển khai VPS. Đây chưa phải xác nhận nhóm đã chọn phương án này.

## 3. Đóng góp cụ thể

- Yêu cầu kiểm tra toàn bộ key; xử lý subscription RapidAPI sau khi kiểm tra báo lỗi 403.
- Yêu cầu làm một phương án riêng để so sánh, triển khai lên VPS ARM 24GB và domain `ali33.sunstudy.app`; yêu cầu tắt run trên laptop.
- Có 6 phiên bản được đo thật: v0 70%, v1 80%, v2–v5-tools 95%; các thử nghiệm không tăng điểm vẫn được giữ.
- Phương án có tool deduplicate_sources, đúng 10 case nhóm (5 single/5 multi, đạt 10/10), 97 test offline pass không skip, bốn phiên chat.py thật gồm sáu lượt và UI Streamlit.
- Dùng user/service riêng trên VPS, upstream loopback, HTTPS và mã demo. Không gửi Telegram thật.

## 4. Bằng chứng và AI đã dùng

- [Báo cáo nhóm của phương án](group_report.md); [version_log](../../starter_v0/artifacts/version_log.csv); [comparison](../../starter_v0/analysis/comparison.json); [live summary](../../starter_v0/analysis/live-summary.json).
- Code tool/test/UI, snapshots, run JSON và transcript đi kèm repo; key không nằm trong Git.
- Tôi dùng Codex để đọc đề, viết code/test, chạy API/eval, phân tích log, viết tài liệu và thao tác triển khai theo yêu cầu. Các số đo do chương trình thực sự chạy tạo ra; không dùng số giả, không gán phần việc hoặc commit cho thành viên khác.
- Cách kiểm: pytest, contract tests, đối chiếu input/output tool, so hash, đọc run lỗi và transcript, kiểm API/HTTPS trên VPS. Tôi cần tự giải thích được từng thay đổi khi coach hỏi; việc có AI hỗ trợ không thay thế yêu cầu hiểu bài.

## 5. Tự đánh giá theo bằng chứng

Phương án đã có code và log cho các phần bắt buộc, nhưng chưa đạt hoàn hảo: base vẫn sai R12 theo tiêu chí tự động; hai vòng v3/v4 không cải thiện. Điểm 95% chỉ là kết quả trên 20 case cố định, không chứng minh mọi câu trả lời đúng. Trong kịch bản gửi có nội dung cụ thể, agent đã hỏi xác nhận và dừng khi hủy; UI còn chặn gửi ở code. Nhóm cần tự dùng thử, review nguồn và chọn phương án trước khi chốt nộp. Tôi không có bằng chứng để ghi cảm nhận hoặc đóng góp của Nghĩa/Hùng thay cho hai bạn.
'''
    (REPO/'report/team/2A202603819_LeThanhTung.md').write_text(personal,encoding='utf-8')
    print('Built report and personal evidence from',len(selected),'real base runs and',len(group['results']),'group cases.')


if __name__=='__main__':
    main()
