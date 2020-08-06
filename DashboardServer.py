
from flask import Flask
from flask import render_template
from flask_material import Material
from bokeh.embed import components
from bokeh.plotting import figure
import pymysql
from sklearn.linear_model import LinearRegression
import numpy as np
from bokeh.io import show
from bokeh.plotting import figure
from flask import Flask
from flask import render_template
from flask_material import Material
import pymysql
from sklearn.linear_model import LinearRegression
import math as ma
from bokeh.models import FactorRange
from bokeh.models import ColumnDataSource




app=Flask("__name__")
Material(app)


def db():
	connection = pymysql.connect(host='localhost', user='root', password='', db='Project')
	cursor=connection.cursor()
	sql=('SELECT pop_1990, pop_2010,pop_2012 FROM project.country_population;')
	cursor.execute(sql)
	data=cursor.fetchall()
	
	return render_template("DashbordServer.html",div=data)

@app.route("/")
def tech():
	connection = pymysql.connect(host='localhost', user='root', password='hamzatheone', db='Project')
	cursor1=connection.cursor()
	cursor2 = connection.cursor()
	cursor3 = connection.cursor()
	cursor4 = connection.cursor()
	cursor5 = connection.cursor()

	sql = 'SELECT Make, sum(Quantity) FROM project.sales group by Make;'
	sql2= 'SELECT Year, sum(Quantity ) as sales FROM project.sales WHERE Make="Renault" group by Year;'
	sql3 = 'SELECT Year, sum(Quantity ) as sales FROM project.sales WHERE Make="Toyota" group by Year;'
	sql4= 'SELECT sum(quantity) as sales, month from project.sales where make="renault" group by month;'
	sql5 = 'SELECT quantity from project.sales;'
	cursor1.execute(sql)
	cursor2.execute(sql2)
	cursor3.execute(sql3)
	cursor4.execute(sql4)
	cursor5.execute(sql5)
	data1 = cursor1.fetchall()
	data2= cursor2.fetchall()
	data3= cursor3.fetchall()
	data4= cursor4.fetchall()
	data5=cursor5.fetchall()

	make = []
	sales = []

	year_1 = []
	sales_1 = []


	Year = []
	sales_R = []

	quantity_R=[]
	month=[]
	for row in data1:
		make.append(row[0])
		sales.append(row[1])

	for row in data2:
		Year.append([row[0]])
		sales_R.append([row[1]])

	p = figure(title="Predictions", plot_height=500, plot_width=500, x_range=(0, 100), y_range=(0, 2000))
	p.vbar(Year, top=sales_R, width=0.0, alpha=0.8)

	sc, dv=components(p)

	for row in data3:
		year_1.append([row[0]])
		sales_1.append([row[1]])

	for row in data4:
		quantity_R.append(row[0])
		month.append(row[1])

	Lin_regression = LinearRegression()
	Lin_regression2 = LinearRegression()
	Lin_regression.fit(np.array(Year).tolist(), np.array(sales_R).tolist())
	Lin_regression2.fit(np.array(year_1).tolist(), np.array(sales_1).tolist())

	W_pred = Lin_regression.predict([[2018]])
	W_pred1 = Lin_regression2.predict([[2018]])

	for row in data1:
		if row[1]== max(sales):
			 a=row[0]

	for row in data1:
		if row[1]== min(sales):
			 b=row[0]


	for row in data4:
		if row[0]== max(quantity_R):
			 c=row[1]

	avg=[]
	for row in data5:
		avg.append(row[0])

	aa = max(avg) - (0.6745*(np.array(avg).std() / ma.sqrt(4377)))
	bb = max(avg) + (0.6745 * (np.array(avg).std() / ma.sqrt(4377)))

	crime_number = [23, 13, 20, 46, 29, 70, 30, 40, 28]
	cities = [("Rabat", "2015"), ("Rabat", "2016"), ("Rabat", "2017"),
			  ("Casa", "2015"), ("Casa", "2016"), ("Casa", "2017"),
			  ("Tanger", "2015"), ("Tanger", "2016"), ("Tanger", "2017")]

	p = figure(x_range=FactorRange(*cities), y_range=(0, 50), x_axis_label="city/year", y_axis_label="crimeNumber")

	p.vbar(x=cities, top=crime_number, width=0.8, alpha=0.8)
	sc, dv = components(p)


	return render_template("index.html", script=max(sales), div=a, script1=min(sales), div1=b,
						   predict=int(W_pred), predict2=int(W_pred1), script2=sc, div2=dv, max=max(quantity_R),
						   m=c, avg=int(aa), avg2=int(bb), plot_div=dv, plot_script=sc)





if __name__ =="__main__" :
    app.run(debug=True)
