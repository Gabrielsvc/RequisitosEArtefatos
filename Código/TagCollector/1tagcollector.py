# encode: utf-8
import os
import time
import io
import json
import requests
from requests.auth import HTTPBasicAuth
#Iterando chaves desconhecidas:
'''
for key,value in dict.iteritems():
	print(key,value)
Json eh um lista de dics [ {
iterar por el usando objeto.get('chave') para pegar valor
'''
# Problema com  umas quebras de linha zoadas em um commit, aparentemente elas sao apenas ignoradas/excluidas
# Como assegurar que peguemos todos os commits? navegando pelas paginas #page=X
# O que posso concatenar no link? per_page=100

def check_request():
	print("Checando")
	request_inicial = requests.get('https://api.github.com/rate_limit',
		auth=('Gabrielsvc', '94553cb22d5204f1e7da1d5f87918f5dec9ca44e'))
	conteudo = request_inicial.json()
	print('Acessos possiveis: ' + str(conteudo['rate']['limit'])+'\n'+
		'Acessos restantes: '+str(conteudo['rate']['remaining']))

def repo_catcher():
	repositorios = []
	requests.get('https://api.github.com/user', auth=HTTPBasicAuth('Gabrielsvc', '70015018g'))
	i = 1
	request = requests.get('https://api.github.com/search/repositories?page='+str(i)+'&q=gov%20br+in:name+created:%3E2014-01-01')
	repositorios_visitados = 0
	if request.ok:
		conteudo = request.json()
		#print ('Recolhendo tags de ' + str(conteudo.get('total_count')) +' repositorios')
		repositorios_total = int(conteudo.get('total_count'))
		while conteudo.get('items') and len(repositorios)< 10:
			for repositorio in conteudo.get('items'):
				link_repositorio = str('https://api.github.com/repos/'+str(repositorio['owner']['login'])+'/'+str(repositorio['name']+'/'))
				if(link_repositorio not in repositorios):
					repositorios.append(link_repositorio)
					repositorios_visitados += 1
			i += 1
			request = requests.get('https://api.github.com/search/repositories?page='+str(i)+'&q=gov%20br+in:name+created:%3E2014-01-01')
			conteudo = request.json()
	return repositorios
'''
Nome do arquivo: {repo}{tipo}{data}
Acessando issues: ''
Acessando commits: 'https://api.github.com/repos/'+user+'/'+repository+'/commits?page='+str(i)+'&per_page=100')
Acessando readme:
'''
def writting_files(repositorios):

	timeAcesso = time.ctime()
	timeAcesso = timeAcesso.replace('  ','')
	timeAcesso = timeAcesso.replace(' ','_')
	timeAcesso = timeAcesso.replace('.','_')
	timeAcesso = timeAcesso.replace(':','_')
	user = 'Gabrielsvc'
	token = '94553cb22d5204f1e7da1d5f87918f5dec9ca44e'
	
	#request = "https://api.github.com/?access_token=94553cb22d5204f1e7da1d5f87918f5dec9ca44e"
	#requests.get(request)

	#Token: 94553cb22d5204f1e7da1d5f87918f5dec9ca44e
		
	for i in repositorios:
		with io.open('01_Erros.txt','a',encoding='utf-8') as arquivo_erros:
			requests_disponiveis = requests.get('https://api.github.com/rate_limit',auth=(user,token))
			conteudo = requests_disponiveis.json()
			
			repo_name = i.split('/')[5]
			repo_user = i.split('/')[4]
			print('Pegando repositorio: '+ str(repo_name) + ' de '+ str(repositorios.index(i)+1)+'/'+str(len(repositorios)))	
			#print('Recolhendo de Repositorio '+ str(repositorios.index(i)) +': '+str(repo_name))
			if(int(conteudo['rate']['remaining']) == 0):
				print('Limite de requisicoes estourado, parando no repositorio'+
					str(repositorios.index(i))+
					 ' '+
					 str(repo_name))
				return

			requestIssues = requests.get(i+'issues?state=all&page=1',auth=(user,token))
			requestCommits = requests.get(i+'commits?page=1',auth=(user,token))
			requestReadme =  requests.get(i+'readme',auth=(user,token))
			
			page = 1

			arq_issues = repo_name+'_'+repo_user+'_'+'issues'+'_'+timeAcesso+'.txt'
			arq_issues.replace(" ","")
			arq_readme = repo_name+'_'+repo_user+'_'+'readme'+'_'+timeAcesso+'.txt'
			arq_readme.replace(" ","")
			arq_commits = repo_name+'_'+repo_user+'_'+'commits'+'_'+timeAcesso+'.txt'
			arq_commits.replace(" ","")
			#print 'Escrevendo readme'
			with io.open(arq_readme,'w',encoding='utf-8') as file:
				if requestReadme.ok:
					conteudoReadme = requestReadme.json()
					raw_content = conteudoReadme['download_url']
					raw_content = requests.get(raw_content,auth=(user,token))
					file.write(json.dumps(conteudoReadme,indent=4,sort_keys=True,ensure_ascii = False))
					file.write(raw_content.text)
				else:
					arquivo_erros.write(str(repositorios.index(i))+" "+ str(i) +' readme, erro: '+unicode(requestReadme.status_code)+'\n')
					file.write('Erro: '+ unicode(requestReadme.status_code))	
			#print 'Escrevendo issues'
			with io.open(arq_issues,'w',encoding='utf-8') as file:
				if requestIssues.ok:		
					conteudoIssues = requestIssues.json()
					if(conteudoIssues == []):
						file.write(unicode('vazio\n'))
					while conteudoIssues:
						file.write(json.dumps(conteudoIssues,indent=4,sort_keys=True,ensure_ascii=False))
						page += 1
						requestIssues = requests.get(i+"issues?state=all&page="+str(page),auth=(user,token))
						conteudoIssues = requestIssues.json()
				else:
					arquivo_erros.write(str(repositorios.index(i))+" "+ str(i)+' issues, erro: '+unicode(requestIssues.status_code)+'\n')
					file.write('Erro: '+ unicode(requestIssues.status_code))
			#print 'Escrevendo commits'
			with io.open(arq_commits,'w',encoding='utf-8') as file:
				if requestCommits.ok:
					page = 1
					conteudoCommits = requestCommits.json()
					if(conteudoCommits == []):
						file.write(unicode('vazio\n'))
					while conteudoCommits:
						file.write(json.dumps(conteudoCommits,indent=4,sort_keys=True,ensure_ascii=False))
						page += 1
						requestCommits = requests.get(i+"commits?page="+str(page),auth=(user,token))
						conteudoCommits = requestCommits.json()
				else:
					arquivo_erros.write(str(repositorios.index(i))+ " "+str(i)+' commits, erro: '+unicode(requestCommits.status_code)+'\n')
					file.write('Erro: '+ unicode(requestCommits.status_code))

def tag_collector():
	print('Verificar requisicoes disponiveis?(1 = sim 2 = nao)')
	i = input()
	if(i == 1):
		check_request()
		return
	if(i == 2):	
		repositorios = repo_catcher()
		writting_files(repositorios)
		return



if __name__ == '__main__':
	tag_collector()
	