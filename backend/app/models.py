from app.database import Base
from sqlalchemy import Column, Integer, String, Boolean, Float
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
import uuid



def generate_uuid() -> str:
    return uuid.uuid4().hex

class Report(Base):
    __tablename__ = 'reports'
    
    id = Column(String(32), primary_key=True, default=generate_uuid, nullable=False)
    label = Column(String, nullable=False)
    message = Column(String, nullable=False)
    percentage = Column(Float, nullable=False, default=0.0)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))