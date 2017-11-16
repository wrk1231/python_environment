# encoding: utf-8
import numpy as np
from quant import *
import math

class MyPlay(trade.Model):
    
    #开始初始化
    def on_initialize(self):

        self.truedata = data #由于在第一次运行的时候需要获取历史数据，一种方法是放在on_initialize()里面处理，但存在现实情况是，初始化的时间未必是数据更新的时间。因此这里将初始化的时候的 data 对象，赋给一个自定义的变量，从而在 on_dataupdate() 里面使用；特别的，这里又要吐槽一下，两个不同生命周期和范围的变量都叫 data，确实容易让人搞不清楚
        
        self.myinstr = "XSHE_000513"
        self.bartype = "Bar_1day"
        self.subscribe(self.myinstr, self.bartype)
        
        self.backrange = 55
        self.hist0 = [] #用来记录每天更新的收盘价，方便将收益率还原为真实股价
        self.hist1 = [] #用来记录每天更新的对数收益率
        self.s_0 = []
        self.miu = [] #用来记录 hist1 的历史数据的均值
        self.delta = [] #用来记录 hist1 的历史数据的方差
        self.s_t = [] #根据 s0 时刻计算出来的 st 时刻的预期对数收益率
        self.s_var = [] #st 时刻的对数收益率的波动率（对数收益率的方差）
        self.expect_price = [] #将 s_t 进行数据还原后得到的预期真实股价的位置
        self.expect_std = [] #
        self.bullline = [] #本程序默认将一个标准差的位置作为牛熊线的取值点
        self.bearline = []
        
        #下单用变量
        self.is_open = False #if 下单只能进行状态判断，但对历史是否下单没有记录，因此做一个是否已经下单的开关
        self.barunit = 100*10 #10手
        
        #研究平台用变量
        self.signalbuy = [] #回测页面没办法看到这里定义的变量的数值，也没有办法在回测页面画图，所以只好做变量收集，把时间对应的买卖点信号记录下来，在研究平台中和股价以及 bullline，bearline 一起画出来
        self.signalsell = []
        
        #参数优化用变量
        self.adj = 1 #用于参数优化，调整范围在 1.0 到 2.0
        
        self.is_first_run = True

    def on_data_update(self, data):
        if self.is_first_run:
            tmptime = self.get_current_time()
            starttime = tmptime-self.backrange*2*24*60*60*1000000 #吐槽一下平台处理时间还是很不方便，如果我要取过去某个时间段的数据做处理，只能有 start到 end 的区间，但是无法 count 一个交易日往前回溯；所以这里取2倍的 backrange，然后再进行数组切片把数据取出来
            endtime = tmptime-24*60*60*1000000
            hist0 = self.truedata.MarketData(self.myinstr, "Bar_1day", starttime, endtime).close #backrange 为对数收益率的天数，因此获取的原始股价数据数量为 backrange+1
            hist0 = hist0[len(hist0)-self.backrange-1:] #因为要取对数收益率，因此再往前一天；前面说过，如果能够有交易日历功能这步是没有必要的
            for i in range(self.backrange-1): 
                list.append(self.hist1, np.log((self.hist0[i+1]/self.hist0[i])))
            list.append(self.s_0, self.hist1[-1])
            list.append(self.miu, np.mean(self.hist1))
            list.append(self.delta, np.var(self.hist1))
            list.append(self.s_t, self.s_0*math.exp(self.miu[-1]))
            list.append(self.s_var, math.pow(self.s_0[-1], 2)*math.exp(2*self.miu[-1])*(math.exp(self.delta[-1])-1))
            list.append(self.expect_price, self.s_0+self. hist0[-1])
            list.append(self.expect_std, math.sqrt(math.exp(self.s_var[-1])*self.hist0[-1])) #注意在之前的计算的时候都是使用房产，这里化归到标准差
            list.append(self.bullline, self.expect_price+self.expect_std)
            list.append(self.bearline, self.expect_price-self.expect_std)            
                                  
            self.is_first_run = False
            
        #if not first_run
        list.append(hist0, data.close)
        list.append(hist1, np.log(hist0[-1]/hist0[-2]))
        hist1.pop(0) #特别注意 his1 这个数组作为一个滑动窗口需要随时删除队首的数据
        list.append(self.s_0, hist1[-1])
        list.append(self.miu, np.mean(hist1))
        list.append(self.delta, np.var(hist1))
        list.append(self.s_t, self.s_0[-1]*math.exp(self.miu[-1]))
        list.append(self.s_var, math.pow(self.s_0[-1], 2)*math.exp(2*self.miu[-1])*(math.exp(self.delta[-1])-1))
        list.append(self.expect_price, self.s_0+self. hist0[-1])
        list.append(self.expect_std, math.sqrt(math.exp(self.s_var[-1])*self.hist0[-1]))
        list.append(self.bullline, self.expect_price+self.expect_std*self.adj) #这里默认使用一个标准差的距离作为牛熊线的位置，之后需要根据回测结果进行优化，这里可以使用到平台的参数优化功能
        list.append(self.bearline, self.expect_price-self.expect_std*self.adj)          
        
        #要开始下单了，现在平台上的尾盘下单时默认将下单移到第二天开盘集合成交以后进行挂盘的
        if(data.close>self.bullline[-1] and self.is_open == False):
            self.place_stock_order(self.myinstr, self.buyunit, MarketPrice(5))
            list.append(self.signalbuy, chrono.time_to_date(data.time)) #因为最终打印在坐标上，不需要 UTC 时间，转换为日期即可，实际上当 bartype 为 Bar_1day 的情况下，可以取到 data.date 直接就是日期就不用转换了
            self.is_open = True #原则上，这个 is_open 应该要根据真正的成交来进行确认，具体做法就是在 on_orderupdate() 里面增加对订单是否 filled 进行判断，如果发现状态是 unfilled，那么最终要将这个 flag 置为 False；不过这种处理方式如果在多只股票的情况下就会有非常复杂的写法；所以建议或许能够增加类似于 callback 的功能，除非 order 获取到了实际的回报，否则这个线程会挂起
                    
        if(data.close<self.bullline[-1] and self.is_open == True):
            self.place_stock_order(self.myinstr, -self.buyunit)
            list.append(self.signalsell, chrono.time_to_date(data.time))
            self.is_open = False                