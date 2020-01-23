"""
##### UTILITIES #####

This module contains our utility functions & information

"""

import numpy as np
import time as time
import pandas as pd
from sodapy import Socrata



# return num_samples random samples from Socrata API
# returned as list of length size sample_size * num_samples
# each list item contains a separate record, formatted as a dictionary

def get_random_samples(client, num_samples=200, sample_size=1000, verbose=False):
    
    start = time.time()

    # Perform a $select=count(*) query to determine how large the set is
    results = client.get("m6dm-c72p", select='count(*)' )
    total_rows = int(results[0].get('count', 0))
    row_indices = np.arange(0, total_rows, sample_size)
    results = []

    # Use rand() locally to come up with some offsets
    sample_offsets = np.random.choice(row_indices, size=num_samples, replace=False)


    # Use $limit and $offset in conjunction with a stable $order to pick out individual records. 
    # Ex: $order=facility_id&$limit=1&$offset=<some rand() number>
    for i, offset in enumerate (sample_offsets):

        if verbose:
            print(f'Sample {i}: offset={offset},sample_size={sample_size}')
            print('Pure Python time:', time.time() - start, 'sec.')
        results.extend(client.get("m6dm-c72p", order='trip_id', limit=sample_size, offset=offset, 
                                                  select='''trip_id, trip_start_timestamp, pickup_community_area, fare, tip, trip_total'''))
        
    if verbose:
        print('Pure Python time:', time.time() - start, 'sec.')

    return pd.DataFrame.from_records(results)       
    
def get_trip_records(limit=100000):
    
    client = Socrata('data.cityofchicago.org',
                 'Tk6RhuGAFvF9P4ehsysybj3IW',
                 username="mokome@gmail.com",
                 password="Ch1cago!!")

    client.timeout = 10000


    results = client.get("m6dm-c72p", limit=limit, select='''trip_id, trip_start_timestamp, trip_end_timestamp, trip_seconds, 
                                                        trip_miles, pickup_community_area, dropoff_community_area, fare, 
                                                        tip, additional_charges, trip_total''' )
    
    return pd.DataFrame.from_records(results)

