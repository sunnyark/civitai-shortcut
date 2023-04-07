import os
from . import model
from . import civitai

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
                    model_type = def_info['model']['type']
                
    return owned_info, model_type, def_name, [v for v in versions_list]

def get_model_title_name(version_info:dict)->str:
    if not version_info:
        return
    
    title_name = ""
    if 'model' not in version_info.keys():
        return
        
    title_name = f"### {version_info['model']['name']} : {version_info['name']}"
    return title_name

def get_version_description(version_info:dict):
    output_html = ""
    output_training = ""

    files_name = []
    
    html_typepart = ""
    html_trainingpart = ""
    html_modelpart = ""
    html_versionpart = ""
    html_descpart = ""
    html_dnurlpart = ""
    html_imgpart = ""
    html_modelurlpart = ""
    
    
    if not version_info:
        return "",None,None,None
    
    if 'modelId' not in version_info:
        return "",None,None,None
        
    if "model" not in version_info.keys():    
        return "",None,None,None
    
    model_id = version_info['modelId']
    model_type = version_info['model']['type']
    model_name = version_info['model']['name']
    model_url = civitai.Url_Page()+str(model_id)
                    
    html_typepart = f"<br><b>Type: {model_type}</b>"    
    html_modelpart = f'<br><b>Model: <a href="{model_url}" target="_blank">{model_name}</a></b>'
    html_modelurlpart = f'<br><b><a href="{model_url}" target="_blank">Civitai Hompage << Here</a></b><br>'

    model_version_name = version_info['name']

    if 'trainedWords' in version_info:  
        output_training = ", ".join(version_info['trainedWords'])
        html_trainingpart = f'<br><b>Training Tags:</b> {output_training}'

    if 'description' in version_info:  
        if version_info['description']:
            html_descpart = f"<br><b>Version : {version_info['name']} Description</b><br>{version_info['description']}<br>"
                            
    html_versionpart = f"<br><b>Version:</b> {model_version_name}"

    if 'files' in version_info:                                
        for file in version_info['files']:
            files_name.append(file['name'])
            html_dnurlpart = html_dnurlpart + f"<br><a href={file['downloadUrl']}><b>Download << Here</b></a>"     
                        
    output_html = html_typepart + html_modelpart + html_versionpart + html_trainingpart + "<br>" +  html_modelurlpart + html_dnurlpart + "<br>" + html_descpart + "<br>" + html_imgpart
    
    return output_html, output_training, files_name, model_type

from . import util
def get_version_description_gallery(versionid):
    if not versionid:
        return None,None
    imagelist = model.get_version_images(versionid)
    return imagelist,imagelist

    
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
