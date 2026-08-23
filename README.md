# 🎬 영화 추천 챗봇 (RAG)

사용자가 원하는 분위기나 취향을 말하면, 벡터DB에서 의미적으로 가장 비슷한 영화를 검색해 LLM이 추천 이유와 함께 답변해주는 챗봇입니다.

지금까지의 프로젝트(날씨 챗봇, 오늘 뭐 먹지 추천봇)가 외부 API를 즉시 호출하는 Tool Calling 구조였다면, 이 프로젝트는 처음으로 **RAG(Retrieval-Augmented Generation)** — 벡터DB에 미리 구축한 데이터를 검색해서 LLM에게 근거로 제공하는 방식 — 을 연습한 프로젝트입니다. 에이전트 오케스트레이션도 `create_agent`(LLM이 자동으로 도구 호출을 판단하는 방식) 대신, LangGraph의 `StateGraph`로 "검색 → 답변 생성" 흐름을 직접 설계했습니다.

**배포 링크**: https://movie-recommend-project-58a3.onrender.com
(Render 무료 플랜 특성상 15분 미접속 시 슬립 상태가 되며, 첫 접속 시 콜드 스타트로 몇십 초 정도 걸릴 수 있습니다.)

## 기술 스택

- **LLM**: Gemini API (`gemini-3.1-flash-lite`, via LangChain `init_chat_model`)
- **임베딩**: Gemini 임베딩 모델 (`gemini-embedding-2-preview`)
- **벡터DB**: Chroma (로컬 파일 기반, 서버/계정 불필요)
- **오케스트레이션**: LangGraph `StateGraph` (raw, `create_agent` 미사용)
- **대화 저장**: LangGraph `SqliteSaver` 체크포인터
- **데이터 소스**: TMDB(The Movie Database) Open API
- **UI**: Streamlit
- **배포**: Docker + Render

## 주요 기능

- 자연어로 원하는 영화 분위기/장르를 입력하면 벡터 검색 기반으로 추천
- 대화 히스토리 저장 및 "새 대화 시작" 기능 (스레드 단위로 대화 구분)
- 요청한 추천 개수를 반영해 답변 (예: "다섯 개 추천해줘")
- 검색 결과가 없거나 LLM 호출이 실패해도 앱이 죽지 않고 안내 메시지 표시

## 아키텍처

```
사용자 질문
   │
   ▼
[retrieve_node]  ── search_movies() 호출 → Chroma 벡터DB에서 의미 유사도 기반 검색
   │
   ▼
[generate_node]  ── 검색된 영화 목록 + 질문을 프롬프트에 담아 LLM 호출 → 추천 답변 생성
   │
   ▼
최종 답변 반환 (SqliteSaver가 스레드별 대화 기록 저장)
```

데이터 흐름은 별도로 다음과 같이 준비됩니다 (최초 1회 또는 컨테이너 시작 시):

```
TMDB API → movie_data.py → data/movies.json
                                   │
                                   ▼
                         vector_store.py (임베딩)
                                   │
                                   ▼
                        Chroma 벡터DB (vectorstore/)
```

## 프로젝트 구조

```
movie-recommend-project/
├── tools/
│   ├── movie_data.py      # TMDB API로 영화 데이터 수집 → data/movies.json 저장
│   └── vector_store.py    # 임베딩 변환 + Chroma 벡터DB 구축/검색
├── llm_client.py           # StateGraph 기반 RAG 에이전트 (retrieve → generate)
├── app.py                  # Streamlit UI
├── Dockerfile
├── entrypoint.sh            # 컨테이너 시작 시 데이터/벡터DB 자동 구축
├── requirements.txt
└── .env.example
```

## 로컬 실행 방법

```bash
# 1. 가상환경 및 의존성 설치
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

# 2. .env 파일 생성 (.env.example 참고)
#    GOOGLE_API_KEY=...
#    TMDB_API_KEY=...

# 3. 영화 데이터 수집 및 벡터DB 구축 (최초 1회)
python -m tools.movie_data
python -m tools.vector_store

# 4. 앱 실행
streamlit run app.py
```

### Docker로 실행

```bash
docker build -t movie-recommend-project .
docker run -p 8501:8501 --env-file .env movie-recommend-project
```

`entrypoint.sh`가 컨테이너 시작 시 `data/movies.json`, `vectorstore/`가 없으면 자동으로 생성합니다. 이미 존재하면 API를 재호출하지 않고 건너뜁니다.

## 알게 된 점 / 한계

- **벡터 검색은 숫자 조건을 이해하지 못함**: "평점 높은 순으로 추천해줘"라고 물어도, `similarity_search()`는 질문과 줄거리 텍스트의 의미적 유사도만 계산할 뿐 평점 같은 숫자 메타데이터로 정렬하지 않습니다. 구조화된 조건(평점순, 최신순 등)은 메타데이터 필터링/일반 정렬로 별도 처리해야 한다는 것을 확인했습니다.
- **멀티턴 대화에서 맥락 유지 안 됨**: 현재 State(`query`, `search_results`, `answer`)에는 이전 대화 요약/히스토리 필드가 없어서, "코믹로맨스 추천해줘" 다음에 "다섯 개 더 보여줘"라고 물으면 이전 턴의 맥락(장르)을 잃습니다. `SqliteSaver`가 대화 자체는 저장하지만, 매 턴 `retrieve_node`가 그 턴의 질문만으로 새로 검색하기 때문입니다. 본격적인 멀티턴 맥락 설계는 이후 프로젝트(에이전트 오케스트레이션 심화)에서 다룰 예정입니다.
- **벡터DB 중복 저장 주의**: `build_vector_store()`를 여러 번 실행하면 기존 컬렉션이 지워지지 않고 계속 추가되어 같은 영화가 중복 저장됩니다. 재구축 시 `vectorstore/` 폴더를 먼저 삭제해야 합니다.

## 향후 개선 아이디어

- State에 대화 히스토리 필드를 추가해 멀티턴 맥락 유지
- 평점/개봉일 등 구조화된 조건에 대한 메타데이터 필터링 추가
- 스트리밍 응답 지원 (`ask_stream`)
