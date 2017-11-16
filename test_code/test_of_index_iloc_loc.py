# -*- coding: UTF-8 -*-
import tushare as ts
import pandas as pd
import numpy as np
from pandas import DataFrame,Series


data = DataFrame(np.arange(16).reshape((4, 4)),
                 index=['Ohio', 'Colorado', 'Utah', 'New York'],
                 columns=['one', 'two', 'three', 'four'])
d = [1,2,3,4]
se1 = DataFrame(columns=['one', 'two', 'three', 'four'],index = ['fu'])
se1.loc['fu'] = [1,2,3,4]
se2 = Series({'a':11,'b':11,'c':11})
se2.name = 'fu'
data = data.append(se1)
df = pd.DataFrame(np.arange(0,60,2).reshape(10,3),columns=list('abc'),index = ['one','two','three','four','five','six','seven','eight','nine','ten'])  
df2 = pd.DataFrame(np.arange(60,120,2).reshape(10,3),columns=list('abc'),index = ['one','two','three','four','five','six','seven','eight','nine','ten'])  
df = df.append(df2)
df
for x in xrange(len(df)):
	if df.iloc[x,2]%4 == 0:		
		print 'hi','_____',df.index[x],df.ix[df.index[x],'b'],'________',df.index[x],df.ix[df.index[x],1]
		df.iloc[x,2] = 'hi'
		df.ix[df.index[x],'d'] = 'hello'
		df.loc[df.index[x],'e'] = 'congrat'
		df.iloc[x,0] = 'hehe'

# for x in xrange(len(data)):
# 	if data.loc[x,'label'] != 'none' and data.loc[x,'label'] != 'nodate':

# 		if data.loc[x,'label2'] != data.loc[x,'label']:
# 			data.loc[x,'double_check'] = 'ERROR'
# 		else:
# 			data.loc[x,'double_check'] = 'CORRECT'
# 			
# 			这个的index是array
print df





