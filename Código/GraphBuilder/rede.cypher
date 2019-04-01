//------------Issues
//cat rede.cypher | bin/cypher-shell -u neo4j -p admin


// CLEAN UP
match (n) detach delete (n);

load csv with headers from "file:///no_issues.csv" as row
create(n:issues)
set n = row,
    n.identificador = row.identificador,
    n.number = row.number,
    n.closed_at = row.closed_at,
    n.title = row.title,
    n.comments = row.comments,
    n.state = row.state,
    n.body = row.body,
    n.updated_at = row.updated_at,
    n.locked = row.locked,
    n.created_at = row.created_at,
    n.milestones = row.milestones,
    n.html_url = row.html_url,
    n.label_id = row.label_id,
    n.user_login = row.user_login,
    n.assignee_login = row.assignee_login;

//------------Labels
load csv with headers from "file:///no_labels.csv" as row
create(n:labels)
set n = row,
	n.identificador = row.identificador,
	n.name = row.name,
	n.color = row.color;

//------------Organization
load csv with headers from "file:///no_organization.csv" as row
create(n:organization)
set n =row,
	n.nome = row.nome,
	n.descricao = row.descricao,
	n.members = row.members;

//------------milestones
load csv with headers from "file:///no_milestones.csv" as row
create(n:milestones)
set n = row,
	n.html = row.html,
	n.id = row.id,
	n.number = row.number,
	n.state = row.state,
	n.title = row.title,
	n.description = row.description,
	n.open_issues = toInt(row.open_issues),
	n.closed_issues = toInt(row.closed_issues),
	n.created_at = row.created_at,
	n.updated_at = row.updated_at,
	n.closed_at = row.closed_at,
	n.due_on = row.due_on,
	n.labels_link = row.labels_link,
	n.creator_login = row.creator_login;

//-----------pull_request
load csv with headers from "file:///no_pull_requests.csv" as row
create(n:pull_requests)
set n = row,
	n.id = row.id,
	n.html_url = row.html_url,
	n.issue_url = row.issue_url,
	n.number = row.number,
	n.state = row.state,
	n.locked = row.locked,
	n.title = row.title,
	n.user_login = row.user_login,
	n.body = row.body,
	n.created_at = row.created_at,
	n.updated_at = row.updated_at,
	n.closed_at = row.closed_at,
	n.merged_at = row.merged_at,
	n.merge_commit_sha = row.merge_commit_sha,
	n.assignees = row.assignees,
	n.requested_reviewers = row.requested_reviewers,
	n.labels = row.labels,
	n.milestone = row.milestone,
	n.commits_url = row.commits_url;

//-----Repository
load csv with headers from "file:///no_repository.csv" as row
create(n:repository)
set n = row,
	n.id = row.id,
	n.name = row.name,
	n.full_name = row.full_name,
	n.owner = row.owner,
	n.private = row.private,
	n.description = row.description,
	n.fork = row.fork,
	n.fork_count = row.fork_count,
	n.keys_url = row.keys_url,
	n.assignees = row.assignees,
	n.comments = row.comments;

//----- Branches
load csv with headers from "file:///no_branch.csv" as row
create(n:branch)
set n = row,
	n.name = row.name,
	n.commit_link = row.commit_link,
	n.branch_protection = row.branch_protection;

//---- Colaborators
//login,pull_permission,push_permission,admin_permission
LOAD CSV WITH HEADERS FROM "file:///no_users_collaborators.csv" AS row
CREATE (n:Users_colaborators)
SET n = row,
	n.login = row.login,
    n.pull_permission = row.pull_permission,
    n.push_permission = row.push_permission,
    n.admin_permission = row.admin_permission;

//-----Contributors
LOAD CSV WITH HEADERS FROM "file:///no_users_contributors.csv" AS row
CREATE (n:Users_contributors)
SET n = row,
    n.login = row.login,
    n.id = row.id,
    n.html_url = row.html_url,
    n.type = row.type,
    n.public_repos = row.public_repos;

