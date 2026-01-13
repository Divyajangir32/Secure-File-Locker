from cryptography.fernet import Fernet
import hashlib
import os
import base64

def generate_key(password):
    return hashlib.sha256(password.encode()).digest()

def encrypt_file(filepath, password):
    key = generate_key(password)
    f = Fernet(base64.urlsafe_b64encode(key))

    with open(filepath, 'rb') as file:
        data = file.read()

    filename = os.path.basename(filepath)
    with open("../locker/" + filename, 'wb') as enc:
        enc.write(f.encrypt(data))

def decrypt_file(filename, password):
    key = generate_key(password)
    f = Fernet(base64.urlsafe_b64encode(key))

    with open("../locker/" + filename, 'rb') as file:
        encrypted = file.read()

    with open("../decrypted_" + filename, 'wb') as dec:
        dec.write(f.decrypt(encrypted))
