import math
from twython import Twython

from iniTwitter import auth, stream

ht = raw_input("Enter a search string: ")
#ht = '#civoti'
Ntweets = raw_input("Enter the number of Tweets you wish to get: ")
#Ntweets = 1000
fnum = 100
pnum = int(math.ceil(float(Ntweets) / fnum))

pages = []
for i in range(pnum):
    pages.append("p"+str(i+1))

oldpages = []
for i in range(pnum):
    oldpages.append("p"+str(i))

p0 = { "next_cursor": -1 } # So the following exec() call doesn't fail.


for i in range(pnum):
    exec(pages[i]+" = auth.search(q=ht, count=fnum, cursor="+oldpages[i]+")")


    "['next_cursor']"
tweets = []

for p in range(pnum):
    try:
        exec("for i in range(fnum): tweets.append("+pages[p]+"['statuses'][i]['text'])")
    except(IndexError):
        pass

print "Found {0} Tweets with string {1}.".format(len(tweets),ht)
