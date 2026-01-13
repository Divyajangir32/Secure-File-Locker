from cryptography.fernet import Fernet
import hashlib
import os
import base64
PASSWORD_FILE = "../locker/.key"
if not os.path.exists("../locker"):
    os.mkdir("../locker")


def save_master_password(pwd):
    with open(PASSWORD_FILE, "wb") as f:
        f.write(generate_key(pwd))


def verify_master_password(pwd):
    if not os.path.exists(PASSWORD_FILE):
        save_master_password(pwd)
        return True
    with open(PASSWORD_FILE, "rb") as f:
        return f.read() == generate_key(pwd)



def generate_key(password):
    return hashlib.sha256(password.encode()).digest()

def encrypt_file(filepath, password):
    key = generate_key(password)
    f = Fernet(base64.urlsafe_b64encode(key))

    with open(filepath, "rb") as file:
        data = file.read()

    filename = os.path.basename(filepath)

    with open(os.path.join("../locker", filename), "wb") as enc:
        enc.write(f.encrypt(data))


def decrypt_file(filename, password):
    key = generate_key(password)
    f = Fernet(base64.urlsafe_b64encode(key))

    with open("../locker/" + filename, 'rb') as file:
        encrypted = file.read()

    with open("../decrypted_" + filename, 'wb') as dec:
        dec.write(f.decrypt(encrypted))
