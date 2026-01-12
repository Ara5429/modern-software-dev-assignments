# Action Item Extractor

## 📋 Overview
- 노트 텍스트에서 액션 아이템(할 일)을 자동으로 추출하는 웹 애플리케이션입니다.
- 주요 기능:
  1. **휴리스틱 기반 추출**: 불릿, 체크박스, 키워드(TODO, Action 등)를 이용해 규칙 기반으로 액션 아이템을 추출합니다.
  2. **LLM 기반 추출 (Ollama)**: 로컬 LLM(Ollama)을 사용해 내러티브 형태의 노트에서도 유연하게 액션 아이템을 추출합니다.

## 🛠️ Tech Stack
- **Backend**: FastAPI, SQLite, Pydantic
- **Frontend**: Vanilla HTML/CSS/JavaScript
- **LLM**: Ollama (`llama3.1:8b` 또는 `mistral-nemo:12b`)
- **Testing**: pytest

## 🚀 Installation & Setup

### Prerequisites
- Python 3.10+
- Poetry
- Ollama

### Steps
1. (선택) 이 레포지토리를 클론합니다.
2. Conda 환경 생성:
   ```bash
   conda create -n cs146s python=3.10
   ```
3. 환경 활성화:
   ```bash
   conda activate cs146s
   ```
4. 의존성 설치:
   ```bash
   poetry install
   ```
5. Ollama 설치: `https://ollama.com`
6. 모델 다운로드:
   ```bash
   ollama pull llama3.1:8b
   ```
7. 추가 패키지 설치:
   ```bash
   pip install ollama python-dotenv pytest
   ```

## 🏃 Running the Application
```bash
poetry run uvicorn week2.app.main:app --reload
```

Access: `http://127.0.0.1:8000/`

## 📖 API Documentation
Swagger UI: `http://127.0.0.1:8000/docs`

## 🔌 API Endpoints

### Notes
- `POST /notes` - Create a new note
- `GET /notes` - List all notes
- `GET /notes/{note_id}` - Get single note

### Action Items
- `POST /action-items/extract` - Extract using heuristics
- `POST /action-items/extract-llm` - Extract using LLM
- `GET /action-items` - List action items
- `POST /action-items/{id}/done` - Mark as done

## 🧪 Running Tests
```bash
# All tests
pytest week2/tests/test_extract.py -v

# Integration tests only
pytest week2/tests/test_extract.py -v -m integration
```

## 🎯 Features
<!-- AI Generated - TODO 5 -->
- ✅ Heuristic-based extraction (bullets, keywords, checkboxes)
- ✅ LLM-powered extraction (Ollama integration)
- ✅ Note storage and retrieval
- ✅ Interactive web UI
- ✅ API documentation (Swagger)
- ✅ Type-safe with Pydantic
- ✅ CORS enabled
- ✅ Error handling

## 🤝 Development
This project was developed as part of CS146 Modern Software Development course, utilizing Cursor AI for code generation and refactoring.

## 📁 Project Structure
`week2/` 하위 구조:

```text
week2/
├── app/
│   ├── main.py           # FastAPI app
│   ├── schemas.py        # Pydantic models
│   ├── db.py             # Database layer
│   ├── routers/          # API endpoints
│   │   ├── notes.py
│   │   └── action_items.py
│   └── services/
│       └── extract.py    # Extraction logic
├── frontend/
│   └── index.html        # UI
├── tests/
│   └── test_extract.py   # Unit tests
└── data/
    └── app.db            # SQLite database
```

# Assignments for CS146S: The Modern Software Developer

This is the home of the assignments for [CS146S: The Modern Software Developer](https://themodernsoftware.dev), taught at Stanford University fall 2025.

## Repo Setup
These steps work with Python 3.12.

1. Install Anaconda
   - Download and install: [Anaconda Individual Edition](https://www.anaconda.com/download)
   - Open a new terminal so `conda` is on your `PATH`.

2. Create and activate a Conda environment (Python 3.12)
   ```bash
   conda create -n cs146s python=3.12 -y
   conda activate cs146s
   ```

3. Install Poetry
   ```bash
   curl -sSL https://install.python-poetry.org | python -
   ```

4. Install project dependencies with Poetry (inside the activated Conda env)
   From the repository root:
   ```bash
   poetry install --no-interaction
   ```