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
        self.a0 = self.add_alarm(chrono.str_to_time("2016-07-12 01:35:00.000000"))
        
        if data.date in Trade_date:

            self.t0 =  self.add_alarm(chrono.str_to_time(str(data.date)+"01:25:00.000000"))

            self.t1 =  self.add_alarm(chrono.str_to_time(str(data.date)+"01:30:00.000000"))
            self.t2 =  self.add_alarm(chrono.str_to_time(str(data.date)+"01:36:00.000000"))
            self.t3 =  self.add_alarm(chrono.str_to_time(str(data.date)+"01:42:00.000000"))
            self.t4 =  self.add_alarm(chrono.str_to_time(str(data.date)+"01:48:00.000000"))
            self.t5 =  self.add_alarm(chrono.str_to_time(str(data.date)+"01:54:00.000000"))



    


    def on_data_update(self, data):
        pass
        
    def on_alarm(self,id):
        if id == self.t0 :
            self.place_stock_order(self.myinstr, 1000, trade.MarketPrice())

        if id == self.t1:
            self.place_stock_order(self.myinstr, 200, trade.MarketPrice())








            
    def on_order_update(self, order):
        if order.state == OrderState.FINAL:
            print (order.filled_value, order.filled_size,order.filled_value/order.filled_size)





            