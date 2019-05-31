# -*- coding : utf-8 -*-
# Create : 2019-03-12
# Author : Bingnan Huo
# Version : 2.0

import os
from datetime import datetime
from pandas import DataFrame
from pyecharts import Bar,Line,Page,Overlap,Pie,Grid,Timeline
from pyecharts.chart import Chart
from pyecharts.echarts import option

PAGE = Page()
PATH = os.path.abspath(".")
__MAP = {"bar":Bar, "line":Line, "pie":Pie}

#=====================================操作全局的Page相关的Function====================================

def add(chart,name=None):
    PAGE.add_chart(chart,name)
    return True

def setup(path=None):
    tp = path or PATH
    PAGE.render(path=tp)
    return True

def NOW():
    t = datetime.now()
    year = str(t.year)
    month = str(t.month)
    day = str(t.day)
    hour = str(t.hour)
    minut = str(t.minute)
    return year + "-" + month + "-" + day + " " + hour + ":" + minut

def getJS():
    return PAGE.get_js_dependencies()

#===========================================隐函数===================================================

def __create(kind, *args, **kwargs):
    return __MAP[kind]( *args, **kwargs)


#=====================================================================================================

def createBarFromDataFrame(dataFrame, xAxis, yAxis, label,bar=None,width=800,height=400,title="柱状图",subtitle=NOW()
                    ,titlePos="50%",**kwargs):
    '''
    从DataFrame构造一个Bar对象。
    :param dataFrame: DataFrame对象，Bar对象的主要数据来源。
    :param xAxis: Bar对象的X轴，也是DataFrame中的一个列。
    :param yAxis: Bar对象的Y轴，也是DataFrame中的一个列。
    :param label: Bar对象的数据标签。
    :param bar: 可以传入一个Bar对象向其中添加数据，默认为None,则会自动创建一个新的Bar对象。两种方式都会返回新的Bar对象。
    :param width: 设置Bar对象的宽度，默认为800。
    :param height: 设置Bar对象的高度，默认为400。
    :param title: 设置标题，默认为‘柱状图’。
    :param subtitle: 设置子标题，默认为当前时间点。
    :param kwargs: add方法中所需参数，在此传入。
    :return: False->创建失败，Bar->创建成功。
    '''
    if not isinstance(dataFrame, DataFrame):
        return False
    if bar:
        if not isinstance(bar, Bar):
            return False
    if xAxis in dataFrame.columns and yAxis in dataFrame.columns:
        # tb = Bar(title=title, subtitle=subtitle,title_text_size=titleSize)
        tb = bar or Bar(title=title, subtitle=subtitle, width=width, height=height, title_pos=titlePos)
        tb.add(label, dataFrame[xAxis], dataFrame[yAxis],**kwargs)
        return tb
    else:
        return False

def tmpBar(title, subtitle, **kwargs):
    return __create("bar", title, subtitle, **kwargs)

def createLineFromDataFrame(dataFrame, xAxis, yAxis, label, line=None, width=800, height=400, title="折线图",
                           subtitle=NOW(),titlePos="50%",**kwargs):
    if not isinstance(dataFrame, DataFrame):
        return False
    if xAxis and yAxis not in dataFrame.columns:
        return False
    if line:
        if not isinstance(line, Line):
            return False
    tl = line or Line(title=title, subtitle=subtitle, width=width, height=height, title_pos=titlePos)
    tl.add(label, dataFrame[xAxis], dataFrame[yAxis],**kwargs)
    return tl

def tmpLine(title, subtitle, **kwargs):
    return __create("line", title, subtitle, **kwargs)

def createPieFromDataFrame(dataFrame, xAxis, yAxis,label ,title="饼图",subtitle=NOW(),
                           width=800, height=400, titlePos="50%",**kwargs):
    if not isinstance(dataFrame, DataFrame):
        return False
    if xAxis and yAxis not in dataFrame.columns:
        return False
    tp = Pie(title=title, subtitle=subtitle, width=width, height=height, title_pos=titlePos)
    tp.add(label, dataFrame[xAxis], dataFrame[yAxis], **kwargs)
    return tp

def tmpPie(title, subtitle, **kwargs):
    return __create("pie", title, subtitle, **kwargs)

def createLayOutManager(title, width=800, height=400,**kwargs):
    tg = Grid(page_title=title, width=width, height=height, **kwargs)
    return tg


#===========================================行为函数================================================

def combinate(base, other, title="组合",width=800, height=400,
              xIndex=0, yIndex=0, addX=False, addY=False):
    # 将两张图标进行整合，最终生成一张图标。以第一张图标为基础。
    if not isinstance(base, Chart) or not isinstance(other, Chart):
        return False
    to = Overlap(page_title=title, width=width, height=height)
    to.add(base, xaxis_index=xIndex, yaxis_index=yIndex, is_add_xaxis=addX, is_add_yaxis=addY)
    to.add(other, xaxis_index=xIndex, yaxis_index=yIndex, is_add_xaxis=addX, is_add_yaxis=addY)
    return to

def layout(one, manager,**kwargs):
    if not isinstance(one, Chart):
        return False
    if not isinstance(manager, Grid):
        return False
    manager.add(one, **kwargs)

def addXY(chart, xAxis,yAxis,label="",**kwargs):
    if not isinstance(chart, Chart):
        return False
    chart.add(label,xAxis,yAxis,**kwargs)

def tooltipParamSet():
    pass

if __name__ == "__main__":
    df = DataFrame({"class":["LOL","PUBG","WZ"],"heat":[1000,2000,3000],"count":[100,200,300]})
    print(df)
    # bar = createBarFromDataFrame(dataFrame=df, xAxis="class", yAxis="heat",label="热度" , bar_category_gap="10%")
    # createBarFromDataFrame(bar=bar, dataFrame=df, xAxis="class", yAxis="count",label="直播人数", bar_category_gap="10%")
    # line = createLineFromDataFrame(dataFrame=df, xAxis="class", yAxis="heat",label="热度",is_smooth=True)
    # createLineFromDataFrame(line=line, dataFrame=df, xAxis="class",yAxis="count",label="直播人数")
    # # new = combinate(bar, line, addY=True)
    # # pie = createPieFromDataFrame(dataFrame=df, xAxis="class", yAxis="heat", label="热度占比")
    # l = createLayOutManager("Test")
    # layout(bar,l, grid_left="55%")
    # layout(line,l, grid_right="65%")
    # add(l)
    bar = tmpBar("热度","", width=1400, height=700)
    addXY(bar,["LOL","PUBG","WZ"],[1000,2000,3000],"热度", is_stack=True)
    addXY(bar,["LOL","PUBG","WZ"],[500,1000,1500],"直播人数",is_stack=True)
    add(bar)

    setup("C:/Users/hbn66/Desktop/test.html")


