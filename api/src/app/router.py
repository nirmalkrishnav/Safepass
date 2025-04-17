from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from uuid import uuid4
from src.app.service.encryption_service import decrypt_string, encrypt_string

router = APIRouter(prefix="/api/secret", tags=["Secret Sharing"])

class SecretRequest(BaseModel):
    title: str
    plaintext: str

# In-memory storage for now (we'll switch to Redis soon)
store = {}

@router.post("/")
def create_secret(request: SecretRequest):
    secret_id = str(uuid4())
    encrypted_data = encrypt_string(request.plaintext)

    store[secret_id] = {
        "title": request.title,
        "ciphertext": encrypted_data["ciphertext"],
        "key": encrypted_data["key"],
        "iv": encrypted_data["iv"]
    }

    return {"id": secret_id}

@router.get("/{secret_id}")
def get_secret(secret_id: str):
    # Retrieve the encrypted data from the store
    encrypted_data = store.get(secret_id)

    if not encrypted_data:
        raise HTTPException(status_code=404, detail="Secret not found")

    # Decrypt the data
    plaintext = decrypt_string(encrypted_data)
    return {
        "title": encrypted_data["title"],
        "plaintext": plaintext
    }
