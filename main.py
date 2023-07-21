import os
import sys
import configparser
from pathlib import Path
import json
cwd = Path(__file__).parent

from  utils.image import *
# from  utils.info import Information

if __name__ == "__main__":
    config_parameter = configparser.ConfigParser()
    config_parameter.read(os.path.join(cwd , "config.ini"))
    
    # ex1(config_parameter)
    wms(config_parameter)
    