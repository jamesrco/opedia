import sys
sys.path.append('../../')
import timeSeries as TS
import pandas as pd
import matplotlib.pyplot as plt


def plot(t, y):
    plt.plot(t, y, 'o')
    plt.show()



table = 'tblVort_REP'
field = 'vort'
startDate, endDate = '2016-01-19', '2016-02-19'
lat1, lat2, lon1, lon2 = 30.57, 35.21, -163.43, -156.17  
arg8_name, arg8_val, extV2, extVV2 = None, None, None, None
t, y, y_std = TS.timeSeries(table, field, startDate, endDate, lat1, lat2, lon1, lon2, arg8_name, arg8_val, extV2, extVV2)
plot(t, y)     