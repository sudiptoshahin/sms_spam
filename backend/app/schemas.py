
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


# {'text': 'Hello how are you',
#  'ham_probability': 0.9998233630390139,
#  'spam_probability': 0.0001766369609861318,
#  'prediction': 'ham'}


class DetectResponse(BaseModel):
    text: str
    ham_probability: float
    spam_probability: float
    prediction: str

class DetectReqPayload(BaseModel):
    message: str
    max_len: Optional[int]

