"""
##### DATA CLEANING #####

This module is for data cleaning.

"""

import pandas as pd
import numpy as np
from datetime import datetime




def merge_weather (df):
    """ Merge weather data into dataset """
    
    weather_df = pd.read_csv('../data/chicago_weather.csv')
    weather_df['hour'] = weather_df['hour'].apply(lambda x: '{:02d}'.format(x))
    weather_df['start_date_plus_hour'] = pd.to_datetime(weather_df['date'] + ' ' + weather_df['hour'] + ':00:00')
    weather_df = weather_df.rename(columns={'icon': 'precip'})

    # def set_precip(precip):
    #     if precip not in ['rain', 'snow']: 
    #         precip = 'clear'

    #     return precip

    # weather_df['precip'] = weather_df['precip'].apply(set_precip)

    precip_df = weather_df[['start_date_plus_hour', 'precip', 'apparentTemperature']]
    df = df.merge(precip_df, how='left', on='start_date_plus_hour')

    return df


def clean_columns(df):
    
    columns_to_use = ['trip_id', 'trip_start_timestamp', 'trip_end_timestamp', 'trip_seconds',
       'trip_miles', 'pickup_community_area', 'fare', 'tip',
       'additional_charges', 'trip_total' ]

    columns_to_drop = [ col for col in df.columns if col not in columns_to_use ]
    df = df.drop(columns=columns_to_drop)

    df['trip_start_timestamp'] = pd.to_datetime(df['trip_start_timestamp'])
    df['trip_end_timestamp'] = pd.to_datetime(df['trip_end_timestamp'])
    df['trip_seconds'] = df['trip_seconds'].fillna('0')
    df['trip_seconds'] = df['trip_seconds'].astype('int64')

    for col in ['trip_miles', 'fare', 'tip', 'additional_charges', 'trip_total']:
        df[col] = df[col].astype(float) 

    df['start_weekday'] = df['trip_start_timestamp'].apply(lambda d: d.weekday())
    df['start_hour'] = df['trip_start_timestamp'].apply(lambda d: d.hour)
    df['start_time_block'] = df['start_hour'] // 3

    df['start_date_plus_hour'] = df['trip_start_timestamp'].apply(lambda d: datetime(d.year, d.month, d.day, d.hour))    
    
    return df


def clean_data(df):
    """
    This is the one function called that will run all the support functions.
    
    :return: cleaned dataset to be passed to hypothesis testing and visualization modules.
    """
    
    df = clean_columns(df)
    df = merge_weather(df)
    
    return df