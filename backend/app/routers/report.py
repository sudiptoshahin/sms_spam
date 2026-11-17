from fastapi import status, Depends, APIRouter
from app import schemas
from app.database import get_db


router = APIRouter(prefix='/report', tags=["Detection Report"])

@router.get('/', status_code=status.HTTP_200_OK)
def report_list():
    pass
