"""
TMDB API 호출 모듈 - 인기 영화 데이터를 가져와서 data/movies.json으로 저장.

weather_tool.py, restaurant_tool.py와 같은 역할: "데이터를 가져오는 배관 작업"만 담당.
이 파일은 최초 1회(또는 데이터 갱신하고 싶을 때) 직접 실행해서 data/movies.json을 만드는 용도야.
LLM이 실시간으로 호출하는 함수가 아니라는 점이 weather_tool/restaurant_tool과 다름.
"""

# TODO: import
#   import os
#   import json
#   import requests
#   from dotenv import load_dotenv
#   load_dotenv()

# TODO: 상수 정의
#   BASE_URL = "https://api.themoviedb.org/3"
#   TMDB_API_KEY = os.getenv("TMDB_API_KEY")


def fetch_popular_movies(pages: int = 5) -> list[dict]:
    """
    TMDB의 "인기 영화" 목록을 여러 페이지 가져와서 필요한 필드만 정리해 반환.

    TODO 1: 빈 리스트 만들기 (결과 담을 곳)

    TODO 2: 1페이지부터 pages까지 for문으로 반복하면서
      - GET {BASE_URL}/movie/popular
      - params = {"api_key": TMDB_API_KEY, "language": "ko-KR", "page": 현재_페이지_번호}
      - res.raise_for_status(), data = res.json()
      - data["results"]가 그 페이지에 있는 영화 리스트 (보통 페이지당 20개)

    TODO 3: data["results"]의 각 영화에서 필요한 필드만 뽑아서 딕셔너리로 만들고 리스트에 추가
      - id -> "id"
      - title -> "제목"
      - overview -> "줄거리"   (이게 나중에 임베딩/검색에 쓸 핵심 텍스트)
      - release_date -> "개봉일"
      - vote_average -> "평점"
      - 주의: overview가 빈 문자열인 영화는 건너뛰기 (검색할 텍스트가 없으면 RAG에 쓸모없음)

    TODO 4: 완성된 리스트 반환
    """
    pass


def save_movies_to_json(movies: list[dict], path: str = "data/movies.json"):
    """
    TODO 1: os.makedirs(os.path.dirname(path), exist_ok=True)로 data 폴더가 없으면 생성

    TODO 2: json.dump(movies, f, ensure_ascii=False, indent=2)로 저장
      - ensure_ascii=False를 꼭 넣어야 한글이 유니코드 escape(\\uXXXX)로 안 깨지고 저장됨
    """
    pass


if __name__ == "__main__":
    # 터미널에서 python -m tools.movie_data 로 실행 (최초 1회, 데이터 수집용)
    movies = fetch_popular_movies(pages=5)
    save_movies_to_json(movies)
    print(f"{len(movies)}개 영화 저장 완료")
