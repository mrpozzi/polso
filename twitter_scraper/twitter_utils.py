import pandas as pd
import sys

from twitter import TwitterHTTPError
from oauth_setup import oauth_login

t = oauth_login()

def get_timeline(screen_name, t):

    all_tweets = []
    new_tweets = t.statuses.user_timeline(screen_name=screen_name, count=200)

    # keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:

        # save most recent tweets
        all_tweets.extend(new_tweets)

        # update the id of the oldest tweet less one
        oldest = all_tweets[-1]['id'] - 1

        print "getting tweets before {0}".format(oldest)

        # all subsequent requests use the max_id param to prevent duplicates
        new_tweets = t.statuses.user_timeline(screen_name=screen_name, count=200, max_id=oldest)

        print "...{0} tweets downloaded so far [{1}]".format(len(all_tweets), screen_name)

    tweets = [{'screen_name': screen_name,
               'id': tweet['id'],
               'created_at': tweet['created_at'],
               'hashtags': tweet['entities']['hashtags'],
               'user_mentions': tweet['entities']['user_mentions'],
               'text': tweet['text'],
              } for tweet in all_tweets]
    return tweets


def get_timelines(followers):
    all_tweets = pd.DataFrame()
    for screen_name in followers:
        try:
            tweets = get_timeline(screen_name, t)
            if len(tweets)>0:
                all_tweets = all_tweets.append(tweets)
        except TwitterHTTPError:
            print >> sys.stderr, "No Response for id ", screen_name
    all_tweets['created_at'] = pd.to_datetime(all_tweets['created_at'])
    all_tweets['text'] = all_tweets['text'].apply(lambda x: x.encode('utf-8'))
    all_tweets = all_tweets.set_index(all_tweets.id)
    return all_tweets
