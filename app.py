import streamlit as st
import uuid
from llm_client import build_agent, ask

# TODO: what-to-eat-project의 app.py를 그대로 복사해서 가져오고 아래 2가지만 바꾸기
#   1) st.title("...")을 "영화 추천 챗봇"으로 변경
#   2) st.chat_input(...) 안내 문구를 영화 취향을 물어보는 문구로 변경
#      예: st.chat_input("어떤 분위기의 영화를 찾으세요?")
#
# 사이드바 "새 대화 시작" 버튼은 what-to-eat-project 그대로 재사용하면 됨.
#
# 주의: 이번 llm_client.py는 raw StateGraph 미니 연습 버전이라 ask_stream()이 없어.
# 그래서 답변 출력 부분은 st.write_stream() 대신 what-to-eat-project 시즌1 때처럼
# answer = ask(...) 로 받아서 st.write(answer)로 그냥 한 번에 보여주면 돼
# (스트리밍은 나중에 여유 생기면 추가로 도전해볼 선택 과제).
