# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 09:54:01 2015

@author: Tobias
"""
import data_preparation as dp
import correlation_tool as ct
import datetime as dt

#x,y = dp.Data_preparation.GetMostRecentData(5);
start = dt.datetime(year = 2015, month = 8, day = 1)
end = dt.datetime(year = 2015, month = 8, day = 5)
x = dp.Data_preparation.getTweetCount(start,end)
print x
#p,r = ct.Correlation_tool.Correlate(x,y,True)
#print p
#print r