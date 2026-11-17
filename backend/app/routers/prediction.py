from app import models, schemas
from app.database import get_db
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app.services.inference import predict_sentiment_onnx
import os

router = APIRouter(prefix='/detect', tags=['Inference'])


@router.post('/', status_code=status.HTTP_200_OK)
async def detect_spam(payload: schemas.DetectReqPayload, db: Session=Depends(get_db)):    
    res = await predict_sentiment_onnx("hello world", max_len=73)
    
    return {'res': res}
    
