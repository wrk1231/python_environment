# encoding: utf-8
import numpy as np
from quant import *
class MyPlay(trade.Model):

    def on_initialize(self):
        self.subscribe("XSGE_RB_201610", "Bar_5min") #订阅5分钟K线
        self.order_num = 0 #order状态标识
        self.opened = 0 #仓位标识
        self.short = 5 #短期均线参数
        self.long = 60 #长期均线参数
        self.shortma = 0 #短期均线
        self.longma = 0 #长期均线
        self.history = np.zeros(self.long) #存历史数据
   

    def on_order_update(self, order):
        #标识order状态，如果订单已经发出，记录一下，避免重复下单
                                        
        if order.state == trade.SENT:  
            self.order_num = 1          
        elif order.state == trade.FINAL:
            self.order_num = 0


        #标识仓位信息，多仓记为1，空位记为-1，没有仓位记为0  
        if(order.position_effect == trade.OPEN and order.direction == trade.BID and order.filled_size == order.signed_size):
            self.opened = 1
        if(order.position_effect == trade.COVER and order.direction == trade.BID and order.filled_size == order.signed_size):
            self.opened = 0
        if(order.position_effect == trade.OPEN and order.direction == trade.ASK and order.filled_size == order.signed_size):
            self.opened = -1
        if(order.position_effect == trade.COVER and order.direction == trade.ASK and order.filled_size == order.signed_size):
            self.opened = 0
         
    def on_data_update(self, data):
        #增加最新数据，去掉最旧数据
        self.history = np.append(self.history, data.close)
        self.history = np.delete(self.history, 0)
        #得到当前时间
        time_tmp = self.get_current_time()
        time = chrono.time_to_datetime(time_tmp, timezone="Asia/Shanghai")
        #计算均线
        if self.history[0] != 0:
            self.shortma = np.mean(self.history[(self.long - self.short):])
            self.longma = np.mean(self.history)
        #如果距离收市时间大于5分钟
        if (time.hour < 14 or (time.hour == 14 and time.minute < 55)):
            #开多仓逻辑：短期均线大于长期均线
            if(self.shortma > self.longma and self.opened == 0 and self.order_num == 0):
                self.place_future_order(data.instrument.symbol, 100, trade.MarketPrice(), trade.OPEN)
            #多单清仓逻辑：短期均线小于长期均线
            elif(self.shortma < self.longma and self.opened == 1 and self.order_num == 0):
                self.place_future_order(data.instrument.symbol, -100, trade.MarketPrice(), trade.COVER)     
            #开空仓逻辑：短期均线小于长期均线
            elif(self.shortma < self.longma and self.opened == 0 and self.order_num == 0):
                self.place_future_order(data.instrument.symbol, -100, trade.MarketPrice(), trade.OPEN)
            #空单清仓逻辑：短期均线大于长期均线
            elif(self.shortma > self.longma and self.opened == -1 and self.order_num == 0):
                self.place_future_order(data.instrument.symbol, 100, trade.MarketPrice(), trade.COVER)
        #每日平仓
        if(time.hour == 14 and time.minute >= 55):
            if(self.opened != 0):
                self.place_future_order(data.instrument.symbol, -1*self.opened, trade.MarketPrice(), trade.COVER)