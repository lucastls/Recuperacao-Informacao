from lxml import etree, cssselect, html
from urllib.error import URLError, HTTPError, ContentTooShortError
import urllib.request
import chardet
from urllib import robotparser
import datetime
import time

"""
# Stops iterating through the list as soon as it finds the value
def getIndexOfTuple(l, index, value):
    for pos,t in enumerate(l):
        if t[index] == value:
            return pos

    # Matches behavior of list.index
    raise ValueError("list.index(x): x not in list")

getIndexOfTuple(tuple_list, 0, "cherry")   # = 1
"""

NumLinks=0

def robots(url):

	parser = robotparser.RobotFileParser()
	robots_url = url+'/robots.txt'
	parser.set_url(robots_url)
	parser.read()

	return parser

def checkTimeLastAccess(url, time_now):

	if url in ServerTime.keys():
		if time_now - ServerTime[url] > 30:
			return 0
		else:
			return (30 - (time_now - ServerTime[url]) )
	return 0

def convert_encoding(data, utf8 = 'UTF-8'):
	encoding = chardet.detect(data)['encoding']
	#encoding = chardet.detect(data)['encoding']
	print (encoding)
	if encoding and utf8.upper() != encoding.upper():
		#data = data.decode(encoding, data).encode(utf8)
		return data.decode(encoding).encode(utf8)
	else:
		return data

def setNumLinks(Links, NumLinks_antigo):
	global NumLinks
	NumLinks = NumLinks_antigo + int(len(Links))

def Clean_links(Links,pagRaiz):
	LinksClean=[]
	for i in range(len(Links)-1):
		#print (Links[i][0])
		if len(Links[i]) < 2:
			continue
		if Links[i][0:2]=='//':
			continue
		if len(Links[i]) > 2 and Links[i][0]=='/' and Links[i][1]!='/':
			Links[i]=pagRaiz+Links[i]

		if len(Links[i]) > 0 and Links[i][0]=='#':
			continue
		if len(Links[i]) > 0 and Links[i][0]=='':
			continue
		LinksClean.append(Links[i])

	return LinksClean

def getPagRaiz(url):
	return url.split(':')[0] + '://' + url.split('//')[1].split('/')[0] + '/'

def getDominio(url):
	return url.split('.')[1].split('.')[0]

def Download_HTML(url, user_agent, num_tentativas):

	global ServerTime

	time_now = datetime.time()

	last_access = checkTimeLastAccess(url, time_now)

	if last_access == 0:

		ServerTime[url] = time_now

		htmldoc = urllib.request.Request(url)
		htmldoc.add_header('User-agent', user_agent)

		try:
			htmldoc = urllib.request.urlopen(htmldoc).read()
			#print(chardet.detect(htmldoc)['encoding'])
			#c=input('Para') Windows-1252
			htmldoc = convert_encoding(htmldoc).decode()
		except (URLError, HTTPError, ContentTooShortError) as error:
			print('Erro: ',error)
			html = None
			if num_tentativas > 0:
				if hasattr(error, 'code') and (500 <= error.code < 600):
					# recursivavmente tenta de novo para erros HTTP 5xx
					return Download_HTML(url, user_agent, num_retries - 1)

		return htmldoc

	else:
		time.sleep(last_access)
		Download_HTML(url, user_agent, num_tentativas)

def Obter_links(url,depth):

	user_agent = 'elmbot'

	global NumLinks

	#Verifica robots.txt da pagina
	rp = robots(url)
	if rp.can_fetch(user_agent, url):
		htmldoc = Download_HTML(url,user_agent,2)
	else:
		print('Bloqueada pelo robots.txt:', url)

	tree = html.fromstring(htmldoc) # parse the HTML and fixes it
	htmldoc = html.tostring(tree, pretty_print=True)
	htmldoc = html.fromstring(htmldoc)

	get_links = cssselect.CSSSelector('a')
	Links = [ link.get('href') for link in get_links(htmldoc)]
	print ('Numero de Links: ',len(Links))

	pagRaiz = getPagRaiz(url)
	print ('Pagina raiz: ',pagRaiz)

	dominio = getDominio(url)
	print('Dominio: ',dominio)

	#Função que determina se os links da lista de links são validos
	LinksClean = Clean_links(Links,pagRaiz)
	del Links

	if NumLinks < 500:
		LinksClean_size = 500 - NumLinks
		if len(LinksClean) > LinksClean_size:
			LinksClean = LinksClean[0:LinksClean_size]

	#Atualiza a contagem de links
	setNumLinks(LinksClean,NumLinks)

	#LinksD é uma lista de tuplas. Elemento da lista: (Link,Profundidade)
	LinksD = [ (link,depth+1) for link in LinksClean ]

	#Verifica se o dominio ja esta na fila de links
	try:
		pos = [i[0] for i in LinksQueue].index(dominio)
	except:
		pos = -1

	#Se o dominio ja esta na fila de links acrescesta os links na sua fila, caso contrario a sua lista é criada
	if pos > -1:
		PLinks = LinksQueue[pos][1]
		LinksQueue[pos][1] = PLinks+LinksD
	else:
		LinksQueue.append((dominio,LinksD))

#LinksQueue é uma lista de tuplas. Elemento da lista: (Dominio,Links)
LinksQueue=[]
ServerTime={}

Seeds = ['http://www.globo.com','http://www.r7.com.br']#,'http://www.uai.com.br'

for url in Seeds:
	#print (url)
	Obter_links(url,0)

print('\n',LinksQueue[0][1][0][0],'\n')

while NumLinks < 500:
	for j in range(len(LinksQueue)):
		for i in range(len(LinksQueue[j])):
			
			link = LinksQueue[i][0][0]
			depth = LinksQueue[i][0][1]
			Obter_links(link,depth)

print ("Numero total de links",NumLinks)
