# Helper functions to unpack and manipulate np.arrays for dataframe modeling


import requests
import json
import pandas as pd
import numpy as np
import time
import random
import re
import os


def numpy_helper(series, indices, action):
    """
    Performs aciton on df series based on given indices through np. array ops
    
    """
    
    # filtered array by indices
    arr = np.array(series)
    values = arr[indices]
    
    # actions to perform on array
    
    if action == 'sum':
        summed = np.sum(values)
        return summed
    elif action == 'mean':
        mean = np.nanmean(values)
        return mean
    elif action == 'median':
        median = np.nanmedian(values)
        return median
    elif action == 'count':
        count = len(indices)
        return count
    elif action == 'percent':
        perc = np.sum(values) / np.sum(arr)
        return perc
    elif action == 'percent_count':
        count = len(indices)
        perc = count / len(arr)
        return perc
    elif action == 'max':
        maxi = np.argmax(values)
        maxv = values[maxi]
        return maxv
    
    
    
def build_gramsdf(sourcedf, grams_dict ):

        # df for analysis
    gdf = pd.DataFrame(data = grams_dict.keys())
    # source data df
    df = sourcedf

    # clean up index
    gdf = gdf.rename(columns = {0: 'gram_group'})
    gdf.set_index('gram_group', inplace = True)

    # initial columns
    gdf['award_indices'] = [grams_dict[key] for key in gdf.index]
    gdf['award_count'] = gdf['award_indices'].apply(lambda x: numpy_helper(df['Award Amount'], x, 'count'))

    # award amounts --> units: millions
    awd_units = 1000000
    gdf['award_sum'] = gdf['award_indices'].apply(lambda x: round(numpy_helper(df['Award Amount'] / awd_units, x, 'sum')))
    # mean awards --> units: millions
    gdf['mean_award'] = gdf['award_indices'].apply(lambda x: round(numpy_helper(df['Award Amount'] / awd_units, x, 'mean'), 2))

    # percent calculations
    gdf['perc_awards_amount'] = gdf['award_indices'].apply(lambda x: round(numpy_helper(df['Award Amount'] / awd_units, x, 'percent'), 2))
    gdf['perc_awards_count'] = gdf['award_indices'].apply(lambda x: round(numpy_helper(df['Award Amount'] / awd_units, x, 'percent_count'), 2))

    # Employee metrics
    gdf['mean_employees'] = gdf['award_indices'].apply(lambda x: round(numpy_helper(df['Number Employees'], x, 'mean'), 2))
    gdf['median_employees'] = gdf['award_indices'].apply(lambda x: round(numpy_helper(df['Number Employees'], x, 'median'), 2))

    # Award to Employee metrics --> units: thousands
    gdf['award_to_employees'] = gdf.apply(lambda x: round(x['mean_award'] / x['mean_employees'] * awd_units), axis = 1)
    
    return gdf