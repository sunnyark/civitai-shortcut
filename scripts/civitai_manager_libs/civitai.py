import os
import re
import json
import requests
from . import util

# Set the URL for the API endpoint

url_dict = {
    "modelPage":"https://civitai.com/models/",
    "modelId": "https://civitai.com/api/v1/models/",
    "modelVersionId": "https://civitai.com/api/v1/model-versions/",
    "modelHash": "https://civitai.com/api/v1/model-versions/by-hash/",
    "imagePage" :  "https://civitai.com/api/v1/images/"
}

def Url_Page():
    return url_dict["modelPage"]

def Url_ModelId():
    return url_dict["modelId"]

def Url_VersionId():
    return url_dict["modelVersionId"]

def Url_Hash():
    return url_dict["modelHash"]

def Url_ImagePage():
    return url_dict["imagePage"]

def request_models(api_url=None):
    try:
        # Make a GET request to the API
        with requests.get(api_url) as response:
            # Check the status code of the response
            if response.status_code != 200:
                util.printD("Request failed with status code: {}".format(response.status_code))
                return         
            data = json.loads(response.text)
    except Exception as e:
        return
    return data

def get_model_info(id:str) -> dict:    
    if not id:
        return
    
    content = None
    try:            
        with requests.get(Url_ModelId()+str(id)) as response:
            content = response.json()
    except Exception as e:
        return None
    
    if 'id' not in content.keys():
        return None
    
    return content

def get_model_info_by_version_id(version_id:str) -> dict:        
    if not version_id:
        return
    
    version_info = get_version_info_by_version_id(version_id) 
    return get_model_info_by_version_info(version_info)

def get_model_info_by_version_info(version_info) -> dict:    
    if not version_info:
        return 
    return get_model_info(version_info['modelId'])
  
def get_version_info_by_hash(hash) -> dict:        
    if not hash:                
        return 
    
    content = None
    
    try:
        with requests.get(f"{Url_Hash()}{hash}") as response:
            content = response.json()
    except Exception as e:
        return None

    if 'id' not in content.keys():
        return None
    
    return content  
  
def get_version_info_by_version_id(version_id:str) -> dict:        
    if not version_id:                
        return 
    
    content = None
    
    try:
        with requests.get(Url_VersionId()+str(version_id)) as response:
            content = response.json()
    except Exception as e:
        return None

    if 'id' not in content.keys():
        return None
    
    return content   

def get_latest_version_info_by_model_id(id:str) -> dict:

    model_info = get_model_info(id)
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
    
    model_info = get_model_info(model_id)
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

# def get_files_by_version_info(version_info:dict)->dict:
#     download_files = {}
    
#     if not version_info:                
#         return         
    
#     for file in version_info['files']:
#         download_files[file['name']] = file
    
#     return download_files

def get_files_by_version_info(version_info:dict)->dict:
    download_files = {}
    
    if not version_info:                
        return         
    
    for file in version_info['files']:
        download_files[str(file['id'])] = file
    
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

def write_model_info(file, model_info:dict)->str:   
    if not model_info:
        return False
           
    try:
        with open(file, 'w') as f:
            f.write(json.dumps(model_info, indent=4))
    except Exception as e:
            return False
    
    return True

def write_version_info(file, version_info:dict):   
    if not version_info:
        return False

    try:
        with open(file, 'w') as f:
            f.write(json.dumps(version_info, indent=4))
    except Exception as e:
            return False              
    
    return True

def write_triger_words_by_version_id(file, version_id:str):
    if not version_id: 
        return False
        
    version_info = get_version_info_by_version_id(version_id)
    
    return write_triger_words_by_version_info(file,version_info)
    
def write_triger_words_by_version_info(file, version_info:dict):   
    if not version_info:
        return False
    
    triger_words = get_triger_by_version_info(version_info)
        
    if not triger_words:
        return False

    try:
        with open(file, 'w') as f:
            f.write(triger_words)
    except Exception as e:
        return False
        
    return True
