import numpy as np
import quant
from quant import *
from quant import chrono
from quant import instr
%matplotlib inline
import matplotlib.pyplot as plt
quant.mustang.load_config("../default.ini")
###########################################################################################################
#获取Instrument
instr1 = instr.Instrument('XSHG_600004')
#定义起始时间
start = chrono.date_to_time(chrono.Date(20150303))
#定义截止时间
stop = chrono.date_to_time(chrono.Date(20150630))
#定义数据类型	
datatype = "Bar_1day"
#取得数据
data1 = data.MarketData(instr1, datatype, start, stop)
#取得从起始时间至截止时间每日收盘价的array  data1.close : type 为np.narray
record = []
# an empty list
# 
# ##########################################################################################################
for i in range(4,len(data1.close)):
    if(data1.close[i] > max(data1.close[i-4:i]) and data1.close[i] > max(data1.close[i+1:i+5])):
        record.append(i) 
# 判断SEP的准则，并记录下每一个符合要求的日期的顺序
for j in record:
    print data1.date[j]
## <type 'numpy.int32'>
## 帮助文档：您可以采用最方便的写法，直接写int类型的时间，比如20160101，我们内部会自动转换成Date类
## 是否意味着可以不用chrono.Date?
for j in record:
    print chrono.Date(data1.date[j])
## 类型： <class 'quant.sdk.Date'>
## 这样我们就找到了SEP所对应的日期（date类数据）