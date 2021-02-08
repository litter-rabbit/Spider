
username = "Tenshine"


import hashlib


md5str = hashlib.md5(username.encode('utf8')).hexdigest()

print(md5str)

s =""
for i in range(0,len(md5str),2):
    s+=str(md5str[i])

print(s)
