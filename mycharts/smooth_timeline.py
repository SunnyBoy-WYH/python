# -*- coding:utf-8; -*-
'''利用封装好的平滑函数做平滑图'''
import pandas as pd
from pyecharts import Line,Page,Pie,Timeline,Overlap,Bar,Gauge
from pyecharts.charts.effectscatter import EffectScatter
from smooth import *
from string_store import *
from read_csv import *
from style import timeline_Style,bar_Style
import  numpy as np 
from  mycharts2 import * 
#柱状图_数据准备
def bar1_timeline_data(data,pinghua):
    data1=data.groupby('class',as_index=False).sum().sort_values(by="heat",ascending= False)
    '''groupby转换的不是标准Dataframe 是另外一种形式，如果不想把依照的列作为索引，
            这不过是MultiIndex形式的一种dataframe罢了。
            可以用as_index=False'''
    for i in range(0,10):
        data_temp=data1[data1['class'].isin([string_class_top10[i]])]
        pinghua[i].append(list(data_temp['heat'])[0])
#柱状图出图
def bar1_timeline(data_array):
    pinghua=[[],[],[],[],[],[],[],[],[],[]]
    chart = Timeline(**timeline_Style)

    for i in range(0,13):
        bar1_timeline_data(data_array[i],pinghua)
    for i in range(0,10):
        pinghua[i]=soomthByStage(pinghua[i],5)
        
    pinghua_t=np.array(pinghua).T
    
    for i in range(0,60):
        df =pd.DataFrame({'class':string_class_top10,'heat':pinghua_t[i]})
        bar = createBarFromDataFrame(dataFrame=df, xAxis="class", yAxis="heat",label="热度",
            title='top10热度变化趋势',titlePos='center',**bar_Style)
        
       
        chart.add(bar,String_filename_1[i])
    return chart
    
#仪表盘
def gauge_timeline(data_array):
    chart1 = Timeline(**timeline_Style)
    array_gauge=[]
    for i  in range(0,13):
        array_gauge.append(data_array[i]['heat'].sum())
    maxgauge=max(array_gauge)
    array_gauge=soomthByStage(array_gauge,5)
    for i  in range(0,60):
        gauge = Gauge("观看人数趋势图 ",title_pos='center')
        gauge.add("","占比",int(array_gauge[i]/maxgauge*100))
        chart1.add(gauge, String_filename_1[i])
    return chart1


        
    
    
        
        
    
    
    
    
    
