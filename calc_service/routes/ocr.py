import re
from io import BytesIO

import easyocr
from fastapi import APIRouter, File, UploadFile
from models.schemas import OCRResponse

router = APIRouter(prefix="/ocr", tags=["ocr"])

# EasyOCR 리더 초기화 (영어, 숫자)
reader = easyocr.Reader(["en"], gpu=False)

# 허용된 문자 패턴 (숫자, 소수점, 사칙연산, 괄호)
ALLOWED_PATTERN = re.compile(r"^[0-9+\-*/().x×÷\s]+$")


def normalize_expression(text: str) -> str:
    """OCR 결과를 수식으로 정규화"""
    # 공백 제거
    text = text.replace(" ", "")
    # 곱하기 기호 변환
    text = text.replace("×", "*").replace("x", "*").replace("X", "*")
    # 나누기 기호 변환
    text = text.replace("÷", "/")
    # 잘못 인식된 문자 처리
    text = text.replace("O", "0").replace("o", "0")
    text = text.replace("l", "1").replace("I", "1")
    text = text.replace("S", "5").replace("s", "5")
    text = text.replace("B", "8")
    return text


def validate_expression(expr: str) -> tuple[bool, str]:
    """수식 유효성 검사"""
    # 빈 문자열 검사
    if not expr:
        return False, "Empty expression"

    # 허용되지 않은 문자 검사
    allowed_chars = set("0123456789+-*/().")
    invalid_chars = [c for c in expr if c not in allowed_chars]
    if invalid_chars:
        return False, f"Invalid characters: {', '.join(set(invalid_chars))}"

    # 괄호 짝 검사
    if expr.count("(") != expr.count(")"):
        return False, "Mismatched parentheses"

    # 연산자 연속 검사 (기본적인 문법 검사)
    if re.search(r"[+\-*/]{2,}", expr.replace("--", "").replace("+-", "")):
        return False, "Consecutive operators"

    return True, ""


@router.post("/", response_model=OCRResponse)
async def recognize_expression(file: UploadFile = File(...)) -> OCRResponse:
    """이미지에서 수식 인식"""
    try:
        # 이미지 읽기
        contents = await file.read()

        # OCR 수행
        results: list[str] = reader.readtext(
            BytesIO(contents).read(),
            detail=0,
            paragraph=True,
        ) # type: ignore

        if not results:
            return OCRResponse(error="No text detected in image")

        # 결과 합치기
        raw_text = "".join(results)

        # 수식 정규화
        expr = normalize_expression(raw_text)

        # 유효성 검사
        is_valid, error_msg = validate_expression(expr)
        if not is_valid:
            return OCRResponse(error=f"Error_{error_msg}")

        return OCRResponse(expr=expr)

    except Exception as e:
        return OCRResponse(error=f"Error_{str(e)}")