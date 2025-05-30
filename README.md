
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

# Diff 분석을 위한 모델 설치치
poetry run python -m spacy download en_core_web_sm

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
- **Diff 분석**: difflib, spaCy, sentence-transformers, HuggingFace emotion classifier
- **Embedding & Similarity**: OpenAI Embedding, cosine similarity

## 04. 화면 구성

- 자연어 입력 → 프롬프트 생성
- 프롬프트 수정 → Diff 시각화 및 편집 의도 분석
- 영상 생성 → 생성된 영상 및 프롬프트 표시
- 과거 이력 기반 추천 → 최적화된 프롬프트 및 편집 질문 제안
- 전체 대화 히스토리 제공

## 05. 주요 기능

- **Prompt 생성 및 최적화**
  - 사용자 입력 기반 시네마틱 영상 프롬프트 자동 생성
  - 영상 API 최적화용 이미지 프롬프트 변환

- **Diff 기반 편집 관리**
  - 의미 기반 편집 분석 (명사, 구조, 감정 톤, 동작 추가 등)
  - 편집 의도 자동 추론
  - difflib 기반 시각적 diff 제공

- **영상 생성**
  - Runway API를 통한 실제 영상 생성

- **프롬프트 이력 저장 및 재활용**
  - 프롬프트 및 diff 저장
  - 유사 프롬프트 추천

- **질문 추천**
  - 편집 가이드용 질문 자동 제안

#### 질문 추천 경로 정리

| 조건                            | 처리 방식                                                                                         |
| ----------------------------- | --------------------------------------------------------------------------------------------- |
| JSON 이력 없음 (`result is None`) | `question_generator.py`를 사용하여 의도 기반 힌트 질문 제시 (fallback 질문 추천)                                 |
| `data/` 폴더에 이력 존재, 유사도 0.8 이상 | `recommender.py`로 유사 JSON 반환 → `history_guided_prompt.jinja` 템플릿을 통해 LLM이 최적화 프롬프트 및 질문 추천 생성 |

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
│   └── runway_api.py          # Runway API 호출
├── styles/
│   └── main.css, diff.css
├── data/
│   └── prompt_*.json          # 프롬프트 기록
├── app.py                     # Streamlit 진입점
└── README.md
