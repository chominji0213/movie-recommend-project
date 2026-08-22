"""
영화 데이터를 임베딩으로 변환해 Chroma 벡터DB에 저장하고, 의미 기반으로 검색하는 모듈.

이 파일이 이번 프로젝트의 핵심(RAG)이야:
- build_vector_store(): movies.json을 읽어서 벡터DB를 "구축"하는 함수 (최초 1회 실행)
- search_movies(): 벡터DB에서 "검색"하는 함수 (LLM이 Tool Calling으로 매번 호출)
"""

# TODO: import
#   import json
#   from langchain_google_genai import GoogleGenerativeAIEmbeddings
#   from langchain_chroma import Chroma
#   from langchain_core.documents import Document
#
#   (langchain-chroma 패키지가 따로 필요하면 requirements.txt에 추가하고 pip install)

PERSIST_DIR = "vectorstore"
EMBEDDING_MODEL = "models/text-embedding-004"


def build_vector_store(movies_path: str = "data/movies.json"):
    """
    영화 데이터를 읽어서 임베딩으로 변환하고 Chroma에 저장(구축)하는 함수.
    데이터가 바뀌지 않는 한 딱 한 번만 실행하면 됨.

    TODO 1: movies_path 파일을 열어서 json.load로 영화 리스트 읽기

    TODO 2: 각 영화를 Document 객체로 변환해서 리스트에 담기
      documents = []
      for movie in movies:
          documents.append(Document(
              page_content=movie["줄거리"],   # 임베딩 대상이 되는 실제 텍스트
              metadata={
                  "제목": movie["제목"],
                  "개봉일": movie["개봉일"],
                  "평점": movie["평점"],
              },
          ))
      - metadata는 검색 결과로 나왔을 때 "부가로 같이 보여줄 정보"라고 생각하면 됨
        (임베딩 자체는 page_content만 가지고 계산됨)

    TODO 3: 임베딩 모델 준비
      embeddings = GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL)

    TODO 4: Chroma.from_documents(documents=documents, embedding=embeddings, persist_directory=PERSIST_DIR)
      - 이 한 줄이 "documents 각각을 임베딩으로 변환 + 벡터DB에 저장"을 한 번에 처리해줌
      - persist_directory를 지정하면 vectorstore/ 폴더에 파일로 저장되어서,
        프로그램을 재시작해도 임베딩을 다시 계산할 필요 없이 불러오기만 하면 됨
        (이것도 결국 지난 프로젝트의 SqliteSaver랑 같은 맥락 - "메모리에만 두지 말고 파일로 영구 저장"이라는 개념)
    """
    pass


def load_vector_store():
    """
    이미 build_vector_store()로 만들어둔 벡터DB를 다시 불러오는 함수.
    search_movies()에서 매번 새로 만들지 않고 이 함수로 기존 것을 불러와서 씀.

    TODO: return Chroma(
        persist_directory=PERSIST_DIR,
        embedding_function=GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL),
    )
    """
    pass


def search_movies(query: str, k: int = 3) -> dict:
    """
    사용자의 취향/질문과 의미적으로 비슷한 영화를 벡터DB에서 검색.
    LLM이 Tool Calling으로 호출할 함수 (restaurant_tool.py의 get_restaurant와 같은 역할).

    TODO 1: load_vector_store()로 벡터DB 인스턴스 가져오기

    TODO 2: vector_store.similarity_search(query, k=k) 호출
      - 이게 "query와 의미상 가장 가까운 문서 k개"를 찾아주는 핵심 RAG 검색 함수
      - 결과는 Document 객체 리스트로 옴

    TODO 3: 검색된 각 Document에서 필요한 정보를 꺼내 딕셔너리로 정리
      - restaurant_tool.py의 _parse_restaurants()처럼, LLM이 읽기 좋은 형태로 가공
      - doc.page_content -> "줄거리"
      - doc.metadata["제목"] -> "제목"
      - doc.metadata["개봉일"], doc.metadata["평점"]도 같이 포함

    TODO 4: {"검색어": query, "결과": 정리된_리스트} 형태로 반환
      - 벡터DB에 데이터가 아예 없거나 결과가 비어있으면 {"error": "..."} 반환 (기존 패턴과 동일)
    """
    pass


if __name__ == "__main__":
    # 터미널에서 python -m tools.vector_store 로 최초 1회 실행해서 벡터DB 구축
    build_vector_store()
    print("벡터DB 구축 완료")

    # 구축 후 바로 검색 테스트 해보고 싶으면 아래 주석 풀기
    # from rich import print as rprint
    # rprint(search_movies("우주를 배경으로 한 감동적인 영화"))
