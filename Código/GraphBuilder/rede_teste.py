# encoding: utf-8
import os
import time
import json
import requests
import csv
import sys
#Mudando para o uso da api do git. Referencias no codigo do Allan e documentacao do github
#Iterando chaves desconhecidas:
'''
for key,value in dict.iteritems():
	print(key,value)

iterar pelo json usando objeto.get('chave') para pegar valor
'''
# O que posso concatenar no link? per_page=100, page= , ...
#Access Token
at = 'd489f3bef2401fef8d99909ac3e1aa370ed594ea' # You will need a new Access Token!
dl = '&since=2015-07-17T15:00:00Z'
def execute(user,repository,at_used):
	global at
	at = at_used
	#issues_listing(user,repository)
	print('issues listed')
	#labels_listting(user,repository)
	print('labels listed')
	#milestones_listting(user,repository)
	print('milestones listed')
	#organization_listting(user,repository)
	print('organization listed')
	#pull_request_listting(user,repository)
	print('Pull requests listed')
	#repo_listting(user,repository)
	print('Repository listed')
	#team_listting(user,repository)
	print('teams listed')
	commit_listing(user,repository)
	print('Commits Listed')

no_issues = [["identificador","number","closed_at","title","comments",
			"state","body","updated_at","locked","created_at","milestones",
			"html_url","label_id","user_login","assignee_login"]]
def issues_listing(user,repository):
	page = 1
	request = requests.get('https://api.github.com/repos/'+user+'/'
		+repository+'/issues?state=all&page='+str(page)+dl+'&per_page=100'
		+'&access_token='+ at)
	if request.ok:
		conteudo = request.json()
		while(conteudo):
			for issue in conteudo:
				novo_no = []
				novo_no.append(issue.get('id',-1))
				novo_no.append(issue.get('number',-1))
				if issue.get('closed_at') == None:
					novo_no.append('null')
				else:
					novo_no.append(issue.get('closed_at',-1))
				novo_no.append(issue.get('title',-1).encode('utf-8'))
				novo_no.append(issue.get('comments',-1))
				novo_no.append(issue.get('state',-1))
				if issue.get('body'):
					string_formatada = str(issue.get('body',-1).encode('utf-8'))
					string_formatada = string_formatada.replace('\r', '')
					string_formatada = string_formatada.replace('\n', '')
					string_formatada = string_formatada.replace('"', '')
					string_formatada = string_formatada.replace('\'', '')
					string_formatada = string_formatada.replace(',', ';')
				else:
					string_formatada = ' '
				novo_no.append(string_formatada)
				novo_no.append(issue.get('updated_at',-1))
				novo_no.append(issue.get('locked',-1))
				novo_no.append(issue.get('created_at',-1))
				milestones = []
				if(issue['milestone']):
					milestones.append(issue['milestone']['id'])
				novo_no.append(milestones)
				novo_no.append(issue.get('html_url',-1))
				b = []
				if issue.get('labels') :
					for i in issue.get('labels'):
						b.append(i.get('id',-1))
				novo_no.append(b)
				novo_no.append(issue['user']['login'])
				assignees = []
				if issue.get('assignees') :
					for i in issue.get('assignees'):
						assignees.append(i.get('id'))
				novo_no.append(assignees)
				no_issues.append(novo_no)
			page += 1
			request = requests.get('https://api.github.com/repos/'+user+'/'
		+repository+'/issues?state=all&page='+str(page)+dl+'&per_page=100'
		+'&access_token='+ at)
			conteudo = request.json()

	else:
		print('Request nao foi efetivado')

	with open('/home/gabsvc/Downloads/neo4j-community-3.3.2/import/no_issues.csv','w') as f:
		writer = csv.writer(f,delimiter=',')
		writer.writerows(no_issues)


