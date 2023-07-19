import os
from PIL import Image
import io

from pathlib import Path
cwd = Path(__file__).parent.parent

import numpy as np
from utils.utils import plot_image
from script.eval import evalscript_clm,evalscript

# from evalscript.query_text import evalscript,setJsonRequestScript
from sentinelhub import SHConfig
from sentinelhub import (
    DataCollection,
    DownloadRequest,
    MimeType,
    MosaickingOrder
)


class Information:
    def __init__(self):
        print("Informations = ")
        
    @property
    def collections(self):
        for collection in DataCollection.get_available_collections():
            print(collection)
        
        print(dir(DataCollection.SENTINEL2_L1C))
        print(type(DataCollection.SENTINEL2_L1C))
        print(DataCollection.SENTINEL2_L1C.__doc__)
            
    
    
        
    
    
    
    
    
    
