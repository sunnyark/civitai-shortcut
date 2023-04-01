import os
import json
from . import util
from . import setting

import shutil
import requests

def get_list(shortcut_types=None)->str:
    
    ISC = load()                           
    if not ISC:
        return
    if "IShortCut" not in ISC.keys():
        return    
    
    tmp_types = []
    if shortcut_types:
        for sc_type in shortcut_types:
            try:
                tmp_types.append(setting.content_types_dict[sc_type])
            except:
                pass
            
    shotcutlist = []
    for k, v in ISC["IShortCut"].items():
        # util.printD(ISC["IShortCut"][k])
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
    if "IShortCut" not in ISC.keys():
        return    
    
    tmp_types = []
    if shortcut_types:
        for sc_type in shortcut_types:
            try:
                tmp_types.append(setting.content_types_dict[sc_type])
            except:
                pass
            
    shotcutlist = []
    for k, v in ISC["IShortCut"].items():
        # util.printD(ISC["IShortCut"][k])
        if v:
            if tmp_types:
                if v['type'] in tmp_types:
                    if is_sc_image(v['id']):
                        shotcutlist.append((os.path.join(setting.civitai_shorcut_image_folder,f"{v['id']}.png"),f"{v['id']}:{v['name']}"))
                    else:
                        shotcutlist.append((setting.civitai_no_card_preview_image,f"{v['id']}:{v['name']}"))
            else:           
                if is_sc_image(v['id']):
                    shotcutlist.append((os.path.join(setting.civitai_shorcut_image_folder,f"{v['id']}.png"),f"{v['id']}:{v['name']}"))
                else:
                    shotcutlist.append((setting.civitai_no_card_preview_image,f"{v['id']}:{v['name']}"))
                    
    return [v for v in shotcutlist]

def download_all_images():
    ISC = load()                           
    if not ISC:
        return

    if "IShortCut" not in ISC.keys():
        return    
    
    for k, v in ISC["IShortCut"].items():
        if v:
            download_image(v['id'], v['imageurl'])

def is_sc_image(model_id):
    if not model_id:    
        return False
            
    if os.path.isfile(os.path.join(setting.civitai_shorcut_image_folder,f"{model_id}.png")):
        return True
    
    return False        
    
def download_image(model_id, url):
    if not model_id:    
        return False

    if not url:    
        return False
    
    if not os.path.exists(setting.civitai_shorcut_image_folder):
        os.makedirs(setting.civitai_shorcut_image_folder)    
        
    if os.path.isfile(os.path.join(setting.civitai_shorcut_image_folder,f"{model_id}.png")):
        return True
    
    try:
        # get image
        with requests.get(url, stream=True) as img_r:
            if not img_r.ok:
                return False
            
            shotcut_img = os.path.join(setting.civitai_shorcut_image_folder,f"{model_id}.png")                                                                   
            with open(shotcut_img, 'wb') as f:
                img_r.raw.decode_content = True
                shutil.copyfileobj(img_r.raw, f)                            
    except Exception as e:
        return False
    
    return True
                        
def delete_image(model_id):
    if is_sc_image(model_id):
        try:
            os.remove(os.path.join(setting.civitai_shorcut_image_folder,f"{model_id}.png"))
        except:
            return        

def add(ISC:dict, model_id ,model_name, model_type, model_url, version_id, image_url)->dict:
    
    if not ISC:
        ISC = {}
        
    if "IShortCut" not in ISC.keys():
        ISC["IShortCut"] = {}
        
    cis = {
            "id" : model_id,
            "type" : model_type,
            "name": model_name,
            "url": model_url,
            "versionid":version_id,
            "imageurl" : image_url
    }
    
    ISC["IShortCut"][model_id] = cis
    
    download_image(model_id, image_url)
    
    return ISC

def delete(ISC:dict, model_id)->dict:
    if not model_id:
        return 
    
    if not ISC:
        return 
        
    if "IShortCut" not in ISC.keys():
        return
    
    ISC["IShortCut"].pop(model_id,None)
    
    delete_image(model_id)
    
    return ISC

def save(cis_data):
    #print("Saving Civitai Internet Shortcut to: " + setting.civitai_shortcut)

    json_data = json.dumps(cis_data, indent=4)

    output = ""

    #write to file
    try:
        with open(setting.civitai_shortcut, 'w') as f:
            f.write(json_data)
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
    with open(setting.civitai_shortcut, 'r') as f:
        json_data = json.load(f)

    # check error
    if not json_data:
        util.printD("load Civitai Internet Shortcut file failed")
        return

    # check for new key
    return json_data
