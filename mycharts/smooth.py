# -*- coding:utf-8; -*-
from numpy import arange,linspace
from bisect import insort
def soomthByExtremum(data:list, degree:int) -> list:
    '''
    极值平滑处理，通过机制计算出每个平滑因子，最终返回平滑之后的数据
    :param data:需要处理的数据
    :param degree:处理的程度
    :return:处理之后的列表
    '''
    try:
        TMP = list(data).copy()
    except:
        return []
    else:
        MIN = min(TMP) # 检查出序列中的最大值
        MAX = max(TMP) # 检查出序列中的最小值
        FACTOR = (MAX - MIN) / degree # 得到因子
        GROUP = arange(MIN+FACTOR, MAX, FACTOR)# 构造序列
        for number in GROUP:
            insort(TMP,number)# 维护有序序列的插入
        return TMP

def soomthByStage(data:list, degree:int) -> list:
    try:
        TMP = list(data).copy()
    except:
        return []
    else:
        INDEX = 0
        R = []
        while INDEX < TMP.__len__()-1:
            T = linspace(TMP[INDEX],TMP[INDEX + 1],degree)
            T = list(T)
            R += T
            INDEX += 1
        return R

def binarySearch(data:list, key) -> int:
    left = 0
    right = data.__len__() - 1
    while left <= right:
        middle = int((left + right) / 2)
        if data[middle] == key:
            return middle
        elif data[middle] < key:
            left = middle + 1
        else:
            right = middle - 1
    return -1
