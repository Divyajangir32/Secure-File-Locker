import os
import hashlib
import base64
from cryptography.fernet import Fernet, InvalidToken

LOCKER_DIR = "locker"

def _ensure_locker():
    if not os.path.exists(LOCKER_DIR):
        os.makedirs(LOCKER_DIR)

def _generate_key(password: str) -> bytes:
    """
    Same password -> same key
    """
    hashed = hashlib.sha256(password.encode()).digest()
    return Fernet(base64.urlsafe_b64encode(hashed))._signing_key

def _derive_fernet(password: str) -> Fernet:
    hashed = hashlib.sha256(password.encode()).digest()
    key = hashlib.sha256(hashed).digest()
    return Fernet(base64.urlsafe_b64encode(key))

def encrypt_file(file_path: str, password: str) -> str:
    _ensure_locker()

    with open(file_path, "rb") as f:
        data = f.read()

    fernet = _derive_fernet(password)
    encrypted = fernet.encrypt(data)

    filename = os.path.basename(file_path)
    encrypted_path = os.path.join(LOCKER_DIR, filename + ".lock")

    with open(encrypted_path, "wb") as f:
        f.write(encrypted)

    # ❗ delete original file
    os.remove(file_path)

    return encrypted_path


def decrypt_file(encrypted_path: str, password: str) -> str:
    with open(encrypted_path, "rb") as f:
        encrypted_data = f.read()

    fernet = _derive_fernet(password)

    try:
        decrypted = fernet.decrypt(encrypted_data)
    except InvalidToken:
        raise ValueError("Wrong password")

    original_name = os.path.basename(encrypted_path).replace(".lock", "")
    output_path = os.path.join(os.path.dirname(encrypted_path), original_name)

    with open(output_path, "wb") as f:
        f.write(decrypted)

    # ❗ delete encrypted file
    os.remove(encrypted_path)

    return output_path
