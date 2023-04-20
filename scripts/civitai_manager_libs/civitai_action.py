import os
import shutil
import requests
import threading
from . import util
from . import model
from . import civitai
from . import setting
from . import downloader

from tqdm import tqdm

def get_model_information(modelid:str=None, versionid:str=None, ver_index:int=None):
    # 현재 모델의 정보를 가져온다.
    
    model_info = None
    version_info = None
    
    if modelid:
        model_info = civitai.get_model_info(modelid)        
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
        downloaded_versions = model.get_model_downloaded_versions(modelid)       
        versions_list = list()            
        for ver in model_info['modelVersions']:
            versions_list.append(ver['name'])
        
        model_url = civitai.Url_ModelId() + str(modelid)        
        dhtml, triger, flist = get_version_description(version_info,model_info)
        title_name = f"# {model_info['name']} : {version_info['name']}"           
        images_url = get_version_description_gallery(version_info)
        vs_foldername = util.generate_version_foldername(model_info['name'],version_name,versionid)        
        model_folder = util.generate_model_foldername(model_info['name'],model_type,False)
        
        # 정리하자... 
        if  os.getcwd() in model_folder and os.path.exists(model_folder):
            info_list = util.scan_folder_for_info(model_folder)
            if info_list:
                for info in info_list:
                    info_dir = os.path.dirname(info)
                    info_basename = os.path.basename(info_dir)
                    if info_dir == model_folder:
                        continue
                    ver_info = util.read_json(info)
                    if not ver_info:
                        continue
                    if 'id' not in ver_info.keys():
                        continue
                    if ver_info['id'] == versionid:
                        vs_foldername = info_basename
                        break
                    
        return model_info, versionid,version_name,model_url,downloaded_versions,model_type,versions_list,dhtml,triger,flist,title_name,images_url,vs_foldername
    return None, None,None,None,None,None,None,None,None,None,None,None,None

def get_version_description_gallery(version_info:dict):       
    if not version_info:
        return None

    images_url = []
    
    if 'images' not in version_info:
        return None
                    
    for pic in version_info["images"]:   
        if "url" in pic:
            img_url = pic["url"]
            # use max width
            # 파일 인포가 있는 원본 이미지.
            if "width" in pic:
                if pic["width"]:
                    img_url = util.change_width_from_image_url(img_url, pic["width"])
            images_url.append(img_url)
                
    return images_url
      
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
                model_info = civitai.get_model_info(model_id)

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
                files_name.append(f"{file['id']}:{file['name']}")
                html_dnurlpart = html_dnurlpart + f"<br><a href={file['downloadUrl']}><b>Download << Here</b></a>"     
                            
        output_html = html_typepart + html_modelpart + html_versionpart + html_creatorpart + html_trainingpart + "<br>" +  html_model_tags + "<br>" +  html_modelurlpart + html_dnurlpart + "<br>" + html_descpart + "<br>" + html_imgpart
        
        return output_html, output_training, files_name             
    
    return "",None,None

def add_number_to_duplicate_files(filenames)->dict:    
    counts = {}
    dup_file = {}
    
    for file in filenames:     
        file_info = file.split(":", 1)
        if len(file_info) > 1:
            if file_info[1] in counts:
                name, ext = os.path.splitext(file_info[1])
                counts[file_info[1]] += 1
                file_info[1] = f"{name} ({counts[file_info[1]]}){ext}"
            else:
                counts[file_info[1]] = 0        
            dup_file[file_info[0]] = file_info[1]
    return dup_file
    
def download_file_thread(file_name, version_id, lora_an, vs_folder, vs_foldername=None):               
    if not file_name:
        return

    if not version_id:
        return
    
    version_info = civitai.get_version_info_by_version_id(version_id)
    
    if not version_info:
        return 
       
    download_files = civitai.get_files_by_version_info(version_info)
    
    if not download_files:
        return

    model_folder = util.make_version_folder(version_info, lora_an , vs_folder, vs_foldername)
    
    if not model_folder:
        return

    dup_names = add_number_to_duplicate_files(file_name)
    
    for fid, file in dup_names.items():                    
        try:
            #모델 파일 저장
            path_dl_file = os.path.join(model_folder, file)            
            thread = threading.Thread(target=downloader.download_file,args=(download_files[str(fid)]['downloadUrl'], path_dl_file))
            # Start the thread
            thread.start()                
        except Exception as e:
            util.printD(e)
            pass
        
    # 저장할 파일명을 생성한다.
    savefile_base = util.generate_version_foldername(version_info['model']['name'],version_info['name'],version_info['id'])    
    if vs_folder:
        # 개별폴더를 만들면 저장 파일명을 지정파일명을 폴더명으로 한다.
        if vs_foldername:
            vs_foldername = vs_foldername.strip()            
            if len(vs_foldername) > 0:
                savefile_base = vs_foldername
                                
    path_file = os.path.join(model_folder, f"{util.replace_filename(savefile_base)}{setting.info_suffix}{setting.info_ext}")
    info_file = civitai.write_version_info(path_file, version_info)
    if info_file:
        util.printD(f"Wrote version info : {path_file}")

    path_file = os.path.join(model_folder, f"{util.replace_filename(savefile_base)}{setting.triger_suffix}{setting.triger_ext}")
    triger_file = civitai.write_triger_words_by_version_info(path_file, version_info)
    if triger_file:
         util.printD(f"Wrote triger words : {path_file}")

    return f"Download started"

