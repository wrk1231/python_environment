# encoding: utf-8
#回测时间：1305-1403
import numpy as np
from quant import *
from quant import trade

class MyPlay(trade.Model):
    def on_initialize(self):
        self.myinstr = "XSHE_000513"
        self.bartype = "Bar_5min"
        self.buyunit = 100*10 # 10手
        self.subscribe(self.myinstr,self.bartype) #订阅1day K线 of 白云机场
        self.order_num = 0 #order状态标识
        
        self.bollLength = 10 #布林线参数，可更改
        self.offset = 0.5 #布林线参数，设定(上下轨和中间线的差)与标准差之比
        self.history = np.zeros(self.bollLength) #存历史数据
        self.MidLine = 0 #中间线
        self.band = 0 #标准差
        self.UpLine = 0 #价格信赖区间的上界：压力线
        self.DownLine = 0 #价格信赖区间的下界：支撑线
        
    def on_order_update(self, order):
        #标识order状态，如果订单已经发出，记录一下，避免重复下单
        if order.state == trade.SENT:
            self.order_num = 1
        elif order.state == trade.FINAL:
            self.order_num = 0

    def on_data_update(self, data):
        if data.type == 'Bar_5min':
            self.history = np.append(self.history, data.close)
            self.history = np.delete(self.history,0) #更新历史数据
            self.MidLine = np.mean(self.history) #计算中间线
            self.band = np.sqrt(np.var(self.history)) #计算标准差

            time_tmp = self.get_current_time()
            time = chrono.time_to_datetime(time_tmp, timezone="Asia/Shanghai") #得到当前时间

            if(self.history[0] != 0):
                self.UpLine = self.MidLine + self.offset * self.band #计算信赖区间上界
                self.DownLine = self.MidLine - self.offset * self.band #计算信赖区间下界


        #开仓步骤：收盘>合理价格上界，价格被高估开空单，尾盘不下单
        if (time.hour < 14 or (time.hour == 14 and time.minute <= 55)):
 
            if (data.close > self.UpLine and self.order_num == 0) :
                self.place_stock_order(self.myinstr, -self.buyunit, trade.MarketPrice())
            #开仓步骤：收盘<合理价格下界，价格被低估开多单，尾盘不下单
            if (data.close < self.DownLine and self.order_num == 0):
                self.place_stock_order(self.myinstr, self.buyunit, trade.MarketPrice())
            
           