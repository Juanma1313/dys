"""
Exports Issues from a specified repository to a CSV file

Uses basic authentication (Github username + password) to retrieve Issues
from a repository that username has access to. Supports Github API v3.
"""
import csv
import requests


#GITHUB_USER = ''
#GITHUB_PASSWORD = ''
REPO = 'Juanma1313/dys'  # format is username/repo
#ISSUES_FOR_REPO_URL = 'https://api.github.com/repos/%s/issues' % REPO
#AUTH = (GITHUB_USER, GITHUB_PASSWORD)

from github import Github
token=Github()
r = token.get_repo(REPO)
issues=r.get_issues(state='open')

def write_issues(issues):
    "output a list of issues to csv"
    for issue in issues:
        csvout.writerow([issue.number, issue.title, issue.body, issue.created_at, issue.updated_at, issue.labels, issue.milestone, issue.state])


#r = requests.get(ISSUES_FOR_REPO_URL, auth=AUTH)
csvfile = '%s-issues.csv' % (REPO.replace('/', '-'))
csvout = csv.writer(open(csvfile, 'w'), dialect='excel', quoting=csv.QUOTE_ALL)
csvout.writerow(['id', 'Title', 'Body', 'Created At', 'Updated At', 'Labels', 'milestone', 'State'])
write_issues(issues)
