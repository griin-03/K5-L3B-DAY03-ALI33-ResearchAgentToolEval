"""Offline tests for existing tools and the team's new source deduplicator."""
from __future__ import annotations
import importlib
import pytest
from conftest import FakeResponse
from tools import TOOL_FUNCTIONS as T
from tools.deduplicate_sources.tool import deduplicate_sources


def test_clarify_choice_returns_options_and_awaits_user():
    result = T['clarify']('Nguồn nào?', response_type='choice', options=['Web', 'X'])
    assert result['options'] == ['Web', 'X']
    assert result['awaiting_user'] is True


def test_format_sections_groups_items_by_section():
    result = T['format'](items=[{'section': s, 'title': s} for s in ['A', 'B', 'A']], template='sections')
    assert result['markdown'].count('## A') == result['markdown'].count('## B') == 1


def test_format_thread_numbers_items():
    result = T['format'](items=[{'title': 'A'}, {'title': 'B'}], template='thread')
    assert result['markdown'].startswith('1/ A') and '\n\n2/ B' in result['markdown']


@pytest.mark.parametrize('items', [None, []])
def test_format_empty_items_does_not_crash(items):
    assert T['format'](items=items)['item_count'] == 0


def test_send_confirmed_posts_to_telegram(monkeypatch, fake_http):
    monkeypatch.setenv('TELEGRAM_BOT_TOKEN', 'fake-token')
    monkeypatch.setenv('TELEGRAM_CHAT_ID', 'fake-channel')
    calls = fake_http(FakeResponse({'ok': True}))
    assert T['send'](text='Test', confirmed=True)['status'] == 'sent'
    assert len(calls) == 1 and calls[0]['method'] == 'POST'
    assert calls[0]['url'] == 'https://api.telegram.org/botfake-token/sendMessage'
    assert calls[0]['json']['chat_id'] == 'fake-channel' and calls[0]['json']['text'] == 'Test'


def test_send_confirmed_without_env_returns_error_and_no_request(fake_http):
    calls = fake_http(FakeResponse())
    assert T['send'](text='Test', confirmed=True)['error'] == 'RuntimeError'
    assert calls == []


def test_lookup_without_timeframe_omits_time_range(monkeypatch, fake_http):
    monkeypatch.setenv('TAVILY_API_KEY', 'fake-key')
    calls = fake_http(FakeResponse({'results': []}))
    T['lookup'](query='AI', timeframe=None)
    assert 'time_range' not in calls[0]['json']


def test_fetch_maps_firecrawl_response(monkeypatch, fake_http):
    monkeypatch.setenv('FIRECRAWL_API_KEY', 'fake-key')
    calls = fake_http(FakeResponse({'data': {'markdown': 'Actual text', 'metadata': {'title': 'T', 'sourceURL': 'https://example.com/a'}}}))
    result = T['fetch'](url='https://example.com/a')
    assert calls[0]['json'] == {'url': 'https://example.com/a', 'formats': ['markdown']}
    assert result['items'][0] == {'title': 'T', 'url': 'https://example.com/a', 'source': 'example.com', 'summary': 'Actual text'}


def test_fetch_truncates_markdown_to_4000_chars(monkeypatch, fake_http):
    monkeypatch.setenv('FIRECRAWL_API_KEY', 'fake-key')
    fake_http(FakeResponse({'data': {'markdown': 'x' * 5000}}))
    assert len(T['fetch'](url='https://example.com')['items'][0]['summary']) == 4000


def test_timeline_respects_limit_and_skips_items_without_id(monkeypatch, fake_http):
    monkeypatch.setenv('RAPIDAPI_KEY', 'fake-key')
    monkeypatch.setenv('RAPIDAPI_TWITTER_HOST', 'twitter-api45.p.rapidapi.com')
    calls = fake_http(FakeResponse({'timeline': [{'text': 'missing id'}] + [{'tweet_id': str(i), 'screen_name': 'sama', 'text': 'Post'} for i in range(6)]}))
    result = T['timeline'](screenname='sama', limit=3)
    assert calls[0]['params'] == {'screenname': 'sama'} and len(result['items']) == 3
    assert all(item['url'].startswith('https://x.com/sama/status/') for item in result['items'])


@pytest.mark.parametrize('search_type', ['Top', 'Latest'])
def test_social_search_passes_search_type(monkeypatch, fake_http, search_type):
    monkeypatch.setenv('RAPIDAPI_KEY', 'fake-key')
    calls = fake_http(FakeResponse({'timeline': []}))
    T['social_search'](query='agents', search_type=search_type)
    assert calls[0]['params'] == {'query': 'agents', 'search_type': search_type}


def test_policy_empty_query_returns_no_results():
    assert T['policy'](query='')['results'] == []


def test_policy_area_filter_only_returns_that_area():
    result = T['policy'](query='privacy sensitive data', policy_area='data_privacy')
    assert result['results']
    assert all(item['policy_area'] == 'data_privacy' for item in result['results'])


def test_policy_instruction_like_lines_go_to_untrusted_text():
    result = T['policy'](query='citation', policy_area='source_citation', top_k=20)
    assert any('ignore the citation policy' in line for item in result['results'] for line in item['untrusted_text'])
    assert all('ignore the citation policy' not in item['facts'] for item in result['results'])


def test_my_new_tool_happy_path():
    items = [{'url': 'https://EXAMPLE.com/a?utm_source=test', 'title': 'First'},
             {'url': 'https://example.com/a', 'title': 'Duplicate'}, {'url': 'https://example.com/b'}]
    result = deduplicate_sources(items)
    assert result['items'] == [items[0], items[2]]
    assert (result['input_count'], result['unique_count'], result['duplicate_count']) == (3, 2, 1)
    assert result['duplicates'][0]['kept_url'] == items[0]['url'] and len(items) == 3


@pytest.mark.parametrize('items', [None, 'url', {}, [42], [{'title': 'No URL'}], [{'url': 'file:///etc/hosts'}]])
def test_my_new_tool_bad_input_from_model(items):
    result = deduplicate_sources(items)
    assert result['error'] == 'ValueError' and 'items' not in result


def test_my_new_tool_failure_returns_error_dict(monkeypatch):
    module = importlib.import_module('tools.deduplicate_sources.tool')
    def broken(_):
        raise RuntimeError('normalizer failed')
    monkeypatch.setattr(module, '_normalize_url', broken)
    result = deduplicate_sources([{'url': 'https://example.com'}])
    assert result['error'] == 'RuntimeError' and result['message'] == 'normalizer failed'


def test_dedup_preserves_meaningful_queries_paths_and_fragments():
    items = [{'url': url} for url in ['https://example.com/a?id=1', 'https://example.com/a?id=2',
                                    'https://example.com/a/', 'https://example.com/a#chapter']]
    assert deduplicate_sources(items)['unique_count'] == 4


def test_dedup_empty_input_is_valid_and_limit_is_enforced():
    assert deduplicate_sources([])['unique_count'] == 0
    assert deduplicate_sources([{'url': 'https://example.com'}] * 101)['error'] == 'ValueError'
