"""
영화 추천 RAG 에이전트.

what-to-eat-project의 llm_client.py와 전체 구조는 동일함 (create_agent + SqliteSaver + ask/ask_stream).
바뀌는 건 도구(tool)와 system_prompt뿐 — 이미 배운 패턴이니 이전 코드를 최대한 재사용해서 채워봐.
"""

# TODO: import
#   what-to-eat-project/llm_client.py의 import를 그대로 가져오되,
#   from tools.weather_tool import get_weather
#   from tools.restaurant_tool import get_restaurant
#   위 두 줄을 지우고 대신:
#   from tools.vector_store import search_movies


def build_agent():
    """
    TODO: what-to-eat-project의 build_agent()를 거의 그대로 복사해서 쓰되:
      - SqliteSaver 체크포인터 부분은 완전히 동일 (이미 배운 패턴 그대로 재사용)
      - tools=[search_movies] 로 변경 (도구 1개짜리 에이전트)
      - system_prompt만 새로 작성
        (예: "너는 사용자의 취향, 원하는 분위기나 장르를 듣고 영화를 추천하는 챗봇이야.
              반드시 search_movies 도구로 검색한 영화들 중에서만 추천하고,
              왜 그 영화가 사용자 취향에 맞는지 이유를 함께 설명해줘.
              검색 결과에 마음에 드는 영화가 없다면 다른 취향을 물어봐줘.")
    """
    pass


def ask(agent, user_message: str, thread_id: str) -> str:
    """
    TODO: what-to-eat-project의 ask()와 완전히 동일한 코드.
    (도메인이 영화로 바뀌어도 이 함수 내용 자체는 하나도 바뀔 게 없음 — 그대로 복사)
    """
    pass


def ask_stream(agent, user_message: str, thread_id: str):
    """
    TODO: what-to-eat-project의 ask_stream()과 완전히 동일한 코드.
    (마찬가지로 그대로 복사해서 재사용하면 됨)
    """
    pass


if __name__ == "__main__":
    agent = build_agent()
    print(ask(agent, "우주를 배경으로 한 감동적인 영화 추천해줘", "test-thread"))
