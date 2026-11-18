from fastapi import status, Depends, APIRouter
from sqlalchemy.orm import Session
from app import schemas
from app.database import get_db
from app.models import Report


router = APIRouter(prefix='/reports', tags=["Detection Report"])

@router.get('/', response_model=schemas.ReportList, status_code=status.HTTP_200_OK)
def report_list(db: Session = Depends(get_db)):
    """Retrieve all detection reports."""
    reports = db.query(Report).all()
    
    # {
    # "id": "88fefebbcbf548768ffd542efb32ef80",
    # "percentage": 99.5,
    # "label": "ham",
    # "created_at": "2026-11-18T04:48:31",
    # "message": "Would you like to buy some fruit?"
    # }

    response = schemas.ReportList(
        reports=[schemas.Report.model_validate(r) for r in reports],
        total=len(reports),
    )

    return response