//-----Commit
LOAD CSV WITH HEADERS FROM "file:///no_commits.csv" AS row
CREATE (n:Commits)
SET n = row,
    n.sha = row.sha,
    n.author_name = row.author_name,
    n.author_email = row.author_email,
    n.author_date = row.author_date,
    n.commiter_email = row.commiter_email,
    n.message = row.message,
    n.comment_count = row.comment_count,
    n.parent = row.parent,
    n.author_login = row.author_login;

//----- Team
LOAD CSV WITH HEADERS FROM "file:///no_teams.csv" AS row
CREATE(n:Teams)
SET n = row,
	n.id = row.id ,
	n.name = row.name,
	n.permission = row.permission,
	n.members = row.members;

CREATE (n:User_external)
set n.login = 'external_user';

//----------MATCHES
//------Issues x Labels
match (i:issues),(l:labels)
where i.label_id contains toString(l.identificador)
create (i)-[:possui_label]->(l);

//-----Milestones X Issues
match (i:issues),(m:milestones)
where toString(i.milestones) contains toString(m.id)
create (m)-[:contains]->(i);

//-----Milestone x Pull_request
match (p:pull_requests),(m:milestones)
where m.id = p.milestone
create (m)-[:contains]->(p);

//----User x Issue (creator)
match (uc:Users_contributors),(i:issues)
where uc.login = i.user_login
create (i)-[:Criada_por]->(uc);

//---- User x Issue (assignee)
match (uc:Users_contributors),(i:issues)
where i.assignee_login contains toString(uc.id)
create (uc)-[:assignee]->(i);

//---- User x Milestone (creator)
match (uc:Users_contributors),(m:milestones)
where m.creator_login = uc.login
create (uc)-[:criou]->(m);

//---- User x Pull_request (creator)
match (uc:Users_contributors),(pr:pull_requests)
where pr.user_login = uc.login
create (uc)-[:criou]->(pr);

//---- User x Pull_request (assignee)
match (uc:Users_contributors),(pr:pull_requests)
where pr.assignees = uc.login
create (pr)-[:assignee]->(uc);

//---- User x Pull_request (requested_reviewer)
match (u),(pr:pull_requests)
where pr.requested_reviewers contains u.login
create (pr)-[:requested_reviewer]->(u);

//---- Commits x Pull_request (merge_commit_sha)
match (c:Commits),(pr:pull_requests)
where pr.merge_commit_sha = c.sha
create (pr)-[:merge_commit]->(c);

//---- Commits x Pull_request (commits_url)
match (c:Commits),(pr:pull_requests)
where pr.merge_commits_url contains c.sha
create (pr)-[:composto_por]->(c);

//---- label x Pull_request
match (l:labels),(pr:pull_requests)
where pr.labels contains l.identificador
create (l)-[:labels]->(pr);

//---- User x Commit(author_login)
match(uc:Users_contributors),(c:Commits)
where uc.login contains c.author_login
create (uc)-[:criou]->(c);

//---- User_External x Commits
match(ue:User_external),(c:Commits)
where not ()-[:criou]->(c)
create (ue)-[:criou]->(c);

//---- User_External x Issues
Match (i:issues),(u:User_external)
where not (i)-[:Criada_por]->()
create (i)-[:Criada_por]->(u);

//---- User_External x pull_request
Match (pr:pull_requests),(u:User_external)
where not ()-[:criou]->(pr)
create (u)-[:criou]->(pr);

create index on :Commits(codigo);

create index on :issues(identificador);

create index on :labels(identificador);

create index on :milestones(identificador);

create index on :pull_requests(identificador);
/*
//---- Consultas
//--- Issues abertas
match (n:issues),(r) where n.state = 'open'
return (n)-[]-(r);

//--- Usuario e artefatos
match (n:Users_contributors),(m) where n.login='caduvieira'
return (n)-[]-(m);

match (n),(m) where
exists(n.created_at) or exists(n.author_date) and n.created_at<=('2016-01-29T00:00:00Z') and (n.created_at >= '2015-01-29T00:00:00Z') or n.author_date<= ('2016-01-29T00:00:00Z') and (n.author_date >=
'2015-01-29T00:00:00Z')
return (n)-[]-(m);
*/
