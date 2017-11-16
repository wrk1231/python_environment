# encoding: utf-8
#回测时间：1305-1403
import numpy as np
from quant import *
from quant import trade

class MyPlay(trade.Model):
    def on_initialize(self):
        self.subscribe("XSGE_RB_201405", "Bar_5min") #订阅5minK线
        self.opened = 0 #仓位标识
        self.order_num = 0 #order状态标识
        self.bollLength = 26 #布林线参数，可更改
        self.offset = 2 #布林线参数，设定(上下轨和中间线的差)与标准差之比
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
        #标识仓位信息         
        if(order.position_effect == trade.OPEN and order.direction == trade.BID and order.filled_size == order.signed_size):
            self.opened = 1
        if(order.position_effect == trade.COVER and order.direction == trade.BID and order.filled_size == order.signed_size):
            self.opened = 0
        if(order.position_effect == trade.OPEN and order.direction == trade.ASK and order.filled_size == order.signed_size):
            self.opened = -1
        if(order.position_effect == trade.COVER and order.direction == trade.ASK and order.filled_size == order.signed_size):
            self.opened = 0
             
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
        if (data.close > self.UpLine and self.opened == 0 and not(time.hour == 14 and time.minute >= 55)):
            self.place_future_order(data.instrument.symbol, -1, trade.MarketPrice(), trade.OPEN, trade.EOD)
        #开仓步骤：收盘<合理价格下界，价格被低估开多单，尾盘不下单
        if (data.close < self.DownLine and self.opened == 0 and not(time.hour == 14 and time.minute >= 55)):
            self.place_future_order(data.instrument.symbol, 1, trade.MarketPrice(), trade.OPEN, trade.EOD)
        #空单清仓逻辑：收盘<合理价格下界，价格被低估，尾盘不下单
        if (data.close < self.DownLine and self.opened < 0 and not(time.hour == 14 and time.minute >= 55)):
            self.place_future_order(data.instrument.symbol, 1, trade.MarketPrice(), trade.COVER, trade.EOD)
        #多单清仓逻辑：收盘>合理价格上界，价格被高估 ，尾盘不下单       
        if (data.close > self.UpLine and self.opened > 0 and not(time.hour == 14 and time.minute >= 55)):
            self.place_future_order(data.instrument.symbol, -1, trade.MarketPrice(), trade.COVER, trade.EOD)
        #定时清仓    
        if(time.hour == 14 and time.minute >= 55):
            portfolio = self.get_futures_portfolio()
            item1 = portfolio.get(instr.Instrument("XSGE_RB_201405"),  HedgeEffect.SPECULATION, FuturesPortfolioPositionType.FUTURES_LONG_POSITION)#得到仓位信息
            item2 = portfolio.get(instr.Instrument("XSGE_RB_201405"),  HedgeEffect.SPECULATION, FuturesPortfolioPositionType.FUTURES_SHORT_POSITION)#得到仓位信息
            if(self.opened != 0 and item1 != None):
                self.place_future_order(data.instrument.symbol, -1*item1.position, trade.MarketPrice(), trade.COVER, trade.EOD)
            elif(self.opened != 0 and item2 != None):
                self.place_future_order(data.instrument.symbol, item2.position, trade.MarketPrice(), trade.COVER, trade.EOD)
    def on_alarm(self):
        print "MyPlay::onAlarm"