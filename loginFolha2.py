#!/usr/bin/python
#coding=utf-8
#Autor: Lucas Jose Monteiro Carvalho

import urllib, urllib2, cookielib, MySQLdb, time, datetime

EMAIL = 'seu-email'
PASSWORD = 'sua-senha'
URL = 'http://login.folha.com.br/login?done=http%3A%2F%2Ffolhainvest.folha.com.br%2Fcarteira&service=folhainvest'
str1 = 'TOTAL GERAL (R$)'
str2 = 'right'

cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

opener.addheaders.append(('User-agent', 'Mozilla/4.0'))
opener.addheaders.append( ('Referer', 'http://www.google.com.br') )

login_data = urllib.urlencode(
							{
								'email': EMAIL,
								'password': PASSWORD,
								'auth': 'Autenticar',
							}
						  )

resp = opener.open(URL, login_data)

db = MySQLdb.connect(host="localhost", user="root", passwd="root", db="acoes")
cur = db.cursor()

timeFechamento = 18*3600 + 15*60
timeAbertura = 10*3600

while True:
	try:

		timeNow = datetime.datetime.now().hour*3600 + datetime.datetime.now().minute*60 + datetime.datetime.now().second

		if timeNow < timeAbertura or timeNow > timeFechamento or datetime.datetime.now().weekday() == 5 or datetime.datetime.now().weekday() == 6:
			print "Bolsa fechada"
		else:
			request = urllib2.Request("http://folhainvest.folha.com.br/carteira")
			source = opener.open(request).read()

			i = source.find(str1, 0)
			i = source.find(str2, i+1)
			i = source.find(str2, i+1)
			i = source.find(str2, i+1)

			begin = i
			end = source.find("<", i+1)


			finalSource = source[begin+7:end]
			finalSource = finalSource.replace(".", "")
			finalSource = finalSource.replace(",", ".")

			print finalSource

			cur_date = datetime.datetime.now()
			cur_date = str(cur_date)

			#Permite SQL Injection
			sql = "INSERT INTO acoes values (NULL, '" + cur_date + "', " + finalSource + ")"
			cur.execute(sql)
			db.commit()
	except:
		db = MySQLdb.connect(host="localhost", user="root", passwd="root", db="acoes")		
		cur = db.cursor()		

	time.sleep(60)

resp.close()
