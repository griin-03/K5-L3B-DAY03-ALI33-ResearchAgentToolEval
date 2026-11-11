"""Exercise original chat.py with real APIs and scripted, disclosed user turns."""
from __future__ import annotations
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from demo_runtime import redact, version_label

SCENARIOS = {
    'normal_research': ['Tìm 2 tin AI hôm nay trên web, viết bản tin ngắn có link nguồn. Chỉ dùng 2 nguồn vừa tìm được.'],
    'missing_url_then_fill': ['Tôi muốn đọc một bài viết nhưng chưa cung cấp đường dẫn. Hỏi tôi đường dẫn trước.',
                             'Đọc https://example.com, chỉ dùng đúng đường dẫn này.'],
    'delivery_then_cancel': ["Nội dung bản tin là 'ALI33 demo kiểm tra xác nhận'. Tôi muốn gửi lên Telegram, hãy hỏi xác nhận trước.",
                             'Không gửi. Hủy yêu cầu này, không cần làm gì khác.'],
    'new_tool_dedup': ['Chỉ lọc trùng các nguồn sau và báo số nguồn còn lại, không tìm thêm hay định dạng: '
                      '[{"url":"https://example.com/a?utm_source=lab","title":"First"},'
                      '{"url":"https://example.com/a","title":"Again"},{"url":"https://example.com/b"}].'],
}


def main():
    version = version_label()
    if version == 'development':
        raise SystemExit('Set artifacts/demo_version.txt after finalizing the candidate first.')
    folder = ROOT/'transcripts'
    folder.mkdir(exist_ok=True)
    rows = []
    stdout_log = []
    with tempfile.NamedTemporaryFile(mode='w', suffix='.env', prefix='day03-live-') as guard:
        guard.write('TELEGRAM_BOT_TOKEN=\nTELEGRAM_CHAT_ID=\n')
        guard.flush()
        env = dict(os.environ, DAY03_ENV_FILE=guard.name, TZ='Asia/Ho_Chi_Minh')
        for name, turns in SCENARIOS.items():
            before = set(folder.glob('*.transcript.json'))
            print('LIVE SCENARIO:', name, flush=True)
            result = subprocess.run([sys.executable, '-u', 'chat.py', '--provider', 'openrouter',
                       '--version', version, '--max-tool-rounds', '4'], cwd=ROOT, env=env,
                       input='\n'.join([*turns, '/exit', '']), capture_output=True, text=True, timeout=240)
            stdout_log.append(name+'\n'+result.stdout+'\n'+result.stderr)
            created = set(folder.glob('*.transcript.json')) - before
            if result.returncode or len(created) != 1:
                raise SystemExit('Live scenario failed; inspect captured output: '+name)
            path = created.pop()
            transcript = json.loads(path.read_text())
            transcript['test_driver'] = 'scripted_cli_live_API'
            transcript['scenario'] = name
            transcript['delivery_enabled'] = False
            transcript = redact(transcript)
            path.write_text(json.dumps(transcript, ensure_ascii=False, indent=2), encoding='utf-8')
            statuses = [turn['status'] for turn in transcript['turns']]
            tool_errors = sum(1 for turn in transcript['turns'] for event in turn.get('tool_events', [])
                              if isinstance(event.get('result'),dict) and event['result'].get('error'))
            row = {'scenario': name, 'file': str(path.relative_to(ROOT)), 'turns': len(transcript['turns']),
                   'statuses': statuses, 'tool_errors': tool_errors,
                   'tool_calls': [[event['tool'] for event in turn.get('tool_events', [])] for turn in transcript['turns']]}
            rows.append(row)
            print(json.dumps(row, ensure_ascii=False), flush=True)
    (ROOT/'analysis/live-cli.txt').write_text(redact('\n\n'.join(stdout_log)),encoding='utf-8')
    (ROOT/'analysis/live-summary.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')


if __name__ == '__main__':
    main()
