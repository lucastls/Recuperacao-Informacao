# Recuperação de Informação

Disciplina de Recuperação de Informação do CEFET-MG

### Instalar pip

pip é um gerenciador de pacotes para python

Para instalar, basta executar o comando:
```
$ sudo apt-get install python3-pip
```
### Instalar venv

venv é uma ferramenta para criação de ambientes virtuais.

Para instalar, basta executar o comando:
```
$ sudo apt-get install python3-venv
```
### Criando ambiente virtual

Para criar um novo ambiente virtual, basta executar, na pasta raiz do repositório o comando:
```
$ python3 -m venv v_amb
```
Onde v_amb é o nome do ambiente virtual a ser criado.

### Ativando o ambiente virtual

Além de instalar, é necessário ativar o ambiente virtual que foi criado. Para isto, dentro da pasta do ambiente virtual que foi criado, basta executar o comando:
```
$ source bin/activate
```
### Desativando o ambiente virtual

Para desativar o ambiente virtual, não importa o diretório que esteja, basta executar o comando:
```
$ deactivate
```
### Clonado o repositório

Após o ambiente virtual estar ativo basta executar o comando na pasta raiz do repositório
```
$ git clone https://github.com/lucastls/Recuperacao_Informacao.git
```
### Instalando dependências

Dentro da pasta raiz do repositório, para instalar todas as dependências do projeto, basta executar:
```
$ pip install -r requirements.txt
```
Serão instalados todos os pacotes listados em requirements.txt

### Atualizando dependências

Sempre que novos pacotes forem instalados, o arquivo requirements.txt deve ser atualizado. Para isto, dentro da pasta raiz do repositório, basta executar:
```
pip freeze > requirements.txt
```
