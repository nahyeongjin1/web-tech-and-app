from pydantic import BaseModel


class EvalRequest(BaseModel):
    """수식 계산 요청 스키마"""

    expr: str


class EvalResponse(BaseModel):
    """수식 계산 응답 스키마"""

    result: str


class RecallRequest(BaseModel):
    """수식 Recall 요청 스키마"""

    recall: str


class RecallResponse(BaseModel):
    """수식 Recall 응답 스키마"""

    expr: list[str]


class OCRResponse(BaseModel):
    """OCR 응답 스키마"""
    
    expr: str | None = None
    error: str | None = None