from lxml import etree, cssselect, html
from urllib.error import URLError, HTTPError, ContentTooShortError
import urllib.request, urllib.parse, urllib.error
import cchardet
from urllib import robotparser
import datetime
import time
import threading

def robots(url):
	parser = robotparser.RobotFileParser()
	robots_url = url+'/robots.txt'
	parser.set_url(robots_url)
	parser.read()
	return parser

def noindex_nofollow(url):
    fhand = urllib.request.urlopen(url).read().decode().strip()
    for line in fhand:
        if not line.startswith('<meta'): continue
        if noindex or nofollow in line: return 0
    return 1

def treads(Seeds, jobs, threads):
	for i in range(threads): #Criamos as threads e atribuimos a função de cada uma
		try:
			thread = threading.Thread(target=obter_links(Seeds[i],depth=0))
			jobs.append(thread)
		except:
			print ('Erro na criação das threads!')
			break
	for j in jobs: #Começa as Threads
		j.start()
	for j in jobs: #Assegura que todas as threads terminaram
		j.join()

def archiveLinks(LinksQueue, tam):
	arch = open('Links_Coletados.txt', 'a')
	stri = ''
	total = list()
	for j in range(tam):
		for i in LinksQueue[j][1]:
			total.append(i[0])
	total = list(set(total))

	for j in range(len(total)):
		stri = stri + total[j] + '\n'			
	arch.write(stri)	
	print ("Numero total de links coletados:", NumLinks)
	arch.close()

def checkTimeLastAccess(url, time_now):
	if url in ServerTime.keys():
		if time_now - ServerTime[url] > 30:
			return 0
		else:
			return (30 - (time_now - ServerTime[url]) )
	return 0

def convert_encoding(data, utf8 = 'UTF-8'):
	encoding = cchardet.detect(data)['encoding']
	print ('Codificação: ',encoding)
	if encoding and utf8.upper() != encoding.upper():
		return data.decode(encoding).encode(utf8)
	else:
		return data

def setNumLinks(Links, NumLinks_antigo):
	global NumLinks
	NumLinks = NumLinks_antigo + int(len(Links))

def clean_links(Links, pagRaiz):
	LinksClean=[]
	for i in range(len(Links)-1):
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

def addVisited(url,access_time):
	global Visited
	Visited[url] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(access_time))

def download_HTML(url, user_agent, num_retries):
	global ServerTime
	time_now = time.time() #Datetime.time()
	print (time_now)
	last_access = checkTimeLastAccess(url, time_now)

	if last_access == 0:
		ServerTime[url] = time_now
		htmldoc = urllib.request.Request(url)
		htmldoc.add_header('User-agent', user_agent)

		try:
			htmldoc = urllib.request.urlopen(htmldoc).read()
			addVisited(url, time_now)
		except (URLError, HTTPError, ContentTooShortError) as error:
			print('Erro: ',error)
			html = None
			if num_retries > 0:
				if hasattr(error, 'code') and (500 <= error.code < 600):
					return download_HTML(url, user_agent, num_retries - 1) # Recursivavmente tenta de novo para erros HTTP 5xx

	else:
		time.sleep(last_access)
		print ('Esperando',last_access,'s')
		download_HTML(url, user_agent, num_retries)
	return htmldoc

def obter_links(url, depth):
	user_agent = 'elmbot'
	global NumLinks
	rp = robots(url) #Verifica robots.txt da pagina
	meta = noindex_nofollow(url) #Verifica nofollow e noindex nos metatags da pagina

	if rp.can_fetch(user_agent, url) and url not in Visited and meta:
		htmldoc = download_HTML(url,user_agent,2)
	else:
		print('Bloqueada pelo protocolo de exlusão de robôs:', url)

	tree = html.fromstring(htmldoc) #Parse o HTML e arruma se necessario
	htmldoc = html.tostring(tree, pretty_print=True)
	htmldoc = html.fromstring(htmldoc)

	get_links = cssselect.CSSSelector('a')
	Links = [ link.get('href') for link in get_links(htmldoc)]

	print ('Numero de Links disponíveis:', len(Links))
	pagRaiz = getPagRaiz(url)
	print ('Pagina raiz:', pagRaiz)
	dominio = getDominio(url)
	print('Dominio:', dominio,'\n')
	LinksClean = clean_links(Links,pagRaiz) #Função que determina se os links da lista de links são validos
	del Links

	if NumLinks < 500:
		NumLinks_remaining = 500 - NumLinks
		if len(LinksClean) > NumLinks_remaining:
			LinksClean = LinksClean[0:NumLinks_remaining]

	setNumLinks(LinksClean,NumLinks) #Atualiza a contagem de links
	LinksD = [ (link,depth+1) for link in LinksClean ] #LinksD é uma lista de tuplas. Elemento da lista: (Link,Profundidade)

	try: #Verifica se o dominio ja esta na fila de links
		pos = [i[0] for i in LinksQueue].index(dominio)
	except:
		pos = -1
	if pos > -1: #Se o dominio ja esta na fila de links acrescesta os links na sua fila, caso contrario a sua lista é criada
		PLinks = LinksQueue[pos][1]
		LinksQueue[pos][1] = PLinks+LinksD
	else:
		LinksQueue.append((dominio,LinksD))

NumLinks = 0
LinksQueue = [] #LinksQueue é uma lista de tuplas, onde cada tupla possui o dominio e a lista de links do determinado dominio. 
                #Elemento da lista: (Dominio, Lista de Links)
ServerTime = {} #Dicionario com a hora do ultimo acesso a um servior,em segundos. Ex: {'http://www.globo.com':1505571681.6166034}
Visited = {} #Dicionario de Visitados
jobs = [] #Lista para as threads
Max_DEPTH = 4 #Profundidade maxima
threads = 3 #Numero de threads
Seeds = ['http://family.disney.com','http://www.globo.com','http://www.r7.com.br'] #Urls de origem
treads(Seeds, jobs, threads)
LinksQueue.reverse()

while NumLinks < 500:
	for j in range(len(LinksQueue)):
		i=0
		while (len(LinksQueue[j]) > 0):
			tp = LinksQueue[j][i].pop()
			depth = tp[1]
			if depth < Max_DEPTH:
				link = tp[0]
				obter_links(link,depth)
			i+=1
archiveLinks(LinksQueue, int(len(Seeds)))
