
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class DetectionResult(BaseModel):
    text: str
    ham_probability: float | str
    spam_probability: float | str
    prediction: str

class DetectReqPayload(BaseModel):
    message: str
    # max_len: Optional[int]


class Report(BaseModel):
    model_config = ConfigDict(from_attributes=True)  # lets it read SQLAlchemy objects

    id: str
    label: str
    message: str
    percentage: float
    created_at: datetime

class ReportList(BaseModel):
    reports: list[Report]
    total: int


class ReportListResponse(BaseModel):
    reports: ReportList
    success: bool
    code: int
    message: str