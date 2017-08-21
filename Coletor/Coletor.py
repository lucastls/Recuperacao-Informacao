from lxml import etree, cssselect, html
from urllib.error import URLError, HTTPError, ContentTooShortError
import urllib.request

url = 'https://www.ign.com/'

def Download_HTML(url, num_tentativas):

	htmldoc = urllib.request.Request(url)
	htmldoc.add_header('User-agent', 'elmbot')

	try:
		htmldoc = urllib.request.urlopen(htmldoc).read().decode()
	except (URLError, HTTPError, ContentTooShortError) as error:
		print('Erro: ',error)
		html = None
		if num_tentativas > 0:
			if hasattr(error, 'code') and (500 <= error.code < 600):
				# recursivavmente tenta de novo para erros HTTP 5xx
				return Obter_links(url, num_retries - 1)

	return htmldoc

def Obter_links(url):

	htmldoc = Download_HTML(url,2)

	tree = html.fromstring(htmldoc) # parse the HTML and fixes it
	htmldoc = html.tostring(tree, pretty_print=True)
	htmldoc = html.fromstring(htmldoc)

	get_links = cssselect.CSSSelector('a')
	Links = [ link.get('href') for link in get_links(htmldoc)]

	pagRaiz = url.split(':')[0] + '://' + url.split('//')[1].split('/')[0] + '/'

	dominio = url.split('.')[1].split('.')[0]

	for i in range(len(Links)):
		if Links[i] and Links[i].startswith('/'):
			Links[i]=pagRaiz+Links[i]
		if Links[i] and Links[i].startswith('#'):
			del Links[i]
	return Links

Obter_links(url)
