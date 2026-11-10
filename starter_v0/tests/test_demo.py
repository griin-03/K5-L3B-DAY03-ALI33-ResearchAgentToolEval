from pathlib import Path

from providers.base import ModelResponse, ToolCall
from streamlit.testing.v1 import AppTest
from demo_runtime import guarded_execute, new_transcript, run_turn


def test_demo_blocks_actual_delivery_and_preserves_requested_call(fake_http):
    calls = fake_http(None)
    event = guarded_execute(ToolCall('send', {'text': 'Never deliver', 'confirmed': True}))
    assert event['tool'] == 'send' and event['args']['confirmed'] is True
    assert event['result']['status'] == 'disabled'
    assert calls == []


def test_demo_real_loop_can_pause_for_missing_information(monkeypatch, tmp_path):
    class Provider:
        def complete(self, *args, **kwargs):
            return ModelResponse(text=None, tool_calls=[ToolCall('clarify', {'question': 'URL nào?', 'response_type': 'text'})])
    monkeypatch.setattr('demo_runtime.make_provider', lambda _: Provider())
    monkeypatch.setenv('DAY03_TRANSCRIPTS_DIR', str(tmp_path))
    transcript = new_transcript()
    result = run_turn('Tóm tắt bài này', transcript)
    assert result['status'] == 'waiting_for_user' and result['assistant_text'] == 'URL nào?'
    assert result['tool_events'][0]['tool'] == 'clarify'
    assert len(list(tmp_path.glob('*.transcript.json'))) == 1


def test_ui_loads_and_chat_turn_is_logged(monkeypatch, tmp_path):
    class Provider:
        def complete(self, *args, **kwargs):
            return ModelResponse(text='Tôi là trợ lý nghiên cứu ALI33.', tool_calls=[])
    monkeypatch.delenv('DEMO_ACCESS_CODE', raising=False)
    monkeypatch.setenv('OPENROUTER_API_KEY', 'test-key-only')
    monkeypatch.setenv('DAY03_TRANSCRIPTS_DIR', str(tmp_path))
    monkeypatch.setattr('demo_runtime.make_provider', lambda _: Provider())
    app = AppTest.from_file(str(Path(__file__).resolve().parents[1]/'app.py')).run(timeout=15)
    assert not app.exception and len(app.chat_input) == 1
    app.chat_input[0].set_value('Bạn làm được gì?').run(timeout=15)
    assert not app.exception
    assert len(app.session_state['transcript']['turns']) == 1
    assert app.session_state['transcript']['turns'][0]['status'] == 'answered'
    assert len(list(tmp_path.glob('*.transcript.json'))) == 1


def test_access_code_is_required_before_chat(monkeypatch):
    monkeypatch.setenv('DEMO_ACCESS_CODE', 'unit-test-code')
    app = AppTest.from_file(str(Path(__file__).resolve().parents[1]/'app.py')).run(timeout=15)
    assert not app.exception and len(app.chat_input) == 0
    app.text_input[0].set_value('wrong')
    app.button[0].click().run(timeout=15)
    assert len(app.error) == 1 and len(app.chat_input) == 0
