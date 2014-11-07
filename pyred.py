#! /usr/bin/python
from urllib2 import urlopen
from sys import stdout
from time import sleep
import json
import argparse
import sys
import os

parser = argparse.ArgumentParser(description="Prints out the newest post from a subreddit.")
parser.add_argument('subreddit', metavar='C', type=str, nargs='*',
	help="Specify the subreddit to follow")
parser.add_argument('-s','--not_secure', dest='secure', action='store_const',
	const='http://', default='https://', help='Flag to disable https, defaults to https.')
parser.add_argument('-1','--once', dest='repeat', action='store_const',
	const=False, default=True, help='Flag to only run once')
parser.add_argument('-u', '--user', dest='username', default=None)
parser.add_argument('-f', '--feed', dest='feed', default=None)
args = vars(parser.parse_args())

secure=args['secure']
subreddit=args['subreddit'][0]

if args['feed']:
	feed=str("&feed="+args['feed'])
else: feed=""
if args['username']:
	username=str("&user="+args['username'])
else: username=""

redditurl="{0}www.reddit.com/r/{1}/new/.json?sort=new{2}{3}".format(secure,subreddit,feed,username)
temp=count=wwwcount=postcount=0

def termPad(input_string):
	columns = int(os.popen('stty size', 'r').read().split()[1])
	spaces = " "*(columns - len(input_string))
	return "{0}{1}".format(input_string, spaces)

def termTrim(title, comments):
	columns = int(os.popen('stty size', 'r').read().split()[1])
	maxLen = columns - len(comments) + 5
	return termPad("\r{0} - {1}".format(title[:maxLen],comments))

while True:
	try:
		feed = json.loads(urlopen(redditurl,timeout=10).read())
		wwwcount=0
	except:
		wwwcount+=1
		stdout.write( termPad("\r- HTTP error - " + str(sys.exc_info()[1]) + " " + str(wwwcount) ) )
		stdout.flush()
		sleep(30)
		continue
	try:
		jsonpost = feed['data']['children'][0]["data"]
		postcount=0
	except:
		postcount+=1
		stdout.write( termPad("\r - no new posts - " + str(postcount) ) )
		stdout.flush()
		sleep(60)
		continue
	pid = jsonpost["id"]
	comments = "{0}www.reddit.com/{1}".format(secure, pid)
	post = termTrim(jsonpost["title"],comments)
	if not (temp == pid):
		temp = pid
		count=0
		stdout.write( termPad(post) )
		stdout.flush()
	if not args['repeat']: break
	sleep(30)
