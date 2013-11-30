# XXX: Go to http://dev.twitter.com/apps/new to create an app and get values
# for these credentials that you'll need to provide in place of these
# empty string values that are defined as placeholders.
# See https://dev.twitter.com/docs/auth/oauth for more information 
# on Twitter's OAuth implementation

import credentials

from twython import Twython
from twython import TwythonStreamer



auth = Twython(credentials.APP_KEY, credentials.APP_SECRET,
                  credentials.OAUTH_TOKEN, credentials.OAUTH_TOKEN_SECRET)

class MyStreamer(TwythonStreamer):
    def on_success(self, data):
        if 'text' in data:
            print data['text'].encode('utf-8')

    def on_error(self, status_code, data):
        print status_code

        # Want to stop trying to get data because of the error?
        # Uncomment the next line!
        # self.disconnect()


stream = MyStreamer(credentials.APP_KEY, credentials.APP_SECRET,
                    credentials.OAUTH_TOKEN, credentials.OAUTH_TOKEN_SECRET)

