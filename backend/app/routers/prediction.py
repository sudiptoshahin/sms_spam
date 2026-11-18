from app import schemas
from app.database import get_db
from fastapi import status, Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from app.services.inference import predict_sentiment_onnx
from app.models import Report


router = APIRouter(prefix='/detect', tags=['Inference'])


@router.post('/', status_code=status.HTTP_200_OK)
async def detect_spam(payload: schemas.DetectReqPayload, db: Session = Depends(get_db)):
    message = str(payload.message)

    res = await predict_sentiment_onnx(message)

    ham_prob = float(res['ham_probability'])
    spam_prob = float(res['spam_probability'])

    report = Report(
        label=res['prediction'],
        message=res['text'],
        percentage=max(ham_prob, spam_prob),
    )

    try:
        db.add(report)
        db.commit()
        db.refresh(report)
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to save the report")

    return {
        'id': report.id,
        'label': report.label,
        'message': report.message,
        'percentage': report.percentage,
    }
