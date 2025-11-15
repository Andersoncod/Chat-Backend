# NequiBot Message Processor (FastAPI + SQLite)

API RESTful para recibir, validar, procesar y almacenar mensajes de chat con soporte de paginación y filtrado por remitente. Incluye pruebas unitarias e integración, manejo robusto de errores y arquitectura limpia.

## Características
- **Endpoints:** POST /api/messages, GET /api/messages/{session_id}
- **Validación:** Pydantic (formato, sender permitido, contenido no vacío)
- **Procesamiento:** Filtro simple de palabras inapropiadas + metadatos (conteo de palabras, caracteres, processed_at)
- **Persistencia:** SQLite con SQLAlchemy
- **Errores:** Respuestas estructuradas (INVALID_FORMAT, DUPLICATE_ID, SERVER_ERROR)
- **Pruebas:** Pytest con cobertura >80%
- **Arquitectura:** Controladores (routers), servicios, repositorios, modelos y esquemas separados

## Requisitos
- **Python:** 3.10+
- **Dependencias:** ver `requirements.txt`

## Instalación
1. **Clonar:**
   ```bash
   git clone https://github.com/Andersoncod/Chat-Backend.git
   cd nequi_backend

