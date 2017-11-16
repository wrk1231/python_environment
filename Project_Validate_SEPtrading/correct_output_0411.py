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
        self.end_date = chrono.Date(20150930) ## 在最后一天输出表格
        self.output_alarm = 0
        self.list = DataFrame(pd.read_csv("/workspace/user-files/Sh_list2.csv"))
        self.df = DataFrame(columns= ['date','history','order0','order1','order2','order3','order4','order5','bar0','bar1','bar2','bar3','bar4','bar5','t0','t1','t2','t3','t4','t5','t_out','Trade_date','date0','total_volumn','total_size','average_price','average_price_once','price0','price1','price2','price3','price4','price5','diff_0','diff_1','diff_2','diff_3','diff_4','diff_5'],index = self.list['name'])
        self.report = DataFrame(columns = ['report','order_record'], index = self.list['name'])
        ## 可以将异常数据和统计量统一打到这张DataFrame里面，然后取出这些行列打表
        ############初始化################################################
        for instr in self.list['name']:
            self.subscribe(instr,self.bartype1) #订阅1day K线 
            self.subscribe(instr,self.bartype2) #订阅1min K线    
            self.df['date'][instr] = []        ## 对应于该只股票的空列表，存档每只股票的交易日，因为不同股票可能不一样
            self.df['Trade_date'][instr] = []  ## 对应于该只股票的空列表，搜集SEP后的第五个交易日期，每一个列表中的交易日，我们将在下一个交易日交易
            self.df['history'][instr] = []     ## 对应于该只股票的空列表，存档每日收盘价
            self.df['date0'][instr] = self.default_date
            ## report 为记录输出结果的DataFrame，‘report'用来记录交易日的信息，’order_record'用来记录订单的详情。
            self.report['report'][instr] = {}
            self.report['report'][instr]['date'] = []     #记录交易日
            #self.report['report'][instr]['stock_id'] = []   #记录交易品种
            #self.report['report'][instr]['possible_error0'] = ['Correct']   #记录可能出现的错误:集合竞价与分次下单平均价格差别太大。
            #self.report['report'][instr]['possible_error1'] = ['Correct']   #记录可能出现的错误:bar线数据与实际成交数据差别太大。
            self.report['report'][instr]['diff_0'] = []  #记录集合竞价与分次成交的差值百分比
            self.report['report'][instr]['diff_1'] = []  #记录分次成交的价格和bar线返回数据的百分比
            self.report['report'][instr]['diff_2'] = []  #记录分次成交的价格和bar线返回数据的百分比
            self.report['report'][instr]['diff_3'] = []  #记录分次成交的价格和bar线返回数据的百分比
            self.report['report'][instr]['diff_4'] = []  #记录分次成交的价格和bar线返回数据的百分比
            self.report['report'][instr]['diff_5'] = []  #记录分次成交的价格和bar线返回数据的百分比
            
            self.report['order_record'][instr] = {}
            self.report['order_record'][instr]['datetime'] = [] #订单对应的交易日
            #self.report['report'][instr]['stock_id'] = []     #重复记录交易品种 其实可有可无
            self.report['order_record'][instr]['time0'] = []  #每天order0结束成交的时间
            self.report['order_record'][instr]['time1'] = []  #每天order1结束成交的时间
            self.report['order_record'][instr]['time2'] = []  #每天order2结束成交的时间
            self.report['order_record'][instr]['time3'] = []  #每天order3结束成交的时间
            self.report['order_record'][instr]['time4'] = []  #每天order4结束成交的时间
            self.report['order_record'][instr]['time5'] = []  #每天order5结束成交的时间
            
            self.report['order_record'][instr]['value_single'] = []    #集合竞价的总价值
            self.report['order_record'][instr]['size_single'] = []     #集合竞价的单子大小
            self.report['order_record'][instr]['auction_price'] = []  #集合竞价价格
            self.report['order_record'][instr]['value_all'] = []    #分次下单的总价值
            self.report['order_record'][instr]['size_all'] = []    #分次下单的总单量
            self.report['order_record'][instr]['average_price'] = [] #分次下单的均价
            
          #########################################################################  
    def on_data_update(self, data):
        for instr in self.list['name']:   

            if str(data.instrument) == instr:

                if data.type == "Bar_1day":
                   
                    cal = chrono.Calendar("ChinaStocks")
                    self.df['history'][instr]= np.append(self.df['history'][instr], data.close)
                    self.df['date'][instr]= np.append(self.df['date'][instr], data.date)

                    if (len(self.df['history'][instr])-10>0):
                        for i in range(max(4,len(self.df['history'][instr])-10),len(self.df['history'][instr])-5):
                            if(self.df['history'][instr][i] > max(self.df['history'][instr][i-4:i]) and self.df['history'][instr][i] > max(self.df['history'][instr][i+1:i+5]) and (self.df['date'][instr][i+5] not in self.df['Trade_date'][instr])):
                                ## 判断SEP条件
                                self.df['Trade_date'][instr].append(self.df['date'][instr][i+5])

                    if data.date in self.df['Trade_date'][instr]:
                      
                        self.df['date0'][instr] = data.date
                        self.df['t0'][instr] =  self.add_alarm(chrono.str_to_time(str(cal.add(self.df['date0'][instr], 1))+"01:25:00.000000"))
                        self.df['t1'][instr] =  self.add_alarm(chrono.str_to_time(str(cal.add(self.df['date0'][instr], 1))+"01:31:00.000000"))   
                        self.df['t2'][instr] =  self.add_alarm(chrono.str_to_time(str(cal.add(self.df['date0'][instr], 1))+"01:37:00.000000"))   
                        self.df['t3'][instr] =  self.add_alarm(chrono.str_to_time(str(cal.add(self.df['date0'][instr], 1))+"01:43:00.000000"))   
                        self.df['t4'][instr] =  self.add_alarm(chrono.str_to_time(str(cal.add(self.df['date0'][instr], 1))+"01:49:00.000000"))   
                        self.df['t5'][instr] =  self.add_alarm(chrono.str_to_time(str(cal.add(self.df['date0'][instr], 1))+"01:55:00.000000"))   
                        self.output_alarm =  self.add_alarm(chrono.str_to_time(str(self.end_date)+"01:55:00.000000"))
                        
                    if cal.add(data.date,-1) in self.df['Trade_date'][instr]:
                        ##记录交易日#####
                        self.report['report'][instr]['date'].append(str(data.date))
                        
                        #self.report['report'][instr]['stock_id'].append(instr)
                        ###$$$$$#######
                        
