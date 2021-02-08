# coding:utf-8
import base64
from Cryptodome.Cipher import AES
import json


class AesEncry(object):
    key = "thisisatestkey=="  # aes秘钥

    def encrypt(self, data):
        data = json.dumps(data)
        mode = AES.MODE_ECB
        padding = lambda s: s + (16 - len(s) % 16) * chr(16 - len(s) % 16)
        cryptos = AES.new(self.key, mode)
        cipher_text = cryptos.encrypt(padding(data).encode("utf-8"))

        return base64.b64encode(cipher_text).decode("utf-8")

    def decrypt(self, data):
        cryptos = AES.new(self.key.encode('utf8'), AES.MODE_ECB)
        decrpytBytes = base64.b64decode(data)

        meg = cryptos.decrypt(decrpytBytes).decode('utf-8')
        return meg[:-ord(meg[-1])]


a = AesEncry().decrypt("9YuQ2dk8CSaCe7DTAmaqAA==")
print(a)
