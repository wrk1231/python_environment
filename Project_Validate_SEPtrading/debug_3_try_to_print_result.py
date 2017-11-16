# encoding: utf-8
import numpy as np
from quant import *
from quant import chrono
import pandas as pd 
from pandas import *
from pandas import DataFrame
from pandas import Series

class MyPlay(trade.Model):
    def on_initialize(self):

        self.bartype1 = "Bar_1day" #type1:订阅1day k线
        self.bartype2 = "Bar_1min" #type2:订阅1min k线
        self.default_date = chrono.Date(19700101)

        self.list = DataFrame(pd.read_csv("/workspace/user-files/Sh_list.csv"))
        self.df = DataFrame(columns= ['date','history','order0','order1','order2','order3','order4','order5','bar0','bar1','bar2','bar3','bar4','bar5','t0','t1','t2','t3','t4','t5','Trade_date','date0','total_volumn','total_size','average_price','average_price_once'],index = self.list['name'])
        ## 可以将异常数据和统计量统一打到这张DataFrame里面，然后取出这些行列打表
        #
        #结果输出可以用pd.concat([])去写
        self.report = DataFrame(columns = ['report'], index = self.list['name'])
        
        for instr in self.list['name']:
            self.subscribe(instr,self.bartype1) #订阅1day K线 
            self.subscribe(instr,self.bartype2) #订阅1min K线    
            self.df['date'][instr] = []        ## 对应于该只股票的空列表，存档每只股票的交易日，因为不同股票可能不一样
            self.df['Trade_date'][instr] = []  ## 对应于该只股票的空列表，搜集SEP后的第五个交易日期，每一个列表中的交易日，我们将在下一个交易日交易
            self.df['history'][instr] = []     ## 对应于该只股票的空列表，存档每日收盘价
            self.df['date0'][instr] = self.default_date
            # self.report['report'][instr] = {}

    def on_data_update(self, data):
        for instr in self.list['name']:   

            if str(data.instrument) == instr:
                if data.type == "Bar_1day":

                    self.df['history'][instr]= np.append(self.df['history'][instr], data.close)
                    self.df['date'][instr]= np.append(self.df['date'][instr], data.date)

                    if (len(self.df['history'][instr])-10>0):
                        for i in range(max(4,len(self.df['history'][instr])-10),len(self.df['history'][instr])-5):
                            if(self.df['history'][instr][i] > max(self.df['history'][instr][i-4:i]) and self.df['history'][instr][i] > max(self.df['history'][instr][i+1:i+5]) and (self.df['date'][instr][i+5] not in self.df['Trade_date'][instr])):
                                ## 判断SEP条件
                                self.df['Trade_date'][instr].append(self.df['date'][instr][i+5])

                    if data.date in self.df['Trade_date'][instr]: ##########################################################################################
                    ## 如果某天是 该只股票的某个SEP日期的后五日：                                                                                                 #
                        cal = chrono.Calendar("ChinaStocks")                                                                                               # 
                        self.df['date0'][instr] = data.date
                        # self.report['report'][instr]['date'] = self.df['date0'][instr]
                        # self.report['report'][instr]['name'] = str(instr)                                                                                                #
                        #print instr,"由SEP确定的交易日为：",cal.add(self.df['date0'][instr], 1)  ## SEP 之后第五个交易日被记录，其下一天为交易日期                    #    
                                                                                                                                                           #
                        self.df['t0'][instr] =  self.add_alarm(chrono.str_to_time(str(cal.add(self.df['date0'][instr], 1))+"01:25:00.000000"))             #
                        self.df['t1'][instr] =  self.add_alarm(chrono.str_to_time(str(cal.add(self.df['date0'][instr], 1))+"01:31:00.000000"))             #
                        self.df['t2'][instr] =  self.add_alarm(chrono.str_to_time(str(cal.add(self.df['date0'][instr], 1))+"01:37:00.000000"))             #
                        self.df['t3'][instr] =  self.add_alarm(chrono.str_to_time(str(cal.add(self.df['date0'][instr], 1))+"01:43:00.000000"))             #
                        self.df['t4'][instr] =  self.add_alarm(chrono.str_to_time(str(cal.add(self.df['date0'][instr], 1))+"01:49:00.000000"))             #
                        self.df['t5'][instr] =  self.add_alarm(chrono.str_to_time(str(cal.add(self.df['date0'][instr], 1))+"01:55:00.000000"))             #
                                                                                                                                                           #
                    cal = chrono.Calendar("ChinaStocks")                                                                                                   #
                                                                                                                                                           #             
                    if cal.add(data.date,-1) in self.df['Trade_date'][instr]: #############################################################################
                        ## 如果某一天的前一天是  instr该只股票SEP之后第五个交易日被记录（已被记录在self.Trade_date[instr]),那么他这一天将是买入的日期
                        ## 在这里打印是为了对应 data.type=="Bar_1day",只需要每天打一次就行
                        print instr,"由SEP确定的交易日为：",data.date,"五次下单分时价格为:",self.df['bar1'][instr],self.df['bar2'][instr],self.df['bar3'][instr],self.df['bar4'][instr],self.df['bar5'][instr]
                        
                        if abs((self.df['average_price'][instr] - self.df['average_price_once'][instr])/self.df['average_price_once'][instr]) >= 0.01:
                            print "##############日期：",data.date, "代码：",instr, "集合竞价：", self.df['average_price_once'][instr],"分次均价：",self.df['average_price'][instr],"#################"
                

                if data.type == "Bar_1min":

                    cal = chrono.Calendar("ChinaStocks")
                    
                    if chrono.time_to_date(data.time) == cal.add(self.df['date0'][instr], 1):
                        ## 对应某一只股票，该天1Min bar线对应的日期为交易日的话：
                    
                        if chrono.str_to_time(str(cal.add(self.df['date0'][instr], 1))+"01:31:00.000000") == data.time:
                            self.df['bar1'][instr] = data.close
                            
                        if chrono.str_to_time(str(cal.add(self.df['date0'][instr], 1))+"01:37:00.000000") == data.time:
                            self.df['bar2'][instr] = data.close
                                           
                        if chrono.str_to_time(str(cal.add(self.df['date0'][instr], 1))+"01:43:00.000000") == data.time:
                            self.df['bar3'][instr] = data.close
                                          
                        if chrono.str_to_time(str(cal.add(self.df['date0'][instr], 1))+"01:49:00.000000") == data.time:
                            self.df['bar4'][instr] = data.close
                                              
                        if chrono.str_to_time(str(cal.add(self.df['date0'][instr], 1))+"01:55:00.000000") == data.time:
                            self.df['bar5'][instr] = data.close



