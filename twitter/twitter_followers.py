import pandas as pd
import json
import sys
from twitter import TwitterHTTPError
from twitter_utils import get_timelines

## MG: The files will be provided at the moment
##     More work on the pipeline approach is needed
data_directory = "data/"
list_of_followers = data_directory + "Free_Twitter_Followers_Report_on_amis.csv"
output_file = data_directory + "twitter_timelines.jsonl"

followers = pd.read_csv(list_of_followers)['Screen Name'].tolist()
all_tweets = get_timelines(followers)

## Save all_tweets in json
all_tweets.apply(lambda x: json.dumps(dict(x)), 1).to_csv(output_file)

#len(all_tweets)
#all_tweets.groupby('screen_name').text.count()

## MG: the json file can be included in the 
##     analyses of the sentiment
