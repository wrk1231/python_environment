# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from pandas import DataFrame,Series

roomrent_list = pd.DataFrame(columns = 
	['location','safe','price','heat','laundry','aircon','size','elevator','discount','broker_fee','e-mail'], index = [1,2])


list1 = ['Amsterdam and 109th st  4bed','y','5000','y','y','y','unknown','n','n','n','y']

list2 = ['MANHATTAN AVE - WEST 115TH ST.   5bed','y','5495','y','y','y','unknown','n','n','y']

list3 = ['108th between Manhattan and Central Park West  5bed','y','6250','y','y','y','unknown','n','n','y']

list4 = ['West 109th Street New York, N.Y. 10025  5bed','y','5700','y','y','y','unknown','n','n','y']

list5 = ['Morningside Heights (Columbia Area) Neighborhood  5bed','y','6250','y','y','y','unknown','n','n','y']

list6 = ['106 BETWEEN BWAY AND AMSTERDAM  5bed','y','6000','y','y','y','unknown','n','n','y']

list7 = ['BETWEEN MANHATTAN AVE & WEST 115TH STREET  5bed','y','6250','y','y','y','unknown','n','n','y']

list8 = ['W 114TH & MANHATTAN AVE  5bed','y','5400','y','y','y','unknown','n','n','y']



roomrent_list.ix[1]  =pd.Series(list1,index=roomrent_list.columns)

roomrent_list.ix[2]  =pd.Series(list2,index=roomrent_list.columns)







print roomrent_list