from datetime import datetime
from typing import Optional, Literal
from pydantic import BaseModel, Field, validator #define esquemas para validar y serializar

SenderType = Literal["user", "system"]

class MessageCreate(BaseModel):     #Mensaje que recibe la API
    message_id: str = Field(..., min_length=1) 
    session_id: str = Field(..., min_length=1)
    content: str = Field(..., min_length=1)
    timestamp: datetime
    sender: SenderType

    @validator("content")
    def content_not_whitespace(cls, v: str):
        if not v.strip():
            raise ValueError("El campo 'content' no puede estar vacío o solo espacios")
        return v

class MessageOut(BaseModel):     #Mensaje que devuelve la API
    message_id: str
    session_id: str
    content: str
    timestamp: datetime
    sender: SenderType
    meta_data: dict

class MessageQueryParams(BaseModel):
    limit: int = Field(20, ge=1, le=100)
    offset: int = Field(0, ge=0)
    sender: Optional[SenderType] = None
