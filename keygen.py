import requests
import base64
import time,os
import Crypto
from Crypto.PublicKey import RSA
from Crypto import Random
import ast

def dumpKey(key=None,fn=''):
    with open(fn,'wb') as file:
        file.write(key.exportKey('PEM'))
        file.close()

key = RSA.generate(2048)
publickey = key.publickey()
dumpKey(key,'private_key.pem')
dumpKey(publickey,'public_key.pem')
