#!/usr/bin/python
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


while True:

	#
	#
	# TODO: Verificar se a Bolsa de Valores está em horario de negociacao ou nao, a fim de nao adicionar numeros inuteis no Banco de Dados.
	#
	#

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

	time.sleep(60)

resp.close()