import streamlit as st
import uuid
from llm_client import build_agent, ask, ask_stream

# TODO: what-to-eat-project의 app.py를 그대로 복사해서 가져오고 아래 2가지만 바꾸기
#   1) st.title("...")을 "영화 추천 챗봇"으로 변경
#   2) st.chat_input(...) 안내 문구를 영화 취향을 물어보는 문구로 변경
#      예: st.chat_input("어떤 분위기의 영화를 찾으세요?")
#
# 사이드바 "새 대화 시작" 버튼, st.write_stream() 스트리밍 응답까지
# what-to-eat-project에서 이미 구현했던 그대로 재사용하면 됨 (새로 짤 부분 없음)
