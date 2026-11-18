from fastapi import status, Depends, APIRouter
from sqlalchemy.orm import Session
from app import schemas
from app.database import get_db
from app.models import Report


router = APIRouter(prefix='/reports', tags=["Detection Report"])

@router.get('/', response_model=schemas.ReportListResponse, status_code=status.HTTP_200_OK)
def report_list(db: Session = Depends(get_db)):
    """Retrieve all detection reports."""
    # reports = db.query(Report).all()
    reports = db.query(Report).order_by(Report.created_at.desc()).all()

    report_list = schemas.ReportList(
        reports=[schemas.Report.model_validate(r) for r in reports],
        total=len(reports),
    )
    
    response = schemas.ReportListResponse(
        reports=report_list,
        success=True,
        code=status.HTTP_200_OK,
        message='Ok'
    )

    return response

