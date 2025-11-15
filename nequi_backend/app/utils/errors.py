from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from fastapi.exceptions import RequestValidationError


#Definicion de errores
def error_response(code: str, message: str, details: str, status_code: int):
    return JSONResponse(
        status_code=status_code,
        content={
            "status": "error",
            "error": {
                "code": code,
                "message": message,
                "details": details,
            },
        },
    )

def register_exception_handlers(app: FastAPI):
    @app.exception_handler(ValidationError)
    async def pydantic_validation_handler(request: Request, exc: ValidationError):
        return error_response(
            "INVALID_FORMAT",
            "Formato de mensaje inválido",
            str(exc),
            422,
        )

    @app.exception_handler(RequestValidationError)
    async def fastapi_validation_handler(request: Request, exc: RequestValidationError):
        return error_response(
            "INVALID_FORMAT",
            "Formato de mensaje inválido",
            str(exc),
            422,
        )


#Errores de duplicacion base de datos
    @app.exception_handler(IntegrityError)
    async def sqlalchemy_integrity_handler(request: Request, exc: IntegrityError):
        return error_response(
            "DUPLICATE_ID",
            "El 'message_id' ya existe",
            "El identificador de mensaje debe ser único",
            409,
        )

#Errores genericos
    @app.exception_handler(Exception)
    async def generic_handler(request: Request, exc: Exception):
        return error_response(
            "SERVER_ERROR",
            "Error del servidor",
            str(exc),
            500,
        )

