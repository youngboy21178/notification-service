import json, config, os

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from dotenv import load_dotenv

load_dotenv()

def get_encryption_key() -> bytes:
    return bytes.fromhex(config.encryption_key)

def aes_gcm_encrypt(plaintext: bytes):
    key = get_encryption_key()
    iv = os.urandom(12)
    encryptor = Cipher(algorithms.AES(key), modes.GCM(iv)).encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()
    return ciphertext, iv, encryptor.tag

def aes_gcm_decrypt(ciphertext: bytes, iv: bytes, tag: bytes):
    key = get_encryption_key()
    decryptor = Cipher(algorithms.AES(key), modes.GCM(iv, tag)).decryptor()
    result = (decryptor.update(ciphertext) + decryptor.finalize()).decode()
    dict_result = json.loads(result)
    return dict_result