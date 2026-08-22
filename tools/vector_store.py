"""
영화 데이터를 임베딩으로 변환해 Chroma 벡터DB에 저장하고, 의미 기반으로 검색하는 모듈.

- build_vector_store(): movies.json을 읽어서 벡터DB를 "구축"하는 함수 (최초 1회 실행)
- search_movies(): 벡터DB에서 "검색"하는 함수 (LLM이 Tool Calling으로 매번 호출)
"""
import json
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from rich import print as rprint

load_dotenv()


PERSIST_DIR = "vectorstore"
EMBEDDING_MODEL = "gemini-embedding-2-preview"


def build_vector_store(movies_path: str = "data/movies.json"):
    """
    영화 데이터를 읽어서 임베딩으로 변환하고 Chroma에 저장하는 함수.
    데이터가 바뀌지 않는 한 딱 한 번만 실행하면 됨.
    """
    with open(movies_path, 'r', encoding='UTF-8') as f:
        movies = json.load(f)

    documents = []
    for movie in movies:
        documents.append(Document(
            page_content=movie['줄거리'],
            metadata={
                '제목': movie['제목'],
                '개봉일': movie['개봉일'],
                '평점': movie['평점']
            }
        ))

    embeddings = GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL)
    Chroma.from_documents(documents=documents, embedding=embeddings, persist_directory=PERSIST_DIR) #persist_directory: 만든 벡터DB를 이 폴더에 파일로 저장(영구저장)


def load_vector_store():
    """
    이미 build_vector_store()로 만들어둔 벡터DB를 다시 불러오는 함수.
    search_movies()에서 매번 새로 만들지 않고 이 함수로 기존 것을 불러와서 씀.
    """
    return Chroma(
        persist_directory=PERSIST_DIR,
        embedding_function=GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL)
    )


def search_movies(query: str, k: int = 5) -> dict:
    """
    사용자의 취향/질문과 의미적으로 비슷한 영화를 벡터DB에서 검색.
    LLM이 Tool Calling으로 호출할 함수
    """
    vector_store = load_vector_store()
    results = vector_store.similarity_search(query, k=k)

    if not results:
        return {'error': '검색결과가 없습니다.'}

    movies = []
    for doc in results:
        movies.append({
            '제목': doc.metadata['제목'],
            '줄거리': doc.page_content,
            '개봉일': doc.metadata['개봉일'],
            '평점': doc.metadata['평점']
        })

    return {'검색어': query, '결과': movies}


if __name__ == "__main__":
    # 터미널에서 python -m tools.vector_store 로 최초 1회 실행해서 벡터DB 구축
    # build_vector_store()
    # print("벡터DB 구축 완료")

    # 구축 후 바로 검색 테스트 해보고 싶으면 아래 주석 풀기
    # from rich import print as rprint
    rprint(search_movies("평점이 높은 영화 10개정도 알려줘"))
