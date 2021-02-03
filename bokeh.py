from bokeh.plotting import figure, curdoc
from random import random
from bokeh.palettes import magma
from bokeh.models import Button, CustomJS, Dropdown
from bokeh.layouts import column
import pickle
all_avg = [37.67831501707314,63.756060487788766,88.38727240174029,130.54572174256634,126.09328773420918,131.3189583898367,100.24893914064054,115.41364319257967,159.9259818691003,0.0,0.0,0.0]

fileObject = open("/home/ubuntu/avghr_dict.pkl",'rb')
cnthr = pickle.load(fileObject)
menu = list(str (x) for x in cnthr.keys())
x_always = list(range(0,12,1))
dd1 = Dropdown(label="Zipcode 1", button_type="warning", menu=menu)
dd2 = Dropdown(label="Zipcode 2", button_type="warning", menu=menu)
def handler1(event):
    lb = event.item
    y1 = cnthr[int(lb)]
    fig.line(x= x_always,y=y1,line_width=2, legend_label = lb, line_color='pink')
def handler2(event):
    lb = event.item
    y2 = cnthr[int(lb)]
    fig.line(x_always,y2, line_width=2, legend_label = lb,line_color='blue')
dd1.on_click(handler1)
dd2.on_click(handler2)
fig = figure(x_range = ['Jan','Feb','Mar','Apr','May','June','July','Aug','Sept','Oct','Nov','Dec'],y_range = (0,1000),title = "NYC 311 Average Response Time 2020",x_axis_label = 'month',y_axis_label='Average response time in hour')
fig.line(x_always,all_avg,line_width=2,legend_label = 'all', line_color = 'grey')
curdoc().add_root(column(dd1,dd2,fig))
