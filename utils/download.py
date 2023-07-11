import os
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from PIL import Image
import io
import numpy as np
import matplotlib.pyplot as plt

import configparser
from pathlib import Path


def read_profiles():
    cwd = Path(__file__).parent.parent
    params = configparser.ConfigParser(interpolation=None)
    params.read( os.path.join(cwd, "env" , "config.ini"),'UTF-8')
    return params



def test():
    
    params = read_profiles()
    # Create a session
    client = BackendApplicationClient(client_id=params["sentinel"]["CLIENT_ID"])
    oauth = OAuth2Session(client=client)
    
    # get an authentication token
    token = oauth.fetch_token(
        token_url='https://services.sentinel-hub.com/oauth/token',
        client_id = params["sentinel"]["CLIENT_ID"], client_secret= params["sentinel"]["CLIENT_SECRET"])
    print(token)

    return

if __name__ == "__main__":
    test()
