# encoding: utf-8
import numpy as np
from quant import *
from quant import chrono

class MyPlay(trade.Model):
    def on_initialize(self):
        self.list = DataFrame(pd.read_csv("/workspace/user-files/realstate.csv"))
        self.myinstr = "XSHE_000513"
        self.bartype1 = "Bar_1day" #type1:订阅1day k线
        self.bartype2 = "Bar_1min" #type2:订阅1min k线
        self.subscribe(self.myinstr,self.bartype1) #订阅1day K线 of 白云机场
        self.subscribe(self.myinstr,self.bartype2)      
        self.date = []
        self.order0 = 0 ##6个订单编号
        self.order1 = 0
        self.order2 = 0
        self.order3 = 0
        self.order4 = 0
        self.order5 = 0
        self.bar0 = 0 ##6个收集bartype收盘价的全局变量
        self.bar1 = 0
        self.bar2 = 0
        self.bar3 = 0
        self.bar4 = 0
        self.bar5 = 0
        self.default_date = chrono.Date(19700101)
        self.date0 = self.default_date
        self.total_volumn = 0 ##用于计算每次分次下单的总交易额，在下一个交易日分次下单之前清零。
        self.total_size = 0 ## 用于计算每次分次下单的总股数，在下一个交易日分次下单之前清零。
        self.average_price = 0 ## 分次下单的平均价格
        self.average_price_once = 0  ## 集合竞价的平均撮合价格
        self.Trade_date = []  ##空列表，搜集SEP后的第五个交易日期，每一个列表中的交易日，我们将在下一个交易日交易
        self.history = [] # 存档历史数据  这个应该是bar类型
        
        
    def on_data_update(self, data):
        if data.type == "Bar_1day":
            #用日度交易数据来收集数据并确定SEP
            #增加最新数据
            self.history = np.append(self.history, data.close)
            self.date = np.append(self.date, data.date)
            
            if (len(self.history)-10>0):
                for i in range(max(4,len(self.history)-10),len(self.history)-5):
                    if(self.history[i] > max(self.history[i-4:i]) and self.history[i] > max(self.history[i+1:i+5]) and (self.date[i+5] not in self.Trade_date)):
                        ## 判断SEP条件
                        self.Trade_date.append(self.date[i+5])
                        
            if data.date in self.Trade_date:
                cal = chrono.Calendar("ChinaStocks")
                self.date0 = data.date
                print "由SEP确定的交易日为：",cal.add(data.date, 1)  ## SEP 之后第五个交易日被记录，其下一天为交易日期

                 # 集合竞价 9：25
                self.t0 =  self.add_alarm(chrono.str_to_time(str(cal.add(self.date0, 1))+"01:25:00.000000"))
                self.t1 =  self.add_alarm(chrono.str_to_time(str(cal.add(self.date0, 1))+"01:31:00.000000"))
                self.t2 =  self.add_alarm(chrono.str_to_time(str(cal.add(self.date0, 1))+"01:37:00.000000"))
                self.t3 =  self.add_alarm(chrono.str_to_time(str(cal.add(self.date0, 1))+"01:43:00.000000"))
                self.t4 =  self.add_alarm(chrono.str_to_time(str(cal.add(self.date0, 1))+"01:49:00.000000"))
                self.t5 =  self.add_alarm(chrono.str_to_time(str(cal.add(self.date0, 1))+"01:55:00.000000"))
            
            cal = chrono.Calendar("ChinaStocks")
            if cal.add(data.date,-1) in self.Trade_date:   
                print "五次下单分时价格为:",self.bar1,self.bar2,self.bar3,self.bar4,self.bar5

        if data.type == "Bar_1min":
            cal = chrono.Calendar("ChinaStocks")
            
            if chrono.time_to_date(data.time) == cal.add(self.date0, 1):
                if chrono.str_to_time(str(cal.add(self.date0, 1))+"01:31:00.000000") == data.time:
                    self.bar1 = data.close
                    
                if chrono.str_to_time(str(cal.add(self.date0, 1))+"01:37:00.000000") == data.time:
                    self.bar2 = data.close
                                   
                if chrono.str_to_time(str(cal.add(self.date0, 1))+"01:43:00.000000") == data.time:
                    self.bar3 = data.close
                                  
                if chrono.str_to_time(str(cal.add(self.date0, 1))+"01:49:00.000000") == data.time:
                    self.bar4 = data.close
                                      
                if chrono.str_to_time(str(cal.add(self.date0, 1))+"01:55:00.000000") == data.time:
                    self.bar5 = data.close
                     
            
    def on_alarm(self,id):
        
        if id == self.t0 :
            self.order0 = self.place_stock_order(self.myinstr, 5, trade.MarketPrice())
            self.total_volumn = 0 
            self.total_size = 0 
            ##   每到一个新的指定交易日，清零之前的累加（用来求新的交易均价）
            
        if id == self.t1:
            self.order1 = self.place_stock_order(self.myinstr, 1, trade.MarketPrice())
            
        if id == self.t2:
            self.order2 = self.place_stock_order(self.myinstr, 1, trade.MarketPrice())
                        
        if id == self.t3:
            self.order3 = self.place_stock_order(self.myinstr, 1, trade.MarketPrice())
            
        if id == self.t4:
            self.order4 = self.place_stock_order(self.myinstr, 1, trade.MarketPrice())
            
        if id == self.t5:
            self.order5 = self.place_stock_order(self.myinstr, 1, trade.MarketPrice())
               


    def on_order_update(self, order):

        
        if order.id == self.order0 and order.state == OrderState.FINAL:
            ## 集合竞价得到的平均购入价格
            self.average_price_once = order.filled_value / order.filled_size
            
        
        if order.id != self.order0 and order.state == OrderState.FINAL:
            ## 累积加和分次下单的总价和下单总量
            self.total_volumn += order.filled_value
            self.total_size += order.filled_size
            
        if order.id == self.order5 and order.state ==OrderState.FINAL:
            ## 最后一单交易完成之后，核算平均成交价格
            self.average_price = self.total_volumn / self.total_size
            print "分次下单总交易量:",self.total_volumn,"分次下单总股数:",self.total_size,"分次下单均价：",self.average_price,"集合竞价均价:",self.average_price_once
            

           
        


















