# encoding: utf-8
import numpy as np
from quant import *
from quant import chrono

class MyPlay(trade.Model):
    def on_initialize(self):
        self.myinstr = "XSHE_000513"
        self.bartype1 = "Bar_1day" #type1:订阅1day k线
        ## self.bartype2 = "Bar_1day" #type2:订阅5min k线
        ## self.buyunit = 100 # 1手
        self.subscribe(self.myinstr,self.bartype1) #订阅1day K线 of 白云机场
        ## self.subscribe(self.myinstr,self.bartype2)
        ## self.order_num = 0 #order状态标识
        self.date = np.zeros(300)
        self.history = np.zeros(300) # 存档300天历史数据  这个应该是bar类型
        
    def on_data_update(self, data):
            #增加最新数据，去掉最旧数据
        self.history = np.append(self.history, data.close)
        self.history = np.delete(self.history, 0)
        
        self.date = np.append(self.date, data.date)
        self.date = np.delete(self.date, 0)
            
        record = []
        SEP_date = []
        
        for i in range(4,len(self.history)-4):
            if(self.history[i] > max(self.history[i-4:i]) and self.history[i] > max(self.history[i+1:i+5])):
                record.append(i) 
                SEP_date.append(self.date[i])
                
        for j in record:
            print j
            
        print chrono.Date(SEP_date)



