# encoding: utf-8
import os
import time
import json
import requests
import csv
#Mudando para o uso da api do git. Referencias no codigo do Allan e documentacao do github
#Iterando chaves desconhecidas:
'''
for key,value in dict.iteritems():
	print(key,value)

#Coletar apenas informacoes desejadas do commit -- como? Ler doc Git api!!!	
 Json eh um lista de dics [ {
iterar por el usando objeto.get('chave') para pegar valor
'''
# Problema com  umas quebras de linha zoadas em um commit, aparentemente elas sao apenas ignoradas/excluidas
# Como assegurar que peguemos todos os commits?
# O que posso concatenar no link? per_page=100
no = [["tipo","codigo","autor","data","mensagem","parent"]]
link=[["Data de link indefinida","link de responsavel"]]
 
def commit_listing(user,repository):
    i = 1
    request = requests.get('https://api.github.com/repos/'+user+'/'+repository+'/commits?page='+str(i)+'&per_page=100')
    if request.ok:
        conteudo = request.json()
        while(conteudo):
            for commit in conteudo:
                a = commit.get('sha',-1)
                b = commit.get('commit').get('author').get('name',-1)
                c = commit.get('commit').get('author').get('date',-1)
                d = commit.get('commit').get('message',-1).encode('utf-8')
                e = commit.get('parents')
                if(e != []):
                    e = e[0].get('sha')
                else :
                    e = 'none'
                d = d.replace("\n", " ")
                no.append(['commit',a,b,c,d,e])
            i+= 1
            request = requests.get('https://api.github.com/repos/'+user+'/'+repository+'/commits?page='+str(i)+'&per_page=100')
            conteudo = request.json()
    else:
        print('Request nao foi efetivado')
     
     
    with open('/home/gnomy/Downloads/neo4j-community-3.3.2/import/no_commits.csv','w') as f:
        writer = csv.writer(f,delimiter=',')
        writer.writerows(no)
if __name__ == '__main__':
	commit_listing('govbr','barra.govbr')

