import os
from . import util
from . import model
from . import civitai
from . import ishortcut


def Load_Downloaded_Models():
    model.update_downloaded_model()

def is_latest(modelid:str)->bool:
    if not modelid:
        return False
   
    if modelid in model.Downloaded_Models.keys():
        # civitai 에서 최신 모델 정보를 가져온다.
        version_info = civitai.get_latest_version_info_by_model_id(modelid)
        if version_info:
            latest_versionid = str(version_info['id']).strip()                
            
            # 현재 가지고 있는 버전들을 가져온다.                
            dnver_list = list()                
            for vid, version_paths in model.Downloaded_Models[str(modelid)]:
                dnver_list.append(str(vid).strip())
                
            if latest_versionid in dnver_list:                        
                return True
    return False
           
def get_model_information(modelid:str=None, versionid:str=None, ver_index:int=None):
    # 현재 모델의 정보를 가져온다.
    model_info = None
    version_info = None
    
    if modelid:
        model_info = model.get_model_info(modelid)      
        version_info = dict()
        if model_info:
            # 숏컷 정보가 있다면 그것으로 대체한다.
            sc_model_info = ishortcut.get_model_info(modelid)
            if sc_model_info:                
                if "modelVersions" in model_info.keys():
                    sc_model_info["modelVersions"] = model_info["modelVersions"]
                    model_info = sc_model_info
                    
            if not versionid and not ver_index:
                if "modelVersions" in model_info.keys():
                    version_info = model_info["modelVersions"][0]
                    if version_info["id"]:
                        versionid = version_info["id"]
            elif versionid:
                if "modelVersions" in model_info.keys():
                    for ver in model_info["modelVersions"]:                        
                        if versionid == ver["id"]:
                            version_info = ver                
            else:
                if "modelVersions" in model_info.keys():
                    if len(model_info["modelVersions"]) > 0:
                        version_info = model_info["modelVersions"][ver_index]
                        if version_info["id"]:
                            versionid = version_info["id"]
                            
    # 존재 하는지 판별하고 있다면 내용을 얻어낸다.
    if model_info and version_info:        
        version_name = version_info["name"]
        model_type = model_info['type']                    
        versions_list = list()            
        for ver in model_info['modelVersions']:
            versions_list.append(ver['name'])
        
        model_url = civitai.Url_ModelId() + str(modelid)        
        dhtml, triger, flist = get_version_description(version_info, model_info)
        title_name = f"### {model_info['name']} : {version_info['name']}"           
        gallery_url, images_url = get_version_description_gallery(versionid)
        
        return model_info, versionid,version_name,model_url,model_type,versions_list,dhtml,triger,flist,title_name,gallery_url,images_url
    return None, None,None,None,None,None,None,None,None,None,None,None
        
def get_version_description_gallery(versionid:str):
    if not versionid:
        return None,None
    imagelist = model.get_version_images(str(versionid))
    return imagelist, imagelist

      
def get_version_description(version_info:dict,model_info:dict=None):
    output_html = ""
    output_training = ""

    files_name = []
    
    html_typepart = ""
    html_creatorpart = ""
    html_trainingpart = ""
    html_modelpart = ""
    html_versionpart = ""
    html_descpart = ""
    html_dnurlpart = ""
    html_imgpart = ""
    html_modelurlpart = ""
    
    model_id = None
    
    if version_info:        
        if 'modelId' in version_info:            
            model_id = version_info['modelId']  
            if not model_info:            
                model_info = model.get_model_info(model_id)
                
    if version_info and model_info:
        
        html_typepart = f"<br><b>Type: {model_info['type']}</b>"    
        model_url = civitai.Url_Page()+str(model_id)

        html_modelpart = f'<br><b>Model: <a href="{model_url}" target="_blank">{model_info["name"]}</a></b>'
        html_modelurlpart = f'<br><b><a href="{model_url}" target="_blank">Civitai Hompage << Here</a></b><br>'

        model_version_name = version_info['name']

        if 'trainedWords' in version_info:  
            output_training = ", ".join(version_info['trainedWords'])
            html_trainingpart = f'<br><b>Training Tags:</b> {output_training}'

        model_uploader = model_info['creator']['username']
        html_creatorpart = f"<br><b>Uploaded by:</b> {model_uploader}"

        if 'description' in version_info:  
            if version_info['description']:
                html_descpart = f"<br><b>Version : {version_info['name']} Description</b><br>{version_info['description']}<br>"
                
        if 'description' in model_info:  
            if model_info['description']:
                html_descpart = html_descpart + f"<br><b>Description</b><br>{model_info['description']}<br>"
                    
        html_versionpart = f"<br><b>Version:</b> {model_version_name}"

        if 'files' in version_info:                                
            for file in version_info['files']:
                files_name.append(file['name'])
                html_dnurlpart = html_dnurlpart + f"<br><a href={file['downloadUrl']}><b>Download << Here</b></a>"     
                            
        output_html = html_typepart + html_modelpart + html_versionpart + html_creatorpart + html_trainingpart + "<br>" +  html_modelurlpart + html_dnurlpart + "<br>" + html_descpart + "<br>" + html_imgpart
        
        return output_html, output_training, files_name             
    
    return "",None,None    


# def get_version_description(version_info:dict, model_info:dict=None):
#     output_html = ""
#     output_training = ""

#     files_name = list()
    
#     html_typepart = ""
#     html_trainingpart = ""
#     html_modelpart = ""
#     html_versionpart = ""
#     html_descpart = ""
#     html_dnurlpart = ""
#     html_imgpart = ""
#     html_modelurlpart = ""
        
#     if not version_info:
#         return "",None,None
    
#     if 'modelId' not in version_info:
#         return "",None,None
        
#     if "model" not in version_info.keys():    
#         return "",None,None
    
#     model_id = version_info['modelId']
#     model_type = version_info['model']['type']
#     model_name = version_info['model']['name']
#     model_url = civitai.Url_Page()+str(model_id)
                    
#     html_typepart = f"<br><b>Type: {model_type}</b>"    
#     html_modelpart = f'<br><b>Model: <a href="{model_url}" target="_blank">{model_name}</a></b>'
#     html_modelurlpart = f'<br><b><a href="{model_url}" target="_blank">Civitai Hompage << Here</a></b><br>'

#     model_version_name = version_info['name']

#     if 'trainedWords' in version_info:  
#         output_training = ", ".join(version_info['trainedWords'])
#         html_trainingpart = f'<br><b>Training Tags:</b> {output_training}'

#     if 'description' in version_info:  
#         if version_info['description']:
#             html_descpart = f"<br><b>Version : {version_info['name']} Description</b><br>{version_info['description']}<br>"
                            
#     html_versionpart = f"<br><b>Version:</b> {model_version_name}"

#     # 다운 받은 파일만 표시
#     vfolder = None
#     files = model.get_version_files(version_info)
#     if files:
#         vfolder , vfile = os.path.split(files[0])
                            
#     if 'files' in version_info:                                
#         for file in version_info['files']:
#             html_dnurlpart = html_dnurlpart + f"<br><a href={file['downloadUrl']}><b>Download << Here</b></a>"     
#             if files:
#                 if os.path.join(vfolder, file['name']) in files:
#                     files_name.append(file['name'])
                                                
#     output_html = html_typepart + html_modelpart + html_versionpart + html_trainingpart + "<br>" +  html_modelurlpart + html_dnurlpart + "<br>" + html_descpart + "<br>" + html_imgpart
    
#     return output_html, output_training, files_name

                        
                        
            