#                         print instr,"由SEP确定的交易日为：",data.date,"五次下单分时价格为:",self.df['bar1'][instr],self.df['bar2'][instr],self.df['bar3'][instr],self.df['bar4'][instr],self.df['bar5'][instr]
                        
                        
                        
#                         if abs((self.df['average_price'][instr] - self.df['average_price_once'][instr])/self.df['average_price_once'][instr]) >= 0.02:
#                             self.report['report'][instr]['possible_error0'].append('Error')
#                         #记录可能出现的错误:集合竞价与分次下单平均价格差别太大。
#                         else:
#                             self.report['report'][instr]['possible_error0'].append('Correct')
#                         if abs((self.df['bar1'][instr] - self.df['price1'][instr])/self.df['bar1'][instr]) + abs((self.df['bar2'][instr] - self.df['price2'][instr])/self.df['bar2'][instr]) + abs((self.df['bar3'][instr] - self.df['price3'][instr])/self.df['bar3'][instr]) + abs((self.df['bar4'][instr] - self.df['price4'][instr])/self.df['bar4'][instr]) + abs((self.df['bar5'][instr] - self.df['price5'][instr])/self.df['bar5'][instr]) >= 0.1:
#                          #记录可能出现的错误:bar线数据与实际成交数据差别太大。
#                             self.report['report'][instr]['possible_error1'].append('Error')
#                         else:
#                             self.report['report'][instr]['possible_error1'].append('Correct')
                        ######这几条diff好像没对齐数据格式？￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥
                        try:
                            self.df['diff_1'][instr] = abs((self.df['bar1'][instr] - self.df['price1'][instr])/self.df['bar1'][instr])
                            self.report['report'][instr]['diff_1'].append(self.df['diff_1'][instr])
                            
                        except:
                            self.report['report'][instr]['diff_1'].append(-1)
                            
                            
                        try:
                            self.df['diff_2'][instr] = abs((self.df['bar2'][instr] - self.df['price2'][instr])/self.df['bar2'][instr])
                            self.report['report'][instr]['diff_2'].append(self.df['diff_2'][instr])
                            
                        except:
                            self.report['report'][instr]['diff_2'].append(-1)
                            
                        
                        try:
                            self.df['diff_3'][instr] = abs((self.df['bar3'][instr] - self.df['price3'][instr])/self.df['bar3'][instr])
                            self.report['report'][instr]['diff_3'].append(self.df['diff_3'][instr])
                            
                        except:
                            self.report['report'][instr]['diff_3'].append(-1)
                            
                        
                        try:
                            self.df['diff_4'][instr] = abs((self.df['bar4'][instr] - self.df['price4'][instr])/self.df['bar4'][instr])
                            self.report['report'][instr]['diff_4'].append(self.df['diff_4'][instr])
                            
                        except:
                            self.report['report'][instr]['diff_4'].append(-1)
                            
                        
                        try:
                            self.df['diff_5'][instr] = abs((self.df['bar5'][instr] - self.df['price5'][instr])/self.df['bar5'][instr])
                            self.report['report'][instr]['diff_5'].append(self.df['diff_1'][instr])
                            
                        except:
                            self.report['report'][instr]['diff_5'].append(-1)
                            
                        
                        try:
                            self.df['diff_0'][instr] = abs((self.df['price1'][instr] + self.df['price2'][instr] + self.df['price3'][instr] + self.df['price4'][instr] + self.df['price5'][instr])/5 - self.df['price0'][instr])/self.df['price0'][instr]
                            
                                            
                            self.report['report'][instr]['diff_0'].append(self.df['diff_0'][instr])
                            
                        except:
                            self.report['report'][instr]['diff_0'].append(-1)
                            

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

                            
                            
                            

    def on_alarm(self,id):
        if id == self.output_alarm:
            print DataFrame(self.report['report'])
            self.report['report'].to_csv('/workspace/user-files/test_output0.csv',encoding="gbk")  
        for instr in self.list['name']: ##遍历股票池中的股票
           
            if id == self.df['t0'][instr] :
                self.df['order0'][instr] = self.place_stock_order(instr, 5 , trade.MarketPrice())
                self.df['total_volumn'][instr] = 0 
                self.df['total_size'][instr] = 0                                                                   
                ##   每到一个新的指定交易日，清零之前的累加（用来求新的交易均价）                                                
            if id == self.df['t1'][instr]:                                                                         
                self.df['order1'][instr] = self.place_stock_order(instr, 1 , trade.MarketPrice())                     
            if id == self.df['t2'][instr]:                                                                         
                self.df['order2'][instr] = self.place_stock_order(instr, 1 , trade.MarketPrice())                        
            if id == self.df['t3'][instr]:                                                                                                                       self.df['order3'][instr] = self.place_stock_order(instr, 1 , trade.MarketPrice())                   
            if id == self.df['t4'][instr]:                                                                               
                self.df['order4'][instr] = self.place_stock_order(instr, 1, trade.MarketPrice())                         
            if id == self.df['t5'][instr]:                                                                               
                self.df['order5'][instr] = self.place_stock_order(instr, 1, trade.MarketPrice())
        

                
                
                
                
                
                
    def on_order_update(self, order):                                                                                        
                                                                                                                             
        for instr in self.list['name']: ##遍历股票池中的股票  
            ####记录各单交易完成的时间、交易量、交易市值#######
            if order.id == self.df['order0'][instr] and order.state == OrderState.FINAL:
                self.report['order_record'][instr]['time0'].append(chrono.time_to_str(get_current_time()))
                self.report['order_record'][instr]['value_single'].append(order.filled_value) 
                self.report['order_record'][instr]['size_single'].append(order.filled_size)
      
                    
            if order.id == self.df['order0'][instr] and order.state == OrderState.FINAL:
                self.report['order_record'][instr]['time0'].append(chrono.time_to_str(get_current_time()))
                try:
                    self.df['price0'][instr] = order.filled_value/order.filled_size
                except:
                    self.df['price0'][instr]  = 0
                    
            if order.id == self.df['order1'][instr] and order.state == OrderState.FINAL:
                self.report['order_record'][instr]['time1'].append(chrono.time_to_str(get_current_time()))
                try:
                    self.df['price1'][instr] = order.filled_value/order.filled_size
                except:
                    self.df['price1'][instr]  = 0
                             
            if order.id == self.df['order2'][instr] and order.state == OrderState.FINAL:
                self.report['order_record'][instr]['time2'].append(chrono.time_to_str(get_current_time()))
                try:
                    self.df['price2'][instr] = order.filled_value/order.filled_size
                except:
                    self.df['price3'][instr]  = 0
                    
            if order.id == self.df['order3'][instr] and order.state == OrderState.FINAL:
                self.report['order_record'][instr]['time3'].append(chrono.time_to_str(get_current_time()))
                try:
                    self.df['price3'][instr] = order.filled_value/order.filled_size
                except:
                    self.df['price3'][instr]  = 0
                    
            if order.id == self.df['order4'][instr] and order.state == OrderState.FINAL:
                self.report['order_record'][instr]['time4'].append(chrono.time_to_str(get_current_time()))
                try:
                    self.df['price4'][instr] = order.filled_value/order.filled_size
                except:
                    self.df['price4'][instr]  = 0
                    
            if order.id == self.df['order5'][instr] and order.state == OrderState.FINAL:
                self.report['order_record'][instr]['time5'].append(chrono.time_to_str(get_current_time()))
                try:
                    self.df['price5'][instr] = order.filled_value/order.filled_size
                except:
                    self.df['price5'][instr]  = 0
                    
            ###############################
            
            if order.id == self.df['order0'][instr] and order.state == OrderState.FINAL:                                     
                ## 集合竞价                                                                                     
                try:
                    self.df['average_price_once'][instr] = order.filled_value / order.filled_size  
                except:
                    self.df['average_price_once'][instr] = -5  
                else:
                    self.report['order_record'][instr]['auction_price'].append(self.df['average_price_once'][instr])
                                                                                                                             
                                                                                                                             
            if order.id != self.df['order0'][instr] and order.state == OrderState.FINAL:                                     
                ## 累积加和分次下单的总价和下单总量                                                                                
                self.df['total_volumn'][instr] += order.filled_value 
                self.df['total_size'][instr]   += order.filled_size
                
            if order.id == self.df['order5'][instr] and order.state ==OrderState.FINAL:
                ## 最后一单交易完成之后，核算平均成交价格
                try:
                    self.df['average_price'][instr] = self.df['total_volumn'][instr] / self.df['total_size'][instr]
                   
                except:
                    self.df['average_price'][instr] = -1
                else:
                    self.report['order_record'][instr]['average_price'].append(self.df['average_price'][instr])
                    
                
            
           
        
















