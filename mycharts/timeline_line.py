# -*- coding:utf-8; -*-
import pandas as pd
from pyecharts import Line,Page,Pie,Timeline,Overlap,Bar,Gauge,Scatter
from pyecharts.charts.effectscatter import EffectScatter
from string_store import *
from read_csv import *
from mycharts2 import *
from style import *
#折线图1——数据准备
def sum_heat(data,array):
    #按照类型分类
    data=data.groupby('class',as_index=False).sum().sort_values(by="heat",ascending= False)
    #查询相应的并把它放入对应list
    for i in range(0,3):
        data1=data[data['class'].isin([string_class[i]])]
        array[i].append(list(data1['heat'])[0])
    return 0;
#折线图2——数据准备
def sum_live_person(data,array2):
    
    temp = data[['room_id','class']].groupby('class',as_index=False)
    #按照class分类的直播人数统计
    temp2=temp.count()
    temp2.rename(columns={'room_id':'live_person_number'}, inplace = True)
    
    for i in range(0,3):
        data1=temp2[temp2['class'].isin([string_class[i]])]
        array2[i].append(list(data1['live_person_number'])[0])
#折线图1——出图
def line1(data_array):
    array=[[],[],[]]#第一个lol热度 第二个pubg热度，第三个wzry热度
    for i in range(0,13):
        sum_heat(data_array[i],array)
    line1 = Line('三大端游一天多时间段热度趋势',width=1400, height=700,title_pos='center')
    #line1 = createLineFromDataFrame(dataFrame=df, xAxis="class", yAxis="heat",label="热度",is_smooth=True,width=1400, height=700,title_pos='center')
    overlop = Overlap('三大端游一天多时间段热度趋势',width=1400, height=700)
    es = EffectScatter()
    
    for i in range(0,3):
        line1.add(string_class[i],time_period,array[i],**line_Style,is_smooth=True)
        mark_x = []
        mark_x.append(   time_period[array[i].index(max(array[i])) ]        )
        mark_x.append(   time_period[array[i].index(min(array[i])) ]        )
        mark_y = []
        mark_y.append(max(array[i]))
        mark_y.append(min(array[i]))
        es.add('',mark_x,mark_y,effect_scale=8)   #闪烁
        overlop.add(line1)                   #必须先添加line,在添加es
        overlop.add(es)
    return overlop
#折线图2——出图
def line2(data_array):
    array2=[[],[],[]]#第一个lol直播人数 第二个pubg直播人数，第三个wzry直播人数
    for i in range(0,13):
        sum_live_person(data_array[i],array2)
    line2 = Line('三大端游一天多时间段直播人数趋势',width=1400, height=700,title_pos='center')
    overlap = Overlap('三大端游一天多时间段热度趋势',width=1400, height=700)
    es = EffectScatter()
    for i in range(0,3):
        #df =pd.DataFrame({'time_period':time_period,'live_person_number':array2[i]})
        line2.add(string_class[i],time_period,array2[i],**line_Style)
        #createLineFromDataFrame(line=line2, dataFrame=df, xAxis="time_period",yAxis="live_person_number",label=string_class[i])
        mark_x = []
        mark_x.append(time_period[array2[i].index(max(array2[i]))] )
        mark_x.append(time_period[array2[i].index(min(array2[i]))])
        mark_y = []
        mark_y.append(max(array2[i]))
        mark_y.append(min(array2[i]))
        es.add('',mark_x,mark_y,effect_scale=8)   #闪烁
        overlap.add(line2)                   #必须先添加line,在添加es
        overlap.add(es)
    print('直播人数趋势图已出')
    return overlap

#为饼图分类提供方法
def tongji(temp,data1):
        temp_heat=0
        for i in range(0,len(temp)):  
            data_temp=data1[data1['class'].isin([temp[i]])]
            if(data_temp.empty==False):
                temp_heat=temp_heat+list(data_temp['heat'])[0]
        return temp_heat
#饼图——出图
def pie_rose(data):
    #获得每个类型的直播人数
    data1=data.groupby('class',as_index=False).sum()
    #所有加起来的热度
    game_heat=data1['heat'].sum()-tongji(yule, data1)-tongji(jiaoyu, data1)-tongji(yuyin, data1)-tongji(danjireyou,data1)-tongji(wangyoujingji,data1)
   
    v1 = [tongji(yule, data1),tongji(jiaoyu, data1),tongji(yuyin, data1),tongji(danjireyou,data1),game_heat,tongji(wangyoujingji, data1)]

    df = DataFrame({'class':x,'heat':v1})
    pie = createPieFromDataFrame(dataFrame=df, xAxis="class", yAxis="heat",title='热度多时间段变化图',label ="饼图",titlePos='center',**pie_rose_style)
    
    
    return pie    
def scatter_size(data):
    data1=data.groupby('class',as_index=False).sum().sort_values(by="heat",ascending= False)
    '''groupby转换的不是标准Dataframe 是另外一种形式，如果不想把依照的列作为索引，
            这不过是MultiIndex形式的一种dataframe罢了。
            可以用as_index=False'''
    #选取50个点
    data2=data1[0:50]
    
   
    scatter = Scatter('不同时间段top50热度变化-气泡图',width=1400, height=700,title_pos='center')
    
    
    scatter.add("热度", x_axis=list(data2['class']),y_axis=list(data2['heat']),**scatter_style)
    
    return scatter
def scatter_timeline(data_array):
    chart = Timeline(**timeline_Style)
    for i in range(0,13):
        chart.add(scatter_size(data_array[i]), time_period[i])
    return chart
def pie_timeline(data_array):

    chart = Timeline(**timeline_Style)
    for i in range(0,13):
        chart.add(pie_rose(data_array[i]),time_period[i])
    return chart
'''if __name__ == "__main__":
    #从文件中提取数据
    data_array=read_csv_data()
    #建一个页
    
    
    page.add(line1(data_array))
    page.add(line2(data_array))
    page.add(scatter_timeline(data_array))
    page.add(pie_timeline(data_array))
    page.render("E:\\图表1.html")
    print('已出图')'''
   

    
    
        
        
    
 
   

    
    
