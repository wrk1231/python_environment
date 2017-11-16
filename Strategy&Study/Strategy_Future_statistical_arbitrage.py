# coding: utf-8
# 统计套利策略：在snapshot上下单，当snapshot的价差大幅超过平衡点时，对价差反方向下单，当价差接近平衡价差时卖出，赚取两个合约价差之间的利润。其中平衡价差由1分钟均线价差来获取。
# 回测起始日期：2014-06-14； 回测结束日期：2014-10-18
# 初始资金：10,000
# 拟合粒度：快照
import numpy as np
from quant import *
class MyPlay(trade.Model):
    def on_initialize(self):
        print "MyPlay::onInitalize"
        self.subscribe("XSGE_RB_201401", "Snapshot") #订阅两个合约的shapshot和1分钟线
        self.subscribe("XSGE_RB_201310", "Snapshot")
        self.subscribe("XSGE_RB_201401", "Bar_1min")
        self.subscribe("XSGE_RB_201310", "Bar_1min")
        self.order_num = 0 #order状态标识
        self.openedleg1 = 0 #两个合约中的一个开平仓的标识
        self.openedleg2 = 0 #两个合约中的另一个开平仓的标识
        self.History1 = np.zeros(100)
        self.History2 = np.zeros(100) #存两个和约1min线历史数据
        self.difflist = np.zeros(200) #存价差的历史数据，用于判断价差是否过大，在策略中暂时没有用到
        self.diffma = 0 #两个合约价差的均值：平衡价差
        self.diff = 0 #snapshot价差与平衡价差之差
        self.ts1 = 0 #合约的snapshot价格
        self.ts2 = 0
    def on_order_update(self, order):
        #更新订单状态，避免重复下单
        if order.state == trade.SENT: 
            self.order_num = 1
        elif order.state == trade.FINAL:
            self.order_num = 0
        #标识仓位信息
        if(order.position_effect == trade.OPEN and order.instrument.symbol=="XSGE_RB_201401" and order.direction == "BID" and order.filled_size == order.signed_size):#开多仓及其标志
            self.openedleg1 = 1
        if(order.position_effect == trade.OPEN and order.instrument.symbol=="XSGE_RB_201310" and order.direction == "BID" and order.filled_size == order.signed_size):
            self.openedleg2 = 1 
        if(order.position_effect == trade.COVER and order.instrument.symbol=="XSGE_RB_201401" and order.direction == "BID" and order.filled_size == order.signed_size):#平空仓及其标志
            self.openedleg1 = 0
        if(order.position_effect == trade.COVER and order.instrument.symbol == "XSGE_RB_201310" and order.direction == "BID" and order.filled_size == order.signed_size):
            self.openedleg2 = 0
        if(order.position_effect == trade.OPEN and order.instrument.symbol == "XSGE_RB_201401" and order.direction == "ASK" and order.filled_size == order.signed_size):#开空仓及其标志
            self.openedleg1 = -1
        if(order.position_effect == trade.OPEN and order.instrument.symbol == "XSGE_RB_201310" and order.direction == "ASK" and order.filled_size == order.signed_size):
            self.openedleg2 = -1
        if(order.position_effect == trade.COVER and order.instrument.symbol == "XSGE_RB_201401" and order.direction == "ASK" and order.filled_size == order.signed_size):#平多仓及其标志
            self.openedleg1 = 0
        if(order.position_effect == trade.COVER and order.instrument.symbol == "XSGE_RB_201310" and order.direction == "ASK" and order.filled_size == order.signed_size):
            self.openedleg2 = 0
    def on_data_update(self, data):
        if data.type == "Bar_1min" and data.instrument.symbol == "XSGE_RB_201401":
            self.History1 = np.append(self.History1, data.close)
            self.History1 = np.delete(self.History1, 0) #更新第一个合约的历史数据 
        if data.type== "Bar_1min" and data.instrument.symbol == "XSGE_RB_201310":
            self.History2 = np.append(self.History2, data.close)
            self.History2 = np.delete(self.History2, 0) #更新第二个合约的历史数据
            self.diffma = np.mean(self.History1) - np.mean(self.History2) #计算平衡价差
        if data.type == "Snapshot" and data.instrument.symbol == "XSGE_RB_201401":
            self.ts1 = data.last_price #获得第一个合约snapshot的价格
        if data.type == "Snapshot" and data.instrument.symbol == "XSGE_RB_201310":
            self.ts2 = data.last_price #获得第二个合约snapshot的价格
           # diff= self.ts1-self.ts2 - self.diffma #两个合约的snapshot价差减平衡价差
           # diff1= self.ts1 - self.ts2 #两个合约的shapshot价差
        time_tmp = self.get_current_time()
        time = chrono.time_to_datetime(time_tmp, timezone="Asia/Shanghai") #取得当前时间
        #开多仓（品种1多仓）逻辑：如果snapshot价差比平衡价差小10且没有开仓，则开仓做多价差,尾盘不开仓
        if (self.ts1 - self.ts2 < self.diffma-10 and self.openedleg1 == 0 and self.openedleg2 == 0 and self.order_num == 0 and not(time.hour == 14 and time.minute >= 55)):
            self.place_future_order("XSGE_RB_201401", 1, trade.MarketPrice(), trade.OPEN, trade.FOK)
            self.place_future_order("XSGE_RB_201310", -1, trade.MarketPrice(), trade.OPEN, trade.FOK)
        #清仓逻辑：如果snapshot价差比平衡价差小3且开多仓，则平仓
        if (self.ts1-self.ts2>self.diffma-3 and self.openedleg1 == 1 and self.openedleg2 == -1 and self.order_num == 0 and not(time.hour == 14 and time.minute >= 55)):
            self.place_future_order("XSGE_RB_201401", -1, trade.MarketPrice(), trade.COVER, trade.FOK)
            self.place_future_order("XSGE_RB_201310", 1, trade.MarketPrice(), trade.COVER,trade.FOK)
        #开空仓（品种1空仓）逻辑：如果snapshot价差比平衡价差小10且没有开仓，则开仓做空价差,尾盘不开仓
        if (self.ts1-self.ts2>self.diffma+10 and self.openedleg1 == 0 and self.openedleg2 == 0 and self.order_num == 0 and not(time.hour == 14 and time.minute >= 55)):
            self.place_future_order("XSGE_RB_201401", -1, trade.MarketPrice(), trade.OPEN, trade.FOK)
            self.place_future_order("XSGE_RB_201310", 1, trade.MarketPrice(), trade.OPEN, trade.FOK)
        #如果snapshot价差比平衡价差大3且开空仓，则平仓
        if (self.ts1 - self.ts2 < self.diffma + 3 and self.openedleg1 == -1 and self.openedleg2 == 1 and self.order_num == 0 and not(time.hour == 14 and time.minute >= 55)):
            self.place_future_order("XSGE_RB_201401", 1, trade.MarketPrice(), trade.COVER, trade.FOK)
            self.place_future_order("XSGE_RB_201310", -1, trade.MarketPrice(), trade.COVER, trade.FOK)
        #定期平仓
        if(time.hour==14 and time.minute>=55):
            if(self.openedleg1 != 0):
                self.place_future_order("XSGE_RB_201401", -1*self.openedleg1, trade.MarketPrice(), trade.COVER, trade.FOK)
            if(self.openedleg2 != 0):
                self.place_future_order("XSGE_RB_201310", -1*self.openedleg2, trade.MarketPrice(), trade.COVER, trade.FOK)
   
    def on_alarm(self):
        print "MyPlay::onAlarm"