# encoding: utf-8
import numpy as np
from quant import *
from quant import chrono
import datetime
from datetime import timedelta

class MyPlay(trade.Model):
    def on_initialize(self):
        self.myinstr = "XSHE_000513"
        self.bartype1 = "Bar_1day" #type1:订阅1day k线
        #self.bartype2 = "Bar_1min" #type2:订阅1min k线
        self.buyunit = 100 # 1手
        self.subscribe(self.myinstr,self.bartype1) #订阅1day K线 of 白云机场
        #self.subscribe(self.myinstr,self.bartype2)      
        self.default_date = chrono.Date(19700101)
        self.date = []
        self.Trade_date = []  ##空列表，搜集SEP后的交易日期
        self.history = [] # 存档300天历史数据  这个应该是bar类型
        
    def on_data_update(self, data):
        if data.type == "Bar_1day":
            #用日度交易数据来收集数据并确定SEP
            #增加最新数据，去掉最旧数据
            self.history = np.append(self.history, data.close)
            self.date = np.append(self.date, data.date)
            
            if (len(self.history)-12>0):
                for i in range(max(4,len(self.history)-12),len(self.history)-6):
                    if(self.history[i] > max(self.history[i-4:i]) and self.history[i] > max(self.history[i+1:i+5]) and (self.date[i+6] not in self.Trade_date)):
                        ## 判断SEP条件
                        self.Trade_date.append(self.date[i+6])
                     
            
            
            if data.date in self.Trade_date:
                print (bool(data.date in self.Trade_date),data.date,self.Trade_date)


