from fastapi import FastAPI #creación de api
from app.api.routers.messages import router as messages_router 
from app.utils.errors import register_exception_handlers

app = FastAPI(title="NequiBot Message Processor", version="1.0.0")

#  #enrutamiento desde fastapi
app.include_router(messages_router, prefix="/api/messages", tags=["messages"])

# Registro de errores personalizados 
register_exception_handlers(app)


#ejecutar con el comando uvicorn app.main:app --reload cuando este ejecutado el entorno virtual