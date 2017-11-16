record = np.zeros[len(stockprice)]

for i in range(len(stockprice)):
	if (stockprice[i] > max(stockprice[i-4:i]) and stockprice[i] > max(stockprice[i+1:i+5])):## 符合定义的SEP对应的点
		record[i] = stockprice[i].date 
		##记录下这个点所对应的交易日

