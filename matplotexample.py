from pylab import *
import MySQLdb

db = MySQLdb.connect(host="localhost", user="root", passwd="root", db="acoes")
cur = db.cursor()

cur.execute("SELECT patrimonio from acoes")
#cur.execute("SELECT patrimonio, data from acoes")
rows = cur.fetchall()
resultados = []
indice = 1
values = []

for row in rows:
	resultados.append(indice)
	#resultados.append(row[1])
	values.append(row[0])
	indice += 1

plot(resultados,values)
show()