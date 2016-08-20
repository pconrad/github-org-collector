#!/usr/bin/python

import os
import getpass
import sys
import argparse

def makeDestinationDirectory(destination):
  if not os.access(destination, os.W_OK):
    os.mkdir(destination, 0700)

def repoMatchesWildcard(repo,repo_pattern):
   return True  # STUB!!!

from github import Github
from github import GithubException

DESCRIPTION='collect files from private github repos'

parser = argparse.ArgumentParser(description=DESCRIPTION)

parser.add_argument('org_name',help='github organization name')
parser.add_argument('repo_pattern',help='naming convention for repos (Python re syntax)')
parser.add_argument('file_pattern',help='naming convention for files to collect (Python re syntax)')

args = parser.parse_args()

username = raw_input('Username: ')
pw = getpass.getpass()
g = Github(username, pw, user_agent='PyGithub')

org = g.get_organization(args.org_name)

### CONTINUE FROM HERE

repos = org.get_repos()

for repo in repos:
  if repoMatchesWildcard(repo,args.repo_pattern):
    print(repo.name)
    
