# Web Calculator

수식 입력 및 계산 기능을 제공하는 웹 계산기 애플리케이션

## 프로젝트 구조

```text
final-proj/
├── webcalc.html      # 계산기 UI
└── calc_service/     # FastAPI 서버
    ├── main.py
    ├── routes/       # API 엔드포인트
    ├── models/       # 데이터 모델
    └── database/     # DB 연결
```

## 기능

- 키패드/키보드로 수식 입력
- 이미지에서 수식 인식 (OCR)
- 수식 계산 및 히스토리 저장
- 저장된 수식 조회/삭제 (Recall)

## 실행 방법

### Backend

```bash
cd backend/calc_service
uv sync
uv run uvicorn main:app --host 0.0.0.0 --port 8000
```

### Frontend

`frontend/webcalc.html`을 브라우저에서 열기 (Live Server 등 사용)
