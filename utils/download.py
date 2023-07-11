import os
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from PIL import Image
import io
import numpy as np
import matplotlib.pyplot as plt

import configparser
from pathlib import Path
import json
cwd = Path(__file__).parent.parent


def read_profiles():
    params = configparser.ConfigParser(interpolation=None)
    params.read( os.path.join(cwd, "env" , "config.ini"),'UTF-8')
    return params

def sentinelhub_compliance_hook(response):
    response.raise_for_tatus()
    return response
    

def setToken():
    
    params = read_profiles()
    # Create a session
    client = BackendApplicationClient(client_id=params["sentinel"]["CLIENT_ID"])
    oauth = OAuth2Session(client=client)
    
    # get an authentication token
    token = oauth.fetch_token(
        token_url='https://services.sentinel-hub.com/oauth/token',
        client_id = params["sentinel"]["CLIENT_ID"], client_secret= params["sentinel"]["CLIENT_SECRET"])

    #All requests using this session will have an access token automatically added
    # response = oauth.get("https://services.sentinel-hub.com/oauth/tokeninfo")
    # print(token) #dict
    # print(response.content)
    # oauth.register_compliance_hook("access_token_response", sentinelhub_compliance_hook)
    return token

def searchAreaByLatLons():
    with open(os.path.join(cwd , "env" , "search_information.json"),"r") as f:
        search_info = json.load(f)
    
    print(search_info)
    


def test():
    # token = setToken()
    searchAreaByLatLons()
    
    

if __name__ == "__main__":
    test()
