import os
# from oauthlib.oauth2 import BackendApplicationClient
# from requests_oauthlib import OAuth2Session
from PIL import Image
import io

import datetime as dt

import logging
from http.client import HTTPConnection
from pathlib import Path
cwd = Path(__file__).parent.parent

import numpy as np
from utils.utils import plot_images_2x2
from script.eval import *

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
    SentinelHubRequest,WcsRequest,WmsRequest,
    bbox_to_dimensions,
    SentinelHubCatalog,
    filter_times
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
        
        self.config.instance_id = config_parameter["sentinelhub"]["INSTANCE_ID"]
        self.config.sh_client_id = config_parameter["sentinelhub"]["CLIENT_ID"]
        self.config.sh_client_secret = r"Knh+H/^;534d%du64.R/}plg^MYV7EtKp|!GO:q?"
        
        ### 解像度の設定
        self.resolution = 30
        # self.bbox_coords = (46.16, -16.15, 46.51, -15.58)
        # self.bbox_coords = (139.607162, 35.727958, 139.674090, 35.738837) #tokyo
        bbox_coords = (139.5, 35.5, 139.55, 35.55) #tokyo
        # error message -"The request image height. Must be an integer between 1 and 2500.
        self.bbox = BBox(bbox = bbox_coords,crs = CRS.WGS84)
        self.size = bbox_to_dimensions(self.bbox,resolution= self.resolution) 
        
        self.start_date = "2022-06-20"
        self.end_date = "2023-06-13"
        self.data_collection = DataCollection.SENTINEL2_L1C
        
        ## 取得するときの条件("all","new")
        self.outimage = "all"
    
    def catalogSearch(self):
        catalog = SentinelHubCatalog(self.config)
        time_interval = self.start_date, self.end_date 

        search_iterator = catalog.search(
            self.data_collection ,
            bbox=self.bbox,
            time=time_interval,
            filter="eo:cloud_cover < 5",
            fields={"include": 
                ["id", "properties.datetime", "properties.eo:cloud_cover"], "exclude": []},
        )
        results = list(search_iterator)
        print("Total number of results:", len(results))
        return search_iterator

    
    def makeRequest(self,evalscript,time_stamp):
        req = SentinelHubRequest(
            evalscript = evalscript,
            input_data = [
                SentinelHubRequest.input_data(
                    data_collection = self.data_collection,
                    time_interval = (time_stamp - dt.timedelta(hours = 1),
                                     time_stamp + dt.timedelta(hours = 1))
                )
            ],
            responses = [ SentinelHubRequest.output_response("default" , MimeType.PNG)],
            bbox = self.bbox,
            size = self.size,
            config = self.config
        )
        return req

    def trueOrtho(self,evalscript):
        
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
            bbox = BBox(bbox = self.bbox_coords,crs = CRS.WGS84),
            size = size,
            config = self.config
        )
        # print(dir(req))
        # print(req.download_list[0])
        # exit()
        
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
        
    def wmsRequest(self,layer,time):
        
        wms_true_color_request = WmsRequest(
            data_collection= DataCollection.SENTINEL2_L1C,
            # layer="TRUE-COLOR-S2-L1C",
            layer=layer,
            bbox = BBox(bbox = self.bbox_coords,crs = CRS.WGS84),
            # time="2017-12-15",
            time=time,
            width=512,
            height=856,
            config= self.config,
        )
        wms_true_color_img = wms_true_color_request.get_data()
        return wms_true_color_img
        
    
def ex1(config_parameter):
    
    sentinel = SentinelHubImage(config_parameter)
    
    img = sentinel.trueOrtho(evalscript)
    
    if isinstance(img,list):
        if len(img)>0:
            for ii,img_each in enumerate(img):
                
                print(dir(img_each))
                exit()
                
                plot_image(img_each,factor=1/255,save_name=f"out-{ii}.png")
                print(ii,img_each.shape)
    else:
        if img is not None:
            plot_image(img,factor=1/255,save_name=f"out-{ii}.png")
        
    
def wms(config):
    
    
    
    sentinel = SentinelHubImage(config)
    search_iterator = sentinel.catalogSearch() #list(search_iterator) = results
    
    time_differene = dt.timedelta(hours = 1)
    search_iterator.get_timestamps()
    unique_acquisitions = filter_times(search_iterator.get_timestamps() , time_differene)
    print(unique_acquisitions)
    
    requests = []
    for ii,timestamp in enumerate(unique_acquisitions):
        false_color_evalscript
        req = sentinel.makeRequest(evalscript=false_color_evalscript,
                                   time_stamp=timestamp)
        requests.append(req)
    
    ##client
    
    print(sentinel.config)
    print(type(sentinel.config))
    client = SentinelHubDownloadClient(config = sentinel.config)
    download_requests = [req.download_list[0] for req in requests]
    data = client.download(download_requests)
    
    print(data[0].shape)
    print(len(data))
    
    # plot datas ---
    plot_images_2x2(data,unique_acquisitions)
    exit()
    
    
    # for ii,result in enumerate(results):
    #     print(ii,result)
    # exit()
    
    # images = sentinel.wmsRequest(layer="TRUE-COLOR-S2-L1C",time="2017-12-15")
    # print("Returned data is of type = %s and length %d." % 
    #       (type(images), len(images)))
    
    
