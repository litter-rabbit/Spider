

import string

base_character = string.ascii_letters+string.digits+'./;*&^%$#@!()-_+=~`'


def decode():
    res = []
    for i in range(12):

        for c in base_character:

            if (chr(((255-i)-100-ord(c))))=='0':
                res.append(c)


    return ''.join(res)





