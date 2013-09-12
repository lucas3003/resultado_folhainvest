#!/usr/bin/python
#Autor: Lucas Jose Monteiro Carvalho

import MySQLdb
from pygooglechart import Chart
from pygooglechart import SimpleLineChart
from pygooglechart import Axis

#line_chart = pygal.Line()
#line_chart.title = 'Patrimonio'

db = MySQLdb.connect(host="localhost", user="root", passwd="root", db="acoes")
cur = db.cursor()
cur.execute("SELECT patrimonio from acoes")

rows = cur.fetchall()

values = []

for row in rows:	
	values.append(row[0])

max_y = 251573 #FIX IT
min_y = 250400 #FIX IT
chart = SimpleLineChart(900,100,y_range=[min_y, max_y])

chart.add_data(values)
chart.set_colours(['0000FF'])
#chart.fill_linear_stripes(Chart.CHART, 0, 'CCCCCC', 0.2, 'FFFFFF', 0.2)

chart.set_grid(0, 25, 5, 5)

left_axis = range(0, max_y+1, 500)
left_axis[0] = ''
chart.set_axis_labels(Axis.LEFT, left_axis)


chart.download('line-stripes.png')
