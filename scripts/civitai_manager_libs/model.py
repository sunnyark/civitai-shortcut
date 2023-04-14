import os
import json
from . import util
from . import setting

# 이 모듈은 다운로드 받은 정보를 관리한다.
# civitai 와의 연결은 최소화하고 local의 관리를 목표로 한다.

Downloaded_Models = dict()      # modelid : [vid:path]
Downloaded_Versions = dict()    # versionid : path

def Test_Models():
    if Downloaded_Models:
        for mid, vidpath in Downloaded_Models.items():
            util.printD(f"{mid} :\n")
            # for vid, path in vidpath:
            #     print(f"{vid} : {path}\n")

def update_downloaded_model():
    global Downloaded_Models
    global Downloaded_Versions
    
    Downloaded_Models, Downloaded_Versions = get_model_path()
    
# 단순히 소유한 모델의 modelid만을 리스트로 반환한다
def get_modelid():
    root_dirs = list(set(setting.folders_dict.values()))
    file_list = util.search_file(root_dirs,None,setting.info_ext)
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
def get_modelid_byType(ctype):
    root_dir = [setting.folders_dict[setting.content_types_dict[ctype]]]
    file_list = util.search_file(root_dir,None,setting.info_ext)
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
def get_model_info()->dict:
    #root_dirs = [setting.folders_dict[setting.content_types_dict[ctype]]]
    root_dirs = list(set(setting.folders_dict.values()))
    file_list = util.search_file(root_dirs,None,setting.info_ext)
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

def get_model_version_list(modelid:str):
    downloaded_version_list = list()
    if modelid:
        if Downloaded_Models:                        
            if str(modelid) in Downloaded_Models.keys():
                file_list = dict()
                
                for vid, version_paths in Downloaded_Models[str(modelid)]:
                    file_list[os.path.basename(version_paths)] = version_paths
                
                for file,path in file_list.items():
                    vinfo = util.read_json(path)
                    if vinfo:                      
                        downloaded_version_list.append(vinfo['name'])
                        
    return downloaded_version_list if len(downloaded_version_list) > 0 else None

# modelid를 키로 modelid가 같은 version_info의 File Path를 list로 묶어 반환한다.
def get_model_path()->dict:
    #root_dirs = [setting.folders_dict[setting.content_types_dict[ctype]]]
    root_dirs = list(set(setting.folders_dict.values()))
    file_list = util.search_file(root_dirs,None,setting.info_ext)
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
                        models[mid].append([vid, file_path])
                        #models[mid].append(file_path)
                        versions[vid] = file_path
                        
            except:
                pass
    
    if len(models) > 0:
        return models, versions
    
    return None,None

def get_version_id_by_version_name(modelid, versionname):
    if not modelid:
        return 

    if not Downloaded_Models:
        return
        
    if str(modelid) in Downloaded_Models.keys():
        file_list = dict()
        for vid, version_paths in Downloaded_Models[str(modelid)]:
            file_list[os.path.basename(version_paths)] = version_paths
        
        for file, path in file_list.items():
            vinfo = util.read_json(path)
            try:  
                if vinfo['name'] == versionname:
                    return vinfo['id']
            except:
                pass        
    return None

def get_default_version_info(modelid):
    if not modelid:
        return 

    if not Downloaded_Models:
        return
        
    if str(modelid) in Downloaded_Models.keys():
        file_list = dict()
        for vid, version_paths in Downloaded_Models[str(modelid)]:
            file_list[os.path.basename(version_paths)] = version_paths
                
        for file,path in file_list.items():
            return util.read_json(path)
        
    return None        
    

def get_version_info(versionid:str)->dict:
    if not versionid:
        return None

    if not Downloaded_Versions:
        return None
                 
    try:
        return util.read_json(Downloaded_Versions[versionid])
    except:
        pass
    
    return None

def get_images():
    if not Downloaded_Versions:
        return

    file_list = list()    
    for versionid in Downloaded_Versions.keys():
        tmp_list = get_version_images(versionid)
        if tmp_list:
            file_list.extend(tmp_list)
    
    file_list = list(set(file_list))
        
    return file_list if len(file_list) > 0 else None    

def get_version_images(versionid:str):
    if not Downloaded_Versions:
        return

    file_list = list()    
    vfolder = None
    if versionid in Downloaded_Versions.keys():        
        path = Downloaded_Versions[versionid]  
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
                    file_list.append(os.path.join(vfolder, file))            
        except:
            return
        
    return file_list if len(file_list) > 0 else None

# 다운로드 받은 파일만 리턴한다
def get_version_files(versioninfo):
    if not Downloaded_Versions:
        return

    if not versioninfo:
        return
    
    versionid = str(versioninfo['id'])

    infofiles = list()
        
    if 'files' in versioninfo.keys():
        for file in versioninfo['files']:
            infofiles.append(file['name'])
    else:
        return
               
    file_list = list()    
    vfolder = None

    if versionid in Downloaded_Versions.keys():        
        path = Downloaded_Versions[versionid]  
        try:
            vfolder , vfile = os.path.split(path)
            for file in os.listdir(vfolder):
                if os.path.isdir(file):
                    continue

                if file in infofiles:
                    file_list.append(os.path.join(vfolder, file))
        except:
            return
        
    return file_list if len(file_list) > 0 else None

def get_model_info(modelid):
    def_info = None
    versions_list = None
    model_info = None
    
    if modelid:
        if Downloaded_Models:
            if str(modelid) in Downloaded_Models.keys():
                file_list = dict()                
                for vid, version_paths in Downloaded_Models[str(modelid)]:
                    file_list[os.path.basename(version_paths)] = version_paths
                
                versions_list = list()
                for file,path in file_list.items():
                    vinfo = util.read_json(path)
                    if vinfo:
                        versions_list.append(vinfo)
                        if not def_info:
                            def_info = vinfo
                if def_info:
                    if "model" in def_info.keys():
                        model_info = dict()
                        model_info['type'] = def_info['model']['type'] 
                        model_info['id'] = def_info['modelId'] 
                        model_info['name'] = def_info['model']['name'] 
                        model_info['modelVersions'] = versions_list        
    # 모델 인포 를 만들어준다.
    return model_info