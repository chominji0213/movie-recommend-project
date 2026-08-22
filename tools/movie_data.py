"""
TMDB API 호출 모듈 - 인기 영화 데이터를 가져와서 data/movies.json으로 저장.

weather_tool.py, restaurant_tool.py와 같은 역할: "데이터를 가져오는 배관 작업"만 담당.
이 파일은 최초 1회(또는 데이터 갱신하고 싶을 때) 직접 실행해서 data/movies.json을 만드는 용도.
"""
import os
import json
import requests
from dotenv import load_dotenv
from rich import print as rprint
load_dotenv()

BASE_URL = "https://api.themoviedb.org/3"
TMDB_API_KEY = os.getenv("TMDB_API_KEY")


def fetch_popular_movies(pages: int = 5) -> list[dict]:
    """
    TMDB의 "인기 영화" 목록을 여러 페이지 가져와서 필요한 필드만 정리해 반환.
    """
    movies = []
    
    for page in range(1, pages+1):
        params = {
            'api_key': TMDB_API_KEY,
            "language": "ko-KR",
            'page': page
        }
        res = requests.get(f"{BASE_URL}/movie/popular", params=params, timeout=5)
        res.raise_for_status()
        data = res.json()

        for d in data['results']:
            overview = d.get('overview', '')

            #overview가 빈 문자열인 영화는 건너뛰기
            if not overview:  
                continue

            movies.append({
                'id': d['id'],
                '제목': d['title'],
                '줄거리': overview,
                '개봉일': d['release_date'],
                '평점': d['vote_average'] 
            })

    return movies   


def save_movies_to_json(movies: list[dict], path: str = "data/movies.json"):
    """
    가져온 movie api 결과를 json 파일로 저장
    """
    os.makedirs(os.path.dirname(path), exist_ok=True) #data 폴더가 없으면 새로 생성

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(movies, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    # 터미널에서 python -m tools.movie_data 로 실행
    movies = fetch_popular_movies(pages=5)
    save_movies_to_json(movies)
    print(f"{len(movies)}개 영화 저장 완료")
