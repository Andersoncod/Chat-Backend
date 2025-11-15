from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.message import Message

class MessagesRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, *, message: Message) -> Message:
        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)
        return message

    def get_by_session(
        self, *, session_id: str, limit: int, offset: int, sender: Optional[str] = None
    ) -> List[Message]:
        stmt = select(Message).where(Message.session_id == session_id)
        if sender:
            stmt = stmt.where(Message.sender == sender)
        stmt = stmt.offset(offset).limit(limit)
        return self.db.execute(stmt).scalars().all()