no_label = [["identificador","name","color"]]
def labels_listting(user,repository):
	page = 1
	request = requests.get('https://api.github.com/repos/'+user+'/'
		+repository+'/labels?page='+str(page)+'&per_page=100'
		+'&access_token='+ at)
	if request.ok:
		conteudo = request.json()
		while(conteudo):
			for label in conteudo:
				novo_no = []
				novo_no.append(label.get('id'))
				novo_no.append(label.get('name').encode('utf-8'))
				novo_no.append(label.get('color'))
				no_label.append(novo_no)
			page += 1
			request = requests.get('https://api.github.com/repos/'+user+'/'
			+repository+'/labels?page='+str(page)+'&per_page=100'
			+'&access_token='+ at)
			conteudo = request.json()

	with open('/home/gabsvc/Downloads/neo4j-community-3.3.2/import/no_labels.csv','w') as f:
		writer = csv.writer(f,delimiter=',')
		writer.writerows(no_label)
no_milestones = [["html","id", "number", "state", "title","description",
				"open_issues","closed_issues","created_at","updated_at",
				"closed_at","due_on","labels_link","creator_login"]]

def milestones_listting(user,repository):
	page = 1
	request = requests.get('https://api.github.com/repos/'+user+'/'
		+repository+'/milestones?page='+str(page)+'&per_page=100'
		+'&access_token='+ at)
	if request.ok:
		conteudo = request.json()
		while(conteudo):
			for milestone in conteudo:
				novo_no = []
				novo_no.append(milestone.get('html_url'))
				novo_no.append(milestone.get('id'))
				novo_no.append(milestone.get('number'))
				novo_no.append(milestone.get('state'))
				novo_no.append(milestone.get('title').encode('utf-8'))
				if milestone.get('description') is None:
					novo_no.append('no description');
				else:
					novo_no.append(milestone.get('description').encode('utf-8'))
				novo_no.append(milestone.get('open_issues'))
				novo_no.append(milestone.get('closed_issues'))
				novo_no.append(milestone.get('created_at'))
				novo_no.append(milestone.get('updated_at'))
				novo_no.append(milestone.get('closed_at'))
				novo_no.append(milestone.get('due_on'))
				page_labels = 1
				requestLinks = requests.get(str(milestone.get('labels_url')+'?page='+str(page_labels))+'&access_token='+ at)
				if requestLinks.ok:
					MilestoneLabels = requestLinks.json()
					labelsId = []
					while(MilestoneLabels):
						for labels in MilestoneLabels:
							labelsId.append((labels.get('id')))
						page_labels += 1
						requestLinks = requests.get(milestone.get('labels_url')+'?page='+str(page_labels)+'&access_token='+ at)
						MilestoneLabels = requestLinks.json()
					novo_no.append(labelsId)
				novo_no.append(milestone['creator']['login'])
				no_milestones.append(novo_no)
			page += 1
			request = requests.get('https://api.github.com/repos/'+user+'/'
		+repository+'/milestones?page='+str(page)+'&per_page=100'
		+'&access_token='+ at)
			conteudo = request.json()

	with open('/home/gabsvc/Downloads/neo4j-community-3.3.2/import/no_milestones.csv','w') as f:
		writer = csv.writer(f,delimiter=',')
		writer.writerows(no_milestones)

# Preview para Blocked Users?
no_organization = [['nome', 'descricao', 'members']]
def organization_listting(user,repository):
	request = requests.get('https://api.github.com/repos/'+user+'/'
		+repository+'?access_token='+ at)
	if request.ok:
		conteudo = request.json()
		if conteudo['owner']['type'] == 'Organization':
			request_org = requests.get('https://api.github.com/orgs/'+
				conteudo['owner']['login']+'?access_token'+ at)
			conteudo = request_org.json()
			novo_no = []
			novo_no.append(conteudo['name'].encode('utf-8'))
			novo_no.append(conteudo['description'].encode('utf-8'))
			members_url = conteudo['members_url']
			members_url = members_url[:-9]
			request_members = requests.get(members_url +'?access_token'+ at)
			if request_members.ok:
				membros = []
				conteudo_membros = request_members.json()
				for user in conteudo_membros:
					membros.append(user['login'])
				novo_no.append(membros)


			no_organization.append(novo_no)

	with open('/home/gabsvc/Downloads/neo4j-community-3.3.2/import/no_organization.csv','w') as f:
		writer = csv.writer(f,delimiter=',')
		writer.writerows(no_organization)

