import os
import json
from . import util
from . import model
from . import civitai
from . import ishortcut
from . import setting


def get_model_information(modelid:str=None, versionid:str=None, ver_index:int=None):
    # 현재 모델의 정보를 가져온다.
    model_info = None
    version_info = None
    
    if modelid:
        model_info = ishortcut.get_model_info(modelid)        
        version_info = dict()
        if model_info:
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
        downloaded_versions_list = model.get_model_version_list(modelid)
        versions_list = list()            
        for ver in model_info['modelVersions']:
            versions_list.append(ver['name'])
        
        model_url = civitai.Url_ModelId() + str(modelid)        
        dhtml, triger, flist = get_version_description(version_info,model_info)
        title_name = f"### {model_info['name']} : {version_info['name']}"           
        gallery_url, images_url = get_version_description_gallery(modelid, versionid)
        
        return model_info, versionid,version_name,model_url,downloaded_versions_list,model_type,versions_list,dhtml,triger,flist,title_name,gallery_url,images_url
    return None, None,None,None,None,None,None,None,None,None,None,None,None

def get_version_description_gallery(modelid:str, versionid:str):
    if not modelid or not versionid:
        return None, None

    model_path = os.path.join(setting.shortcut_info_folder, modelid)         
    version_image_prefix = f"{versionid}-"
    version_images_url = list()
    try:        
        for file in os.listdir(model_path):
            if os.path.isdir(file):
                continue
            if file.endswith(setting.preview_image_ext) and file.startswith(version_image_prefix):
                version_images_url.append(os.path.join(model_path, file))            
    except:
        return None,None
                
    return version_images_url,version_images_url
      
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
    html_model_tags = ""
        
    model_id = None
    
    if version_info:        
        if 'modelId' in version_info:            
            model_id = version_info['modelId']  
            if not model_info:            
                model_info = ishortcut.get_model_info(model_id)

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

        if 'tags' in model_info:  
            if model_info['tags']:
                model_tags = [tag["name"] for tag in model_info["tags"]]
                if len(model_tags) > 0:
                    html_model_tags = "<br><b>Model Tags:</b>"
                    for tag in model_tags:
                        html_model_tags = html_model_tags + f"<b> [{tag}] </b>"
                                        
        if 'description' in model_info:  
            if model_info['description']:
                html_descpart = html_descpart + f"<br><b>Description</b><br>{model_info['description']}<br>"
                    
        html_versionpart = f"<br><b>Version:</b> {model_version_name}"

        if 'files' in version_info:                                
            for file in version_info['files']:
                files_name.append(file['name'])
                html_dnurlpart = html_dnurlpart + f"<br><a href={file['downloadUrl']}><b>Download << Here</b></a>"     
                            
        output_html = html_typepart + html_modelpart + html_versionpart + html_creatorpart + html_trainingpart + "<br>" +  html_model_tags + "<br>" +  html_modelurlpart + html_dnurlpart + "<br>" + html_descpart + "<br>" + html_imgpart
        
        return output_html, output_training, files_name             
    
    return "",None,None    

def get_thumbnail_list(shortcut_types=None, only_downloaded=False, search=None):
    
    shortlist =  ishortcut.get_image_list(shortcut_types, search)
    if not shortlist:
        return None
    
    if only_downloaded:
        if model.Downloaded_Models:                
            downloaded_list = list()            
            for short in shortlist:
                sc_name = short[1]
                mid = str(sc_name[0:sc_name.find(':')])
                if mid in model.Downloaded_Models.keys():
                    downloaded_list.append(short)
            return downloaded_list
    else:
        return shortlist
    return None
    
def upload_shortcut_by_files(files, progress):
    modelids = list()
    if files:
        shortcut = None
        add_ISC = dict()
        for file in progress.tqdm(files, desc=f"Civitai Shortcut"):                        
            shortcut = util.load_InternetShortcut(file.name)            
            if shortcut:                                  
                model_id = util.get_model_id_from_url(shortcut)                
                if model_id:                    
                    add_ISC = ishortcut.add(add_ISC, model_id)
                    modelids.append(model_id)
                      
        ISC = ishortcut.load()
        if ISC:
            ISC.update(add_ISC)
        else:
            ISC = add_ISC            
        ishortcut.save(ISC)
        
    return modelids

def update_shortcut_model(modelid):
    if modelid:
        add_ISC = dict()                
        add_ISC = ishortcut.add(add_ISC, modelid)           
        
        ISC = ishortcut.load()
        if ISC:
            ISC.update(add_ISC)
        else:
            ISC = add_ISC            
        ishortcut.save(ISC)
        
def update_all_shortcut_model(progress):
    preISC = ishortcut.load()                           
    if not preISC:
        return
    
    for k in progress.tqdm(preISC,desc="Update Shortcut's Model Information"):        
        if k:
            preISC = ishortcut.add(preISC,str(k))
                
    # 중간에 변동이 있을수 있으므로 병합한다.                
    ISC = ishortcut.load()
    if ISC:
        ISC.update(preISC)
    else:
        ISC = preISC            
    ishortcut.save(ISC)

def delete_shortcut_model(modelid):
    if modelid:
        ISC = ishortcut.load()                           
        ISC = ishortcut.delete(ISC, modelid)
        ishortcut.save(ISC) 
            
def scan_downloadedmodel_to_shortcut(progress):        
    add_ISC = dict()

    # util.printD(len(model.Downloaded_Models))
    if model.Downloaded_Models:
        for modelid in progress.tqdm(model.Downloaded_Models, desc=f"Scan Downloaded Models to shortcut"):        
            if modelid:
                add_ISC = ishortcut.add(add_ISC, str(modelid))
            
    ISC = ishortcut.load()
    if ISC:
        ISC.update(add_ISC)
    else:
        ISC = add_ISC            
    ishortcut.save(ISC) 
        