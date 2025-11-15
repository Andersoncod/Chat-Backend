from sqlalchemy import Column, String, DateTime, Integer, JSON, UniqueConstraint #definicion para llamado de la tabla
from app.db.base import Base

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(String, unique=True, index=True, nullable=False) 
    session_id = Column(String, index=True, nullable=False)
    content = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    sender = Column(String, index=True, nullable=False)  # solo escribir "user" | "system"
    meta_data = Column(JSON, nullable=False)

    __table_args__ = (
        UniqueConstraint("message_id", name="uq_message_id"),
    )
