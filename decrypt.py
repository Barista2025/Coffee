import requests
import base64
import time,os
import Crypto
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_PKCS1_v1_5
import ast

def decrypt(message):
    private_key = None
    with open('private_key.pem','rb') as file:
        private_key = RSA.importKey(file.read())
    decipher = Cipher_PKCS1_v1_5.new(private_key)
    encrypted_received = base64.b64decode(message)
    decrypted_bytes = decipher.decrypt(encrypted_received, None)
    decrypted_text = decrypted_bytes.decode('utf-8')
    return decrypted_text
