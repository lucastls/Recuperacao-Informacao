from math import log2, sqrt
from operator import itemgetter
import json

def LoadIndex(indexFilePath):
	Index={}

	with open(indexFilePath) as f:
	    All = f.read()

	All = All.strip().split('\n')

	for i in range(int(len(All)/10)):
		content = All[i]

		term = content.split('[',1)[0]
		#Index[term]=[]
		Index[term]={}
		values = content.split('[',1)[1].lstrip('[').rstrip(']]').split('], [')

		for element in values:
			#Index[term].append(tuple(element.split(', ')))
			try:
				docId = int(element.split(', ')[0])
				freq = int(element.split(', ')[1])
				Index[term][docId]=freq
			except:
				pass

	return Index

def TF(Index, termo, docId):

	freq = int(Index[termo].get(docId, 0))

	if freq > 0:
		tf = 1 + log2(freq)
	else:
		tf = 0

	return tf

def IDFBM25 (Index, termsList, N):

	idfBM25 = {}

	for termo in termsList:
		ni = len(Index[term].keys())
		idfBM25[termo] = (N-ni+0.5)/(ni+0.5)

	return idfBM25

def NormaDocs(Index, termsList, N):
	docsNorma={}

	for term in termsList:
		docsList = list(Index[term].keys())
		for docId in docsList:
			tf = TF(Index, term, docId)
			idf = N/(len(Index[term].keys()))
			tfidf = tf*idf
			norma = (tfidf**2) + docsNorma.get(docId, 0)
			docsNorma[docId] = norma

	for docId, norma in docsNorma.items():
		docsNorma[docId] = sqrt(norma)

	return docsNorma

def DocTam(Index, termsList):
	docTam={}
	for term in termsList:
		docsList = list(Index[term].keys())
		for docId in docsList:
			docTam[docId] = int(docTam.get(docId,0)) + int(Index[term].get(docId,0))
	return docTam

#TODO: avgDocLen de todos os documentos ou só os da pesquisa?
def AvgDocLen(docsTam, docsList):
	acc = 0

	for docId in docsList:
		acc = acc + docsTam[docId]

	avgDocLen = float(acc)/float(len(docsList))

	return avgDocLen

def main():

	Index = LoadIndex('Index.dat')
	print('Indice carregado')

	#Cria lista de termos a partir do indice
	termsList = list(Index.keys())
	print('Lista de termos criada')

	#Cria lista de Documentos a partir dos termos
	docsList = []
	for term in termsList:
		docsList = docsList + list(Index[term].keys())
	print('Lista de documentos criada')

	N = len(docsList)

	docsNorma = NormaDocs(Index, termsList, N)
	print('Norma calculada')
	idfBM25 = IDFBM25 (Index, termsList, N)
	print('IDFBM25 calculada')
	docsTam = DocTam(Index, termsList)
	print('DocTam calculada')
	docsAvgLen = AvgDocLen(docsTam, docsList)
	print('AvgDocLen calculada')


	json.dump(docsNorma, open("docsNorma.dat",'w'))
	json.dump(idfBM25, open("idfBM25.dat",'w'))
	json.dump(docsTam, open("docsTam.dat",'w'))
	json.dump(docsAvgLen, open("docsAvgLen.dat",'w'))

    
if __name__ == "__main__":
    main()