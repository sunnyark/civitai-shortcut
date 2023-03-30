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
    "modelHash": "https://civitai.com/api/v1/model-versions/by-hash/"
}

models_exts = (".bin", ".pt", ".safetensors", ".ckpt")        

def Url_Page():
    return url_dict["modelPage"]

def Url_ModelId():
    return url_dict["modelId"]

def Url_VersionId():
    return url_dict["modelVersionId"]

def Url_Hash():
    return url_dict["modelHash"]

def request_models(api_url=None):
    # Make a GET request to the API
    response = requests.get(api_url)

    # Check the status code of the response
    if response.status_code != 200:
        util.printD("Request failed with status code: {}".format(response.status_code))
        exit()

    data = json.loads(response.text)
    return data

def get_model_info_by_model_id(id:str) -> dict:    
    if not id:
        return
    
    content = None
    try:            
        r = requests.get(Url_ModelId()+str(id))            
        content = r.json()
    except Exception as e:
        pass
  
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
        return get_model_info_by_model_id(version_info['modelId'])
    except Exception as e:
        return
    
def get_version_info_by_version_id(version_id:str) -> dict:    
    content = None
    if not version_id:                
        return 
    
    try:
        r = requests.get(Url_VersionId()+str(version_id))
        content = r.json()
    except Exception as e:
        pass

    return content   

def get_latest_version_info_by_model_id(id:str) -> dict:

    model_info = get_model_info_by_model_id(id)
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
    
    model_info = get_model_info_by_model_id(model_id)
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
                
# 버전 모델 인포 데이터를 파일에서 읽어옴
def load_version_info(path)->dict:
    version_info = None
    with open(path, 'r') as f:
        try:
            version_info = json.load(f)
        except Exception as e:
            util.printD("Selected file is not json: " + path)
            pass
        
    return version_info      

 # 버전 모델 인포 데이터를 파일로 저장
def write_version_info_by_version_id(folder, version_id:str)->str:
    if not version_id: 
        return
    
    version_info = get_version_info_by_version_id(version_id)
    
    return write_version_info_by_version_info(folder, version_info)

def write_version_info_by_version_info(folder, version_info:dict)->str:   
    if not version_info:
        return

    primary_file = get_primary_file_by_version_info(version_info)
    
    if not primary_file:
        return

    base, ext = os.path.splitext(primary_file['name'])
    path_info_file = os.path.join(folder, f"{base}.civitai.info")
            
    try:
        with open(path_info_file, 'w') as f:
            f.write(json.dumps(version_info, indent=4))
    except Exception as e:
            return                
    
    return f"{base}.civitai.info"

def write_triger_words_by_version_id(folder, version_id:str)->str:
    if not version_id: 
        return    
        
    version_info = get_version_info_by_version_id(version_id)
    
    return write_triger_words_by_version_info(folder,version_info)
    
def write_triger_words_by_version_info(folder, version_info:dict)->str:   
    if not version_info:
        return
    
    triger_words = get_triger_by_version_info(version_info)

    if not triger_words:
        return 

    primary_file = get_primary_file_by_version_info(version_info)
    
    if not primary_file:
        return

    base, ext = os.path.splitext(primary_file['name'])
    path_triger_file = os.path.join(folder, f"{base}.triger.txt")

    try:
        with open(path_triger_file, 'w') as f:
            f.write(triger_words)
    except Exception as e:
        return
        
    return f"{base}.triger.txt"
