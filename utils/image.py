import os
# from oauthlib.oauth2 import BackendApplicationClient
# from requests_oauthlib import OAuth2Session
from PIL import Image
import io

import logging
from http.client import HTTPConnection
from pathlib import Path
cwd = Path(__file__).parent.parent

import numpy as np
from utils.utils import plot_image
from script.eval import evalscript_clm,evalscript

# from evalscript.query_text import evalscript,setJsonRequestScript
from sentinelhub import SHConfig
from sentinelhub import (
    CRS,
    BBox,
    DataCollection,
    DownloadRequest,
    MimeType,
    MosaickingOrder,
    SentinelHubDownloadClient,
    SentinelHubRequest,
    bbox_to_dimensions,
)

def get_logger():
    HTTPConnection.debuglevel = 1
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(levelname)s:%(name)s:%(threadName)s:%(message)s',
    )
    logger = logging.getLogger("requests.packages.urllib3")
    logger.setLevel(logging.DEBUG)
    logger.propagate = True
    return logger

class SentinelHubImage:
    def __init__(self,config_parameter):
        self.config = SHConfig()
        self.config.sh_client_id = config_parameter["sentinelhub"]["CLIENT_ID"]
        self.config.sh_client_secret = r"Knh+H/^;534d%du64.R/}plg^MYV7EtKp|!GO:q?"
        
        ### 解像度の設定
        self.resolution = 60
        self.bbox_coords = (46.16, -16.15, 46.51, -15.58)
        self.start_date = "2020-06-12"
        self.end_date = "2020-06-13"
        self.data_collection = DataCollection.SENTINEL2_L1C
        
        ## 取得するときの条件("all","new")
        self.outimage = "new"
        


    def get(self,evalscript):
        
        ## Area Bounds and Size settings ...
        bbox = BBox(bbox = self.bbox_coords,crs = CRS.WGS84)
        size = bbox_to_dimensions(bbox,resolution= self.resolution ) 
        print("Image shape of {}m resolution: {} pixels".format(self.resolution , size))
        
        ## Sentinel Data API requests...
        req = SentinelHubRequest(
            evalscript = evalscript,
            input_data = [
                SentinelHubRequest.input_data(
                    data_collection = self.data_collection,
                    time_interval = (self.start_date , self.end_date)
                )
            ],
            responses = [ SentinelHubRequest.output_response("default" , MimeType.PNG)],
            bbox = bbox,
            size = size,
            config = self.config
        )
        
        imgs = req.get_data()
        print(f"Returned data is of type = {type(imgs)} and length {len(imgs)}.")
        print(f"Single element in the list is of type {type(imgs[-1])} and has shape {imgs[-1].shape}")
        if len(imgs)>0:
            if self.outimage== "new":
                return imgs[-1]
            else:
                return imgs
        else:
            return []
        
    
def ex1(config_parameter):
    
    shi = SentinelHubImage(config_parameter)
    
    img = shi.get(evalscript_clm)
    if img is None:
        exit()
    
    plot_image(img,factor=1/255)
        
    
    
    
    
    
    
