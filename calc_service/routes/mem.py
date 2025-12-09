from fastapi import APIRouter, Depends
from sqlmodel import Session, select, desc, asc

from database import get_session
from models import Expression, RecallRequest, RecallResponse

router = APIRouter(prefix="/mem", tags=["memory"])


def reindex_expressions(session: Session) -> None:
    """삭제 후 ID 재정렬 (1부터 순차적으로)"""
    expressions = session.exec(select(Expression).order_by(asc(Expression.id))).all()
    for idx, expr in enumerate(expressions, start=1):
        if expr.id != idx:
            expr.id = idx
    session.commit()


@router.post("/", response_model=RecallResponse)
def recall_expression(
    request: RecallRequest,
    session: Session = Depends(get_session),
) -> RecallResponse:
    """수식 Recall 서비스"""
    recall_value = request.recall.strip()

    # Case 1: 모든 수식 삭제 (-*)
    if recall_value == "-*":
        expressions = session.exec(select(Expression)).all()
        if not expressions:
            return RecallResponse(expr=["No Expressions to Delete"])
        for expr in expressions:
            session.delete(expr)
        session.commit()
        return RecallResponse(expr=["All expressions deleted"])

    # Case 2: 마지막 수식 삭제 (--)
    if recall_value == "--":
        last_expr = session.exec(
            select(Expression).order_by(desc(Expression.id))
        ).first()
        if not last_expr:
            return RecallResponse(expr=["No Expressions to Delete"])
        deleted_expr = last_expr.expr
        session.delete(last_expr)
        session.commit()
        return RecallResponse(expr=[f"Deleted: {deleted_expr}"])

    # Case 3: 특정 ID 삭제 (-숫자)
    if recall_value.startswith("-") and recall_value[1:].isdigit():
        target_id = int(recall_value[1:])
        expr_to_delete = session.get(Expression, target_id)
        if not expr_to_delete:
            return RecallResponse(expr=[f"No Such Expression: {target_id}"])
        deleted_expr = expr_to_delete.expr
        session.delete(expr_to_delete)
        session.commit()
        reindex_expressions(session)
        return RecallResponse(expr=[f"Deleted [{target_id}]: {deleted_expr}"])

    # Case 4: 모든 수식 조회 (all 또는 빈 값)
    # 비어있는 상태에서 R 버튼을 누르면 프론트에서 "all"을 담아서 보내게 만들까?
    if recall_value == "all" or recall_value == "":
        expressions = session.exec(select(Expression).order_by(asc(Expression.id))).all()
        if not expressions:
            return RecallResponse(expr=["No Expressions to Recall"])
        return RecallResponse(expr=[f"[{e.id}] {e.expr}" for e in expressions])

    # Case 5: 특정 ID 조회 (숫자)
    if recall_value.isdigit():
        target_id = int(recall_value)
        expression = session.get(Expression, target_id)
        if not expression:
            return RecallResponse(expr=[f"No Such Expression: {target_id}"])
        return RecallResponse(expr=[expression.expr])

    # 잘못된 형식
    return RecallResponse(expr=[f"No Such Expression: {recall_value}"])