def project_listting(user,repository):
	return true
	#Accept header problem

'''
"id","html_url","issue_url","number","state",
"locked","title","user_login","body","created_at",
"updated_at","closed_at","merged_at","merge_commit_sha",
"assignees","requested_reviewers","labels","milestone",
"commits_url"
'''
no_pull_request = [["id","html_url","issue_url","number","state",
					"locked","title","user_login","body","created_at",
					"updated_at","closed_at","merged_at","merge_commit_sha",
					"assignees","requested_reviewers","labels","milestone",
					"commits_url"]]

def pull_request_listting(user, repository):
	page = 1
	request = requests.get('https://api.github.com/repos/'+user+'/'+repository+'/pulls?page='+str(page)+'&state=all'+dl+'&access_token='+ at)
	if request.ok:
		conteudo = request.json()
		while(conteudo):
			for pull_request in conteudo:
				novo_no = []
				#Weird extra data here. Why im getting things that aren't pull requests??
				novo_no.append(pull_request['id'])
				novo_no.append(pull_request['html_url'])
				#Pegando issuesID para fazer link
				link = pull_request['issue_url']
				new_request = requests.get(link+'?access_token='+at)
				conteudo = new_request.json()
				novo_no.append(conteudo['id'])
				novo_no.append(pull_request['number'])
				novo_no.append(pull_request['state'])
				novo_no.append(pull_request['locked'])
				novo_no.append(pull_request['title'].encode('utf-8'))
				novo_no.append(pull_request['user']['login'])
				if pull_request['body'] is not None :
					novo_no.append(pull_request['body'].encode('utf-8'))
				else :
					novo_no.append('No body')
				novo_no.append(pull_request['created_at'])
				novo_no.append(pull_request.get('updated_at','sem update'))
				novo_no.append(pull_request.get('closed_at','nao fechada'))
				novo_no.append(pull_request.get('merged_at','sem merge'))
				novo_no.append(pull_request['merge_commit_sha'])
				assignees_login = []
				for user1 in pull_request.get('assignees'):
					assignees_login.append(user1['login'])
				novo_no.append(assignees_login)
				reviewers_login = []
				for user1 in pull_request.get('requested_reviewers'):
					reviewers_login.append(user1['login'])
				novo_no.append(reviewers_login)
				labels = []
				for label in pull_request.get('labels'):
					labels.append(label.get('id'))
				novo_no.append(labels)
				if pull_request['milestone']:
					novo_no.append(str(pull_request['milestone']['id']))
				else:
					novo_no.append('-1')
				request_commits = requests.get(pull_request['commits_url']+'?access_token='+ at)
				if request_commits.ok:
					conteudo = request_commits.json()
					commitsId = []
					for commit in conteudo:
						commitsId.append(commit['sha'])
					novo_no.append(commitsId)
				no_pull_request.append(novo_no)
			if len(no_pull_request) > 200:
				break
			page += 1
			request = requests.get('https://api.github.com/repos/'+user+'/'+repository+'/pulls?page='+str(page)+'&state=all'+dl+'&access_token='+ at)
			conteudo = request.json()

	with open('/home/gabsvc/Downloads/neo4j-community-3.3.2/import/no_pull_requests.csv','w') as f:
		writer = csv.writer(f,delimiter=',')
		writer.writerows(no_pull_request)

no_repository = [['id','name','full_name','owner','private','description',
				'fork','fork_count','keys_url','assignees','comments']]
