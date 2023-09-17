import os
import json
from . import util
from . import setting

# 이 모듈은 다운로드 받은 정보를 관리한다.
# civitai 와의 연결은 최소화하고 local의 관리를 목표로 한다.

Downloaded_Models = dict()      # modelid : [vid:path...] #현재 가지고 있는 모델을 저장한다. 대표 경로가 저장되어 있다.
Downloaded_InfoPath = dict()    # infoPath : vid          #경로를 기준으로 저장한다. info 파일 하나당 버전 하나 / 버전 아이디로 저장된 경로파일을 찾을수 있다. 
                                # get_infopaths 해당버전의 중복된 모든 경로를 구할수 있다

def Test_Models():
    if Downloaded_Models:
        for mid, vidpath in Downloaded_Models.items():
            util.printD(f"{mid} :\n")
            # for vid, path in vidpath:
            #     print(f"{vid} : {path}\n")

def update_downloaded_model():
    global Downloaded_Models
    global Downloaded_InfoPath 
    
    Downloaded_Models, Downloaded_InfoPath = get_model_path()

def get_default_model_folder(mid):
    if mid:
        path = None
        if str(mid) in Downloaded_Models.keys():       
            for vid, version_paths in Downloaded_Models[str(mid)]:
               path = version_paths
               break
            
        if path:
            vfolder , vfile = os.path.split(path)
            return vfolder
            
    return None

def get_default_version_folder(vid):
    if vid:
        
        paths = get_infopaths(vid)        
        
        if not paths:
            return None
        
        for path in paths.keys():
            vfolder , vfile = os.path.split(path)
            return vfolder
            
    return None    

def get_default_version_infopath(vid):
    if vid:
        
        paths = get_infopaths(vid)        
        
        if not paths:
            return None
        
        for path in paths.keys():
            return path
            
    return None
    
def get_model_downloaded_versions(modelid:str):
    
    if not modelid:
        return None
    
    if not Downloaded_Models:                        
        return None
    
    downloaded_version = dict()
    
    if str(modelid) in Downloaded_Models.keys():       
        for vid, version_paths in Downloaded_Models[str(modelid)]:
            vinfo = util.read_json(version_paths)
            if vinfo:                      
                downloaded_version[str(vinfo['id'])] = vinfo['name']
                        
    return downloaded_version if len(downloaded_version) > 0 else None

def get_infopaths( versionid ):
    if not Downloaded_InfoPath:
        return    
    result = {path : vid for path, vid in Downloaded_InfoPath.items() if str(vid) == str(versionid)}
    return result if len(result) > 0 else None  

# modelid를 키로 modelid가 같은 version_info의 File Path를 list로 묶어 반환한다.
def get_model_path()->dict:
    root_dirs = list(set(setting.get_model_folders()))
    file_list = util.search_file(root_dirs,None,[setting.info_ext])
    
    models = dict()
    infopaths = dict()
    
    if not file_list:             
        return None,None
    
    for file_path in file_list:        
        try:
            with open(file_path, 'r') as f:
                json_data = json.load(f)
                if "modelId" in json_data.keys():
                    mid = str(json_data['modelId']).strip()
                    vid = str(json_data['id']).strip()
                    
                    infopaths[file_path] = vid

                    if mid not in models.keys():
                        models[mid] = list()
                        
                    models[mid].append([vid, file_path])    
        except:
            pass
    
    if len(models) > 0:
        return models, infopaths
    
    return None,None
