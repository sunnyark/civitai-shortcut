import os
import json
from . import util
from . import setting

# 이 모듈은 다운로드 받은 정보를 관리한다.
# civitai 와의 연결은 최소화하고 local의 관리를 목표로 한다.

Owned_Models = dict()
Owned_Versions = dict()

def Test_Models():
    if Owned_Models:
        for mid, vlist in Owned_Models.items():
            util.printD(f"{mid} :\n")
            # for path in vlist:
            #     print(f"{path}\n")
            
def Load_Owned_Models():
    global Owned_Models
    global Owned_Versions
    
    Owned_Models, Owned_Versions = get_owned_modelpath()
    
# 단순히 소유한 모델의 modelid만을 리스트로 반환한다
def get_owned_modelid():
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
def get_owned_modelid_byType(ctype):
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
def get_owned_modelinfo()->dict:
    #root_dirs = [setting.folders_dict[setting.content_types_dict[ctype]]]
    root_dirs = list(set(setting.folders_dict.values()))
    file_list = util.search_file(root_dirs,None,".info")
    models = dict()
    versions = dict()
    
    if file_list:             
        for file_path in file_list:        
            try:
                with open(file_path, 'r') as f:
                    json_data = json.load(f)
                    if "modelId" in json_data.keys():
                        mid = str(json_data['modelId']).strip()
                        vid = str(json_data['id']).strip()
                        
                        if mid not in models.keys():
                            models[mid] = list()
                            
                        models[mid].append(json_data)
                        versions[vid] = file_path                        
            except:
                pass
            
    if len(models) > 0:
        return models,versions
    
    return None,None

# modelid를 키로 modelid가 같은 version_info의 File Path를 list로 묶어 반환한다.
def get_owned_modelpath()->dict:
    #root_dirs = [setting.folders_dict[setting.content_types_dict[ctype]]]
    root_dirs = list(set(setting.folders_dict.values()))
    file_list = util.search_file(root_dirs,None,".info")
    models = dict()
    versions = dict()
    
    if file_list:             
        for file_path in file_list:        
            try:
                with open(file_path, 'r') as f:
                    json_data = json.load(f)
                    if "modelId" in json_data.keys():
                        mid = str(json_data['modelId']).strip()
                        vid = str(json_data['id']).strip()
                        
                        if mid not in models.keys():
                            models[mid] = list()
                        models[mid].append(file_path)
                        versions[vid] = file_path                        
            except:
                pass
            
    if len(models) > 0:
        return models,versions
    
    return None,None

def get_version_id_by_version_name(modelid, versionname):
    if not modelid:
        return 

    if not Owned_Models:
        return
        
    if str(modelid) in Owned_Models.keys():
        file_list = dict()
        for version_paths in Owned_Models[str(modelid)]:
            file_list[os.path.basename(version_paths)] = version_paths
        
        for file,path in file_list.items():
            vinfo = read_owned_versioninfo(path)
            try:  
                if vinfo['name'] == versionname:
                    return vinfo['id']
            except:
                pass        
    return None

def get_default_version_info(modelid):
    if not modelid:
        return 

    if not Owned_Models:
        return
        
    if str(modelid) in Owned_Models.keys():
        file_list = dict()
        for version_paths in Owned_Models[str(modelid)]:
            file_list[os.path.basename(version_paths)] = version_paths
                
        for file,path in file_list.items():
            return read_owned_versioninfo(path)
        
    return None        
    

def get_version_info(versionid:str)->dict:
    if not versionid:
        return None

    if not Owned_Versions:
        return None
    
    # if versionid in Owned_Versions.keys():
    #     util.printD(Owned_Versions[versionid])

    # for vid,path in Owned_Versions.items():
    #     util.printD(f"{str(vid)} : {path}")

    # util.printD(f"end {versionid}")                
    try:
        return read_owned_versioninfo(Owned_Versions[versionid])
    except:
        pass
    
    return None
    
def get_version_images(versionid:str):
    if not Owned_Versions:
        return

    file_list = list()    
    if versionid in Owned_Versions.keys():        
        path = Owned_Versions[versionid]  
        try:
            vfolder , vfile = os.path.split(path)
            # versionname . civitai.info 형식이다.
            # 그래서 두번
            base , ext = os.path.splitext(vfile)
            base , ext = os.path.splitext(base)
            
            for file in os.listdir(vfolder):
                if os.path.isdir(file):
                    continue
                if file.endswith(".png") and file.startswith(base):
                    file_list.append(os.path.join(vfolder,file))            
        except:
            return
        
    return file_list if len(file_list) > 0 else None
            
# 버전 모델 인포 데이터를 파일에서 읽어옴
def read_owned_versioninfo(path)->dict:
    version_info = None
    if not path:
        return None    
    try:
        with open(path, 'r') as f:
            version_info = json.load(f)            
    except:
        return None
                
    return version_info

