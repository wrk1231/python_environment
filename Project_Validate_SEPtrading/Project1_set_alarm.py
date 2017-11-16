# encoding: utf-8
import numpy as np
from quant import *
from quant import trade
from quant import chrono
from quant import instr

class MyPlay(trade.Model):       
    #开始初始化
    def on_initialize(self):
        #load参数
        self.myinstr = "XSHE_000513"
        self.bartype = "Bar_5min" #订阅5分钟k线
        self.buyunit = 100 # 1手
        self.subscribe(self.myinstr,self.bartype)         
        self.best_day = chrono.Date(20160712)
        self.a0 = self.add_alarm(chrono.str_to_time(str(self.best_day)+" 01:35:00.000000"))
                                 

            
    def on_data_update(self, data):
        pass
        
    def on_alarm(self,id):
        if id == self.a0 :
            self.place_stock_order(self.myinstr, 2000, trade.MarketPrice())
            
    def on_order_update(self, order):
        if order.state == OrderState.FINAL:
            print (order.filled_value, order.filled_size,order.filled_value/order.filled_size)














