import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import db
import timeSeries as TS
from datetime import datetime, timedelta
import time
from math import pi
from bokeh.plotting import figure, show, output_file
from bokeh.layouts import column
from bokeh.models import DatetimeTickFormatter
from bokeh.palettes import all_palettes
from bokeh.models import HoverTool
from bokeh.embed import components


def embedComponents(fname, data):
    f = open(fname, 'w')
    f.write(data)
    f.close()
    return


def prepareTimeSpaceQuery(table, date1, date2, lat1, lat2, lon1, lon2):
    query = "SELECT AVG(sla) AS sla, AVG(sst) AS sst, AVG(u) AS u, AVG(v) as v FROM %s WHERE "
    #query = query + "[time]>='%s' AND [time]<='%s' AND "
    query = query + "[time]='%s' AND "
    query = query + "lat>=%f AND lat<=%f AND "
    query = query + "lon>=%f AND lon<=%f "
    #query = query % (table, date1, date2, lat1, lat2, lon1, lon2)
    query = query % (table, date1, lat1, lat2, lon1, lon2)
    return query


def exportData(t, y, yErr, table, variable, lat1, lat2, lon1, lon2, extV, extVV, extV2, extVV2):
    df = pd.DataFrame()
    df['time'] = t
    df[variable] = y
    df[variable+'_std'] = yErr
    df['lat1'] = lat1
    df['lat2'] = lat2
    df['lon1'] = lon1
    df['lon2'] = lon2
    df[extV] = extVV
    df[extV2] = extVV2
    dirPath = 'data/'
    if not os.path.exists(dirPath):
        os.makedirs(dirPath)        
    path = dirPath + 'TS_' + table + '_' + variable + '.csv'
    df.to_csv(path, index=False)    
    return


def plotTS(tables, variables, startDate, endDate, lat1, lat2, lon1, lon2, extV, extVV, extV2, extVV2, exportDataFlag, marker='-', msize=30, clr='purple'):
    p = []
    lw = 2
    w = 800
    h = 400
    TOOLS = 'pan,wheel_zoom,zoom_in,zoom_out,box_zoom, undo,redo,reset,tap,save,box_select,poly_select,lasso_select'
    for i in range(len(tables)):
        t, y, yErr = TS.timeSeries(tables[i], variables[i], startDate, endDate, lat1, lat2, lon1, lon2, extV[i], extVV[i], extV2[i], extVV2[i])
        if exportDataFlag:
            exportData(t, y, yErr, tables[i], variables[i], lat1, lat2, lon1, lon2, extV[i], extVV[i], extV2[i], extVV2[i])
        p1 = figure(tools=TOOLS, toolbar_location="above", plot_width=w, plot_height=h)
        #p1.xaxis.axis_label = 'Time'
        p1.yaxis.axis_label = variables[i] + ' [' + db.getVar(tables[i], variables[i]).iloc[0]['Unit'] + ']'
        leg = variables[i]
        if extV[i] != None:
            leg = leg + '   ' + extV[i] + ': ' + ( '%d' % float(extVV[i]) ) 
            if tables[i].find('Pisces') != -1:
                leg = leg + ' ' + 'm'
        fill_alpha = 0.07        
        if tables[i].find('Pisces') != -1:
            fill_alpha = 0.3
        cr = p1.circle(t, y, fill_color="grey", hover_fill_color="firebrick", fill_alpha=fill_alpha, hover_alpha=0.3, line_color=None, hover_line_color="white", legend=leg, size=msize)
        p1.line(t, y, line_color=clr, line_width=lw, legend=leg)
        p1.add_tools(HoverTool(tooltips=None, renderers=[cr], mode='hline'))
        p1.xaxis.formatter=DatetimeTickFormatter(
                hours=["%d %B %Y"],
                days=["%d %B %Y"],
                months=["%d %B %Y"],
                years=["%d %B %Y"],
            )
        p1.xaxis.major_label_orientation = pi/4
        #p1.xaxis.visible = False
        p.append(p1)
    dirPath = 'embed/'
    if not os.path.exists(dirPath):
        os.makedirs(dirPath)        
    output_file(dirPath + fname + ".html", title="TimeSeries")
    show(column(p))
    return



tables = sys.argv[1].split(',')      #tables
variables = sys.argv[2].split(',')      #variables
startDate = sys.argv[3]      #dt1
endDate = sys.argv[4]      #dt2
#startDate = sys.argv[3].split('T')[0]      #dt1
#endDate = sys.argv[4].split('T')[0]      #dt2

lat1 = float(sys.argv[5])      #lat1
lat2 = float(sys.argv[6])      #lat2
lon1 = float(sys.argv[7])      #lon1
lon2 = float(sys.argv[8])      #lon2
fname = sys.argv[9]
exportDataFlag = bool(int(sys.argv[10]))
extV = sys.argv[11].split(',')       #extra condition: var_name
extVV = sys.argv[12].split(',')       #extra condition: var_val
extV2 = sys.argv[13].split(',')       #extra condition: var_name
extVV2 = sys.argv[14].split(',')       #extra condition: var_val



if float(lat1)>float(lat2):
    temp = lat1
    lat1 = lat2
    lat2 = temp

if float(lon1)>float(lon2):
    temp = lon1
    lon1 = lon2
    lon2 = temp

if datetime.strptime(startDate, '%Y-%m-%d')>datetime.strptime(endDate, '%Y-%m-%d'):
    temp = startDate
    startDate = endDate
    endDate = temp


for i in range(len(tables)):
    if extV[i].find('ignore') != -1:
        extV[i]=None
    if extVV[i].find('ignore') != -1:
        extVV[i]=None
    if extV2[i].find('ignore') != -1:
        extV2[i]=None
    if extVV2[i].find('ignore') != -1:
        extVV2[i]=None


tic = time.clock()
plotTS(tables, variables, startDate, endDate, lat1, lat2, lon1, lon2, extV, extVV, extV2, extVV2, exportDataFlag)
toc = time.clock()
print('Fetch time: %2.2f s' % (toc-tic))
