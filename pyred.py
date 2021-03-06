#! /usr/bin/python
# author: /u/rasputine
import urllib2
from sys import stdout
from time import sleep
import json
import argparse
from datetime import datetime
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
delay=2

secure=args['secure']
subreddit=args['subreddit'][0]

if args['feed']:
    feed=str("&feed="+args['feed'])
else: feed=""
if args['username']:
    username=str("&user="+args['username'])
else: username=""


hdr = { 'User-Agent' : 'pyred/1.0 by rasputine' }
redditurl="{0}www.reddit.com/r/{1}/new/.json?sort=new{2}{3}".format(secure,subreddit,feed,username)
req = urllib2.Request(redditurl, None, hdr)
temp=post=""

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def termPad(input_string):
    try: 
        columns = int(os.popen('stty size', 'r').read().split()[1])
    except:
        columns = 80
    spaces = " "*(columns - len(input_string))
    return u"{0}{1}".format(input_string, spaces)

def termTrim(title, comments, age):
    try: 
        columns = int(os.popen('stty size', 'r').read().split()[1])
    except:
        columns = 80
    maxLen = columns - len(comments) - len(age) - 4
    return termPad(u"\r{0} - {1} {2}".format(title[:maxLen],comments, age))
clear()
while True:
    try:
        feed = json.loads(urllib2.urlopen(req).read())
    except:
        clear()
        stdout.write( termPad("\r Error: " + str(sys.exc_info())) )
        stdout.flush()
        sleep(delay)
        continue
    try:
        jsonpost = feed['data']['children'][0]["data"]
    except:
        clear()
        stdout.write( termPad("\r - No new posts - "  ) )
        stdout.flush()
        sleep(delay)
        continue
    pid = jsonpost["id"]
    delta = datetime.now() - datetime.fromtimestamp(jsonpost["created_utc"])
    comments = "{0}www.reddit.com/{1}".format(secure, pid)
    post = termTrim(jsonpost["title"],comments, str(delta)[:-7])
    if not (temp == pid):
        temp = pid
        clear()
        stdout.write( post + '\a')
        stdout.flush()
    if not args['repeat']: break
    sleep(delay
    	)