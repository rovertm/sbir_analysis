
import requests
import json
import pandas as pd
import numpy as np
import time
import random
import re
import os




def group_year_counts(source_dict, max_val, min_val, step_val):
    """
    Builds a dict for grouped key:value pairs by specified year range
    
    Params:
    source_dict -- all key:value pairs to sort
    min_val -- max boundary for min (last) value group in response dict
    
    """
    step_val = abs(step_val)
    
    # sum of dict values... counts for awards in all years
    year_counts = sum([x[1] for x in source_dict.items()])

    # keys for new response dict
    year_keys = [str(val) for val in range(max_val - step_val, min_val - step_val, -1*step_val)]

    # new dict for values in list format
    year_windows_dict = {year_key: [] for year_key in year_keys}


    for year_key in year_windows_dict:
        
        val_to_append = sum([ source_dict[year] for year in source_dict 
                            if int(year_key) <= int(year) < int(year_key) + step_val ])
   
        year_windows_dict[year_key].append(val_to_append)
    
    # insert min_val key:val pair for final dict key:val pair
    min_key = f'<{min_val}'
    year_windows_dict[min_key] = []

    # last value in dict... all less than min_val
    min_val_append = round(sum([ val[1] for val in source_dict.items() if int(val[0]) < int(min_val)]))
    year_windows_dict[min_key].append(min_val_append)
    
    # year percentiles from % of total counts
    year_percentiles = [ x[1] / year_counts for x in year_windows_dict.items() ]


    # Verify correct response length
    if sum([val[1][0] for val in year_windows_dict.items()]) == year_counts:
        return year_windows_dict, year_percentiles
    else:
        return "Error: Window counts do NOT equal total year counts provided by source dict."