######next step##########
    def on_alarm(self,id):
         for instr in self.list['name']: ##遍历股票池中的股票
           
            if id == self.df['t0'][instr] :
                self.df['order0'][instr] = self.place_stock_order(instr, 5 , trade.MarketPrice())
                self.df['total_volumn'][instr] = 0 ###########################################################################
                self.df['total_size'][instr] = 0                                                                             #
                                                                                                                             #
                ##   每到一个新的指定交易日，清零之前的累加（用来求新的交易均价）                                                       #
                                                                                                                             #
            if id == self.df['t1'][instr]:                                                                                   #
                self.df['order1'][instr] = self.place_stock_order(instr, 1 , trade.MarketPrice())                            #        
                                                                                                                             #
            if id == self.df['t2'][instr]:                                                                                   #
                self.df['order2'][instr] = self.place_stock_order(instr, 1 , trade.MarketPrice())                            #
                                                                                                                             #
            if id == self.df['t3'][instr]:                                                                                   #
                self.df['order3'][instr] = self.place_stock_order(instr, 1 , trade.MarketPrice())                            #
                                                                                                                             #
            if id == self.df['t4'][instr]:                                                                                   #
                self.df['order4'][instr] = self.place_stock_order(instr, 1, trade.MarketPrice())                             #
                                                                                                                             #
            if id == self.df['t5'][instr]:                                                                                   #
                self.df['order5'][instr] = self.place_stock_order(instr, 1, trade.MarketPrice())                             #
                                                                                                                             #
                                                                                                                             #
#########ALL CORRECT ABOVE####                                                                                               #
    def on_order_update(self, order):                                                                                        #
                                                                                                                             #
         for instr in self.list['name']: ##遍历股票池中的股票                                                                   #
                                                                                                                             #
            if order.id == self.df['order0'][instr] and order.state == OrderState.FINAL:                                     #
                ## 集合竞价得到购入价格                                                                                          #
                try:
                    self.df['average_price_once'][instr] = order.filled_value / order.filled_size  
                except:
                    self.df['average_price_once'][instr] = -1                                                                #

                                                                                                                             #
            if order.id != self.df['order0'][instr] and order.state == OrderState.FINAL:                                     #
                ## 累积加和分次下单的总价和下单总量                                                                                #
                self.df['total_volumn'][instr] += order.filled_value #########################################################
                self.df['total_size'][instr]   += order.filled_size
                
            if order.id == self.df['order5'][instr] and order.state ==OrderState.FINAL:
                ## 最后一单交易完成之后，核算平均成交价格
                try:
                    self.df['average_price'][instr] = self.df['total_volumn'][instr] / self.df['total_size'][instr]
                except:
                    self.df['average_price'][instr] = -1

