def get_image_base_name(version_info):
    # 이미지 파일명도 primary 이름으로 저장한다.
    
    # primary_file = civitai.get_primary_file_by_version_info(version_info)
    # if not primary_file:
    #     base = util.replace_filename(version_info['model']['name'] + "." + version_info['name'])
    # base, ext = os.path.splitext(primary_file['name'])
        
    base = None    
    primary_file = civitai.get_primary_file_by_version_info(version_info)
    if not primary_file:
        base = util.replace_filename(version_info['model']['name'] + "." + version_info['name'])
    else:
        base, ext = os.path.splitext(primary_file['name'])   
    return base

def download_preview_image(version_id, lora_an, vs_folder,vs_foldername=None):
    message =""
    base = None
    
    if not version_id:                
        return         
    
    version_info = civitai.get_version_info_by_version_id(version_id)          
    
    if not version_info:
        return
    
    if 'images' not in version_info.keys():
        return
        
    model_folder = util.make_version_folder(version_info, lora_an , vs_folder,vs_foldername)
    
    if not model_folder:
        return

    base = get_image_base_name(version_info)
    base = os.path.join(setting.root_path, model_folder, util.replace_filename(base))
    
    if base and len(base.strip()) > 0:  
        if "images" in version_info.keys():
            try:            
                img_dict = version_info["images"][0] 
                if "url" in img_dict:
                    img_url = img_dict["url"]
                    # use max width
                    if "width" in img_dict:
                        if img_dict["width"]:
                            img_url =  util.change_width_from_image_url(img_url, img_dict["width"])
                        # get image
                        with requests.get(img_url, stream=True) as img_r:
                            if not img_r.ok:
                                util.printD("Get error code: " + str(img_r.status_code))
                                return
                            # write to file
                            description_img = f"{base}{setting.preview_image_suffix}{setting.preview_image_ext}"

                            with open(description_img, 'wb') as f:
                                img_r.raw.decode_content = True
                                shutil.copyfileobj(img_r.raw, f)
            except Exception as e:
                return
    return

def download_image_files(version_id, lora_an, vs_folder,vs_foldername=None):
    message =""
    base = None
    preview_base = None
    
    if not version_id:                
        return         
    
    version_info = civitai.get_version_info_by_version_id(version_id)          
    
    if not version_info:
        return
    
    if 'images' not in version_info.keys():
        return
        
    model_folder = util.make_version_folder(version_info, lora_an , vs_folder,vs_foldername)
    
    if not model_folder:
        return

    base = get_image_base_name(version_info)
    base = os.path.join(setting.root_path, model_folder, util.replace_filename(base))
    
    if base and len(base.strip()) > 0:                                           
        #image_count = 0 
        
        for image_count, img_dict in enumerate(tqdm(version_info["images"], desc=f"Download image"), start=0):
            # if "nsfw" in img_dict:
            #     if img_dict["nsfw"]:
            #         printD("This image is NSFW")

            if "url" in img_dict:
                img_url = img_dict["url"]
                # use max width
                if "width" in img_dict:
                    if img_dict["width"]:
                        img_url =  util.change_width_from_image_url(img_url, img_dict["width"])
                
                try:
                    # get image
                    with requests.get(img_url, stream=True) as img_r:
                        if not img_r.ok:
                            util.printD("Get error code: " + str(img_r.status_code) + ": proceed to the next file")
                            continue

                        # write to file
                        description_img = f'{base}_{image_count}{setting.preview_image_suffix}{setting.preview_image_ext}'
                        if image_count == 0:
                            #첫 프리뷰는 호환성 때문에 filename에 따라간다.
                            description_img = f'{base}{setting.preview_image_suffix}{setting.preview_image_ext}'
                                                                                
                        with open(description_img, 'wb') as f:
                            img_r.raw.decode_content = True
                            shutil.copyfileobj(img_r.raw, f)
                except Exception as e:
                    pass
                
                # set image_counter
                image_count = image_count + 1
            
        message = f"Downloaded images"
    return message       
