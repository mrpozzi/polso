import math
from twython import Twython, exceptions as twyErr


from iniTwitter import auth, stream

user = raw_input("Enter Twitter handle to get followers of: ")
#user = 'civati'
suser = auth.show_user(screen_name=user)
fnum = 200
pnum = int(math.ceil(float(suser["followers_count"]) / fnum))

pages = []
for i in range(pnum):
    pages.append("p"+str(i+1))

oldpages = []
for i in range(pnum):
    oldpages.append("p"+str(i))

p0 = { "next_cursor": -1 } # So the following exec() call doesn't fail.

for i in range(pnum):
    try:
        exec(pages[i]+" = auth.get_followers_list(screen_name=user, count=fnum, skip_status=1, cursor="+oldpages[i]+"['next_cursor'])")
    except(twyErr.TwythonRateLimitError):
        break

followers = []

for p in range(pnum):
    try:
        exec("for i in range(fnum): followers.append("+pages[p]+"['users'][i])")
    except(IndexError):
        pass

print "{0} Followers of {1} Found.".format(len(followers),user)

for x in followers:
    print("""Name:  %s
Username:  %s
""" % (x["name"], x["screen_name"]))
