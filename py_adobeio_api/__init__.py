from libs.read_config import load_config_file
from libs.adobe_rest import AdobeIORestAPI

def get_api(config={}):
    return AdobeIORestAPI(config)

def get_api_from_filename(config_file):
    return get_api(load_config_file(config_file))