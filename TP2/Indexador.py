import codecs, re, os, nltk.test, unidecode
from bs4 import BeautifulSoup
from operator import itemgetter
from collections import defaultdict
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize

def makeDirectoryList():
    files = list()
    for filename in os.listdir(os.getcwd()): #Recebemos o ambiente(local) em que estamos 
        if re.match(r'[0-9]', filename): #Procuramos pelas pastas que conteem os arquivos html's
            files.append(filename)

    filesHtml = list()
    for file in files: #Entramos em cada pasta que contem os arquivos html's
        path = '/home/sants_/Documents/RecuperacaoInformacao/TP2/'
        path = path + file
        for filename in os.listdir(path): #Adicionamos o endereço de cada arquivo de cada pasta em nossa lista
                filesHtml.append(path + '/' + filename) 

    return filesHtml #Retornamos uma lista com o endereco de tds os html's

def getID(file):
    pos = file[::-1].find('/')
    file = file[::-1][0:pos][::-1]
    pos = file.find('.')

    if re.match(r'[0-9]', file[0:pos]):
        return file[0:pos] #Retornamos o ID do arquivo em questao
    else:
        return 0

def makeFileDict(element, ID):
    file = codecs.open(element, 'r', 'iso-8859-1') #Abrimos o arquivo em questao
    
    content = defaultdict(list)
    stemmer = nltk.stem.RSLPStemmer() #Importamos a Steammer
    stopwords = nltk.corpus.stopwords.words('portuguese') #Importamos as Stopwords da lingua portuguesa
    docwordsStem = list()
    
    try: 
        document = BeautifulSoup(file, "lxml").get_text() #Leitura do html (+rapida)
    except:
        try:
            document = BeautifulSoup(file, 'html5lib').get_text() #Leitura do html caso nao tenha tido sucesso com a abordagem anterior (+lenta)
        except:
            print('Formatação da página %n não reconhecida!', ID)
            return content

    document = document.lower() #Colocamos todas palvras em lowercase
    docwords = word_tokenize(document) #Separamos as palavras uma a uma 
    for word in docwords:
        if word not in stopwords: #Verificamos se a palavra é ou nao um stopword
            try:
                new = unidecode.unidecode(word) #Retiramos a acentuaçao da palavra
                docwordsStem.append(stemmer.stem(new)) #Realizamos o steamming da palavra e a adicionamos na lista de palvras deste documento
            except:
                docwordsStem.append(stemmer.stem(word)) #Realizamos o steamming da palavra e a adicionamos na lista de palvras deste documento
    del document, docwords 
 
    for i in range(len(docwordsStem)): #Para cada palavra do documento em questao
        if re.match(r'[a-z]', docwordsStem[i]): #Para cada palavra do documento filtramos as que comecam com letras        
            if docwordsStem[i] not in content:
                content[docwordsStem[i]].append([int(ID),1]) #Adicionamos a palavra e o ID do documento que ela ocorre
            else:
                content[docwordsStem[i]][0][1] = content[docwordsStem[i]][0][1]+1 #Caso ja exista adicionamos 1 na ocorrencia da palavra
                    
    return content

def makeOrdenation(index):
    for key in index:
        #Ordenamos cada key do dicionario com base no primeiro elemento de cada elemento da lista de ocorrencias  
        index[key].sort(key=lambda x: x[0]) 

    return index

def makeArchive(index):
    archive = open('Index.txt', 'w')

    try:
        for key in index: #Escrevos o Indice no arquivo termo a termo
            stri = str(key) + str(index[key]) + '\n'
            archive.write(stri) #Cada termo ocupa uma linha no arquivo .txt
        print ("Indice criado com sucesso! (Index.txt)")
    except:
        print ("Erro na criação do Indice! (Index.txt)")
            
    archive.close()

filesHtml = makeDirectoryList() #Criamos a lista com os endereços de cada um dos arquivos
index = defaultdict(list) #Estrutura: index[Key] = [[ID_Documento,Numero_Ocorrencias],[ID_Documento,Numero_Ocorrencias],...] 
                          #Um dicionario de lista de listas
for element in filesHtml: #Para cada elemento na lista dos diretorios dos arquivos
    ID = getID(element) #Recebemos o ID do determinado elemento
    if ID is 0:
        continue
        
    content = makeFileDict(element, ID) #Criamos o dicionario para o elemento em questao
    print ('Vivo!')
    for key in content: #Adicionamos o dicionario do elemento em questao ao dicionario global
        if key not in index:
            index[key] = content[key]
        else:
            index[key].append(content[key][0])
        print ('Aye!')
makeOrdenation(index) #Realizamos a ordenação
makeArchive(index) #Criamos o arquivo de saida com o Indice
