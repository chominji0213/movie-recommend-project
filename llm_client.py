"""
영화 추천 RAG 에이전트 - raw LangGraph StateGraph
"""
from typing import TypedDict
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3
from tools.vector_store import search_movies
from rich import print as rprint

class MovieState(TypedDict):
    query: str              # 사용자 질문
    search_results: dict    # search_movies() 검색 결과
    answer: str             # 최종 답변


def retrieve_node(state):
    """
    검색 노드: state["query"]로 벡터DB를 검색해서 state["search_results"]를 채워 반환.
    """
    result = search_movies(state['query'])

    return {'search_results': result}


def generate_node(state):
    """
    답변 생성 노드: state["search_results"]를 참고해서 LLM에게 추천 답변을 만들게 하고
    state["answer"]를 채워 반환.
    """
    search_results = state["search_results"]

    if isinstance(search_results, dict) and "error" in search_results:
        return {"answer": "죄송해요, 취향에 맞는 영화를 찾지 못했어요. 다른 분위기나 키워드로 다시 말씀해 주시겠어요?"}

    llm = init_chat_model('gemini-3.1-flash-lite', model_provider='google_genai')
    prompt = f'''
          사용자 질문: {state["query"]}
          검색된 영화 목록: {search_results}

          위 영화들 중에서 사용자 취향에 가장 맞는 영화를 골라 이유와 함께 추천해줘.
          검색 결과에 마음에 드는 영화가 없다면 다른 취향을 물어봐줘.
          '''

    try:
        result = llm.invoke([HumanMessage(content=prompt)])
        content = result.content

        answer = content[0]['text'] if isinstance(content, list) else content
    except Exception as e:
        rprint(f"[generate_node] LLM 호출 실패: {e}")
        answer = "죄송해요, 지금 답변을 생성하는 중 문제가 생겼어요. 잠시 후 다시 시도해 주세요."

    return {'answer': answer}


def build_agent():
    """
    retrieve_node -> generate_node 순서로 연결된 그래프를 만들고 컴파일해서 반환.
    """
    conn = sqlite3.connect('checkpoint.db', check_same_thread=False)
    memory = SqliteSaver(conn)

    graph = StateGraph(MovieState)

    graph.add_node('retrieve', retrieve_node)
    graph.add_node('generate', generate_node)

    graph.add_edge(START, 'retrieve')
    graph.add_edge('retrieve', 'generate')
    graph.add_edge('generate', END)

    app = graph.compile(checkpointer=memory)

    return app


def ask(agent, user_message: str, thread_id: str) -> str:
    """
    사용자 질문을 받아 에이전트(그래프)를 실행하고 최종 답변만 반환하는 진입점 함수.
    app.py 등 외부에서는 State 구조를 몰라도 이 함수 하나만 호출하면 됨.
    thread_id로 SqliteSaver가 대화별 기록을 구분해서 저장/이어감.
    """
    config = {'configurable': {'thread_id': thread_id}}
    result = agent.invoke({'query': user_message}, config)

    return result['answer']


if __name__ == "__main__":
    agent = build_agent()
    print(ask(agent, "우주를 배경으로 한 감동적인 영화 추천해줘", "test-thread"))
