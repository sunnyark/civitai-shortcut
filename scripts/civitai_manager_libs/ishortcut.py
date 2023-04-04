import os
import json
from . import util
from . import setting
from . import civitai

import shutil
import requests

from tqdm import tqdm

def OwnedModel_to_Shortcut():
    root_dirs = list(set(setting.folders_dict.values()))
    file_list = util.search_file(root_dirs,None,".info")
    
        
    add_ISC = dict()
            
    if file_list:             
        # ISC = load()
        for file_path in tqdm(file_list, desc=f"Scan to shortcut"):        
            #util.printD(f"{file_path}\n")    
            try:
                json_data = None
                with open(file_path, 'r') as f:
                    json_data = json.load(f)
                    
                if "id" not in json_data.keys():
                    continue
                
                version_id = json_data['id']
                        
                if "modelId" not in json_data.keys():
                    continue
                
                model_id = json_data['modelId']
                
                model_url = f"{civitai.Url_ModelId()}{model_id}" 
                
                if "model" not in json_data.keys():
                    continue
                
                model_type = json_data['model']['type']
                model_name = json_data['model']['name']
                
                if "images" not in json_data.keys():
                    continue         
                                                
                image_url  = json_data['images'][0]['url']
                
                # util.printD(f"{model_id},{model_name},{model_type},{model_url},{version_id},{image_url}")           
                add_ISC = add(add_ISC,model_id ,model_name, model_type, model_url, version_id, image_url)  
            except:
                pass 
            
        ISC = load()
        if ISC:
            ISC.update(add_ISC)
        else:
            ISC = add_ISC            
        save(ISC)    
            
        
def get_list(shortcut_types=None)->str:
    
    ISC = load()                           
    if not ISC:
        return
    
    tmp_types = list()
    if shortcut_types:
        for sc_type in shortcut_types:
            try:
                tmp_types.append(setting.content_types_dict[sc_type])
            except:
                pass
            
    shotcutlist = list()
    for k, v in ISC.items():
        # util.printD(ISC[k])
        if v:
            if tmp_types:
                if v['type'] in tmp_types:
                    shotcutlist.append(f"{v['id']}:{v['name']}")
            else:                                
                shotcutlist.append(f"{v['id']}:{v['name']}")                
                    
    return [v for v in shotcutlist]


def get_image_list(shortcut_types=None)->str:
    
    ISC = load()                           
    if not ISC:
        return
    
    tmp_types = list()
    if shortcut_types:
        for sc_type in shortcut_types:
            try:
                tmp_types.append(setting.content_types_dict[sc_type])
            except:
                pass
            
    shotcutlist = list()
    for k, v in ISC.items():
        # util.printD(ISC[k])
        if v:
            if tmp_types:
                if v['type'] in tmp_types:
                    if is_sc_image(v['id']):
                        shotcutlist.append((os.path.join(setting.civitai_shortcut_thumnail_folder,f"{v['id']}.png"),f"{v['id']}:{v['name']}"))
                    else:
                        shotcutlist.append((setting.civitai_no_card_preview_image,f"{v['id']}:{v['name']}"))
            else:           
                if is_sc_image(v['id']):
                    shotcutlist.append((os.path.join(setting.civitai_shortcut_thumnail_folder,f"{v['id']}.png"),f"{v['id']}:{v['name']}"))
                else:
                    shotcutlist.append((setting.civitai_no_card_preview_image,f"{v['id']}:{v['name']}"))
                    
    return [v for v in shotcutlist]

def download_all_images():
    ISC = load()                           
    if not ISC:
        return
    
    for k, v in ISC.items():
        if v:
            download_image(v['id'], v['imageurl'])

def is_sc_image(model_id):
    if not model_id:    
        return False
            
    if os.path.isfile(os.path.join(setting.civitai_shortcut_thumnail_folder,f"{model_id}.png")):
        return True
    
    return False        
    
def download_image(model_id, url):
    if not model_id:    
        return False

    if not url:    
        return False
    
    if not os.path.exists(setting.civitai_shortcut_thumnail_folder):
        os.makedirs(setting.civitai_shortcut_thumnail_folder)    
        
    # if os.path.isfile(os.path.join(setting.civitai_shortcut_thumnail_folder,f"{model_id}.png")):
    #     return True
    
    try:
        # get image
        with requests.get(url, stream=True) as img_r:
            if not img_r.ok:
                return False
            
            shotcut_img = os.path.join(setting.civitai_shortcut_thumnail_folder,f"{model_id}.png")                                                                   
            with open(shotcut_img, 'wb') as f:
                img_r.raw.decode_content = True
                shutil.copyfileobj(img_r.raw, f)                            
    except Exception as e:
        return False
    
    return True
                        
def delete_image(model_id):
    if is_sc_image(model_id):
        try:
            os.remove(os.path.join(setting.civitai_shortcut_thumnail_folder,f"{model_id}.png"))
        except:
            return        

def add(ISC:dict, model_id ,model_name, model_type, model_url, version_id, image_url)->dict:
    
    if not ISC:
        ISC = dict()
        
    cis = {
            "id" : model_id,
            "type" : model_type,
            "name": model_name,
            "url": model_url,
            "versionid" : version_id,
            "imageurl" : image_url
    }
    
    ISC[str(model_id)] = cis
    
    cis_to_file(cis)
    
    download_image(model_id, image_url)
    
    return ISC

def delete(ISC:dict, model_id)->dict:
    if not model_id:
        return 
    
    if not ISC:
        return 
           
    cis = ISC.pop(str(model_id),None)
    
    cis_to_file(cis)
    
    delete_image(model_id)
    return ISC

def cis_to_file(cis):
    if cis: 
        if "name" in cis.keys() and 'id' in cis.keys():
                if not os.path.exists(setting.civitai_shortcut_save_folder):
                    os.makedirs(setting.civitai_shortcut_save_folder)              
                util.write_InternetShortcut(os.path.join(setting.civitai_shortcut_save_folder,f"{util.replace_filename(cis['name'])}.url"),f"{civitai.Url_ModelId()}{cis['id']}")
    
def save(ISC:dict):
    #print("Saving Civitai Internet Shortcut to: " + setting.civitai_shortcut)

    output = ""
    
    #write to file
    try:
        with open(setting.civitai_shortcut, 'w') as f:
            json.dump(ISC, f, indent=4)
    except Exception as e:
        util.printD("Error when writing file:"+setting.civitai_shortcut)
        return output

    output = "Civitai Internet Shortcut saved to: " + setting.civitai_shortcut
    #util.printD(output)

    return output

def load()->dict:
    #util.printD("Load Civitai Internet Shortcut from: " + setting.civitai_shortcut)

    if not os.path.isfile(setting.civitai_shortcut):
        util.printD("No Civitai Internet Shortcut file, use blank")
        return
    
    json_data = None
    try:
        with open(setting.civitai_shortcut, 'r') as f:
            json_data = json.load(f)
    except:
        return None            

    # check error
    if not json_data:
        util.printD("load Civitai Internet Shortcut file failed")
        return None

    # check for new key
    return json_data
