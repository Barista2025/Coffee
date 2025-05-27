import requests
import base64
import time,os
import Crypto
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_PKCS1_v1_5
import ast

private_key = None
public_key = None
with open('private_key.pem','rb') as file:
    private_key = RSA.importKey(file.read())

with open('public_key.pem','rb') as file:
    public_key = RSA.importKey(file.read())

data = input("please input the plain text:")
cipher = Cipher_PKCS1_v1_5.new(public_key)
decipher = Cipher_PKCS1_v1_5.new(private_key)
encrypted_bytes = cipher.encrypt(data.encode())
encrypted_b64 = base64.b64encode(encrypted_bytes).decode('utf-8')
print(f"\n🔒 加密後（Base64）: {encrypted_b64}")
#decrypted = decipher.decrypt(encrypted, None).decode()
#print(encrypted.decode("utf-8"))
#print(decrypted)
