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



def processAllFilesInDirectory(repo,dir,fn):
  ''' 
  call function f(repo,dirent) for every file or directory in path 

  in fn, 
     f.name is the filename, 
     f._path.value is the full path of the file
     f._type.value is u'file' or u'dir'

     Other values: '_encoding', '_type', '_sha', '_content', '_headers', '_rawData',
                  '_name', '_html_url', '_repository', '_requester', '_url', '_git_url', 
                  '_size', '_CompletableGithubObject__completed', '_path'

     f._rawData[u'download_url']
     f._rawData[u'size']

  '''
  dirents = repo.get_dir_contents(dir)
  for f in dirents:
     if f._type.value == u'dir':
        processAllFilesInDirectory(repo,f._path.value,fn)
     else:
        fn(repo,f)

def downloadIfFileMatchesRe(args, g, repo, f):
  result = re.match(args.file_re,f._path.value)
  if result:
    print f._path.value, " matches ", args.file_re
    path = f._path.value
    downloadFile(args, g, repo, f._path.value, f._rawData[u'download_url'])

def processRepo(args, g, repo):
  processFile = lambda repo, f : downloadIfFileMatchesRe(args, g, repo, f)  
  processAllFilesInDirectory(repo,"/",processFile)

def downloadFile(args, g, repo, path, download_url):

  thisRepoDestination = os.path.join(args.destination,repo.name)    
  dirToStoreItIn = os.path.join(thisRepoDestination,os.path.dirname(path))
  makeDestinationDirectory(dirToStoreItIn)
    
  whereToStoreIt = os.path.join(thisRepoDestination,path)
    
  print "Downloading from " + repo.name + " to " + whereToStoreIt
  try:
    mode = 'b' if args.binary else ''
    downloadFileToDestination(download_url, whereToStoreIt, mode=mode)
  except: 
    print "Error downloading " + path + " from repo " + repo.name + " to " + args.destination
    print "Download URL:" + download_url
    print "Unexpected error:", sys.exc_info()[0]
    
def handleArgs():
  parser = argparse.ArgumentParser(description=DESCRIPTION)

  parser.add_argument('org_name',help='github organization name')
  parser.add_argument('repo_pattern',help='naming convention for repos (Python re syntax)')
  parser.add_argument('file_re',help='regular expression in Python syntax for matching files')
  parser.add_argument('destination',help='where to put the files retrieved')
  parser.add_argument('-b', '--binary',action='store_true',
                      help='treat file contents as binary instead of text')
  
  args = parser.parse_args()
  return args

def setupGithub():
  username = raw_input('Username: ')
  pw = getpass.getpass()
  g = Github(username, pw, user_agent='PyGithub')
  return g

      
def main():

  args = handleArgs()
  print "args.file_re=", args.file_re
  g = setupGithub()
  org = g.get_organization(args.org_name)
  repos = org.get_repos()
  
  makeDestinationDirectory(args.destination)
  
  for repo in repos:
    if repoMatchesWildcard(repo,args.repo_pattern):
      processRepo(args, g, repo)


if __name__ == "__main__":
  main()



