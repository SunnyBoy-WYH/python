# -*- coding : utf -8 -*-
# Create : 2019-4-23
# Author : Bingnan Huo
# Version : 0.0.1
import os
from pyecharts import Timeline,Bar,Page,Style,Overlap,Grid,Line
from pandas import DataFrame

class TimeBar:

    def __init__(self, bars, timePoints, width=800, height=600):
        self.title = None
        self.bars = bars
        self.timePoints = timePoints
        self.width = width
        self.height = height
        self.speed = 500

    def _initial(self, speed):
        timeline = Timeline(width=self.width, height=self.height, timeline_play_interval=speed)
        index = 0
        for bar in self.bars:
            timeline.add(bar, time_point=self.timePoints[index])
            index += 1
        return timeline

    def setup(self, name,page=None):
        tPage = page or Page()
        t = self._initial(self.speed)
        tPage.add_chart(t,name=name)
        return page

#==================================================global variable declartion==========================================
PAGE = Page()
PATH = os.path.abspath(".")
TIMELINE = {}
#======================================================================================================================
def addXY(chart,xAxis, yAxis, label="data"):
    if not hasattr(chart, "add"):
        return False
    chart.add(label, xAxis, yAxis)
#======================================================================================================================
def createBarD(data,attrs=None,names=None):
    bar = Bar()
    tc = []
    if attrs:
        for a in attrs:
            if a not in data.columns:
                return False
    else:
        attrs = list(data.columns)
    if names:
        for n in names:
            if n not in data.index:
                return False
    else:
        names = list(data.index)
    for name in names:
        v = data.loc[name,:].values
        v = list(v)
        tc.append(v)
    print(tc)
    cnt = 0
    for item in tc:
        bar.add(names[cnt], attrs, item)
        cnt += 1
    return bar

def creatBarsD(data):
    xAxis = list(data.columns)
    tl = []
    for d in data.index:
        tb = Bar()
        tb.add(str(d),xAxis, data.loc[d,:])
        tl.append(tb)
    return tl

def createLineD(data):
    line = Line()
    xAxis = list(df.columns)
    for d in data.index:
        line.add(str(d),xAxis, data.loc[d,:], is_label_show=True)
    return line


def createBarL(data,attrs,names):
    d = len(attrs)
    for i in data:
        if len(i) != d:
            return  False
    if len(data) != len(names):
        return False
    cnt = 0
    bar = Bar()
    for name in names:
        bar.add(name,attrs[cnt],data[cnt])
        cnt += 1
    return bar

def creatTimeLine(charts, timepoints, speed=500, showTimeLine=True):
    tt = Timeline(timeline_play_interval=speed, is_timeline_show=showTimeLine)
    cnt = 0
    for chart in charts:
        tt.add(chart,time_point=timepoints[cnt])
        cnt += 1
    return tt

def creatTimeLineG(speed):
    tt = Timeline(timeline_play_interval=speed)
    for k,v in TIMELINE.items():
        tt.add(v,k)
    return tt

def add2TIMELINE(chart,timepoint):
    if not isinstance(timepoint, str):
        return False
    TIMELINE[timepoint] = chart
    return True

def removeFromTIMELINE(chart, timepoint):
    if not isinstance(timepoint, str):
        return False
    _ = TIMELINE.pop(timepoint)
    return True

def clearTIEMLINE():
    TIMELINE.clear()
    return True

def updateTIMELINE(chart, timepoint):
    if not isinstance(timepoint, str):
        return False
    TIMELINE.update(timepoint, chart)
    return True


def add(chart, name=None):
    PAGE.add_chart(chart,name)


def combinate(base, other,xIndex=0,yIndex=0,addX=False, addY=False):
    nt = Overlap()
    nt.add(base)
    nt.add(other,xaxis_index=xIndex,yaxis_index=yIndex,is_add_xaxis=addX,is_add_yaxis=addY)
    return nt


def style(chart, **kwargs):
    pass

def setup(path=None):
    p = path or PATH
    PAGE.render(path=p)

if __name__ == "__main__":
    df = DataFrame({"LOL":[i+100 for i in range(100,1100,10)],"PUBG":[i+100 for i in range(200, 1200,10)],"WZ":[i+100 for i in range(300,1300,10)]})
    print(df)
    bars = creatBarsD(df)
    t1 = creatTimeLine(bars, [i for i in range(100,1100,10)], 50)
    add(t1)
    setup("C:/Users/hbn66/Desktop/test.html")










