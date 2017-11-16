# -*- coding: UTF-8 -*-
import tushare as ts
import pandas as pd
import numpy as np
from pandas import DataFrame,Series

data = DataFrame(pd.read_excel('o1.xlsx'))
print data.columns
for x in xrange(len(data)):
 	if  (data.loc[x,'BonusRatio']  == 0 and data.loc[x,'PlaceRatio']== 0 and data.loc[x,'IssuePrice'] == 0 and data.loc[x,'DividendCash']== 0 ):
		data.loc[x,'label2' ] = 'del'
	else :
		data.loc[x,'label2' ] = 'keep'

for x in xrange(len(data)):
	if data.loc[x,'label'] != 'none' and data.loc[x,'label'] != 'nodate':

		if data.loc[x,'label2'] != data.loc[x,'label']:
			data.loc[x,'double_check'] = 'ERROR'
		else:
			data.loc[x,'double_check'] = 'CORRECT'

data.to_excel('o3.xlsx')