version_code = 15

version_name = "X<cP[?PHNB<P?aj"


def decode():

    s = ""
    for i in range(len(version_name)):
        s+=chr(ord(version_name[i])^version_code)
    return s
print(decode())




