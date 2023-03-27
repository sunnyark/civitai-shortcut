import re
import json
import requests
from . import util

# Set the URL for the API endpoint

url_dict = {
    "modelPage":"https://civitai.com/models/",
    "modelId": "https://civitai.com/api/v1/models/",
    "modelVersionId": "https://civitai.com/api/v1/model-versions/",
    "hash": "https://civitai.com/api/v1/model-versions/by-hash/"
}

content_types_dict = {
    "All" : "",    
    "Checkpoint": "Checkpoint",
    "LORA": "LORA",
    "LyCORIS": "LoCon",
    "Hypernetwork": "Hypernetwork",
    "TextualInversion": "TextualInversion",            
    "AestheticGradient":"AestheticGradient",    
    "Controlnet" : "Controlnet", 
    "Poses":"Poses"
}

page_dict = {
    "limit" : 50,
}

page_action_dict = {
    "search" : "Search", 
    "prevPage" : "Prev Page",
    "nextPage" : "Next Page",    
}

models_exts = (".bin", ".pt", ".safetensors", ".ckpt")        

# get image with full size
# width is in number, not string
# 파일 인포가 있는 원본 이미지 주소이다.
def get_full_size_image_url(image_url, width):
    return re.sub('/width=\d+/', '/width=' + str(width) + '/', image_url)

# get id from url
def get_model_id_from_url(url):
    id = ""

    if not url:
        return ""

    if url.isnumeric():
        # is already an id
        id = str(url)
        return id
    
    s = url.split("/")
    if len(s) < 2:
        return ""
    
    if s[-2].isnumeric():
        id  = s[-2]
    elif s[-1].isnumeric():
        id  = s[-1]
    else:
        return ""
    
    return id

def request_models(api_url=None):
    # Make a GET request to the API
    response = requests.get(api_url)

    # Check the status code of the response
    if response.status_code != 200:
        print("Request failed with status code: {}".format(response.status_code))
        exit()

    data = json.loads(response.text)
    return data

def get_model_info_by_id(id:str) -> dict:
    content = None
    if not id:
        return
    
    try:            
        r = requests.get(url_dict["modelId"]+str(id))            
        content = r.json()
    except Exception as e:
        return

    if not content:
        return    
    return content

def get_model_info_by_version_id(version_id:str) -> dict:        
    if not version_id:
        return
    
    version_info = get_version_info_by_version_id(version_id) 
    return get_model_info_by_version_info(version_info)

def get_model_info_by_version_info(version_info) -> dict:    
    if not version_info:
        return 
    
    try:
        return get_model_info_by_id(version_info['modelId'])
    except Exception as e:
        return
    
def get_version_info_by_version_id(version_id:str) -> dict:    
    content = None
    if not version_id:                
        return 
    
    try:
        r = requests.get(url_dict["modelVersionId"]+str(version_id))
        content = r.json()
    except Exception as e:
        return None

    return content   

def get_latest_version_info_by_model_id(id:str) -> dict:

    model_info = get_model_info_by_id(id)
    if not model_info:
        return

    if "modelVersions" not in model_info.keys():
        return
            
    def_version = model_info["modelVersions"][0]
    if not def_version:
        return
    
    if "id" not in def_version.keys():
        return
    
    version_id = def_version["id"]

    version_info = get_version_info_by_version_id(str(version_id))

    return version_info

def get_version_id_by_version_name(model_id:str,name:str)->str:
    version_id = None
    if not model_id:
        return 
    
    model_info = get_model_info_by_id(model_id)
    if not model_info:
        return
    
    if "modelVersions" not in model_info.keys():
        return
            
    version_id = None
    
    for version in model_info['modelVersions']:
        if version['name'] == name:
            version_id = version['id']
            break
        
    return version_id

def get_files_by_version_info(version_info:dict)->dict:
    download_files = {}
    
    if not version_info:                
        return         
    
    for file in version_info['files']:
        download_files[file['name']] = file
    
    return download_files

def get_files_by_version_id(version_id=None)->dict:   
    if not version_id:                
        return         
    
    version_info = get_version_info_by_version_id(version_id)          
    
    return get_files_by_version_info(version_info)

def get_primary_file_by_version_info(version_info:dict)->dict:
   
    if not version_info:
        return
    
    for file in version_info['files']:
        if file['primary']:
            return file        
    return
        
def get_primary_file_by_version_id(version_id=None)->dict:   
    if not version_id:                
        return         
    
    version_info = get_version_info_by_version_id(version_id)          
    
    return get_primary_file_by_version_info(version_info)

def get_images_by_version_id(version_id=None)->dict:   
    if not version_id:                
        return         
    
    version_info = get_version_info_by_version_id(version_id)          
    
    return get_images_by_version_info(version_info)

                
def get_images_by_version_info(version_info:dict)->dict:   
    if not version_info:                
        return         
    
    return version_info["images"]


def get_triger_by_version_info(version_info:dict)->str:   
    if not version_info:                
        return         
    try:
        triger_words = ", ".join(version_info['trainedWords'])    
        if len(triger_words.strip()) > 0:
            return triger_words
    except:
        pass
    
    return

def get_triger_by_version_id(version_id=None)->str:   
    if not version_id:                
        return         
    
    version_info = get_version_info_by_version_id(version_id)          
    
    return get_triger_by_version_info(version_info)