def repo_listting(user,repository):
	page = 1
	request = requests.get('https://api.github.com/repos/'+
		user+'/'+repository+'?access_token='+ at)
	if request.ok:
		dado = request.json()
		novo_no = []

		novo_no.append(dado['id'])
		novo_no.append(dado['name'].encode('utf-8'))
		novo_no.append(dado['full_name'].encode('utf-8'))
		novo_no.append(dado['owner']['login'])
		novo_no.append(dado['private'])
		novo_no.append(dado['description'].encode('utf-8'))
		novo_no.append(dado['fork'])
		novo_no.append(dado['forks'])
		request_key = requests.get(dado['keys_url'][:-9])
		conteudo = request_key.json()
		if(conteudo['message']== 'Not Found'):
			keys = []
		else :
			keys = []
			for key in conteudo:
				keys.append(key['key'])
		novo_no.append(keys)
		collaborators_listting(user,repository)
		assignees = []
		page_assignees = 1
		request_as = requests.get(dado['assignees_url'][:-7]+'?page='+str(page_assignees)+'&access_token='+at)
		conteudo_assignees = request_as.json()
		while conteudo_assignees:
			for i in conteudo_assignees:
				assignees.append(i['login'])
			page_assignees += 1
			request_as = requests.get(dado['assignees_url'][:-7]+'?page='+str(page_assignees)+'&access_token='+at)
			conteudo_assignees = request_as.json()
		novo_no.append(assignees)
		novo_no.append(dado['comments_url'])
		print('assignees listed')
		branch_listting(user,repository)
		print('branches listed')
		users_listting_con(user,repository)
		print('contributors listed')
		no_repository.append(novo_no)



		with open('/home/gabsvc/Downloads/neo4j-community-3.3.2/import/no_repository.csv','w') as f:
			writer = csv.writer(f,delimiter=',')
			writer.writerows(no_repository)

		#Deploy keys?

no_branch = [['name','commit_link','branch_protection']]
def branch_listting(user,repository):
	page = 1
	request = requests.get('https://api.github.com/repos/'+	user+'/'+repository+'/branches?page='+str(page)+'&access_token='+ at)
	if request.ok:
		dados = request.json()
		while dados:
			for branch in dados:
				novo_no = []
				novo_no.append(branch['name'])
				novo_no.append(branch['commit']['url'])
				no_branch.append(novo_no)
			page += 1
			request = requests.get('https://api.github.com/repos/'+	user+'/'+repository+'/branches?page='+str(page)+'&access_token='+ at)
			dados = request.json()

	with open('/home/gabsvc/Downloads/neo4j-community-3.3.2/import/no_branch.csv','w') as f:
		writer = csv.writer(f,delimiter=',')
		writer.writerows(no_branch)

#-------------------------------------

no_users_collaborators = [['login','pull_permission','push_permission','admin_permission']]
def collaborators_listting(user,repository):
	page = 1
	request = requests.get('https://api.github.com/repos/'+
		user+'/'+repository+ '/collaborators'+'?page='+str(page)+
		'&per_page=100'+'&access_token='+ at)
	if request.ok:
		conteudo = request.json()
		while conteudo:
			for user1 in conteudo:
				novo_no =[]
				novo_no.append(user1['login'])
				novo_no.append(user1['permissions']['pull'])
				novo_no.append(user1['permissions']['push'])
				novo_no.append(user1['permissions']['admin'])
				no_users_collaborators.append(novo_no)
			page += 1
			request = requests.get('https://api.github.com/repos/'+
			user+'/'+repository+ '/collaborators'+'?page='+str(page)+
			'&per_page=100&access_token='+ at)
			conteudo = request.json()
	else:
		print('This token lacks access authorization to the info')

	with open('/home/gabsvc/Downloads/neo4j-community-3.3.2/import/no_users_collaborators.csv','w') as f:
		writer = csv.writer(f,delimiter=',')
		writer.writerows(no_users_collaborators)

	print('Collaborators listed')


no_user_contributors = [['login','id','html_url','type','public_repos']]

def users_listting_con(user,repository):
	page = 1
	request = requests.get('https://api.github.com/repos/'+
				user+'/'+repository+'/contributors'+'?page='+str(page)+
				'&per_page=100'+'&access_token='+ at)
	if request.ok:
		conteudo = request.json()
		while conteudo:
			for user_con in conteudo:
				novo_no = []
				novo_no.append(user_con['login'])
				novo_no.append(user_con['id'])
				novo_no.append(user_con['html_url'])
				novo_no.append(user_con['type'])
				request_user = requests.get(user_con['url']+'?access_token='+at)
				conteudo_userpage = request_user.json()
				novo_no.append(conteudo_userpage['public_repos'])
				no_user_contributors.append(novo_no)
			page += 1
			request = requests.get('https://api.github.com/repos/'+
				user+'/'+repository+'/contributors'+'?page='+str(page)+
				'&per_page=100'+'&access_token='+ at)
			conteudo = request.json()

	with open('/home/gabsvc/Downloads/neo4j-community-3.3.2/import/no_users_contributors.csv','w') as f:
		writer = csv.writer(f,delimiter=',')
		writer.writerows(no_user_contributors)


