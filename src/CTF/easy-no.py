

constant = "f72c5a36569418a20907b55be5bf95ad"


def decode(s):
    s_list = list(s)
    for i in range(0,len(s_list),2):

        s_list[i],s_list[i+1] = s_list[i+1],s_list[i]


    for i in range(0,len(s_list)>>1):
        s_list[i],s_list[i+16] = s_list[i+16],s_list[i]


    return ''.join(s_list)


print(decode(constant))




