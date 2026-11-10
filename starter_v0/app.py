from __future__ import annotations
import json
import os

import streamlit as st
from demo_runtime import ROOT, new_transcript, redact, run_turn, version_label
from tools import load_tool_declarations

st.set_page_config(page_title='ALI33 · Research Desk', page_icon='🔎', layout='wide')
st.markdown('''<style>
.block-container{max-width:1120px;padding-top:2.8rem;padding-bottom:5rem}
[data-testid="stSidebar"]{border-right:1px solid #e2e8f3}
.eyebrow{font-size:12px;font-weight:700;letter-spacing:.2em;color:#2263cf;margin-bottom:14px}
.hero{font-size:clamp(32px,4vw,52px);line-height:1.1;font-weight:750;letter-spacing:-.045em;color:#152441;margin:0 0 18px}
.intro{font-size:17px;line-height:1.65;color:#61718b;max-width:680px;margin-bottom:28px}
.badge{display:inline-block;background:#e9f0ff;color:#2559a0;border-radius:20px;padding:5px 11px;font-size:12px;margin:0 6px 9px 0}
[data-testid="stChatMessage"]{border:1px solid #e5eaf4;border-radius:16px;padding:1.2rem;margin:.6rem 0;background:white}
button{border-radius:9px!important}
</style>''', unsafe_allow_html=True)

if 'transcript' not in st.session_state:
    st.session_state.transcript = new_transcript()
transcript = st.session_state.transcript
tools = load_tool_declarations(ROOT/'artifacts/tools.yaml')
names = {tool['name'] for tool in tools}
pending = None

with st.sidebar:
    st.markdown('### 🔎 ALI33\nResearch Desk')
    st.caption('Tìm nguồn · Đọc bài · Tổng hợp có dẫn chứng')
    st.divider()
    st.markdown('**Bắt đầu nhanh**')
    examples = [
        ('📰 Tin AI hôm nay', 'Tìm 3 tin AI hôm nay trên web, có nguồn để tôi tự đọc.'),
        ('💬 Bài đăng của Sam Altman', 'Lấy 3 tweet mới nhất của Sam Altman, dẫn link từng bài.'),
        ('📄 Đọc một đường dẫn', 'Đọc và tóm tắt trang https://example.com, giữ link nguồn.'),
        ('📚 Quy định trích nguồn', 'Tìm trong policy nội bộ quy định về citation và nguồn social.'),
    ]
    for label, query in examples:
        if st.button(label, use_container_width=True):
            pending = query
    st.divider()
    with st.expander(f'{len(names)} công cụ khả dụng'):
        for name in sorted(names):
            st.markdown('`'+name+'`')
    st.caption('Gửi Telegram đang tắt trong bản demo. Yêu cầu gửi vẫn cần xác nhận; không có tin nhắn được gửi ra ngoài.')
    st.caption('Phiên bản: ' + version_label())
    if st.button('Bắt đầu cuộc trò chuyện mới', use_container_width=True):
        st.session_state.transcript = new_transcript()
        st.rerun()
    st.download_button('Tải nhật ký phiên này', json.dumps(redact(transcript), ensure_ascii=False, indent=2),
                       file_name='ali33-session.transcript.json', mime='application/json', use_container_width=True)

st.markdown('<div class="eyebrow">ALI33 / RESEARCH DESK</div>', unsafe_allow_html=True)
st.markdown('<div class="hero">Từ câu hỏi đến<br>bản tin có nguồn.</div>', unsafe_allow_html=True)
st.markdown('<div class="intro">Tra cứu web và mạng xã hội, đọc tài liệu, lọc nguồn trùng. Mỗi bước đều có nhật ký để bạn kiểm tra.</div>', unsafe_allow_html=True)
st.markdown('<span class="badge">Web & tin tức</span><span class="badge">Bài đăng trên X</span><span class="badge">URL & tài liệu</span><span class="badge">Người dùng quyết định</span>', unsafe_allow_html=True)

if not transcript['turns']:
    left, right = st.columns(2)
    with left:
        with st.container(border=True):
            st.markdown('**01 · Đặt câu hỏi cụ thể**')
            st.write('Nêu chủ đề, tài khoản hoặc URL; thêm số lượng và khoảng thời gian nếu cần.')
    with right:
        with st.container(border=True):
            st.markdown('**02 · Kiểm tra nguồn trước khi dùng**')
            st.write('Mở link gốc, xem bước gọi công cụ và các lỗi được hiển thị ngay trong phiên.')


def render_turn(turn):
    with st.chat_message('user'):
        st.write(turn['user'])
    with st.chat_message('assistant'):
        if turn.get('error'):
            st.error(turn['error'])
        elif turn.get('assistant_text'):
            st.markdown(turn['assistant_text'])
        else:
            st.info('Chưa có câu trả lời; xem nhật ký xử lý bên dưới.')
        for event in turn.get('tool_events', []):
            result = event.get('result', {})
            if isinstance(result, dict) and result.get('error'):
                st.error(f"{event['tool']}: {result.get('error')} — {result.get('message', '')}")
            if isinstance(result, dict) and result.get('status') == 'disabled':
                st.info('Gửi tin đang tắt trong bản demo; chưa có nội dung nào được gửi.')
        events = turn.get('tool_events', [])
        st.caption(f"{turn.get('elapsed_seconds', 0):g}s · {len(events)} lần gọi công cụ · {turn.get('status', '')}")
        if events:
            with st.expander('Xem công cụ, dữ liệu và nguồn'):
                st.json(redact(events))


for turn in transcript['turns']:
    render_turn(turn)

ready = bool(os.getenv('OPENROUTER_API_KEY'))
limit_reached = len(transcript['turns']) >= 15
if not ready:
    st.error('Dịch vụ model chưa được cấu hình trên máy chủ. Vui lòng liên hệ người vận hành demo.')
if limit_reached:
    st.info('Phiên này đã đủ 15 lượt. Tải nhật ký rồi bắt đầu cuộc trò chuyện mới nếu cần.')
submitted = st.chat_input('Bạn muốn tìm hiểu điều gì? Ví dụ: tin robotics trong tuần này…',
                          key='research_input', max_chars=4000, disabled=not ready or limit_reached)
query = submitted or pending
if query and ready and not limit_reached:
    with st.chat_message('user'):
        st.write(query)
    with st.spinner('Đang tra cứu và đối chiếu nguồn…'):
        run_turn(query, transcript)
    st.rerun()
