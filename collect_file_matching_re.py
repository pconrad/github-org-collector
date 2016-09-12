#!/usr/bin/env python

from __future__ import print_function

import os
import getpass
import sys
import traceback
import argparse
import re

import urllib2
import pycurl

DEBUG = 1  # global, set by argparse from args.debug

import shutil

import requests


def makeDestinationDirectory(destination):
  if not os.access(destination, os.W_OK):
    os.makedirs(destination, 0700)

def repoMatchesWildcard(repo,repo_pattern,args):
   return re.match(repo_pattern,repo.name,0 if args.case_sensitive else re.IGNORECASE)

def html_url_to_raw_url(html_url):
  result = html_url.replace("github.com","raw.githubusercontent.com")
  result = result.replace("/blob","")
  return result

def filename_that_wont_clobber_existing_file(destinationDir, filename):

  filename_only, extension_only = os.path.splitext(filename)
  extra = ""
  iteration=0
  fullpath = os.path.join(destinationDir,filename_only+extension_only)
  (DEBUG < 3) or print("checking fullpath=" + fullpath)
  while os.path.exists(fullpath):
    iteration += 1
    extra = "_" + str(iteration)
    fullpath = os.path.join(destinationDir,filename_only+extra+extension_only)
  if extra!="":
    (DEBUG < 1) or print ("WARNING: renaming " + filename + " to " + fullpath + " to avoid overwriting existing file in destination")
  
  return os.path.join(destinationDir,filename_only+extra+extension_only)

def downloadFileToDestination(url,destinationFullPath,filename,repo,mode=''):
  # From http://stackoverflow.com/questions/4589241/downloading-files-from-an-http-server-in-python

  try:
    response = urllib2.urlopen(url).read()
    (DEBUG < 3 ) or  print ("download file: response ok" )

    fp = open(destinationFullPath, "w" + mode)
    (DEBUG < 3 ) or print ("download file: open ok" )
    
    curl = pycurl.Curl()
    curl.setopt(pycurl.URL, url)
    curl.setopt(pycurl.WRITEDATA, fp)
    curl.perform()
    curl.close()
    fp.close()
    (DEBUG < 1) or print ("Downloaded " + filename + " from " + repo.name + " to " + destinationFullPath)
  except:
    traceback.print_exc(file=sys.stdout)
    raise

from github import Github
from github import GithubException

DESCRIPTION='collect files from private github repos'



def processAllFilesInDirectory(repo,directory,fn):
  ''' 
  call function f(repo,f) for every file or directory in path 

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
  try:
    dirents = repo.get_dir_contents(directory)
  except GithubException as ghe:
    print ("could not get directory contents of ",directory," for repo ",repo.name)
    return

  for f in dirents:
     if f._type.value == u'dir':
        processAllFilesInDirectory(repo,f._path.value,fn)
     else:
        fn(repo,f)

def downloadIfFileMatchesRe(args, g, repo, f):
  name = f.name
  (DEBUG < 2) or print ("filename = " + name)
  result = re.match(args.file_re, f._path.value, 0 if args.case_sensitive else re.IGNORECASE)
  if result:
    (DEBUG < 2) or print (f._path.value, " matches ", args.file_re)
    path = f._path.value
    downloadFile(args, g, repo, f._path.value, f._rawData[u'download_url'], name)

def processRepo(args, g, repo):
  processFile = lambda repo, f : downloadIfFileMatchesRe(args, g, repo, f)  
  processAllFilesInDirectory(repo,"/",processFile)

def downloadFile(args, g, repo, path, download_url, filename):

  #thisRepoDestination = os.path.join(args.destination,repo.name)    
  #dirToStoreItIn = os.path.join(thisRepoDestination,os.path.dirname(path))
  #makeDestinationDirectory(dirToStoreItIn)
  #whereToStoreIt = os.path.join(thisRepoDestination,path)

  whereToStoreIt = filename_that_wont_clobber_existing_file(args.destination,filename)
    
  (DEBUG < 2) or print ("Downloading from " + repo.name + " to " + whereToStoreIt)
  try:
    mode = 'b' if args.binary else ''
    downloadFileToDestination(download_url, whereToStoreIt, filename, repo, mode=mode)
  except: 
    print ("Error downloading " + path + " from repo " + repo.name + " to " + whereToStoreIt)
    print ("Download URL:" + download_url)
    print ("Unexpected error:", sys.exc_info()[0])
    
def handleArgs():
  global DEBUG
  parser = argparse.ArgumentParser(description=DESCRIPTION)

  parser.add_argument('org_name',help='github organization name')
  parser.add_argument('repo_pattern',help='naming convention for repos (Python re syntax)')
  parser.add_argument('file_re',help='regular expression in Python syntax for matching files')
  parser.add_argument('destination',help='where to put the files retrieved')
  parser.add_argument('-b', '--binary',action='store_true', default=False, 
                      help='treat file contents as binary instead of text')
  parser.add_argument('-c', '--case_sensitive',action='store_true', default=False, 
                        help='do a case sensitive match on re (default is case insensitive so that .PDF and .pdf are treated the same)')
  parser.add_argument('-d', '--debug', type=int, default=1,
                      help='debug level; 0=silent 1=basic logging, 2=help with re matching, 3=diagnostics')
  
  args = parser.parse_args()
  DEBUG = args.debug
  return args

def setupGithub():
  username = raw_input('Username: ')
  pw = getpass.getpass()
  g = Github(username, pw, user_agent='PyGithub')
  return g

      
def main():

  args = handleArgs()
  (DEBUG < 2) or print ("args.file_re=", args.file_re)
  (DEBUG < 3) or print ("args=" + repr(args))
  g = setupGithub()
  org = g.get_organization(args.org_name)
  repos = org.get_repos()
  
  makeDestinationDirectory(args.destination)
  
  for repo in repos:
    if repoMatchesWildcard(repo,args.repo_pattern,args):
      (DEBUG < 2) or print (repo.name," matches args.repo_pattern: ",args.repo_pattern      )
      processRepo(args, g, repo)
    else:
      (DEBUG < 2) or print (repo.name," does not match args.repo_pattern: ",args.repo_pattern)


if __name__ == "__main__":
  main()



