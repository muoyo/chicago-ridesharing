"""
##### DATA CLEANING #####

This module is for data cleaning.

"""

import pandas as pd
import numpy as np
from datetime import datetime




def merge_weather (df):
    """ Merge weather data into dataset """
    
    # Read in weather data from CSV 
    # (425 days of hourly weather data from Chicago, obtained via the Dark Sky API)
    
    weather_df = pd.read_csv('../data/chicago_weather.csv')
    
    # Create the start_date_plus_hour column, used to merge weather data with trip data
    weather_df['hour'] = weather_df['hour'].apply(lambda x: '{:02d}'.format(x))
    weather_df['start_date_plus_hour'] = pd.to_datetime(weather_df['date'] + ' ' + weather_df['hour'] + ':00:00')
    weather_df = weather_df.rename(columns={'icon': 'precip'})

    # Uncomment below code if we want to limit precipitation options to rain, snow, and clear only (see Dark Sky API)
    
    # def set_precip(precip):
    #     if precip not in ['rain', 'snow']: 
    #         precip = 'clear'

    #     return precip

    # weather_df['precip'] = weather_df['precip'].apply(set_precip)

    precip_df = weather_df[['start_date_plus_hour', 'precip', 'apparentTemperature']]
    df = df.merge(precip_df, how='left', on='start_date_plus_hour')

    return df


def clean_columns(df):
    
    # Trim data to the columns we are interested in, listed below
    
    columns_to_use = ['trip_id', 'trip_start_timestamp', 'trip_end_timestamp', 'trip_seconds',
       'trip_miles', 'pickup_community_area', 'fare', 'tip',
       'additional_charges', 'trip_total' ]

    columns_to_drop = [ col for col in df.columns if col not in columns_to_use ]
    df = df.drop(columns=columns_to_drop)

    # Convert numeric & timestamp data from strings to the appropriate datatypes
    
    df['trip_start_timestamp'] = pd.to_datetime(df['trip_start_timestamp'])
    df['trip_end_timestamp'] = pd.to_datetime(df['trip_end_timestamp'])
    df['trip_seconds'] = df['trip_seconds'].fillna('0')
    df['trip_seconds'] = df['trip_seconds'].astype('int64')
    df['pickup_community_area'] = df['pickup_community_area'].fillna('0')
    df['pickup_community_area'] = df['pickup_community_area'].astype('int64')

    for col in ['trip_miles', 'fare', 'tip', 'additional_charges', 'trip_total']:
        df[col] = df[col].astype(float) 

    # Create columns for the weekday, hour, and time block when the trip was initiated
    # There are 8 three hour time blocks in each 24 hour day, with block 0 starting at 12AM
    
    df['start_weekday'] = df['trip_start_timestamp'].apply(lambda d: d.weekday())
    df['start_hour'] = df['trip_start_timestamp'].apply(lambda d: d.hour)
    df['start_time_block'] = df['start_hour'] // 3

    # We use the start_date_plus hour column to merge trip data with weather data at the hourly level
    
    df['start_date_plus_hour'] = df['trip_start_timestamp'].apply(lambda d: datetime(d.year, d.month, d.day, d.hour))    
    
    return df


def clean_data(df):
    """
    This function runs our support functions to clean and merge the data before returning a final dataframe for analysis
    
    :return: cleaned dataset to be passed to hypothesis testing and visualization modules.
    """
    
    df = clean_columns(df)
    df = merge_weather(df)
    
    return df