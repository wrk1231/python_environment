两个文件包：
1.Version1.0
（1）data_original.csv:
测试数据，注意使用别的数据源的时候，要像data_original.csv一样安排格式，第一列的列名改为date。格式保存为csv，否则读入数据的模块识别不了。

（2）GC_risk_parity.py:
记录常量，所有调参频率（月or季度），各个资产权重的上下限，L-BFGS-B算法的初始点。
可以在ipython notebook里编辑修改，也可以用任何文本编辑器打开修改。修改完之后保存.

（3）Version1.0_risk_parity.ipynb
Jupyter(ipython) notebook文件，可以直接运行。开头import了GC_risk_parity.py，所以常量修改仅需要在GC_risk_parity.py里面修改就行。
结果都记录在record这个list里面，每一次的优化结果是一个长度为Num_of_assets的array,记录各个资产的权重。

2.Original Code:
(1）data_original.csv:同上
（2）GC_risk_parity.py:同上
（3）risk_parity_data.py:数据读入、整理的模块
（4）risk_parity_computation.py:优化计算的模块
这个文件夹里面是源码，供进一步开发用。