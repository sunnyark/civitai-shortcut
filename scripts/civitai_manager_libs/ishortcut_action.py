import os
import json
from . import util
from . import model
from . import civitai
from . import ishortcut
from . import setting

def get_model_info(modelid:str):
    if not modelid:
        return    
    contents = None    
    model_path = os.path.join(setting.shortcut_info_folder, modelid, f"{modelid}{setting.info_suffix}{setting.info_ext}")       
    try:
        with open(model_path, 'r') as f:
            contents = json.load(f)            
    except:
        return None
    
    if 'id' not in contents.keys():
        return None
    
    return contents

def get_version_info(modelid:str, versionid:str):
    if not modelid or not versionid:
        return    
    contents = None    

    model_info = get_model_info(modelid)
    
    if not model_info:
        return
    if "modelVersions" not in model_info.keys():
        return 
    
    for version_info in model_info["modelVersions"]:
        if "id" in version_info.keys():
            if str(version_info["id"]) == str(versionid):
                return version_info
    
    return contents

def get_versionid_by_index(modelid:str, index):
    if not modelid:
        return    
    
    model_info = get_model_info(modelid)
    
    if not model_info:
        return
    
    if "modelVersions" not in model_info.keys():
        return 
    
    try:
        version_info = model_info["modelVersions"][index]
        return version_info['id']
    except:
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
    
def DownloadedModel_to_Shortcut(progress):        
    add_ISC = dict()

    # 다운로드 받은 모델 정보를 갱신한다.
    model.Load_Downloaded_Models()   
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
    
def get_selected_model_info(modelid):
    model_type= None
    def_name = ""
    def_id = ""    
    versions_list = list()
    
    if modelid:
        model_info = get_model_info(modelid)
        if model_info:
            model_type = model_info['type']            

            if "modelVersions" in model_info.keys():            
                def_version = model_info["modelVersions"][0]
                def_name = def_version["name"]
                def_id = def_version["id"]
                for version_info in model_info['modelVersions']:
                    versions_list.append(version_info['name'])                        
                
    return model_type, def_name, def_id, versions_list

def get_version_description(modelid:str ,versionid:str):
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
    
    if not modelid or not versionid:
        return "",None,None,None,None
    
    model_info = get_model_info(modelid)
    version_info = get_version_info(modelid, versionid) 
    
    if not version_info or not model_info:
        return "",None,None,None,None
                
    html_typepart = f"<br><b>Type: {model_info['type']}</b>"    
    model_url = civitai.Url_Page()+str(modelid)

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

    title_name = f"### {model_info['name']} : {version_info['name']}"
        
    return output_html, output_training, files_name, model_info['type'], title_name

def get_version_description_gallery(modelid:str, versionid:str):
    if not modelid or not versionid:
        return None,None

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
    