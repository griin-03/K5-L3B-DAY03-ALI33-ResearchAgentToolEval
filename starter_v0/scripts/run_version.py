"""Run the real harness against immutable artifact snapshots and record evidence."""
from __future__ import annotations

import argparse
from collections import Counter
import csv
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from env_loader import load_lab_env


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('version')
    parser.add_argument('--hypothesis', required=True)
    parser.add_argument('--changed', default='baseline')
    parser.add_argument('--suite', choices=['base', 'group', 'extension'], default='base')
    args = parser.parse_args()
    if not args.version or any(c not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_' for c in args.version):
        parser.error('Version must be a simple label.')
    load_lab_env(ROOT)
    secrets = [value for key, value in os.environ.items() if ('KEY' in key or 'TOKEN' in key) and len(value) >= 8]

    def redact(text: str) -> str:
        for value in secrets:
            text = text.replace(value, '[REDACTED]')
        return text

    snapshot = ROOT / 'artifacts' / 'versions' / args.version
    snapshot.mkdir(parents=True, exist_ok=True)
    for filename in ('system_prompt.md', 'tools.yaml'):
        content = (ROOT / 'artifacts' / filename).read_bytes()
        target = snapshot / filename
        if target.exists() and target.read_bytes() != content:
            raise SystemExit('Refusing to overwrite different artifacts for ' + args.version)
        target.write_bytes(content)

    runs = ROOT / 'runs'
    existing = set(runs.glob('*.json'))
    command = [sys.executable, '-u', 'run_eval.py', '--provider', 'openrouter', '--version', args.version,
               '--suite', args.suite, '--eval-cases', f'data/eval_{args.suite}.json',
               '--system-prompt', str((snapshot / 'system_prompt.md').relative_to(ROOT)),
               '--tools', str((snapshot / 'tools.yaml').relative_to(ROOT))]
    # Evaluation of a send boundary must never deliver a real message.
    # Keep the real provider/research keys in inherited memory; clear only delivery.
    with tempfile.NamedTemporaryFile(mode='w', prefix='day03-eval-', suffix='.env') as guard:
        guard.write('TELEGRAM_BOT_TOKEN=\nTELEGRAM_CHAT_ID=\n')
        guard.flush()
        env = dict(os.environ, DAY03_ENV_FILE=guard.name, TZ='Asia/Ho_Chi_Minh')
        process = subprocess.Popen(command, cwd=ROOT, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for line in process.stdout:
            print(redact(line), end='', flush=True)
        if process.wait() != 0:
            raise SystemExit(process.returncode)

    created = set(runs.glob('*.json')) - existing
    if len(created) != 1:
        raise SystemExit('Expected exactly one new run JSON.')
    run_path = created.pop()
    raw = run_path.read_text(encoding='utf-8')
    cleaned = redact(raw)
    if cleaned != raw:
        run_path.write_text(cleaned, encoding='utf-8')
    run = json.loads(cleaned)
    summary = run['summary']
    errors = Counter(event.get('tool', 'unknown') for case in run['results']
                     for event in case.get('tool_results', [])
                     if isinstance(event.get('result'), dict) and event['result'].get('error'))
    print('TOOL_EXECUTION_ERRORS:', json.dumps(errors, ensure_ascii=False), flush=True)
    valid = summary['provider_error_cases'] == 0 and summary['measured_cases'] == summary['total_cases']
    print('VALID_PROVIDER_RUN:', valid, flush=True)
    if args.suite == 'base':
        log = ROOT / 'artifacts' / 'version_log.csv'
        with log.open(newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            fields = reader.fieldnames
            rows = list(reader)
        before = rows[-1]['metric_after'] if rows else ''
        rows.append({
            'version': args.version, 'author': 'Le Thanh Tung (AI-assisted)', 'changed_artifact': args.changed,
            'artifact_version': run['artifact_version'], 'prompt_hash': run['prompt_hash'], 'tools_hash': run['tools_hash'],
            'reason': 'Real OpenRouter run; Telegram delivery disabled; valid=' + str(valid),
            'hypothesis': args.hypothesis, 'metric_before': before,
            'metric_after': summary['case_accuracy'] if valid else '',
            'run_file': str(run_path.relative_to(ROOT)),
        })
        with log.open('w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fields, lineterminator='\n')
            writer.writeheader()
            writer.writerows(rows)
    print('RECORDED_RUN:', run_path.relative_to(ROOT), flush=True)
    if not valid:
        raise SystemExit('Provider errors: diagnostic run preserved; do not use as a valid score.')


if __name__ == '__main__':
    main()
