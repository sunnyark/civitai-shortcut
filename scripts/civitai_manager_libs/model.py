import os
import json
from . import util
from . import setting

# 이 모듈은 다운로드 받은 정보를 관리한다.
# civitai 와의 연결은 최소화하고 local의 관리를 목표로 한다.

Downloaded_Models = dict()      # modelid : [vid:path...] #현재 가지고 있는 모델을 저장한다. 대표 경로가 저장되어 있다.
# Downloaded_Versions = dict()  # versionid : path        #현재 가지고 있는 버전을 저장한다. 같은 버전이 여러개 있더라도 대표 하나만 저장한다.
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
    # global Downloaded_Versions
    global Downloaded_InfoPath 
    
    Downloaded_Models, Downloaded_InfoPath = get_model_path()
    # Downloaded_Models, Downloaded_Versions, Downloaded_InfoPath = get_model_path()

def get_default_version_folder(vid):
    if vid:
        
        paths = get_infopaths(vid)        
        
        if not paths:
            return None
        
        for path in paths.keys():
            vfolder , vfile = os.path.split(path)
            return vfolder
            
        # if vid in Downloaded_Versions:
        #     path = Downloaded_Versions[str(vid)]        
        #     vfolder , vfile = os.path.split(path)
        #     return vfolder
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
                downloaded_version[vinfo['id']] = vinfo['name']
                        
    return downloaded_version if len(downloaded_version) > 0 else None

def get_infopaths( versionid ):
    if not Downloaded_InfoPath:
        return    
    result = {path : vid for path, vid in Downloaded_InfoPath.items() if vid == versionid}
    return result if len(result) > 0 else None  

# modelid를 키로 modelid가 같은 version_info의 File Path를 list로 묶어 반환한다.
def get_model_path()->dict:
    root_dirs = list(set(setting.get_model_folders()))
    file_list = util.search_file(root_dirs,None,[setting.info_ext])
    
    models = dict()
    # versions = dict()
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
                                            
                    # if vid not in versions.keys():
                    #     versions[vid] = file_path

                    #     if mid not in models.keys():
                    #         models[mid] = list()
                            
                    #     models[mid].append([vid, file_path])                        
        except:
            pass
    
    if len(models) > 0:
        return models, infopaths
        # return models, versions, infopaths
    
    return None,None
    # return None,None,None  
        
# def get_version_images(versionid:str):
#     if not Downloaded_Versions:
#         return

#     file_list = list()    
#     vfolder = None
#     if versionid in Downloaded_Versions.keys():        
#         path = Downloaded_Versions[versionid]
        
#         vinfo = get_version_info(versionid)
#         base = get_save_base_name(vinfo)
        
#         try:                
#             vfolder , vfile = os.path.split(path)            
#             for file in os.listdir(vfolder):
#                 if os.path.isdir(file):
#                     continue
#                 if file.endswith(setting.preview_image_ext) and file.startswith(base):
#                     file_list.append(os.path.join(vfolder, file))            
#         except:
#             return
        
#     return file_list if len(file_list) > 0 else None

# def get_save_base_name(version_info):
#     base = None    
#     primary_file = get_primary_file_by_version_info(version_info)
#     if not primary_file:
#         base = setting.generate_version_foldername(version_info['model']['name'],version_info['name'],version_info['id'])
#     else:
#         base, ext = os.path.splitext(primary_file['name'])   
#     return base
            
# def get_model_info(modelid):
#     def_info = None
#     versions_list = None
#     model_info = None
    
#     if modelid:
#         if Downloaded_Models:
#             if str(modelid) in Downloaded_Models.keys():
#                 file_list = dict()                
#                 for vid, version_paths in Downloaded_Models[str(modelid)]:
#                     file_list[os.path.basename(version_paths)] = version_paths
                
#                 versions_list = list()
#                 for file,path in file_list.items():
#                     vinfo = util.read_json(path)
#                     if vinfo:
#                         versions_list.append(vinfo)
#                         if not def_info:
#                             def_info = vinfo
#                 if def_info:
#                     if "model" in def_info.keys():
#                         model_info = dict()
#                         creator = dict()
#                         creator['username'] =""
#                         creator['image'] = ""
#                         model_info['type'] = def_info['model']['type'] 
#                         model_info['id'] = def_info['modelId'] 
#                         model_info['name'] = def_info['model']['name'] 
#                         model_info['creator'] = creator
#                         model_info['description'] = ""
#                         model_info['tags'] = ""
#                         model_info['modelVersions'] = versions_list        
#     # 모델 인포 를 만들어준다.
#     return model_info

# def get_version_info(versionid:str)->dict:
#     if not versionid:
#         return None

#     if not Downloaded_Versions:
#         return None
                 
#     try:
#         return util.read_json(Downloaded_Versions[versionid])
#     except:
#         pass
    
#     return None

# def get_primary_file_by_version_info(version_info:dict)->dict:
   
#     if not version_info:
#         return
    
#     for file in version_info['files']:
#         if file['primary']:
#             return file        
#     return
