import numpy as np


def fill(ary):
    # todo:   完成函数fill的内容, 返回填充好的矩阵

    while (-1 in ary) == True:
        for i in range(len(ary)):
            for j in range(len(ary[0])):
                while ary[i, j] == -1:
                    if i != 0 and ary[i - 1, j] != -1:
                        ary[i, j] = ary[i - 1, j]
                    elif j != len(ary[0]) - 1 and ary[i, j + 1] != -1:
                        ary[i, j] = ary[i, j + 1]
                    elif i != len(ary) - 1 and ary[i + 1, j] != -1:
                        ary[i, j] = ary[i + 1, j]
                    elif j != 0 and ary[i, j - 1] != -1:  #
                        ary[i, j] = ary[i, j - 1]

    return ary




def find(valid,i,j):
    pass





if __name__ == '__main__':
    shape = (3000, 3000)
    ary = np.random.randint(0., 100, shape)

    ary[ary < 60] = -1

    fill(ary)
    print(ary)