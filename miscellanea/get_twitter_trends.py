import os
import sys
import datetime
import time
import json
import yweather
from twitter import TwitterHTTPError
from oauth_setup import oauth_login

t = oauth_login()

client = yweather.Client()
countries = ['US', 'AU', 'CA', 'IE', 'GB']
WORLD_WOE_IDS = [1] + [client.fetch_woeid(country) for country in countries]

trend_file = open('twitter_trends.json', 'ab')

while True:

    now = str(datetime.datetime.now())

    trends = dict()
    for WORLD_WOE_ID in WORLD_WOE_IDS:
        try:
            local_trends = t.trends.place(_id=WORLD_WOE_ID)
            trends[WORLD_WOE_ID] = json.dumps(
                [{'location': local_trends[0]['locations'][0]['name'],
                  'tweet_volume': trend['tweet_volume'],
                  'trend': trend['name']
                  } for trend in local_trends[0]['trends']], indent=1)
        except TwitterHTTPError:
            print >> sys.stderr, "No Response for id ", WORLD_WOE_ID
    trend_file.write(json.dumps(trends, indent=1))

    print >> sys.stderr, "Read Trends ", now
    print >> sys.stderr, "Zzz..."

    time.sleep(86400)  # one day
