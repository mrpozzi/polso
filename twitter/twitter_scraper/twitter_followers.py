import pandas as pd
import json
import sys
from twitter import TwitterHTTPError
from twitter_utils import get_timelines

## MG: The files will be provided at the moment
##     More work on the pipeline approach is needed
data_directory = "data/"
list_of_followers = data_directory + "Free_Twitter_Followers_Report_on_amis.csv"
output_file = data_directory + "twitter_timelines.json"

followers = pd.read_csv(list_of_followers)
all_tweets = get_timelines(followers['Screen Name'].tolist())

## Save all_tweets in json
all_tweets[['created_at', 'id', 'screen_name', 'text']].to_json(output_file)

#len(all_tweets)
#all_tweets.groupby('screen_name').text.count()

## MG: the json file can be included in the 
##     analyses of the sentiment
