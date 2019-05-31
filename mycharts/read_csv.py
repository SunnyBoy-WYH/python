'''读取文件用'''
import os
import pandas as pd
from string_store import *
os.chdir(os.path.abspath("."))
def read_csv_data():
    csv_array=[]
    for i  in range(0,13):
        csv_array.append(pd.read_csv('../result/data/out'+String_filename[i]+'.csv').drop_duplicates(["room_id"]))
    return csv_array

