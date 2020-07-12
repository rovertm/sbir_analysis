# functions for retrieving API data from SAM database


import requests
import json
import pandas as pd
import numpy as np
import time
import random
import re
import os

"""
Endpoint + API key format:

https://api.data.gov/sam/v8/registrations/1459697830000?api_key=YOUR_API_KEY

"""

api_key = '?api_key=B7srOs3m0J4IfdayqY6vqvyR7iByOIafTjdakRlW'
base = 'https://api.data.gov/sam/v8/registrations/'

def sam_request(api_key, duns):
    """
    Makes a .get request to SAM endpoint for one DUNS number (entity)
    Note:
    api_key formatted: '?api_key={api key here...}'
    
    """
 
    response = requests.get(base+duns+api_key).json()
    
    return response


def duns_screener(duns):
    """
    Takes a duns number and returns a modified string to comply with DUNS+4 format
    
    common DUNS errors:
   
    * leading zero removed: len == 8 --> add leading zero back + '0000' trailing
    * 9-digits --> duns + '0000'
    * else: 'error'
    
    """
    
    if len(duns) == 9:
        duns = duns + '0000'
        return duns
    elif len(duns) == 8:
        duns = '0' + duns + '0000'
        return duns
    else:
        return 'error'
    
    
def unpack_samdata(wanted_data, sam_response):
    """
    Unpacks SAM response .json() file and returns requested data
    
    wanted_data: list of strings for .json keys
    sam_response: sam .json object
    
    """
    
    response_data = []
    
    base = sam_response['sam_data']['registration']
    
    if 'naics' in wanted_data:
        naics = []
        name = base['naics'][0]['naicsName']
        naics.append(name)
        code = base['naics'][0]['naicsCode']
        naics.append(code)
        
        response_data.append(naics)
        
        
    if 'inception' in wanted_data:
        inception = []
        start = base['businessStartDate']
        inception.append(start)

        response_data.append(inception)
        
        
    return response_data
        
        
