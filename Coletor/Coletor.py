from lxml import etree, cssselect, html
from urllib.error import URLError, HTTPError, ContentTooShortError
import urllib.request

url = 'https://www.ratebeer.com/breweries/brazil/0/31/'

def Obter_links(url):

	htmldoc = urllib.request.Request(url)
	htmldoc.add_header('User-agent', 'elmbot')

	try:
		Links.pop()

	try:
		htmldoc = urllib.request.urlopen(htmldoc).read()
	except (URLError, HTTPError, ContentTooShortError) as error:
		print('Erro: ',error)

	tree = html.fromstring(htmldoc) # parse the HTML and fixes it
	htmldoc = html.tostring(tree, pretty_print=True)
	htmldoc = html.fromstring(htmldoc)

	get_links = cssselect.CSSSelector('a')
	Links = [ link.get('href') for link in get_links(htmldoc)]

	dominio=url[:len(url)-1]

	print(Links)

	for i in range(len(Links)):
		if Links[i] and Links[i].startswith('/'):
			Links[i]=dominio+Links[i]

	return Links
