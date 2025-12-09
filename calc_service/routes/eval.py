from fastapi import APIRouter, Depends
from simpleeval import simple_eval
from sqlmodel import Session

from database import get_session
from models import EvalRequest, EvalResponse, Expression

router = APIRouter(prefix="/eval", tags=["eval"])


@router.post("/", response_model=EvalResponse)
def evaluate_expression(
    request: EvalRequest,
    session: Session = Depends(get_session),
) -> EvalResponse:
    """수식을 계산하고 결과를 반환, DB에 저장"""
    expr = request.expr

    try:
        # python의 eval은 보안 취약점이 있으므로 simple_eval 사용
        result = simple_eval(expr)
        result_str = str(result)

        # DB에 수식 저장
        expression = Expression(expr=expr)
        session.add(expression)
        session.commit()

        return EvalResponse(result=result_str)
    except Exception as e:
        return EvalResponse(result=f"Error: {str(e)}")