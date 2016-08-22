#!/usr/bin/python

import os
import getpass
import sys
import argparse
import re

import urllib2
import pycurl



import shutil

import requests


def makeDestinationDirectory(destination):
  if not os.access(destination, os.W_OK):
    os.mkdir(destination, 0700)

def repoMatchesWildcard(repo,repo_pattern):
   return re.match(repo_pattern,repo.name)

def html_url_to_raw_url(html_url):
  result = html_url.replace("github.com","raw.githubusercontent.com")
  result = result.replace("/blob","")
  return result

def getDownloadUrl(repo,path):
  ''' repo is a PyGithub Repository object, path is a string.  May throw GithubException. '''

  result = repo.get_file_contents(path)
  return result.raw_data['download_url']

def downloadFileToDestination(url,filename,mode=''):
  # From http://stackoverflow.com/questions/4589241/downloading-files-from-an-http-server-in-python

  response = urllib2.urlopen(url).read()
  fp = open(filename, "w" + mode)
  curl = pycurl.Curl()
  curl.setopt(pycurl.URL, url)
  curl.setopt(pycurl.WRITEDATA, fp)
  curl.perform()
  curl.close()
  fp.close()

'''
def downloadFileToDestination(url,destination,mode=''):

  # From: http://stackoverflow.com/questions/13137817/how-to-download-image-using-requests
  #   set mode to 'b' for binary files

  response = requests.get(url, stream=True)
  with open(destination, 'w' + mode) as out_file:
    shutil.copyfileobj(response.raw, out_file)
  del response
'''

from github import Github
from github import GithubException

DESCRIPTION='collect files from private github repos'

parser = argparse.ArgumentParser(description=DESCRIPTION)

parser.add_argument('org_name',help='github organization name')
parser.add_argument('repo_pattern',help='naming convention for repos (Python re syntax)')
parser.add_argument('path',help='path, relative to repo, of file to get')
parser.add_argument('destination',help='where to put the files retrieved')
parser.add_argument('-b', '--binary',action='store_true',
                    help='treat file contents as binary instead of text')

args = parser.parse_args()

username = raw_input('Username: ')
pw = getpass.getpass()
g = Github(username, pw, user_agent='PyGithub')

org = g.get_organization(args.org_name)

### CONTINUE FROM HERE

repos = org.get_repos()

makeDestinationDirectory(args.destination)

for repo in repos:
  if repoMatchesWildcard(repo,args.repo_pattern):
    try:
      download_url = getDownloadUrl(repo, args.path)
    
      thisRepoDestination = os.path.join(args.destination,repo.name)

      dirToStoreItIn = os.path.join(thisRepoDestination,os.path.dirname(args.path))
      whereToStoreIt = os.path.join(thisRepoDestination,args.path)
      makeDestinationDirectory(dirToStoreItIn)

      mode = 'b' if args.binary else ''

      print "Downloading from " + repo.name
      downloadFileToDestination(download_url, whereToStoreIt, mode=mode)
    except GithubException as ghe:
      print "Error: unable to access " + args.path + " in repo " + repo.name
    except: 
      print "Error downloading " + args.path + " from repo " + repo.name + " to " + args.destination
      print "Unexpected error:", sys.exc_info()[0]
    




