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
        self.list = DataFrame(pd.read_csv("/workspace/user-files/Sh_list3.csv"))
        self.df = DataFrame(columns= ['date','history','order0','order1','order2','order3','order4','order5','bar0','bar1','bar2','bar3','bar4','bar5','t0','t1','t2','t3','t4','t5','Trade_date','date0','total_volumn','total_size','average_price','average_price_once'],index = self.list['name'])
        
        self.report = DataFrame(columns = ['report','order_record'], index = self.list['name'])
        
        for instr in self.list['name']:
            self.subscribe(instr,self.bartype1) #订阅1day K线 
            self.subscribe(instr,self.bartype2) #订阅1min K线    
            self.df['date'][instr] = []        ## 对应于该只股票的空列表，存档每只股票的交易日，因为不同股票可能不一样
            self.df['Trade_date'][instr] = []  ## 对应于该只股票的空列表，搜集SEP后的第五个交易日期，每一个列表中的交易日，我们将在下一个交易日交易
            self.df['history'][instr] = []     ## 对应于该只股票的空列表，存档每日收盘价
            
            self.report['report'][instr] = {}
            self.report['report'][instr]['date'] = []
            self.report['report'][instr]['stock_id'] = []
            self.report['report'][instr]['price'] = [0]
            self.report['report'][instr]['history'] = []
            self.report['report'][instr]['value'] = [0]
            self.report['report'][instr]['size'] = [0]
            self.report['report'][instr]['states'] = []
            self.report['report'][instr]['order_time'] = []
            self.report['report'][instr]['end_time'] = []
            self.report['order_record'][instr] = {}
            self.report['order_record'][instr]['datetime'] = []
            self.report['order_record'][instr]['time'] = []
            self.report['order_record'][instr]['value'] = []    
            self.report['order_record'][instr]['size'] = []
            
    
              
    def on_data_update(self, data):
        for instr in self.list['name']:
            if str(data.instrument) == instr:
                if data.type == 'Bar_1day':
                    self.report['report'][instr]['end_time'].append(chrono.time_to_str(get_current_time()))
                    cal = chrono.Calendar("ChinaStocks")
                    self.df['history'][instr] = np.append(self.df['history'][instr], data.close)
                    self.df['date'][instr] = np.append(self.df['date'][instr], data.date)
                    
                    print 'Today is:',data.date,'Stock id: ',instr
                    
                    
                    self.report['report'][instr]['date'].append(cal.add(data.date, 1))
                    self.report['report'][instr]['stock_id'].append(str(instr))
                    self.report['report'][instr]['history'].append(data.close)
                    
                    
                    print "日期记录:",self.report['report'][instr]['date'],'\n',"交易价记录:",self.report['report'][instr]['price'],'\n',"每日收盘价记录:",self.report['report'][instr]['history'],'\n','value:',self.report['report'][instr]['value'],'size:',self.report['report'][instr]['size'],'order id: ', self.report['report'][instr]['states'],'\n',"订单时间：",self.report['report'][instr]['order_time'],'\n','data返回终止时间：',self.report['report'][instr]['end_time'],'\n'
                    self.df['t0'][instr] = self.add_alarm(chrono.str_to_time(str(cal.add(data.date, 1))+"01:55:00.000000"))
                    self.df['t1'][instr] = self.add_alarm(chrono.str_to_time(str(cal.add(data.date, 1))+"06:55:00.000000"))

	        
           
    def on_alarm(self,id):
        for instr in self.list['name']:
            if id == self.df['t0'][instr]:
                    self.df['order0'][instr] = self.place_stock_order(instr, 1 , trade.MarketPrice())
           
                    
    def on_order_update(self, order):
    	for instr in self.list['name']:
            if order.id == self.df['order0'][instr] and order.state == OrderState.FINAL:
                
                self.report['order_record'][instr]['datetime'].append(chrono.time_to_date(get_current_time()))
                self.report['order_record'][instr]['time'].append(chrono.time_to_str(get_current_time()))
                self.report['order_record'][instr]['value'].append(order.filled_value)
                self.report['order_record'][instr]['size'].append(order.filled_size)
                
                self.report['report'][instr]['order_time'].append(chrono.time_to_str(get_current_time()))
                self.report['report'][instr]['value'].append(order.filled_value)
                self.report['report'][instr]['size'].append(order.filled_size)
                self.report['report'][instr]['states'].append(order.id)
                
                try:
                    self.df['average_price'][instr] = order.filled_value / order.filled_size
                except:
                    self.df['average_price'][instr] = -1
                    self.report['report'][instr]['price'].append(self.df['average_price'][instr])
                else:
                    self.report['report'][instr]['price'].append(self.df['average_price'][instr])
                   
      





