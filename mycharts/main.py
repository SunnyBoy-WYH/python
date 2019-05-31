import os
from timeline_line import *
from smooth_timeline import *
from static_image import *
os.chdir(os.path.abspath("."))
if __name__ == "__main__":
    #从文件中提取数据
    data_array=read_csv_data()
    page_1 = Page()
    page_2 = Page()
    page_3 = Page()
    page_4 = Page()
    page_5 = Page() 
    page_1.add(line1(data_array))
    page_1.add(line2(data_array))
    print("page_1",page_5.get_js_dependencies())
    page_1.render("../result/line.html")

    page_2.add(scatter_timeline(data_array))
    page_2.add(scatter_size(data_array[6]))
    print("page_2",page_5.get_js_dependencies())
    page_2.render("../result/scatter.html")

    page_3.add(pie_timeline(data_array))
    page_3.add(pie(data_array[6]))
    print("page_3",page_5.get_js_dependencies())
    page_3.render("../result/pie.html")


    page_4.add(bar1_timeline(data_array))
    page_4.add(bar1(data_array[6]))
    page_4.add(bar2(data_array[6]))
    print("page_4",page_5.get_js_dependencies())
    page_4.render("../result/bar.html")


    page_5.add(gauge_timeline(data_array))
    page_5.add(word_cloud(data_array[6]))
    print("page_5",page_5.get_js_dependencies())
    page_5.render("../result/main.html")

        
    
    
    
