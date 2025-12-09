from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import conn
from routes import eval_router, mem_router, ocr_router


# 수업에서 다루지 않은, non-deprecated 방식의 테이블 생성 및 연결
@asynccontextmanager
async def lifespan(app: FastAPI):
    """앱 시작시 DB 테이블 생성"""
    conn()
    yield


app = FastAPI(
    lifespan=lifespan,
)

# CORS 설정 (Frontend에서 접근 허용)
# front와 back을 같은 머신에서 로컬로 실행시에는 필요하지 않음
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(eval_router)
app.include_router(mem_router)
app.include_router(ocr_router)


# healthcheck 용도
@app.get("/")
def root():
    return {"message": "Web Calculator API is running"}

# python cli로 실행해도 uvicorn을 사용하도록
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)