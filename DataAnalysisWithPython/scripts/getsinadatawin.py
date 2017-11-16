# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 21:17:59 2015

@author: he
"""


from lxml.html import parse
from urllib2 import urlopen
from os.path import getsize
import pandas as pd
import urllib 


 

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
            print "download failed for year=" +str(cq.year)+',  jidu='+str(cq.month/3)
            continue
        doc = parsed.getroot()
        tables=doc.findall('.//table')     
        da= tables[-1] # last table 19 for fuquan data and 4 for index
        datatem = parse_options_data(da,isstock,fuquan)
        data=pd.concat([data,datatem])
    return pd.DataFrame(data[start:end],dtype=float)    
 
    
    

from Tkinter import *
import tkMessageBox, tkFileDialog
 
 
        
class SinaStock(Frame):
  def __init__(self, master=None):
    Frame.__init__(self, master)
    self.pack()
    self.createWidgets()
 
  def createWidgets(self):
    self.stockInputLabel =  Label(self, text="Stock code").grid(row=0)
    self.stockid = Entry(self)
    #self.stockid=Text(self,height=4,width=20)
    self.stockid.grid(row=0,column=1)
    self.stockid.insert(0,"000001")
    
    self.stockInputLabel1_t =  Label(self, text="Stock (Yes ) or index(No)").grid(row=1)
    self.Isstock = Entry(self)
    self.Isstock.grid(row=1,column=1)
    self.Isstock.insert(0,"Yes")
    
    self.stockInputLabel_t1 =  Label(self, text="Adjusted price?").grid(row=2)
    self.fuquan = Entry(self)
    self.fuquan.grid(row=2,column=1)
    self.fuquan.insert(0,"Yes")
    ####
#    self.stockInputLabel1 =  Label(self, text="Stock?").grid(row=1)
#    self.Isstock = Listbox(self,height=2)
#    self.Isstock.insert(True, "Stock")
#    self.Isstock.insert(False,"Index") 
#    self.Isstock.grid(row=1,column=1)
    ##
#    self.stockInputLabel2 =  Label(self, text="Adjusted or not").grid(row=2)
#    self.fuquan = Listbox(self,height=2)
#    self.fuquan.insert(True, "Adjusted close price")
#    self.fuquan.insert(False,"close price") 
#    self.fuquan.grid(row=2,column=1)
    #
    self.stockInputLabe3 =  Label(self, text="Start Date").grid(row=3)
    self.s1 = Entry(self)
    self.s1.grid(row=3,column=1) 
    self.s1.insert(0,"1990-12-19")
    #
    self.stockInputLabe4 =  Label(self, text="End Date").grid(row=4)
    self.s2 = Entry(self)
    self.s2.grid(row=4,column=1)
    self.s2.insert(0,str(pd.datetime.now().date()))
    ##
    self.OKbutton = Button(self, text='Download and save to a csv file', command=self.savesinadata)
    self.OKbutton.grid(row=5) 
  def savesinadata(self):
      stid = self.stockid.get()
      isstockv=self.Isstock.get() 
      isstockv= isstockv[0].lower()=="y"
      fuquanv=self.fuquan.get()
      fuquanv= fuquanv[0].lower()=="y"
      start=self.s1.get()
      end=self.s2.get()
      #tkMessageBox.showinfo("",message=stid+str(isstockv)+str(fuquanv)+start+end)
      data=get_sina_stock(stid,start,end,isstockv,fuquanv)
      name=tkFileDialog.asksaveasfilename()
      data.to_csv(name)
app=SinaStock()
app.mainloop()    