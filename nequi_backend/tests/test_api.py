from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


#Creacion de mensaje validado 
def test_post_message_success():
    payload = {
        "message_id": "msg-1",
        "session_id": "session-a",
        "content": "Hola, ¿cómo puedo ayudarte hoy?",
        "timestamp": "2023-06-15T14:30:00Z",
        "sender": "system",
    }
    r = client.post("/api/messages", json=payload)
    assert r.status_code == 201
    body = r.json()
    assert body["status"] == "success"
    assert body["data"]["message_id"] == "msg-1"
    assert "meta_data" in body["data"]
    assert body["data"]["meta_data"]["word_count"] > 0


#Detecta duplicados 
def test_post_message_duplicate_id():
    payload = {
        "message_id": "msg-dup",
        "session_id": "session-b",
        "content": "Hola",
        "timestamp": "2023-06-15T14:30:00Z",
        "sender": "user",
    }
    r1 = client.post("/api/messages", json=payload)
    assert r1.status_code == 201
    r2 = client.post("/api/messages", json=payload)
    assert r2.status_code == 409
    body = r2.json()
    assert body["status"] == "error"
    assert body["error"]["code"] == "DUPLICATE_ID"


#Filtrado de mensajes 
def test_get_messages_by_session_with_pagination_and_sender():
    # seed
    for i in range(5):
        client.post("/api/messages", json={
            "message_id": f"msg-{i+100}",
            "session_id": "session-c",
            "content": "Hola mundo",
            "timestamp": "2023-06-15T14:30:00Z",
            "sender": "user" if i % 2 == 0 else "system",
        })
    r = client.get("/api/messages/session-c", params={"limit": 2, "offset": 1, "sender": "user"})
    assert r.status_code == 200
    data = r.json()["data"]
    assert len(data) <= 2
    for item in data:
        assert item["sender"] == "user"


# Valida los remitentes incorrectos
def test_post_invalid_sender():
    payload = {
        "message_id": "msg-invalid-sender",
        "session_id": "session-x",
        "content": "Hola",
        "timestamp": "2023-06-15T14:30:00Z",
        "sender": "robot",
    }
    r = client.post("/api/messages", json=payload)
    assert r.status_code == 422
    body = r.json()
    assert body["status"] == "error"
    assert body["error"]["code"] == "INVALID_FORMAT"
