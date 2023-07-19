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

from evalscript.query_text import evalscript,setJsonRequestScript


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
    return token,oauth

def searchAreaByLatLons():
    
    token,oauth = setToken()
    assert "access_token" in list(token.keys()) , "access token Not Get..."
    
    with open(os.path.join(cwd , "env" , "search_information.json"),"r") as f:
        search_info = json.load(f)
    
    json_request = setJsonRequestScript(search_info,evalscript)
    # Set the request url and headers
    url_request = 'https://services.sentinel-hub.com/api/v1/process'
    headers_request = {
        "Authorization" : "Bearer %s" % token['access_token']
    }
    #Send the request
    response = oauth.request(
        "POST", url_request, headers=headers_request, json = json_request
    )
    
    return response


    
def test():
    response = searchAreaByLatLons()
    
    # read the image as numpy array
    image_arr = np.array(Image.open(io.BytesIO(response.content)))
    
    print(image_arr.shape)
    print(np.min(image_arr) , np.max(image_arr))
    print(np.nanmin(image_arr) , np.nanmax(image_arr))
    exit()
    # plot the image for visualization
    plt.figure(figsize=(16,16))
    plt.axis('off')
    plt.tight_layout()
    # plt.imshow(image_arr)
    plt.savefig(os.path.join(cwd ,"output", "tmp.png"),bbox_inches="tight")
    plt.close()
    
    
if __name__ == "__main__":
    test()
