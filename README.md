# 📽️ Prompt Optimization-Based Video Generation Agent System

## 01. 프로젝트에 대한 정보

### 1. 프로젝트 제목

**Prompt Optimization-Based Video Generation Agent System**

### 2. 프로젝트 소개

사용자의 자연어 입력을 기반으로 AI가 자동으로 영상 제작에 최적화된 시네마틱 프롬프트를 생성하고, 이를 수정 및 편집한 후 최종 프롬프트로 Runway API를 통해 실제 영상을 생성하는 시스템입니다. 사용자의 프롬프트 수정 이력을 의미 기반 Diff로 저장하여 유사한 요청이 있을 때 자동으로 최적화된 프롬프트를 추천하는 기능을 포함하고 있습니다. Streamlit을 통해 직관적인 UI를 제공하고, FastAPI와 LangGraph를 활용해 안정적인 멀티에이전트 워크플로우를 구축했습니다.

## 02. 시작 가이드

### 1. 요구 사항

- Python >= 3.12
- Poetry
- OpenAI API Key (.env)
- Runway API Key (.env)
- Streamlit
- FastAPI

### 2. 설치 및 실행

```bash
# Repository 클론
git clone https://github.com/your-id/video-agent-system.git
cd video-agent-system

# Poetry로 환경 설정
poetry install

# 환경 변수 설정 (.env 파일 생성)
echo "OPENAI_API_KEY=your_openai_api_key" >> .env
echo "RUNWAY_API_KEY=your_runway_api_key" >> .env

# Diff 분석을 위한 모델 설치
poetry run python -m spacy download ko_core_news_sm

# FastAPI 서버 실행
poetry run uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

# Streamlit 프론트엔드 실행
poetry run streamlit run app.py
```

## 03. 기술 스택

- **Frontend**: Streamlit
- **Backend**: FastAPI, LangGraph
- **LLM Integration**: OpenAI GPT-4
- **Video API**: Runway Gen-4 Image & Gen-4 Turbo
- **Diff 분석**: difflib, spaCy(한국어 모델), sentence-transformers, HuggingFace emotion classifier
- **Embedding & Similarity**: OpenAI Embedding, cosine similarity, ChromaDB
- **다국어 지원**: 한국어 spaCy 모델, 다국어 임베딩 모델

## 04. 화면 구성

- 자연어 입력 → 프롬프트 생성
- 프롬프트 수정 → Diff 시각화 및 편집 의도 분석
- 영상 생성 → 생성된 영상 및 프롬프트 표시
- 과거 이력 기반 추천 → 최적화된 프롬프트 및 편집 질문 제안
- 전체 대화 히스토리 제공

![image](https://github.com/user-attachments/assets/cacad6e6-24b8-4619-be51-e34bcd89cde3)


## 05. 주요 기능

- **Prompt 생성 및 최적화**
  - 사용자 입력 기반 시네마틱 영상 프롬프트 자동 생성
  - 영상 API 최적화용 이미지 프롬프트 변환

- **Diff 기반 편집 관리**
  - 의미 기반 편집 분석 (명사, 구조, 감정 톤, 동작 추가 등)
  - 편집 의도 자동 추론
  - difflib(html) 기반 시각적 diff 제공

- **영상 생성**
  - Runway API를 통한 실제 영상 생성

- **프롬프트 이력 저장 및 재활용**
  - 프롬프트 및 diff 저장
  - 유사 프롬프트 추천

- **질문 추천**
  - 편집 가이드용 질문 자동 제안

- **다국어 지원**
  - 한국어 텍스트 분석 (ko_core_news_sm)
  - 다국어 임베딩 모델 (paraphrase-multilingual-MiniLM-L12-v2)

#### 질문 추천 경로 정리

| 조건                            | 처리 방식                                                                                         |
| ----------------------------- | --------------------------------------------------------------------------------------------- |
| JSON 이력 없음 (`result is None`) | 가장 최신에 저장된 JSON 기반 LLM이 최적화 프롬프트 및 질문 추천 생성                           |
| `data/` 폴더에 이력 존재, 유사도 0.65 이상 | `recommender.py`로 유사 JSON 반환 → `history_guided_prompt.jinja` 템플릿을 통해 LLM이 최적화 프롬프트 및 질문 추천 생성 |

## 06. 아키텍처 및 디렉토리 구조

```text
📦 video-agent-system
├── backend
│   ├── main.py                # FastAPI 진입점
│   └── agent_router.py        # HTTP 라우팅
├── agent
│   ├── node/                  # LangGraph 개별 노드 정의
│   ├── graph/                 # 워크플로우 정의
│   ├── templates/             # Jinja 템플릿
│   └── state.py               # 상태 관리 (VideoAgentState)
├── modules
│   ├── prompt_editor.py       # Diff 시각화
│   ├── semantic_diff.py       # 의미 기반 Diff
│   ├── intent_infer.py        # 편집 의도 추론
│   ├── recommender.py         # 유사 프롬프트 추천
│   ├── history_manager.py     # 프롬프트 저장
│   ├── vector_store.py        # ChromaDB 벡터 저장소
│   └── runway_api.py          # Runway API 호출
├── styles/
│   └── main.css, diff.css
├── data/
│   └── prompt_*.json          # 프롬프트 기록
├── chroma_db/                 # 벡터 데이터베이스 저장소
├── app.py                     # Streamlit 진입점
└── README.md
```

## 07. 시스템 워크플로우

### 기본 워크플로우

```
사용자 (Streamlit UI)
├── [입력] ──► FastAPI (/agent/start)
│              └─ LangGraph(generate_prompt_node)
├── [프롬프트 수정] ──► FastAPI (/agent/edit-preview)
│                        └─ LangGraph(edit_prompt_node)
└── [영상 생성 요청] ──► FastAPI (/agent/edit-confirm)
                         └─ LangGraph(save→optimize→video)
                               └─ Runway API 호출
```

### 유사 이력 기반 추천 워크플로우

```
사용자 입력
└─ ChromaDB 벡터 검색
    └─ 유사한 이전 프롬프트 검색
        ├─ 유사한 프롬프트 존재: 최적화 프롬프트 제공
        └─ 유사한 프롬프트 없음: 가장 최신 JSON 기반 질문 제공
```

## 08. 개발 진행 상황 및 Todo List

### 완료된 작업 ✅

- [x] 기본 시스템 아키텍처 설계 및 구현
- [x] LangGraph 기반 워크플로우 구축
- [x] Streamlit UI 개발
- [x] FastAPI 백엔드 서버 구현
- [x] 의미 기반 Diff 분석 기능 구현
- [x] 편집 의도 추론 기능 구현
- [x] Runway API 연동 (이미지 및 영상 생성)
- [x] 프롬프트 저장 및 관리 기능 구현
- [x] 세션 관리 기능 추가
- [x] ChromaDB 벡터 데이터베이스 통합
  - [x] 효율적인 임베딩 저장 및 검색 구현
  - [x] 실시간 임베딩 생성 대신 캐싱 방식 적용
  - [x] JSON 파일과 벡터 DB 동시 저장 구현
  - [x] 서버 시작 시 자동 데이터베이스 초기화
- [x] 다국어 지원 기능 추가
  - [x] 한국어 spaCy 모델(ko_core_news_sm) 통합
  - [x] 다국어 임베딩 모델 적용

### 향후 계획 📝

- [ ] 한국어 감정 분석 모델 통합
- [ ] spaCy 모델 비교 (Eng vs Ko)

