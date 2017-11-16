# -*- coding: utf-8 -*-
"""
Created on Thu Oct 15 16:57:42 2015

@author: he math
"""
from sympy import symbols,sqrt,simplify,lambdify 
import  matplotlib.pyplot as plt
import numpy as np

def portfolioplot( muf=0.06,mu1=0.14,mu2=0.08,sig1=0.2,sig2=0.15,rho12=0,figsize=None):
    #the first risk asset has higher returns and risk in this function
    w=symbols("w")
    ExpRet=mu2+(mu1-mu2)*w
    Varf=simplify(sig1**2*w**2+sig2**2*(1-w)**2+2*w*(1-w)*rho12*sig1*sig2)
    StdRet=sqrt(Varf)
    #init_printing()
    ExpRet,simplify(StdRet)
    
    meanf= lambdify(w, ExpRet, "numpy")
    varf=lambdify(w,Varf,"numpy")   

    #%matplotlib inline
    if figsize is None:
        plt.figure(figsize=(12,8))
    else:
        plt.figure(figsize=figsize)
    
    plt.text(sig1,mu1*1.02,"$R_1$")
    plt.text(sig2,mu2*0.95,"$R_2$")
    
    wmin=float(-Varf.coeff(w,1)/(2*Varf.coeff(w,2)))
    mx=sqrt(varf(wmin));my=meanf(wmin)
    plt.plot([sig1,sig2,0,mx],[mu1,mu2,muf,my],"bo")
    plt.text(mx*1.02,my,"M (minimum variance portfolio)",fontsize=15)
    plt.text(0,muf*1.1,"F",fontsize=15)
    
    wv=np.linspace(0,wmin,100)
    stdv=np.sqrt(varf(wv))
    meanv=meanf(wv)
    plt.plot(stdv,meanv,"r-")  
    plt.annotate("$w\in$"+str([0,round(wmin,3)]), size=15,xy=(stdv[30],meanv[30]),
                 xytext=(stdv[30]*1.1,meanv[30]),
                arrowprops=dict(facecolor="red"))
    
    
    wv=np.linspace(wmin,1,100)
    stdv=np.sqrt(varf(wv))
    meanv=meanf(wv)
    plt.plot(stdv,meanv,"b-") 
    plt.annotate("efficient frontier\n"+"$w\in$"+str([round(wmin,3),1]), size=15,xy=(stdv[80],meanv[80]),
                 xytext=(stdv[80]*0.6,meanv[80]),
                arrowprops=dict(facecolor="blue"))
    
    plt.xlim([-0.01,max(sig1,sig2)*1.1])
    plt.ylim([max(0,muf-0.02)*0.9,max(mu1,mu2)*1.1])
    plt.plot([0,mx],[muf,my],"b--")
    plt.plot([0,sig2],[muf,mu2],"r-.")
    
    # tangency portfolio
    v1=mu1-muf;v2=mu2-muf;
    Wt=(v1*sig2**2-v2*rho12*sig1*sig2)/(v1*sig2**2+v2*sig1**2-(v1+v2)*rho12*sig1*sig2)
    Tx=sqrt(varf(Wt));Ty=meanf(Wt)
    plt.plot([Tx],[Ty],"bo")
    plt.plot([Tx,0],[Ty,muf],"b--")
    plt.text(Tx*1.01,Ty*0.93,"T (tangency portfolio)\n "+"$w=$"+str(round(Wt,3)),fontsize=15)