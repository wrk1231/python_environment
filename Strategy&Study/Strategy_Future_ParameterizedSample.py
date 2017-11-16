# encoding: utf-8
import numpy as np
from quant import *
import json
import tushare

class MyPlay(trade.Model):
    
    @staticmethod
    #该函数定义参数化参数列表
    def getpara_json():
        parameters = [{
            'longma': 20,
            'shortma': 5,
            'Instr':"XSGE_RB_201510"
        }]
        return json.dumps(parameters); #返回字符串
    @classmethod
    #该函数将获得的参数传给变量self.json_para_str
    def setPara(self,str):
        self.json_para_str=str


    #开始初始化
    def on_initialize(self):
        #load参数
        paras= json.loads(self.json_para_str)
        self.subscribe(str(paras['Instr']), "Bar_5min") #订阅5分钟k线

        self.opened = 0 #仓位标识
        self.short = int(paras['shortma']) #短期均线参数
        self.long = int(paras['longma'])  #长期均线参数
        self.history = np.zeros(self.long) #存历史数据
        self.shortma = 0
        self.longma = 0
        self.order_num = 0 #下单标识

    def on_order_update(self, order):
        #标识order状态，如果订单已经发出，记录一下，避免重复下单
        if order.state ==trade.SENT:
             self.order_num = 1
        if order.state == trade.FINAL:
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
        if(data.type == 'Bar_5min'):
            time_stamp = chrono.time_to_datetime(self.get_current_time(), timezone="Asia/Shanghai")
            self.history = np.append(self.history,data.close)
            self.history = np.delete(self.history,0)
        #print time_stamp,time_stamp.minute,time_stamp.hour
        

        #计算均线
            if self.history[0] != 0:
                self.shortma = np.mean(self.history[(self.long - self.short):])
                self.longma = np.mean(self.history)
#             print self.opened, self.order_num
        #短期均线大于长期均线，平空，开多；反之，平多，开空
            if(self.shortma > self.longma and self.opened == 0 and self.order_num == 0 and not(time_stamp.hour ==15  or (time_stamp.hour >=14 and time_stamp.minute >=54))):
                self.place_future_order(data.instrument.symbol,10,trade.MarketPrice(),trade.OPEN)
            elif(self.shortma < self.longma and self.opened == 1 and self.order_num == 0 or (time_stamp.hour <15 and time_stamp.hour >=14 and time_stamp.minute >=54)):
                self.place_future_order(data.instrument.symbol,-10,trade.MarketPrice(),trade.COVER)
            elif(self.shortma < self.longma and self.opened == 0 and self.order_num == 0 and not(time_stamp.hour ==15 or (time_stamp.hour >=14 and time_stamp.minute >=54))):
                self.place_future_order(data.instrument.symbol,-10,trade.MarketPrice(),trade.OPEN)######
            elif(self.shortma > self.longma and self.opened == -1 and self.order_num == 0 or (time_stamp.hour <15 and time_stamp.hour >=14 and time_stamp.minute >=54)):
                self.place_future_order(data.instrument.symbol,10,trade.MarketPrice(),trade.COVER)


