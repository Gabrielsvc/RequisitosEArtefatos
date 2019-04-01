# encode: utf-8
import os
import time
import json
import requests
import csv
from requests.auth import HTTPBasicAuth
key_list = []
rede_chaves = open('rede.txt','a')
rede_chaves_consulta = open("rede.txt","r")

def gitApireader():
	requests.get('https://api.github.com/user', auth=HTTPBasicAuth('Gabrielsvc', '70015018g'))
	
	tag = "Activities"
	if(checkIfNotRead(tag)):
		rede_chaves.write('Activities\n')
		tag = 'events'
		if checkIfNotRead(tag):
			request = requests.get('https://api.github.com/repos/govbr/barra.govbr/events')
			rede_chaves.write('\t'+tag+'\n')
			readrequest(request)
		
		tag = 'notifications'
		if checkIfNotRead(tag):
			request = requests.get('https://api.github.com/repos/govbr/barra.govbr/notifications')
			rede_chaves.write('\tnotifications\n')
			readrequest(request)

		tag = 'stargazers'
		if checkIfNotRead(tag):	
			request = requests.get('https://api.github.com/repos/govbr/barra.govbr/stargazers')
			rede_chaves.write('\tstargazers\n')
			readrequest(request)
		
		tag = 'watchers'
		if checkIfNotRead(tag):
			request = requests.get('https://api.github.com/repos/govbr/barra.govbr/subscribers')
			rede_chaves.write('\twatchers\n')
			readrequest(request)

	tag = "Gist"
	if(checkIfNotRead(tag)):
		rede_chaves.write('Gist\n')
		request = requests.get('https://api.github.com/gists/public')
		readrequest(request)

	tag = "Git Data"
	if(checkIfNotRead(tag)):
		rede_chaves.write('Git Data\n')
		
		tag = "blob"
		if(checkIfNotRead(tag)):
			rede_chaves.write('\tblob\n')
			request = requests.get('https://api.github.com/repos/govbr/barra.govbr/git/blobs')
			readrequest(request)
		
		tag = "commitDATA"
		if checkIfNotRead(tag):
			request = requests.get('https://api.github.com/repos/govbr/barra.govbr/commits')
			rede_chaves.write('\tcommitDATA\n')
			readrequest(request)
		
		tag = "referenceDATA"
		if(checkIfNotRead(tag)):
			request = requests.get("https://api.github.com/repos/govbr/barra.govbr/git/refs")
			rede_chaves.write("\treferenceDATA\n")
			readrequest(request)
		
		tag = "tagsDATA"
		if(checkIfNotRead(tag)):
			request = requests.get("https://api.github.com/repos/govbr/barra.govbr/git/refs/tags")
			rede_chaves.write("\t"+tag+"\n")
			readrequest(request)
	
		tag = 'treeDATA'
		if checkIfNotRead(tag):
			request =requests.get('https://api.github.com/repos/govbr/barra.govbr/git/trees/5a747249732f5025bac6dc4b1b91e826a96f8630')
			rede_chaves.write("\t"+tag+"\n")
			readrequest(request)

	tag = 'Issues'
	if checkIfNotRead(tag):
		request =requests.get('https://api.github.com/repos/govbr/barra.govbr/issues')
		rede_chaves.write("\t"+tag+"\n")
		readrequest(request)

		tag = 'assignees'
		if checkIfNotRead(tag):
			request =requests.get('https://api.github.com/repos/govbr/barra.govbr/assignees')
			rede_chaves.write("\t"+tag+"\n")
			readrequest(request)

		tag = 'commentsISSUES'
		if checkIfNotRead(tag):
			request =requests.get('https://api.github.com/repos/govbr/barra.govbr/issues/comments')
			rede_chaves.write("\t"+tag+"\n")
			readrequest(request)

	tag = 'codes_of_conduct'
	if checkIfNotRead(tag):
		request =requests.get('https://api.github.com/codes_of_conduct')
		rede_chaves.write("\t"+tag+"\n")
		readrequest(request)

	tag = "pulls"
	if checkIfNotRead(tag):
		request =requests.get('https://api.github.com/repos/tensorflow/tensorflow/pulls')
		rede_chaves.write("\t"+tag+"\n")
		readrequest(request)

	tag = "repositories"
	if checkIfNotRead(tag):
		request =requests.get('https://api.github.com/repositories')
		rede_chaves.write("\t"+tag+"\n")
		readrequest(request)

	tag = "commentsREPO"
	if checkIfNotRead(tag):
		request =requests.get('https://api.github.com/repos/govbr/barra.govbr/comments')
		rede_chaves.write("\t"+tag+"\n")
		readrequest(request)

	tag = "commitsREPO"
	if checkIfNotRead(tag):
		request =requests.get('https://api.github.com/repos/govbr/barra.govbr/commits')
		rede_chaves.write("\t"+tag+"\n")
		readrequest(request)

	tag = "forksREPO"
	if checkIfNotRead(tag):
		request =requests.get('https://api.github.com/repos/xx45/dayjs/forks')
		rede_chaves.write("\t"+tag+"\n")
		readrequest(request)
	
	tag = "releasesREPO"
	if checkIfNotRead(tag):
		request =requests.get('https://api.github.com/repos/xx45/dayjs/releases')
		rede_chaves.write("\t"+tag+"\n")
		readrequest(request)


	rede_chaves.close()
"""	tag = 'commits'
	if checkIfNotRead(tag):
		request = requests.get('https://api.github.com/repos/govbr/barra.govbr/commits')
		rede_chaves.write('\tcommits\n')
		readrequest(request)
"""
	

def checkIfNotRead(tag):
	if(tag in rede_chaves_consulta.read()):
		rede_chaves_consulta.seek(0)
		return False
	else :
		rede_chaves_consulta.seek(0)
		return True

def readrequest(request):
	if request.ok:
		conteudo = request.json()
		if(len(conteudo) > 1):
			rede_chaves.write('\t\tLIST\n')
		for item in conteudo:
			prettyfy(item)
	del key_list[:] 
	
	
def prettyfy(d, indent = 2):
	for key,value in d.items():
		if(key not in key_list):
			rede_chaves.write('\t'*indent +str(key)+'\n')
			key_list.append(key)
			if isinstance(value,dict):
				key_list.append(key)
				prettyfy(value,indent+1)

if __name__ == '__main__':
	gitApireader()
