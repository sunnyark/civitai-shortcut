import os
from . import model
from . import civitai
from . import util
    
def get_selected_downloaded_modelinfo(modelid):
    model_type= None
    downloaded_info = ""
    def_name = ""
    def_info = None
    def_id = None
    versions_list = []    
    if modelid:
        if model.Downloaded_Models:
            if str(modelid) in model.Downloaded_Models.keys():
                file_list = dict()
                
                for version_paths in model.Downloaded_Models[str(modelid)]:
                    file_list[os.path.basename(version_paths)] = version_paths
                
                for file,path in file_list.items():
                    vinfo = model.read_versioninfo(path)
                    if vinfo:
                        if not def_info:
                            def_info = vinfo
                        try:  
                            downloaded_info = downloaded_info + "\n" if len(downloaded_info.strip()) > 0 else ""
                            downloaded_info = downloaded_info + f"{vinfo['name']}"
                            versions_list.append(vinfo['name'])  
                        except:
                            pass

            if def_info:
                def_name = def_info['name']
                def_id = def_info['id']
                if "model" in def_info.keys():
                    model_type = def_info['model']['type']                
                                    
    return downloaded_info, model_type, def_name, def_id, versions_list

def get_model_versions(modelid:str):
    downloaded_version_list = list()
    if modelid:
        if model.Downloaded_Models:                        
            if str(modelid) in model.Downloaded_Models.keys():
                file_list = dict()
                
                for version_paths in model.Downloaded_Models[str(modelid)]:
                    file_list[os.path.basename(version_paths)] = version_paths
                
                for file,path in file_list.items():
                    vinfo = civitai.read_version_info(path)
                    if vinfo:                      
                        downloaded_version_list.append(vinfo['name'])
                        
    return downloaded_version_list if len(downloaded_version_list) > 0 else None

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

    files_name = list()
    
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

    # 다운 받은 파일만 표시
    vfolder = None
    files = model.get_version_files(version_info)
    if files:
        vfolder , vfile = os.path.split(files[0])
                            
    if 'files' in version_info:                                
        for file in version_info['files']:
            html_dnurlpart = html_dnurlpart + f"<br><a href={file['downloadUrl']}><b>Download << Here</b></a>"     
            if files:
                if os.path.join(vfolder, file['name']) in files:
                    files_name.append(file['name'])
                                                
    output_html = html_typepart + html_modelpart + html_versionpart + html_trainingpart + "<br>" +  html_modelurlpart + html_dnurlpart + "<br>" + html_descpart + "<br>" + html_imgpart
    
    return output_html, output_training, files_name, model_type
                        
def get_version_description_gallery(versionid):
    if not versionid:
        return None,None
    imagelist = model.get_version_images(versionid)
    return imagelist, imagelist


