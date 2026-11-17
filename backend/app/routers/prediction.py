from app import schemas
from app.database import get_db
from fastapi import status, Depends, APIRouter
from sqlalchemy.orm import Session
from app.services.inference import predict_sentiment_onnx


router = APIRouter(prefix='/detect', tags=['Inference'])


@router.post('/', status_code=status.HTTP_200_OK)
async def detect_spam(payload: schemas.DetectReqPayload, db: Session = Depends(get_db)):
    message = str(payload.message)
    
    res = await predict_sentiment_onnx(message)
    
    # save the report to db
    
    return {'res': res, 'message': message}
