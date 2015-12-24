# XXX: Go to http://dev.twitter.com/apps/new to create an app and get values
# for these credentials that you'll need to provide in place of these
# empty string values that are defined as placeholders.
# See https://dev.twitter.com/docs/auth/oauth for more information 
# on Twitter's OAuth implementation


from twitter import Twitter, OAuth
from twython import Twython
from twython import TwythonStreamer
import os

class Credentials:
    def __init__(self):
        self.APP_KEY =  ""
        self.APP_SECRET =  ""
        self.OAUTH_TOKEN = ""
        self.OAUTH_TOKEN_SECRET = ""

    def read_from_file(self, file_name=os.path.expanduser('~')+"/credentials.txt"):
        credentials = dict()
        credentials_file = file(file_name)
        for line in file.readlines(credentials_file):
            token = line.split("=")
            credentials[token[0]] = token[1].replace("\n","")
        self.APP_KEY =  credentials["APP_KEY"]
        self.APP_SECRET =  credentials["APP_SECRET"]
        self.OAUTH_TOKEN = credentials["OAUTH_TOKEN"]
        self.OAUTH_TOKEN_SECRET = credentials["OAUTH_TOKEN_SECRET"]


class MyStreamer(TwythonStreamer):
    def on_success(self, data):
        if 'text' in data:
            print data['text'].encode('utf-8')

    def on_error(self, status_code, data):
        print status_code

        # Want to stop trying to get data because of the error?
        # Uncomment the next line!
        # self.disconnect()



credentials = Credentials()
credentials.read_from_file()

#auth = Twython(credentials.APP_KEY, credentials.APP_SECRET,
#               credentials.OAUTH_TOKEN, credentials.OAUTH_TOKEN_SECRET)

auth = OAuth(credentials.OAUTH_TOKEN, credentials.OAUTH_TOKEN_SECRET,
             credentials.APP_KEY, credentials.APP_SECRET)

stream = MyStreamer(credentials.APP_KEY, credentials.APP_SECRET,
                    credentials.OAUTH_TOKEN, credentials.OAUTH_TOKEN_SECRET)



