import pandas as pd
import os
import json

from stravalib.client import Client
from stravalib import unithelper

import datetime
import calendar


import matplotlib
from matplotlib import pyplot as plt
plt.style.use('ggplot')


class StravaScraper(object):
    
    M_TO_YD = 1.09361
    
    def __init__(self, strava_credentials='{0}/strava_credentials.json'.format(os.getenv("HOME"))):
        """
        """
        
        json_data=open(strava_credentials).read()
        credentials = json.loads(json_data)
        self.client = Client(access_token=credentials['AccessToken'])
        
        self.swims = None
        self.in_out = None
        self.monthly_yardage = None
        self.total_yards = 0.0
    
        
    def get_swims(self, after='2017-11-01', before='2018-09-05'):
        """
        """
        activities = self.client.get_activities(after=after, before=before)
        
        self.swims = pd.DataFrame([{'name':activity.name, 
                                  'id': activity.id, 
                                  'stroke_count': 2 * activity.average_cadence if activity.average_cadence is not None else None,
                                  'average_speed':float(unithelper.meters_per_second(activity.average_speed)),
                                  'elapsed_time':unithelper.timedelta_to_seconds(activity.elapsed_time), 
                                  'start_date': activity.start_date,
                                  'distance':float(unithelper.meters(activity.distance)) * self.M_TO_YD} for activity in activities if activity.type=='Swim'])
        self.swims = self.swims.set_index('start_date')
        self.swims.index = pd.DatetimeIndex(self.swims.index)
        self.swims.index = self.swims.index.tz_convert('US/Pacific')
        self.swims['month'] = self.swims.index.month
        self.swims['month_name'] = self.swims['month'].apply(lambda x: calendar.month_abbr[x])
        self.swims['ds_week_ending'] = self.swims.index.to_period('W').end_time.floor('d')
        self.swims['ds_month_ending'] = self.swims.index.to_period('M').end_time.floor('d')
        self.swims['is_pool'] = ['pool' if "[POOL]" in name else 'open water' for name in self.swims.name]
        self.swims['hours']= self.swims.elapsed_time/3600
        
        self.total_yards = int(self.swims.distance.sum())
        
        self.in_out = self.swims.groupby(['is_pool'])['distance'].agg({'total' : 'sum'})
        self.in_out['percentage'] = 100 * self.in_out['total'] / self.in_out['total'].sum()
        
        # TODO: wrap in utility
        # TODO: sort by ds_month_ending
        self.monthly_yardage = self.swims.groupby(self.swims.index.month)['distance', 'hours'].sum()
        self.monthly_yardage["weekly distance"] = self.monthly_yardage.distance/4.0
        self.monthly_yardage.index = self.monthly_yardage.index.map(lambda x: datetime.date(1900, x, 1).strftime('%B'))
    
    
    def get_xtraining(self, after='2017-11-01', before='2018-09-05'):
        """
        """
        activities = self.client.get_activities(after=after, before=before)
        
        self.x_training = pd.DataFrame([{'name':activity.name, 
                                  'id': activity.id, 
                                  'activity': activity.type,
                                  'elapsed_time':unithelper.timedelta_to_seconds(activity.elapsed_time), 
                                  'start_date': activity.start_date,
                                  'distance':float(unithelper.meters(activity.distance)) * self.M_TO_YD} for activity in activities if activity.type!='Swim'])
        self.x_training = self.x_training.set_index('start_date')
        self.x_training.index = pd.DatetimeIndex(self.x_training.index)
        self.x_training.index = self.x_training.index.tz_convert('US/Pacific')
        self.x_training['month'] = self.x_training.index.month
        self.x_training['month_name'] = self.x_training['month'].apply(lambda x: calendar.month_abbr[x])
        self.x_training['ds_week_ending'] = self.x_training.index.to_period('W').end_time.floor('d')
        self.x_training['ds_month_ending'] = self.x_training.index.to_period('M').end_time.floor('d')
        self.x_training['hours']= self.x_training.elapsed_time/3600
        
        
    def get_full_training(self):
        """
        """
        swims = self.swims[['ds_week_ending', 'name', 'distance', 'hours', 'is_pool']].copy()
        swims.rename(columns={"is_pool": "activity"}, inplace=True)
        
        x_training = self.x_training[['ds_week_ending', 'name', 'distance', 'hours', 'activity']]
        
        full_training = pd.concat([swims, x_training])
        full_training = full_training.sort_index(axis=0, ascending=True, inplace=False)
        #full_training.index = full_training.index.round('60min')
        
        return full_training
    
        
    def plot_daily_yards(self, figsize=(25.0, 15.0)):
        """
        """
        fig, axes = plt.subplots(nrows=2, ncols=1, figsize=figsize)
        axes[0].set_title('Yards by day')
        axes[1].set_title('Hours by day')
        
        self.swims.groupby(self.swims.index.normalize()).distance.sum().plot(kind='bar', ax=axes[0], sharex=True, color='#E24A33')
        axes[0].axhline(4000, color='k', linestyle='--')
        axes[0].set_ylabel('Yards')
        #axes[0].step([-1, max(np.where(my_swims.index.normalize().unique().month <= 1)[0])-0.5, 100.5], [0, 3000 / m_to_yd, 4000 / m_to_yd], color='k', linestyle='--')
        
        
        self.swims.groupby(self.swims.index.normalize()).elapsed_time.sum().apply(lambda x: x / 3600).plot(kind='bar', ax=axes[1], color='#E24A33')
        axes[1].set_ylabel('Hours')
        axes[1].set_xlabel('Day')
        axes[1].axhline(1, color='k', linestyle='--')
        #axes[1].step([-1, max(np.where(my_swims.index.normalize().unique().month <= 1)[0])-0.5, 100.5], [0, 1, 2], color='k', linestyle='--')
        
        return fig, axes
        
        
    def plot_summary(self, in_n_out=False, by='week', yardage_goal=35323.71, figsize=(25.0, 15.0)):
        """
        """
        
        fig, axes = plt.subplots(nrows=2, ncols=1, figsize=figsize)
        axes[0].set_title('Yards by {by}'.format(by=by))
        axes[1].set_title('Hours by {by}'.format(by=by))

        if in_n_out:
            self.swims.groupby(['ds_{by}_ending'.format(by=by), 'is_pool'])['distance'].sum().unstack().plot(kind='bar', ax=axes[0], sharex=True)
        else:
            self.swims.groupby(self.swims['ds_{by}_ending'.format(by=by)]).distance.sum().plot(kind='bar', ax=axes[0], sharex=True, color='#E24A33')
            axes[0].axhline(yardage_goal, color='r', linestyle='--')
            #axes[0].step([-1, 3.5, 7.5, 12.5, 16.5, 20.5, 24.5, 28.5, 36.5], 
            #             [0, 28225, 32500, 31615, 31615, 31615, 35000, 33870, 33870], color='k', linestyle='--')
        
        #axes[0].axhline(28000 / m_to_yd, color='k', linestyle='--')
        axes[0].set_ylabel('Yards')
            
        if in_n_out:
            self.swims.groupby(['ds_{by}_ending'.format(by=by), 'is_pool'])['elapsed_time'].sum().apply(lambda x: x / 3600).unstack().plot(kind='bar', ax=axes[1])
        else:
            self.swims.groupby(self.swims['ds_{by}_ending'.format(by=by)]).elapsed_time.sum().apply(lambda x: x / 3600).plot(kind='bar', ax=axes[1], color='#E24A33')
        
        #axes[1].axhline(7.6, color='k', linestyle='--')
        axes[1].set_ylabel('Hours')
        axes[1].set_xlabel(by.capitalize())
        
        return fig, axes
    
    def plot_x_training(self, figsize=(25.0, 15.0)):
        """
        """
        swims = self.swims
        swims['activity'] = swims['is_pool'].apply(lambda x: {'open water': 'OpenWater', 'pool':'Pool'}[x])
        full_training = pd.concat([swims[self.x_training.columns], self.x_training])
        
        fig, axes = plt.subplots(nrows=2, ncols=1, figsize=figsize)
        axes[0].set_title('Hours by week')
        axes[1].set_title('Hours by month')
        
        #axes[0].axhline(28000 / m_to_yd, color='k', linestyle='--')
        #axes[0].set_ylabel('Yards')
        
        full_training.groupby(['ds_week_ending', 'activity'])['elapsed_time'].sum().apply(lambda x: x / 3600).unstack().plot(kind='bar', ax=axes[0], sharex=True)
        
        full_training.groupby(['ds_month_ending', 'activity'])['elapsed_time'].sum().apply(lambda x: x / 3600).unstack().plot(kind='bar', ax=axes[1])

        
        #axes[1].axhline(7.6, color='k', linestyle='--')
        axes[1].set_ylabel('Hours')
        axes[1].set_xlabel('Month')
        
        return fig, axes
