# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 16:26:53 2015

@author: he math
"""

# Calculating efficient frontior with n risk assets  

# Ret is a dataframe with   n  columns  
import os
os.chdir('E:\\kuaipan\\2015aut\\notebook')
import pandas as pd
from getsinadata import get_sina_stock
idstock=["600352","600109","601939"]
start="2012-1-1"
end="2015-1-1"
freq="W-FRI"
for i in range(len(idstock)):    
    datat=get_sina_stock(idstock[i],start,end)
    close=datat["close"]
    closew=close.resample(freq,how="last")
    ret1=closew.pct_change()
    ret1.name=idstock[i]
    if i==0:
        data=ret1.copy()
    else:
        data=pd.concat([data,ret1],axis=1)  

data=data.dropna(how="all")

Mu=data.mean().reshape((3,1))
Sigma=data.cov()

import numpy as np
Sigma=np.matrix(Sigma)
N=len(Mu)
Mu=np.matrix(Mu.reshape(N,1))
onesv=np.matrix(np.ones((N,1)))
SI=Sigma.I

A=Mu.T*SI*onesv; A=A[0,0]
B=Mu.T*SI*Mu; B=B[0,0]
C=onesv.T*SI*onesv; C=C[0,0]
D=B*C-A**2
g=SI*onesv*B/D-SI*Mu*A/D
h=SI*Mu*C/D-SI*onesv*A/D


mmin=np.min(Mu)
mmax=np.max(Mu)
meanv=np.linspace(mmin,mmax,100)
wv=map(lambda x: g+x*h,meanv)
sigmav=map(lambda x: np.sqrt(x.T*Sigma*x)[0,0],wv)

mumin=-g.T*Sigma*h/(h.T*Sigma*h)
sigmamin=np.sqrt(g.T*Sigma*g-(g.T*Sigma*h)**2/(h.T*Sigma*h))

muf=0.001
wt=SI*(Mu-muf)
wt=wt/(onesv.T*wt)
mut=wt.T*Mu
sigmat=np.sqrt(wt.T*Sigma*wt)

import matplotlib.pyplot as plt
#%matplotlib inline
#曲线

Sig=data.std()
plt.plot(sigmav,meanv)
plt.plot(Sig,Mu,"bo")
plt.plot(sigmamin,mumin,"ro")


plt.plot([0,sigmat.item(0)],[muf,mut.item(0)],"bo--")


plt.xlim([-0.005,0.073]) 
plt.ylim([0,0.013])


####  efficient frontior with optim

import pandas as pd
import numpy as np
from datetime import datetime
import scipy as sp
import scipy.optimize as scopt
import scipy.stats as spstats
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from getsinadata import get_sina_stock
def create_portfolio(tickers, weights=None):
    if weights is None: 
        weights = np.ones(len(tickers))/len(tickers)
    portfolio = pd.DataFrame({'Tickers': tickers, 
                              'Weights': weights}, 
                             index=tickers)
    return portfolio


def calculate_weighted_portfolio_value(portfolio, 
                                       returns, 
                                       name='Value'):
    total_weights = portfolio.Weights.sum()
    weighted_returns = returns * (portfolio.Weights / 
                                  total_weights)
    return pd.DataFrame({name: weighted_returns.sum(axis=1)})
    
def plot_portfolio_returns(returns, title=None):
    returns.plot(figsize=(12,8))
    plt.xlabel('Year')
    plt.ylabel('Returns')
    if title is not None: plt.title(title)
    plt.show()
    plt.savefig('5104OS_09_02.png', dpi=300)
    
##we get data from sina.com
def get_historical_closes(ticker, start_date, end_date):
    for i in range(len(ticker)):    
        datat=get_sina_stock(ticker[i],start_date,end_date)
        close=datat["close"]
        #closew=close.resample(freq,how="last")
        #ret1=closew.pct_change()
        close.name=ticker[i]
        if i==0:
            data=close.copy()
        else:
            data=pd.concat([data,close],axis=1)  
    
    data=data.dropna(how="all")
    return data
    
def calc_returns(closes,freq="W-FRI",tye="simple"):    
    returndaily=np.log(closes).diff()
    returns=returndaily.resample(freq,how="sum") 
    if tye=="simple":
        return np.exp(returns)-1
    elif tye=="log":
        return returns
    
def calc_portfolio_var(returns, weights=None):
    if weights is None: 
        weights = np.ones(returns.columns.size) / \
        returns.columns.size
    sigma = returns.cov()
    var = weights.dot(sigma).dot(weights)
    return var


#######

def negative_sharpe_ratio( weights,returns,risk_free_rate):
    # get the portfolio variance
    var = calc_portfolio_var(returns, weights)
    # and the means of the stocks in the portfolio
    means = returns.mean()
    # and return the sharpe ratio
    return -((means.dot(weights) - risk_free_rate)/np.sqrt(var))
     

def optimize_portfolio(returns, risk_free_rate,sellshort=True):
    """ 
    Performs the optimization
    """
    means=returns.mean()
    if sellshort:
        bounds=None
    else:
        bounds = [(0,1) for i in np.arange(returns.columns.size)]
        
    weights = np.ones(returns.columns.size, 
                 dtype=float) * 1.0 / returns.columns.size
    # minimize the negative sharpe value
    
    
    constraints = ({'type': 'eq', 
                        'fun': lambda W: np.sum(W) - 1})
    results = scopt.minimize(negative_sharpe_ratio, weights, (returns, risk_free_rate), 
                                 method='SLSQP', 
                                 constraints = constraints,
                                 bounds = bounds)
    if not results.success: # handle error
        raise Exception(results.message)
    mean_sharpe=results.x.dot(means)  
    std_sharpe=calc_portfolio_var(returns,results.x)
    return {'Means': mean_sharpe, 
            'Stds': std_sharpe, 
            'Weights': results.x}
            
    
optimize_portfolio(annual_returns, 0.0003)

 

def plot_efficient_frontier(frontier_data):
    plt.figure(figsize=(12,8))
    plt.title('Efficient Frontier')
    plt.xlabel('Standard Deviation of the porfolio (Risk))')
    plt.ylabel('Return of the portfolio')
    plt.plot(frontier_data['Stds'], frontier_data['Means'], '--'); 
    plt.savefig('5104OS_09_20.png', bbox_inches='tight', dpi=300)

            


def objfun(W, R, target_ret):
    #stock_mean = np.mean(R,axis=0)
    #port_mean = np.dot(W,stock_mean) # portfolio mean
    cov=np.cov(R.T) # var-cov matrix
    port_var = np.dot(np.dot(W,cov),W.T) # portfolio variance
    #penalty = 2000*abs(port_mean-target_ret)# penalty 4 deviation
    #return np.sqrt(port_var) + penalty # objective function
    return np.sqrt(port_var)
def calc_efficient_frontier(returns,sellshort=True):
    result_means = []
    result_stds = []
    result_weights = []
    
    means = returns.mean()
    min_mean, max_mean = means.min(), means.max()
    
    nstocks = returns.columns.size
    if sellshort:
        bounds=None
    else:
        bounds = [(0,1) for i in np.arange(nstocks)]
    for r in np.linspace(min_mean, max_mean, 100):
        weights = np.ones(nstocks)/nstocks        
        constraints = ({'type': 'eq', 
                        'fun': lambda W: np.sum(W) - 1},
                      {'type': 'eq', 
                        'fun': lambda W: np.sum(W*means) -r})
        results = scopt.minimize(objfun, weights, (returns, r), 
                                 method='SLSQP', 
                                 constraints = constraints,
                                 bounds = bounds)
        if not results.success: # handle error
            raise Exception(results.message)
        result_means.append(np.round(r,4)) # 4 decimal places
        std_=np.round(np.std(np.sum(returns*results.x,axis=1)),6)
        result_stds.append(std_)        
        result_weights.append(np.round(results.x, 5))
    return {'Means': result_means, 
            'Stds': result_stds, 
            'Weights': result_weights}

            