# encoding: utf-8
import numpy as np
from quant import *
class MyPlay(trade.Model):

    def on_initialize(self):
    
        self.myinstr = "XSHE_000513"
        self.bartype = "Bar_5min"
        self.subscribe(self.myinstr,self.bartype)#订阅1day K线 of 白云机场
        self.buyunit = 100*10 #10手
        

        self.order_num = 0 #order状态标识
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
            #买入逻辑：短期均线大于长期均线
            if(self.shortma > self.longma and self.order_num == 0):
                self.place_stock_order(self.myinstr, self.buyunit, trade.MarketPrice())

                ## 下单规则： place_stock_order(symbol, signed_size, price, duration=EOD, deal_account_id='', gate_type='')
            #卖出逻辑：短期均线小于长期均线
            
            elif(self.shortma < self.longma and self.order_num == 0):
                self.place_stock_order(self.myinstr, self.buyunit, trade.MarketPrice())
                

              
            