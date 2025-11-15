from datetime import datetime
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.db.session import get_session, engine
from app.db.base import Base
from app.schemas.message import MessageCreate, MessageOut, MessageQueryParams
from app.models.message import Message
from app.repositories.messages_repo import MessagesRepository
from app.services.processing import filter_inappropriate, build_metadata

# Crear tablas si no existen (simple auto-migrate)
Base.metadata.create_all(bind=engine)

router = APIRouter()

#POST para recibir los mensajes
@router.post("", response_model=dict, status_code=201)
def create_message(payload: MessageCreate, db: Session = Depends(get_session)):
    # Filtro de contenido
    is_clean, filtered = filter_inappropriate(payload.content)
    meta_data = build_metadata(filtered)

    # Si no es limpio, igual se guarda pero enmascarado y se informa
    repo = MessagesRepository(db)
    msg = Message(
        message_id=payload.message_id,
        session_id=payload.session_id,
        content=filtered,
        timestamp=payload.timestamp,
        sender=payload.sender,
        meta_data=meta_data | {"flag_inappropriate": (not is_clean)},
    )
    saved = repo.create(message=msg)

    return {
        "status": "success",
        "data": MessageOut(
            message_id=saved.message_id,
            session_id=saved.session_id,
            content=saved.content,
            timestamp=saved.timestamp,
            sender=saved.sender,
            meta_data=saved.meta_data,
        ).dict(),
    }

@router.get("/{session_id}", response_model=dict)
def list_messages(
    session_id: str,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    sender: str | None = Query(None, pattern="^(user|system)$"),
    db: Session = Depends(get_session),
):
    params = MessageQueryParams(limit=limit, offset=offset, sender=sender)
    repo = MessagesRepository(db)
    records = repo.get_by_session(
        session_id=session_id,
        limit=params.limit,
        offset=params.offset,
        sender=params.sender,
    )
    items = [
        {
            "message_id": r.message_id,
            "session_id": r.session_id,
            "content": r.content,
            "timestamp": r.timestamp,
            "sender": r.sender,
            "metadata": r.meta_data,
        }
        for r in records
    ]
    return {"status": "success", "data": items} #Devuelve la respuesta en formato estándar
