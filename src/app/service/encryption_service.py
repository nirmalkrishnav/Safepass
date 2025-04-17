from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
import base64

def encrypt_string(plain_text: str) -> dict:
    key = os.urandom(32)  # AES-256
    iv = os.urandom(16)

    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    encrypted = encryptor.update(plain_text.encode()) + encryptor.finalize()

    return {
        "ciphertext": base64.b64encode(encrypted).decode(),
        "key": base64.b64encode(key).decode(),
        "iv": base64.b64encode(iv).decode()
    }


def decrypt_string(encrypted_data: dict) -> str:
    ciphertext = base64.b64decode(encrypted_data["ciphertext"])
    key = base64.b64decode(encrypted_data["key"])
    iv = base64.b64decode(encrypted_data["iv"])

    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    decrypted = decryptor.update(ciphertext) + decryptor.finalize()
    return decrypted.decode()