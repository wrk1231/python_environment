# encoding: utf-8
import numpy as np
from quant import *
from quant import chrono

class MyPlay(trade.Model):
    def on_initialize(self):

        self.list = DataFrame(pd.read_csv("/workspace/user-files/Sh_list.csv"))
        
        self.bartype1 = "Bar_1day" #type1:订阅1day k线
        self.bartype2 = "Bar_1min" #type2:订阅1min k线

        for instr in self.list['name']:
            self.subscribe(instr,self.bartype1) #订阅1day K线 
            self.subscribe(instr,self.bartype2) #订阅1min K线    

          
        self.date = {}

        self.order0 = {} ##6个订单编号
        self.order1 = {}
        self.order2 = {}
        self.order3 = {}
        self.order4 = {}
        self.order5 = {}

        self.bar0 = {}##6个收集bartype收盘价的全局变量
        self.bar1 = {}
        self.bar2 = {}
        self.bar3 = {}
        self.bar4 = {}
        self.bar5 = {}
        
        self.Trade_date = {}  ##空字典，搜集SEP后的第五个交易日期，每一个列表中的交易日，我们将在下一个交易日交易
        self.history = {} # 存档历史数据  这个应该是bar类型

        self.t0 = {}    ##存档对应于某一只股票的交易闹钟
        self.t1 = {}
        self.t2 = {}
        self.t3 = {}
        self.t4 = {}
        self.t5 = {}


        self.default_date = chrono.Date(19700101)
        self.date0 = {} ##用来在timeline上更新 对于某一只股票来说，每一日是否是买入日


        self.total_volumn = {} ##用于计算每次分次下单的总交易额，在下一个交易日分次下单之前清零。
        self.total_size = {} ## 用于计算每次分次下单的总股数，在下一个交易日分次下单之前清零。
        self.average_price = {} ## 分次下单的平均价格
        self.average_price_once = {}  ## 集合竞价价格
        
        
        
    def on_data_update(self, data):
        for instr in self.list['name']: ##遍历股票池中的股票
            if str(data.instrument) == instr:##对于某只特定的股票：

                self.date[instr] = []        ## 字典中对应于该只股票的空列表，存档每只股票的交易日，因为不同股票可能不一样
                self.Trade_date[instr] = [] ##字典中对应于该只股票的空列表，搜集SEP后的第五个交易日期，每一个列表中的交易日，我们将在下一个交易日交易
                self.history[instr] = []    ## 字典中对应于该只股票的空列表， 存档每日收盘价

                ## 这几个变量都得用字典形式存储，防止数据跑窜了地方

                self.order0[instr]= 0 ##6个订单编号
                self.order1[instr]= 0
                self.order2[instr]= 0
                self.order3[instr]= 0
                self.order4[instr]= 0
                self.order5[instr]= 0 
                self.bar0[instr]= 0 ##6个收集bartype收盘价的全局变量
                self.bar1[instr] = 0
                self.bar2[instr] = 0
                self.bar3[instr] = 0
                self.bar4[instr] = 0
                self.bar5[instr] = 0
                self.date0[instr] = self.default_date



                if data.type == "Bar_1day":
                    #用日度交易数据来收集数据并确定SEP
                    #增加最新数据
                    self.history [instr]= np.append(self.history[instr], data.close)
                    self.date [instr]= np.append(self.date[instr], data.date)
                    
                    if (len(self.history[instr])-10>0):
                        for i in range(max(4,len(self.history[instr])-10),len(self.history[instr])-5):
                            if(self.history[instr][i] > max(self.history[instr][i-4:i]) and self.history[instr][i] > max(self.history[instr][i+1:i+5]) and (self.date[instr][i+5] not in self.Trade_date[instr])):
                                ## 判断SEP条件
                                self.Trade_date[instr].append(self.date[instr][i+5])
                                
                    if data.date in self.Trade_date[instr]: 
                    ## 如果某天是 该只股票的某个SEP日期的后五日：
                        cal = chrono.Calendar("ChinaStocks")
                        self.date0[instr] = data.date
                        print "由SEP确定的交易日为：",cal.add(data.date, 1)  ## SEP 之后第五个交易日被记录，其下一天为交易日期

                        ## 设定不同的闹钟进行买入交易
                        self.t0[instr] =  self.add_alarm(chrono.str_to_time(str(cal.add(data.date, 1))+"01:25:00.000000"))
                        self.t1[instr] =  self.add_alarm(chrono.str_to_time(str(cal.add(data.date, 1))+"01:31:00.000000"))
                        self.t2[instr] =  self.add_alarm(chrono.str_to_time(str(cal.add(data.date, 1))+"01:37:00.000000"))
                        self.t3[instr] =  self.add_alarm(chrono.str_to_time(str(cal.add(data.date, 1))+"01:43:00.000000"))
                        self.t4[instr] =  self.add_alarm(chrono.str_to_time(str(cal.add(data.date, 1))+"01:49:00.000000"))
                        self.t5[instr] =  self.add_alarm(chrono.str_to_time(str(cal.add(data.date, 1))+"01:55:00.000000"))
                    
                    cal = chrono.Calendar("ChinaStocks")

                    if cal.add(data.date,-1) in self.Trade_date[instr]: 
                        ## 如果某一天的前一天是  instr该只股票SEP之后第五个交易日被记录（已被记录在self.Trade_date[instr]),那么他这一天将是买入的日期
                        ## 在这里打印是为了对应 data.type=="Bar_1day",只需要每天打一次就行
                        print "五次下单分时价格为:",self.bar1[instr],self.bar2[instr],self.bar3[instr],self.bar4[instr],self.bar5[instr]

                if data.type == "Bar_1min":
                    cal = chrono.Calendar("ChinaStocks")
                    
                    if chrono.time_to_date(data.time) == cal.add(self.date0[instr], 1):
                        ## 对应某一只股票，改天1Min bar线对应的日期为交易日的话：
                    
                        if chrono.str_to_time(str(cal.add(self.date0[instr], 1))+"01:31:00.000000") == data.time:
                            self.bar1[instr] = data.close
                            
                        if chrono.str_to_time(str(cal.add(self.date0[instr], 1))+"01:37:00.000000") == data.time:
                            self.bar2[instr] = data.close
                                           
                        if chrono.str_to_time(str(cal.add(self.date0[instr], 1))+"01:43:00.000000") == data.time:
                            self.bar3[instr] = data.close
                                          
                        if chrono.str_to_time(str(cal.add(self.date0[instr], 1))+"01:49:00.000000") == data.time:
                            self.bar4[instr] = data.close
                                              
                        if chrono.str_to_time(str(cal.add(self.date0[instr], 1))+"01:55:00.000000") == data.time:
                            self.bar5[instr] = data.close
                             
            
    def on_alarm(self,id):
        for instr in self.list['name']: ##遍历股票池中的股票
           
            if id == self.t0[instr] :
                self.order0 = self.place_stock_order(instr, 5, trade.MarketPrice())
                
                self.total_volumn[instr] = 0 
                self.total_size[instr] = 0

                ##   每到一个新的指定交易日，清零之前的累加（用来求新的交易均价）
                
            if id == self.t1[instr]:
                self.order1 = self.place_stock_order(instr, 1, trade.MarketPrice())
                
            if id == self.t2[instr]:
                self.order2 = self.place_stock_order(instr, 1, trade.MarketPrice())
                            
            if id == self.t3[instr]:
                self.order3 = self.place_stock_order(instr, 1, trade.MarketPrice())
                
            if id == self.t4[instr]:
                self.order4 = self.place_stock_order(self.myinstr, 1, trade.MarketPrice())
                
            if id == self.t5[instr]:
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
            

           
        


















