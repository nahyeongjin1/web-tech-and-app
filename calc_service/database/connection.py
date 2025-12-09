from collections.abc import Generator

from sqlmodel import Session, SQLModel, create_engine


# 강의에서 진행한 방식과 동일
filename = "mem.db"
dialect = "sqlite"
db_conn_url = f"{dialect}:///{filename}"
c_args = { "check_same_thread": False }

engine = create_engine(db_conn_url, echo=True, connect_args=c_args)


def conn() -> None:
    """DB 테이블 생성"""
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """DB 세션 생성 (의존성 주입용)"""
    with Session(engine) as session:
        yield session