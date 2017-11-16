# -*- coding: utf-8 -*-
"""
Created on Fri Sep 04 17:44:34 2015
revised 2016 for python 3
@author: he math
"""

from lxml.html import parse
from urllib.request import urlopen
from os.path import getsize
import pandas as pd
import urllib 


def get_sina_high(stockid,start,end):
    #stockid with pre sh or sz
    data=pd.DataFrame()
    daterange=pd.date_range(start,end,freq="B")
    for cq in daterange:
        url='http://market.finance.sina.com.cn/downxls.php?date='+str(cq.date())+'&symbol='+stockid
        urllib.urlretrieve(url, "temp.txt")    
        # if no data, temp.txt just contains few words        
        if getsize("temp.txt")<100:
            continue
        HighF=pd.read_table("temp.txt",na_values="--",encoding="gbk",index_col=0,parse_dates=True)
        HighF=HighF.ix[range(len(HighF)-1,-1,-1)]
        delta=cq.date()-HighF.index.date[0]
        HighF.index=HighF.index+delta
        data=pd.concat([data,HighF])
    return data
 

def get_sina_stock(stockid,start="1990-12-19",end=pd.datetime.now(),isstock=True,fuquan=True):    
    def _unpack(row, kind='td'):
        elts = row.findall('.//%s' % kind)
        return [val.text_content().strip() for val in elts] # .strip()去掉\r\t\n之类的字符    
    def parse_options_data(table,isstock,fuquan):
        rows = table.findall('.//tr')
        data = [_unpack(r) for r in rows[2:]]
        if isstock & fuquan:
            colnames = ['date','open','high','close','low','vol','amount','ratio'] # 回避中文处理
        else:
            colnames = ['date','open','high','close','low','vol','amount']
        data= pd.DataFrame(data,columns=colnames)
        data.index=pd.to_datetime(data["date"])
        data=data.drop("date",axis=1)
        data=data.ix[range(len(data)-1,-1,-1)]
        return  data
    data=pd.DataFrame()
    daterange=pd.date_range(start,end,freq="Q")
    daterange=daterange.insert(len(daterange),daterange[-1]+1)
    stockid=str(stockid).zfill(6)
    for cq in daterange: 
        if isstock:
            if fuquan:
                url='http://vip.stock.finance.sina.com.cn/corp/go.php/vMS_FuQuanMarketHistory/stockid/'+str(stockid)+'.phtml?year='+str(cq.year)+'&jidu='+str(cq.month/3)
            else:
                url='http://vip.stock.finance.sina.com.cn/corp/go.php/vMS_MarketHistory/stockid/'+str(stockid)+'.phtml?year='+str(cq.year)+'&jidu='+str(cq.month/3)            
        else:            
            url='http://vip.stock.finance.sina.com.cn/corp/go.php/vMS_MarketHistory/stockid/'+str(stockid)+'/type/S.phtml?year='+str(cq.year)+'&jidu='+str(cq.month/3)
        try:
            parsed = parse(url)
        except:
            print("download failed for year=" +str(cq.year)+',  jidu='+str(cq.month/3))
            continue
        doc = parsed.getroot()
        tables=doc.findall('.//table')     
        da= tables[-1] # last table 19 for fuquan data and 4 for index
        datatem = parse_options_data(da,isstock,fuquan)
        data=pd.concat([data,datatem])
    return pd.DataFrame(data[start:end],dtype=float)    
#data1=get_sina_stock(601899,"1990-1-1","2015-8-15")
#data2=get_sina_stock("000001","1990-1-1","2015-8-15",isstock=False)

def get_sina_fin(stockid,year):
    def _unpack(row,kind='td'):
        elts = row.findall('.//%s' % kind)
        return [val.text_content().strip() for val in elts] # .strip()去掉\r\t\n之类的字符    
    def parse_options_data(table):
        rows = table.findall('.//tr')
        data = [_unpack(r) for r in rows[1:]]    
        data= pd.DataFrame(data)
        
        datacol=pd.to_datetime(data.ix[0][1:])
        dataindex=data[0][1:]        
        data=data.drop(0,axis=1)
        data=data.ix[1:]
        data.index=dataindex
        data.columns=datacol
        return  data

    url="http://money.finance.sina.com.cn/corp/go.php/vFD_ProfitStatement/stockid/"+str(stockid)+"/ctrl/"+str(year)+"/displaytype/4.phtml"
    
    parsed = parse(url)
    doc = parsed.getroot()
    tables=doc.findall('.//table')
    da= tables[-2]      
    datatem = parse_options_data(da)
     
    return datatem