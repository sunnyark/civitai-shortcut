import os
from . import model

def get_selected_owned_modelinfo(modelid):
    model_type= None
    owned_info = ""
    def_name = ""
    def_info = None
    versions_list = []    
    if modelid:
        if model.Owned_Models:
            if str(modelid) in model.Owned_Models.keys():
                file_list = dict()
                
                for version_paths in model.Owned_Models[str(modelid)]:
                    file_list[os.path.basename(version_paths)] = version_paths
                
                for file,path in file_list.items():
                    vinfo = model.read_owned_versioninfo(path)
                    if vinfo:
                        def_info = vinfo
                        try:  
                            if owned_info != "":
                                owned_info = owned_info + "\n"
                            owned_info = owned_info + f"{def_info['name']}"
                            versions_list.append(def_info['name'])  
                        except:
                            pass

            if def_info:
                def_name = def_info['name']
                if "model" in def_info.keys():
                    model_type = def_info['type']
                
    return owned_info, model_type, def_name, [v for v in versions_list]

# def get_selected_owned_versioninfo(model_id:str):
#     model_name = None
#     model_type = None
#     def_id = None
#     def_name = None
#     def_image = None
#     model_url = None
    
#     model_info = civitai.get_model_info(model_id)
#     if model_info:
#         model_name = model_info['name']
#         model_type = model_info['type']
#         model_url = f"{civitai.Url_ModelId()}{model_id}"
        
#         if "modelVersions" in model_info.keys():            
#             def_version = model_info["modelVersions"][0]
#             def_id = def_version['id']
#             def_name = def_version['name']
            
#             if 'images' in def_version.keys():
#                 if len(def_version["images"]) > 0:
#                     img_dict = def_version["images"][0]
#                     def_image = img_dict["url"]                  
        
#     return model_name, model_type, model_url, def_id, def_name, def_image
