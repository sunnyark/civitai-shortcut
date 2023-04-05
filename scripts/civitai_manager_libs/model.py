import os
import json
import requests
from . import util
from . import civitai
from . import setting

Owned_Models = dict()

def Test_Models():
    if Owned_Models:
        for mid, vlist in Owned_Models.items():
            util.printD(f"{mid} :\n")
            # for path in vlist:
            #     print(f"{path}\n")
            
def Load_Owned_ModelInfo():
    global Owned_Models
    Owned_Models = get_Owned_Model_Info()
    

# 단순히 소유한 모델의 modelid만을 리스트로 반환한다
def get_Owned_ModelId():
    root_dirs = list(set(setting.folders_dict.values()))
    file_list = util.search_file(root_dirs,None,".info")
    modelid_list = list()   

    if file_list:             
        for file_path in file_list:        
            try:
                with open(file_path, 'r') as f:
                    json_data = json.load(f)
                    if "modelId" in json_data.keys():
                        modelid_list.append(str(json_data['modelId']))    
            except:
                pass
            
    if len(modelid_list) > 0:
        return modelid_list
    
    return None

# 단순히 소유한 모델의 타입별 modelid만을 리스트로 반환한다
def get_Owned_ModelId_byType(ctype):
    root_dir = [setting.folders_dict[setting.content_types_dict[ctype]]]
    file_list = util.search_file(root_dir,None,".info")
    modelid_list = list()   

    if file_list:             
        for file_path in file_list:        
            try:
                with open(file_path, 'r') as f:
                    json_data = json.load(f)
                    if "modelId" in json_data.keys():
                        modelid_list.append(str(json_data['modelId']))
            except:
                pass
            
    if len(modelid_list) > 0:
        return modelid_list
    
    return None

# modelid를 키로 modelid가 같은 version_info를 list로 묶어 반환한다.
def get_Owned_Model_Info()->dict:
    #root_dirs = [setting.folders_dict[setting.content_types_dict[ctype]]]
    root_dirs = list(set(setting.folders_dict.values()))
    file_list = util.search_file(root_dirs,None,".info")
    models = dict()
    
    if file_list:             
        for file_path in file_list:        
            try:
                with open(file_path, 'r') as f:
                    json_data = json.load(f)
                    if "modelId" in json_data.keys():
                        mid = str(json_data['modelId'])
                        if mid not in models.keys():
                            models[mid] = list()
                        models[mid].append(json_data)
            except:
                pass
            
    if len(models) > 0:
        return models
    
    return None

# modelid를 키로 modelid가 같은 version_info의 File Path를 list로 묶어 반환한다.
def get_Owned_Model_Path()->dict:
    #root_dirs = [setting.folders_dict[setting.content_types_dict[ctype]]]
    root_dirs = list(set(setting.folders_dict.values()))
    file_list = util.search_file(root_dirs,None,".info")
    models = dict()
    
    if file_list:             
        for file_path in file_list:        
            try:
                with open(file_path, 'r') as f:
                    json_data = json.load(f)
                    if "modelId" in json_data.keys():
                        mid = str(json_data['modelId'])
                        if mid not in models.keys():
                            models[mid] = list()
                        models[mid].append(file_path)
            except:
                pass
            
    if len(models) > 0:
        return models
    
    return None