from fastapi import APIRouter, HTTPException
from ..app.service.encryption_service import encrypt_string, decrypt_string
from pydantic import BaseModel
from uuid import uuid4
import redis
import os

# Set up Redis client
redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = os.getenv("REDIS_PORT", 6379)
redis_client = redis.StrictRedis(host=redis_host, port=redis_port, db=0, decode_responses=True)

router = APIRouter(prefix="/api/secret", tags=["Secret Sharing"])

class SecretRequest(BaseModel):
    title: str
    plaintext: str

@router.post("/")
def create_secret(request: SecretRequest):
    secret_id = str(uuid4())  # Generate a unique ID for the secret
    encrypted_data = encrypt_string(request.plaintext)

    # Store encrypted data in Redis
    redis_client.hmset(secret_id, {
        "title": request.title,
        "ciphertext": encrypted_data["ciphertext"],
        "key": encrypted_data["key"],
        "iv": encrypted_data["iv"]
    })

    return {"id": secret_id}

@router.get("/{secret_id}")
def get_secret(secret_id: str):
    # Retrieve encrypted data from Redis
    encrypted_data = redis_client.hgetall(secret_id)

    if not encrypted_data:
        raise HTTPException(status_code=404, detail="Secret not found")

    # Decrypt the data
    decrypted_data = decrypt_string({
        "ciphertext": encrypted_data["ciphertext"],
        "key": encrypted_data["key"],
        "iv": encrypted_data["iv"]
    })
    
    return {
        "title": encrypted_data["title"],
        "plaintext": decrypted_data
    }
