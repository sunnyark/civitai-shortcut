import os
import json
import requests
from . import util
from . import civitai

# url에서 model info 정보를 반환한다
def get_selected_model_info_by_url(url:str):
    model = None
    versions_list = []
    def_version = None
    
    if not url:
        return None,None,None,None
    
    model_id = civitai.get_model_id_from_url(url)    
    
    if not model_id:
        return None,None,None,None
    
    model_url = f"{civitai.url_dict['modelId']}{model_id}"             
    
    try:
        r = requests.get(model_url)
        model = r.json()
    except Exception as e:
        util.printD("Load failed")
        return None,None,None,None

    if not model:
        return None,None,None,None   
        
    if "modelVersions" not in model.keys():
        return None,None,None,None
    
    def_version = model["modelVersions"][0]
    
    if not def_version:
        return None,None,None,None
                    
    for version_info in model['modelVersions']:
        versions_list.append(version_info['name'])
    
    return model_id, [v for v in versions_list], def_version['name'], def_version['id']
                        
def get_search_page_action(action:str, json_state:dict, content_type, sort_type, search_term, show_nsfw=True):
    json_data = json_state
    if action == civitai.page_action_dict['search']:
        if search_term:
            search_term = search_term.strip().replace(" ", "%20")
        
        c_types = civitai.content_types_dict[content_type]
        urls = f"{civitai.url_dict['modelId']}?limit={civitai.page_dict['limit']}"             
        if c_types and len(c_types) > 0:        
            urls = f"{urls}&types={c_types}"
        urls = f"{urls}&sort={sort_type}&query={search_term}"    
        json_data = civitai.request_models(urls)
        
    elif action == civitai.page_action_dict['prevPage']:
        try:        
            json_data = civitai.request_models(json_state['metadata']['prevPage'])
        except:   
            pass
    elif action == civitai.page_action_dict['nextPage']:
        try:        
            json_data = civitai.request_models(json_state['metadata']['nextPage'])
        except:   
            pass

    if json_data:
        json_state = json_data
                
    try:
        json_state['items']
    except:
        return None,None    
                            
    models_name=[]
        
    if show_nsfw:
        for model in json_state['items']:
            models_name.append(model['name'])
    else:
        for model in json_state['items']:
            temp_nsfw = model['nsfw']
            if not temp_nsfw:
                models_name.append(model['name'])
    return [v for v in models_name],json_state
                
# 버전 모델 인포 데이터를 파일에서 읽어옴
def load_version_info(path)->dict:
    version_info = None
    with open(path, 'r') as f:
        try:
            version_info = json.load(f)
        except Exception as e:
            util.printD("Selected file is not json: " + path)
            return
        
    return version_info

        
 # 버전 모델 인포 데이터를 파일로 저장
def write_version_info(path, version_id:str)->dict:
    if not version_id: 
        return
    
    version_info = civitai.get_version_info_by_version_id(version_id)
    
    if not version_info:
        return
    
    try:
        with open(path, 'w') as f:
            f.write(json.dumps(version_info, indent=4))
    except Exception as e:
            return                
    
    return version_info

 # 버전 모델 인포 데이터를 파일로 저장
def write_version_info_by_version_id(folder, version_id:str)->str:
    if not version_id: 
        return
    
    version_info = civitai.get_version_info_by_version_id(version_id)
    
    if not version_info:
        return

    return write_version_info_by_version_info(folder, version_info)

def write_version_info_by_version_info(folder, version_info:dict)->str:   
    if not version_info:
        return

    primary_file = civitai.get_primary_file_by_version_info(version_info)
    
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
        
    version_info = civitai.get_version_info_by_version_id(version_id)
    
    if not version_info:
        return
    
    return write_triger_words_by_version_info(folder,version_info)
    
def write_triger_words_by_version_info(folder, version_info:dict)->str:   
    if not version_info:
        return
    
    triger_words = civitai.get_triger_by_version_info(version_info)

    if not triger_words:
        return 

    primary_file = civitai.get_primary_file_by_version_info(version_info)
    
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
