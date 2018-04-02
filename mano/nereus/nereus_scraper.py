import pandas as pd
import numpy as np

import pytz
import datetime 
from dateutil.parser import parse

import urllib.request
from bs4 import BeautifulSoup

NOAA_URL = 'https://tidesandcurrents.noaa.gov/stationhome.html?id=9414290#sensors'
TIDES_URL = 'http://tides.mobilegeographics.com/locations/5545.html'


class TideScraper(object):
    
    def __init__(self):
        self.tide_info = self.read_tides()
    
    def _parse_tides(self, s):
        tokens = s.split('PDT')
        ts = parse(tokens[0]).replace(tzinfo=pytz.timezone('US/Pacific'))
        conditions = tokens[1].split('knots')
        
        try:
            knots = float(conditions[0].replace(' ', ''))
            conditions = conditions[1].replace(' ', '').replace(',', '')
        except ValueError:
            knots = np.NaN
            conditions = 'Sunrise' if ts.hour<12 else 'Sunset'
        return({
            'time':ts,
            'ds': str(ts.date()),
            'knots':knots,
            'conditions':conditions
        })
    
    def read_tides(self):
        flob = urllib.request.urlopen(TIDES_URL)
        s = flob.read()
        flob.close()
        soup = BeautifulSoup(s)
        tide_table = soup.findAll('pre', {'class':'predictions-table'})[0].get_text().split('\n')
        location = tide_table[0]
        tides = pd.DataFrame([self._parse_tides(tide) for tide in tide_table[3:-1]])
        tides = tides.set_index('time')
        tides.index = pd.DatetimeIndex(tides.index)
        return({'location': location.replace('Current', ''),
                'tides': tides})
    
    def _extract_tide(self, tides, phase, ds):
        begins = tides[(tides.ds == ds) &
                       (tides.conditions.str.contains('Begins'))]
        highs = tides[(tides.ds == ds) &
                      (tides.conditions.str.contains('Max'))]
        starts = begins[begins.conditions.str.contains(phase)].index.strftime('%H:%M').tolist()
        phase_max = highs[highs.conditions.str.contains(phase)].knots
        return({'starts': starts, 'phase_max': phase_max})
    
    def _format_tides_info(self, tides, 
                          ds = str(datetime.date.today() + datetime.timedelta(days=1))):
        out = tides['location']
        tides = tides['tides']
        sun_times = tides[tides.conditions.str.contains('Sun')][ds].index.strftime('%H:%M').tolist()
        out = out + ' [{0}]:\nSun rises at {1}, sets at {2}\n'.format(ds, sun_times[0], sun_times[1])
        floods = self._extract_tide(tides, 'Flood', ds)
        ebbs = self._extract_tide(tides, 'Ebb', ds)
        if floods['starts'][0] < ebbs['starts'][0]:
            out = out + \
            'Flood {0}-{1} (Max: {2} @ {3})\n'.format(
                floods['starts'][0], ebbs['starts'][0], 
                floods['phase_max'][0], floods['phase_max'].index.strftime('%H:%M')[0])
            out = out + \
            'Ebb {0}-{1} (Max: {2} @ {3})\n'.format(
                ebb['starts'][0], flood['starts'][1], 
                ebbs['phase_max'][0], ebbs['phase_max'].index.strftime('%H:%M')[1])
            out = out + \
            'Flood {0}-{1} (Max: {2} @ {3})\n'.format(
                floods['starts'][1], ebbs['starts'][1], 
                floods['phase_max'][1], floods['phase_max'].index.strftime('%H:%M')[1])
        else:
            out = out + \
            'Ebb {0}-{1} (Max: {2} @ {3})\n'.format(
                ebbs['starts'][0], floods['starts'][0], 
                ebbs['phase_max'][0], ebbs['phase_max'].index.strftime('%H:%M')[0])
            out = out + \
            'Flood {0}-{1} (Max: {2} @ {3})\n'.format(
                floods['starts'][0], ebbs['starts'][1], 
                floods['phase_max'][0], floods['phase_max'].index.strftime('%H:%M')[1])
            out = out + \
            'Ebb {0}-{1} (Max: {2} @ {3})\n'.format(
                ebbs['starts'][1], floods['starts'][1], 
                ebbs['phase_max'][1], ebbs['phase_max'].index.strftime('%H:%M')[1])
        return(out)
    
    def get_tides_info(self, ds = str(datetime.date.today() + datetime.timedelta(days=1))):
        return self._format_tides_info(self.tide_info, ds)