import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import h5py
# h5py用来读取HDF格式样例数据,使用方法到官方网站调研


def main():
    f=h5py.File('FY3B_VIRR_SST_DAILY_20190501_5000.0M.HDF','r')
    data= f['SST']
    x_ticks = np.linspace(0,7200,7)
    y_ticks=np.linspace(0,3600,7)
    plt.matshow(data)
    plt.xticks(x_ticks,[r'180°',r'120°W',r'60°W',r'0°',r'60°E',r'120°E@',r'180°'])
    plt.yticks(y_ticks,[r'90°N',r'60°N',r'30°N',r'0°',r'30°S',r'60°S',r'90°'])
    plt.colorbar()
    plt.savefig('FY3B_VIRR_SST_DAILY_20190501_5000.0M.HDF.png')
    plt.show()


def test():
    import time
    print(int(time.time()))
if __name__ == '__main__':
    argv = sys.argv
    test()