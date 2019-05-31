# -*- coding : utf-8 -*-
# Create : 2019-3-22
# Author : Bingnan Huo

from numpy import arange,linspace
from bisect import insort
from pandas import DataFrame,Series

def smoothByExtremum(data:list, degree:int) -> list:
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

def smoothByStage(data:list, degree:int) -> list:
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

def list2dataFrame(names, datas, ignoreIndex=False):
    if not isinstance(datas, (list,tuple)):
        return False
    if len(datas) != len(names):
        return False
    td = DataFrame()
    cnt = 0
    for data in datas:
        ts = Series(data, name=names[cnt])
        td = td.append(ts, ignore_index=ignoreIndex)
        cnt +=1
    return td.T

def smoothDataFrame(dataFrame, degree,columns=[], way=0):
    if not isinstance(dataFrame, DataFrame):
        return False
    if columns:
        for i in columns:
            if i not in dataFrame.columns:
                return False
            if dataFrame[i].dtype in ("bool", "complex"):
                return False
        td = DataFrame()
        if way == 0:
            for column in columns:
                t = list(dataFrame[column])
                r = smoothByExtremum(t,degree)
                td[column] = Series(r)
            return td
        elif way == 1:
            for column in columns:
                t = list(dataFrame[column])
                r = smoothByStage(t,degree)
                td[column] = Series(r)
            return td
    else:
        columns = df.columns
        for column in columns:
            if df[column].dtype in ("bool", "complex"):
                return False
        td = DataFrame()
        if way == 0:
            for column in columns:
                t = list(dataFrame[column])
                r = smoothByExtremum(t, degree)
                td[column] = Series(r)
            return td
        elif way == 1:
            for column in columns:
                t = list(dataFrame[column])
                r = smoothByStage(t, degree)
                td[column] = Series(r)
            return td

def part(dataFrame, axis, *args):
    if not isinstance(dataFrame, DataFrame):
        return False
    if axis not in (0,1):
        return False
    td = DataFrame()
    if axis == 1:
        for arg in args:
            td[arg] = dataFrame[arg]
    if axis == 0:
        for arg in args:
            ts = dataFrame.loc[arg,:]
            td = td.append(ts)
    return td

def get(dataFrame,row, column):
    if not isinstance(dataFrame, DataFrame):
        return False
    return dataFrame.loc[row,column]

def dropRepateData(dataFrame):
    if not isinstance(dataFrame, DataFrame):
        return False
    return dataFrame.drop_duplicates()

def groupBy(dataFrame, keyword):
    if not isinstance(dataFrame, DataFrame):
        return False
    td = {"__cnt__":0, "__kind__":[]}
    tg = dataFrame.groupby(keyword)
    for kind, df in tg:
        td[kind] = df
        td["__cnt__"] += 1
        td["__kind__"].append(kind)
    return td

def sumby(dataFrame, keywordg, keywords):
    #分类
    if not isinstance(dataFrame, DataFrame):
        return False
    td = {"__cnt__":0, "__kind__":[]}
    tg = dataFrame.groupby(keywordg)
    for kind, df in tg:
        td[kind] = df
        td["__cnt__"] += 1
        td["__kind__"].append(kind)
    #求和
    r = DataFrame(columns=[keywordg, keywords])
    for kind in td["__kind__"]:
        s = td[kind][keywords].sum()
        ts = Series([kind,s],index=[keywordg, keywords])
        r = r.append(ts, ignore_index=True)
    return r

def sort(dataFrame, key, axis=0):
    if not isinstance(dataFrame, DataFrame):
        return False
    return dataFrame.sort_values(key, axis=axis)

if __name__ == "__main__":
    names = ["LOL", "PUBG", "WZ"]
    datas = [[1000,2000,3000,4000], [1100, 2100,3100, 4100],[1200, 2200, 3300, 4400]]
    df = list2dataFrame(names=names, datas=datas)
    print(df)
    new = smoothDataFrame(df,10,way=1)
    print(new)

