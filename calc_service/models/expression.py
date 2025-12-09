from sqlmodel import SQLModel, Field


class Expression(SQLModel, table=True):
    """수식 저장용 DB 테이블 모델"""

    id: int | None = Field(default=None, primary_key=True)
    expr: str