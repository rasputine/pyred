pyred
=====

python script for tracking newest post to a subreddit.

Use as:

`#ptyhon pyred.py funny`

Which will print the newest visible post on /r/funny, which will update every 30 seconds.

Supports private subreddits that you need to authenticate to look at, like the lounge. Specify your username with -u and your feed key with -f, like the following:

Get your key from your profile preferences, under the RSS tab: [Here](https://www.reddit.com/prefs/feeds/)

`#pyred.py -u rasputine -f a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6 centuryclub`

---------

`usage: pyred.py [-h] [-s] [-1] [-u USERNAME] [-f FEED] [C [C ...]]`

-1: Diables loop after successful load, will only print one link.

-s: Disables https

-u: Specify username for authentication

-f: Specify feed key for authentication
