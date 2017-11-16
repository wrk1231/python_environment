# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import tushare as ts
from pandas import *
from pandas import DataFrame,Series
import sys

stock_id_str = sys.argv[3]
start_date = sys.argv[1]
end_date = sys.argv[2]
stock_id_list = stock_id_str.split(',')

frame = DataFrame( columns=['TYPE', 'TRADEDATE', 'SECURITYCODE', 'CURRENCY','OPEN','HIGH','LOW','NEW','TVOL','TVAL','TURNRATE','BUYVOL','SELLVOL'])
df = ts.get_k_data(stock_id_list[0],start = start_date,end = end_date)
frame['TRADEDATE'] = df['date']
frame['TYPE'] = 'TUSHARE'
frame['TVOL'] = None
frame['TVAL'] = None
frame['SECURITYCODE'] = stock_id_list[0]
frame['CURRENCY'] = 'RMB'
frame['OPEN'] = df['open']
frame['HIGH'] = df['high']
frame['LOW'] = df['low']
##frame['TURNDATE'] = df['turnover'] doc上有的，结果导出来的表里面没得了

for i in xrange(1,len(stock_id_list)):
	dframe = DataFrame( columns=['TYPE', 'TRADEDATE', 'SECURITYCODE', 'CURRENCY','OPEN','HIGH','LOW','NEW','TVOL','TVAL','TURNRATE','BUYVOL','SELLVOL'])
	df2 = ts.get_k_data(stock_id_list[i],start = start_date,end = end_date)
	dframe['TRADEDATE'] = df['date']
	dframe['TYPE'] = 'TUSHARE'
	dframe['TVOL'] = None
	dframe['TVAL'] = None
	dframe['SECURITYCODE'] = stock_id_list[i]
	dframe['CURRENCY'] = 'RMB'
	dframe['OPEN'] = df['open']
	dframe['HIGH'] = df['high']
	dframe['LOW'] = df['low']
	frame = pd.concat([frame,dframe])


filename = sys.argv[-1]
frame.to_csv(filename +'_' + str(start_date) + '_' + str(end_date) + '.csv')

