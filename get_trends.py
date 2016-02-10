__author__ = 'mrpozzi'

import os
import sys
import datetime
import time
import json

from tweet_data_base import db
from oauth_setup import oauth_login

t = oauth_login()
WORLD_WOE_ID = 1  # The Yahoo! Where On Earth ID for the entire world


if not os.path.isdir('out/trends_data'):
    os.makedirs('out/trends_data')

cursor = db.cursor()

while True:

    now = str(datetime.datetime.now())
    trends = json.dumps(t.trends.place(_id=WORLD_WOE_ID), indent=1)
    sql = """INSERT INTO DEPRESSION (DATE, LOCATION, JSON) VALUES (%s, %s, %s)"""

    try:
        # Execute the SQL command
        cursor.execute(sql, (now, WORLD_WOE_ID, trends))
        # Commit your changes in the database
        db.commit()
    except:
        # Rollback in case there is any error
        db.rollback()
        print >> sys.stderr, "Error with Entry", sql

    print >> sys.stderr, "Read Trends ", now
    print >> sys.stderr, "Zzz..."

    time.sleep(60)  # 60 seconds
