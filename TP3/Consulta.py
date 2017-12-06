from math import log2, sqrt
from operator import itemgetter
import json
from PreProcessamento import LoadIndex

def LoadTitlePerDoc(indexFilePath):
	titlePerDoc={}

	with open(indexFilePath) as f:
	    All = f.read()

	All = All.strip().split('\n')

	for i in range(int(len(All)/20)):
		content = All[i]

		docId, title = content.split(';',1)

		titlePerDoc[docId]=title

	return titlePerDoc

def Bolean(termosPesquisa):
	resultados = []
	for termo in termosPesquisa:
		docsList = Index[termo].keys()
		for docId in docsList:
			resultados.append()

def TF(Index, termo, docId):

	freq = int(Index[termo].get(docId, 0))

	if freq > 0:
		tf = 1 + log2(freq)
	else:
		tf = 0

	return tf

def PesqTF(termosPesquisa):
	pesqFreq={}

	for termo in termosPesquisa:
		pesqFreq[termo] = pesqFreq.get(termo, 0) + 1

	pesqTf = 1 + log2(pesqFreq.get(termo, 0))

	return pesqTf

def TFIDF(Index, termo, docId, termsIDF, N):

	tf = TF(Index,termo, docId)
	idf = termsIDF[termo]

	return tf*idf

def SimTFIDF(N, termosPesquisa, docsNorma):

	termosEmComum = termosPesquisa

	docsList=[]
	for termo in termosEmComum:
		docsList = docsList + list(Index[termo].keys())

	resultados=[]
	for docId in docsList:
		pesoAcc=0
		for termo in termosEmComum:

			tf = TF(Index,termo, docId)

			pesqTf = PesqTF(termosPesquisa)

			idf = N/(len(Index[termo].keys()))

			pesoAcc = pesoAcc + tf*idf*pesqTf*idf
		pesoAcc = pesoAcc/docsNorma[docId]
		resultados.append([docId, pesoAcc])

	for i in range(len(resultados)):
		resultados[i][0] = titlePerDoc[resultados[i][0]]

	resultados.sort(key=itemgetter(1))

	return resultados

def SimBM25(Index, termosPesquisa, docsAvgLen, idfBM25, docsTam, k = 1, b = 0.75):

	termosEmComum = termosPesquisa

	docsList=[]
	for termo in termosEmComum:
		docsList = docsList + list(Index[termo].keys())

	for docId in docsList:
		pesoAcc=0
		for termo in termosEmComum:
			betaBM25 = BetaBM25(Index, termo, docId, docsAvgLen, docsTam, k, b)
			pesoAcc = pesoAcc + betaBM25*idfBM25[termo]
		resultados.append([docId, pesoAcc])

	for i in range(len(resultados)):
		resultados[i][0] = titlePerDoc[resultados[i][0]]

	return resultados

def BetaBM25 (Index, termo, docId, avgDocLen, docsTam,  k = 1, b = 0.75):

	freq = int(Index[termo].get(docId, 0))
	if freq == 0:
		betaBM25 = 0
	else:
		#betaBM25 = ((k+1)* freq)/((k*((1-b) + ((b*docsTam[docId])/avgDocLen)))+freq)
		betaBM25 = ((k+1)*freq) / (k*((1-b) + (b*docsTam[docId]/avgDocLen))+freq)
	
	return betaBM25

def main():

	Index = LoadIndex('Index.dat')

	#Cria lista de termos a partir do indice
	termsList = list(Index.keys())

	docsNorma = json.loads(open("docsNorma.dat",'r').read())
	docsAvgLen = json.loads(open("docsAvgLen.dat",'r').read())
	idfBM25 = json.loads(open("idfBM25.dat",'r').read())

	docsList = list(docsNorma.keys())

	N = len(docsList)

	idfBM25=json.loads(open("idfBM25.dat",'r').read())
	docsTam=json.loads(open("docsTam.dat",'r').read())
	docsAvgLen=json.loads(open("docsAvgLen.dat",'r').read())

	menu=1
	while (menu):
		termosPesquisa = input('Digite o que deseja pesquisar\n\nPesquisa: ')
		termosPesquisa = termosPesquisa.split(' ')
		pesquisas=1

		print('\nDigite o metodo qual deseja usar\n1 - Modelo Vetorial\n2 - Modelo Booleano\n3 - Modelo Probabilistico\n4 - Fazer outra pesquisa\n5 - Sair\n')

		op = int(input('Método: '))
		print('Opção escolhida:',op)
		if op == 1:
			print('check')
			resultados = SimTFIDF(N, termosPesquisa, docsNorma)
			print(resultados)
			print('\n\n')
		elif op == 2: break
		elif op == 3: 
			resultados = SimBM25(Index, termosPesquisa, docsAvgLen, idfBM25, docsTam, k = 1, b = 0.75)
			print(resultados,'\n\n')
		elif op == 4:
			menu=0
		else:
			continue

		menu=0

if __name__ == "__main__":
    main()

