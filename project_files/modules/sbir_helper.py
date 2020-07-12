# functions that support interactions between SBIR gov database, etc.

import requests
import json
import pandas as pd
import numpy as np
import time
import random
import re
import os

def get_open_solicitations(agency):
    """
    Gets open solicitations for a given agency abbreviation
    
    Returns json() response object
    
    """
    try:
        base_url = f'https://www.sbir.gov/api/solicitations.json?keyword=sbir&agency={agency}&open=1'

        return requests.get(base_url).json()
    except: 
        return 'error'
    
    
def get_closed_solicitations(agency):
    """
    Gets closed solicitations for a given agency abbreviation
    
    Returns json() response object
    
    """
    try:
        base_url = f'https://www.sbir.gov/api/solicitations.json?keyword=sbir&agency={agency}&closed=1'

        return requests.get(base_url).json()
    except: 
        return 'error'
    
    
    
        
def get_awards(agency, keyword, year):
    """
    Get awards by agency, keyword, and year variables

    Returns json() response object

    """
    try:
        base_url = f'https://www.sbir.gov/api/awards.json?keyword={keyword}&agency={agency}&year={year}'

        return requests.get(base_url).json()
    except: 
        return 'error'
    
    
    

def add_year_col(solicitations, agency):
    """
    Adds the year of each solicitation.
    
    Params:
    solicitations --> .json response object for open or closed solicitations
    agency --> DOD, HHS, NASA, etc...
    
    """
    for sdict in solicitations[f'{agency}']:
        year = sdict['SolicitationYear']

        for sub in sdict['SolicitationTopics']:
            sub['Year'] = year


            
def add_status_col(solicitations, agency):
    """
    Adds the status of each solicitation.
    
    Params:
    solicitations --> .json response object for open or closed solicitations
    agency --> DOD, HHS, NASA, etc...
    
    """
    for frame in solicitations[f'{agency}']:
        status = frame['CurrentStatus']

        for sub in frame['SolicitationTopics']:
            sub['Status'] = status
            
            
def concat_solic_frames(solicitations, agency):
    """
    Build dfs for solicitations frames, concat if more than one.
    
    Params:
    solicitations --> .json response object for open or closed solicitations
    agency --> DOD, HHS, NASA, etc...
    
    """
    dfs_list = []
    for frame in solicitations[f'{agency}']:
        
        df = pd.DataFrame.from_dict(data = frame['SolicitationTopics'], orient ='columns' )
        dfs_list.append(df)

    return dfs_list


def clean_description(solic_description):
    """
    Separates 'DESCRIPTION' and 'KEYWORDS' section of solicitation text.
    
    """
    stringer = solic_description
    description = stringer[stringer.find('DESCRIPTION:')+len('DESCRIPTION: ') : stringer.find('KEYWORDS:')]
    description = description.replace('</p><p>', '')

    keywords = stringer[stringer.find('KEYWORDS:')+len('KEYWORDS: ') : stringer.find('<p>References:')]
    keywords = keywords.split(',')
    keywords = [w.replace('</p>','') for w in keywords]
    keywords = [w.replace('<p>','') for w in keywords]
    keywords = [w.replace(' p ','') for w in keywords]
    keywords = [w.replace('nbsp','') for w in keywords]

    keywords = [re.sub(pattern = r'[^\w]', repl = " ", string = word ) for word in keywords]
    keywords = [w.lower() for w in keywords]
    keywords = [i for i in keywords if i]
    keywords = [w.strip() for w in keywords]


    return description, keywords

    

