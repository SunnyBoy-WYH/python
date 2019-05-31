# -*- coding:utf-8; -*-
import pandas as pd
from mycharts2 import *
import numpy as np
from pyecharts import WordCloud,Scatter
from string_store import *
from style import scatter_style,bar_Style,pie_style

 
#统计各个分类的热度
def tongji(temp,data1):
        temp_heat=0
        for i in range(0,len(temp)):  
            data_temp=data1[data1['class'].isin([temp[i]])]
            if(data_temp.empty==False):
                temp_heat=temp_heat+list(data_temp['heat'])[0]
        return temp_heat
        
def pie(data):
    
    #获得每个类型的直播人数
    data1=data.groupby('class',as_index=False).sum()
    #所有加起来的热度
    game_heat=data1['heat'].sum()-tongji(yule, data1)-tongji(jiaoyu, data1)-tongji(yuyin, data1)-tongji(danjireyou,data1)-tongji(wangyoujingji, data1)
    v1 = [tongji(yule, data1),tongji(jiaoyu, data1),tongji(yuyin, data1),tongji(danjireyou,data1),game_heat,tongji(wangyoujingji, data1)]
    
    df=pd.DataFrame({'laber':x,'heat':v1})
    
    pie = createPieFromDataFrame(dataFrame=df, xAxis="laber", yAxis="heat", title ='各类直播占比',titlePos='center',label="热度占比",**pie_style)
    print("饼图已出")
    return pie
def bar1(data):
    #按照类型分类
    
    data1=data.groupby('class',as_index=False).sum().sort_values(by="heat",ascending= False)
    '''groupby转换的不是标准Dataframe 是另外一种形式，如果不想把依照的列作为索引，
            这不过是MultiIndex形式的一种dataframe罢了。
            可以用as_index=False'''
    #热度top10
    data2=data1[0:10]
    bar = createBarFromDataFrame(title ="TOP10热度", dataFrame=data2, xAxis="class", yAxis="heat",titlePos='center',
        label="热度" , **bar_Style)
    
    
    print("条形图已出")
    return bar
def bar2(data):
    
    temp = data[['room_id','class']].groupby('class',as_index=False).count()#直播人数
    
    data1=data.groupby('class',as_index=False).sum()#热度总和
    
    temp['heat_sum']=data1['heat']
    
    data4=temp.sort_values(by="room_id",ascending= False)
    
    data4.rename(columns={'room_id':'live_person_number'}, inplace = True)

    data5=data4[0:15]
    data5['average_heat']=data5['heat_sum']/data5['live_person_number']
    f = lambda x:x/10
    data5['average_heat']=data5['average_heat'].apply(f)
    bar = createBarFromDataFrame(dataFrame=data5, xAxis="class", yAxis="live_person_number",label="直播人数",
        title ="TOP10各分类直播人数与平均热度对比",titlePos='center',**bar_Style)
    createBarFromDataFrame(bar=bar, dataFrame=data5, xAxis="class", yAxis="average_heat",label="平均热度",titlePos='center',xaxis_rotate='30',**bar_Style)
    print("条形图已出")
    return bar
    
def scatter_size(data):
    data1=data.groupby('class',as_index=False).sum().sort_values(by="heat",ascending= False)
    data2=data1[0:50]
    
    scatter = Scatter('散点示例图',width=1400, height=700,title_pos='center')
    a=[10,50,100,30,50,45,10,35,45,30]
    scatter.add("热度", x_axis=list(data2['class']),y_axis=list(data2['heat']),**scatter_style)
    print("sandian图已出")
    return scatter
def word_cloud(data):
    data1=data.groupby('class',as_index=False).sum()
    wordcloud = WordCloud("直播类型-热度 词云图" ,"时间：2019-4-9-13:14",title_pos='center',width=1400, height=700)
    wordcloud.add('',list(data1['class']), list(data1['heat']),word_size_range=[20,100],is_more_utils=True,shape="circle")
                  
    return wordcloud;
    
if __name__ == '__main__':
    data = pd.read_csv('E:\out16.csv')
    data = data.drop_duplicates('room_id')
    add(word_cloud())
    add(bar1())
    add(bar2())
    add(pie())
    add(scatter_size())
    setup("E:\\tu.html")
    
    
    
    
    
    
    
    
    

    
    






    
    
