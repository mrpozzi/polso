import pandas as pd
import numpy as np

import sys
import time
import datetime 
from dateutil.parser import parse
import pytz

import urllib2
from bs4 import BeautifulSoup

from twitter import TwitterHTTPError
from oauth_setup import oauth_login

t = oauth_login()


url='http://tides.mobilegeographics.com/locations/5545.html'

flob = urllib2.urlopen(url)
s = flob.read()
flob.close()
soup = BeautifulSoup(s)

tide_table = soup.findAll('pre', {'class':'predictions-table'})[0].get_text().split('\n')
location = tide_table[0]
def parse_tides(s):
    tokens = s.split('PDT')
    conditions = tokens[1].split('knots')
    
    try:
        knots = float(conditions[0].replace(' ', ''))
        conditions = conditions[1].replace(' ', '').replace(',', '')
    except ValueError:
        knots = np.NaN
        conditions = 'Sunset'
    return({
        'time':parse(tokens[0]).replace(tzinfo=pytz.timezone('US/Pacific')),
        'knots':knots,
        'conditions':conditions
     })

tides = pd.DataFrame([parse_tides(tide) for tide in tide_table[3:-1]])