no_commit = [["sha","author_name","author_email","author_date",
				"commiter_email","message","comment_count","parent","author_login"]]

def commit_listing(user,repository):
	i = 1
	request = requests.get('https://api.github.com/repos/'+user+
			'/'+repository+'/commits?page='+str(i)+dl+'&per_page=100'+
			'&access_token='+at)
	if request.ok:
		conteudo = request.json()
		while(conteudo):
			for commit in conteudo:
				novo_no = []
				novo_no.append(commit.get('sha',-1))
				novo_no.append(commit.get('commit').get('author').get('name',-1).encode('utf-8'))
				novo_no.append(commit.get('commit').get('author').get('email'))
				novo_no.append(commit.get('commit').get('author').get('date',-1))
				novo_no.append(commit.get('commit').get('committer').get('email'))
				d = commit.get('commit').get('message',-1).replace('\n',' ').encode('utf-8')
				novo_no.append(d)
				novo_no.append(commit.get('commit').get('comment_count'))
				if(commit.get('parents')):
					e = commit.get('parents')[0].get('sha')
				else :
					e = 'none'
				novo_no.append(e)
				if commit.get('author'):
					novo_no.append(commit.get('author').get('login'))
				else :
					novo_no.append('-1')
				no_commit.append(novo_no)
			i+= 1
			request = requests.get('https://api.github.com/repos/'+user+
				'/'+repository+'/commits?page='+str(i)+dl+'&per_page=100'+
				'&access_token='+at)
			conteudo = request.json()
	else:
		print('Request nao foi efetivado')


	with open('/home/gabsvc/Downloads/neo4j-community-3.3.2/import/no_commits.csv','w') as f:
		writer = csv.writer(f,delimiter=',')
		writer.writerows(no_commit)


no_team = [['id','name','permission','members']]
def team_listting(user,repository):
	page=1
	request = requests.get('https://api.github.com/repos/'+	user+'/'+repository+'/teams?page='+str(page)+'&access_token='+ at)
	if request.ok:
		dados = request.json()
		while dados:
			for team in dados:
				novo_no = []
				novo_no.append(team['id'])
				novo_no.append(team['name'])
				novo_no.append(team['permission'])
				members = []
				page_members = 1
				link = team['members_url'][:-9]
				request_members = requests.get(link+'?page='+str(page_members)+'&access_token='+at)
				membros_time = []
				if request_members.ok:
					conteudo_membros = request_members.json()
					while conteudo_membros:
						for membro in conteudo_membros:
							membros_time.append(membro['login'])
						page_members += 1
						request_members = requests.get(link+'?page='+str(page_members)+'&access_token='+at)
						conteudo_membros = request_members.json()
				else:
					print(request_members.status_code)
				novo_no.append(membros_time)
				no_team.append(novo_no)
			page +=1
			request = requests.get('https://api.github.com/repos/'+	user+'/'+repository+'/teams?page='+str(page)+'&access_token='+ at)
			dados = request.json()
	with open('/home/gabsvc/Downloads/neo4j-community-3.3.2/import/no_teams.csv','w') as f:
		writer = csv.writer(f,delimiter=',')
		writer.writerows(no_team)


'''
[['id','name','full_name','owner','private','description',
				'fork','fork_count','keys_url','collaborators','teams',
				'assignees','branches','tags','contributors','commits',
				'comments','issues','issues','pulls','milestones','labels',
				'releases']]
'''

if __name__ == '__main__':
	if(len(sys.argv) == 4):
		execute(sys.argv[1],sys.argv[2],sys.argv[3])
	if(len(sys.argv) == 3):
		execute(sys.argv[1],sys.argv[2],at)
	else:
		execute('govbr','barra.govbr',at)
