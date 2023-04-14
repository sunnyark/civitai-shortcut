import os
import json
import shutil
import requests
import gradio as gr

from . import util
from . import setting
from . import civitai

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

# def get_version_info(modelid:str, versionid:str):
#     if not modelid or not versionid:
#         return    
#     contents = None    

#     model_info = get_model_info(modelid)
    
#     if not model_info:
#         return
#     if "modelVersions" not in model_info.keys():
#         return 
    
#     for version_info in model_info["modelVersions"]:
#         if "id" in version_info.keys():
#             if str(version_info["id"]) == str(versionid):
#                 return version_info
    
#     return contents

def write_model_information(modelid:str):    
    if not modelid:
        return     
    model_info = civitai.get_model_info(modelid)
    if model_info:
        version_list = list()
        if "modelVersions" in model_info.keys():
            for version_info in model_info["modelVersions"]:
                version_id = version_info['id']
                if "images" in version_info.keys():
                    image_list = list()
                    for img in version_info["images"]:                                                
                        if "url" in img:
                            img_url = img["url"]
                            # use max width
                            if "width" in img.keys():
                                if img["width"]:
                                    img_url =  util.change_width_from_image_url(img_url, img["width"])
                            image_list.append([version_id,img_url])        
                    if len(image_list) > 0:
                        version_list.append(image_list)
        try:
            # model 폴더 생성
            model_path = os.path.join(setting.shortcut_info_folder, modelid)        
            if not os.path.exists(model_path):
                os.makedirs(model_path)

            # model info 저장            
            model_info_file = os.path.join(model_path, f"{modelid}{setting.info_suffix}{setting.info_ext}")            
            with open(model_info_file, 'w') as f:
                f.write(json.dumps(model_info, indent=4))
                
        except Exception as e:
            return
                        
        # 이미지 다운로드    
        if len(version_list) > 0:
            for image_list in version_list:
                for image_count, (vid, url) in enumerate(image_list,start=0):
                    try:
                        # get image
                        with requests.get(url, stream=True) as img_r:
                            if not img_r.ok:
                                util.printD("Get error code: " + str(img_r.status_code) + ": proceed to the next file")
                                continue

                            # write to file
                            description_img = os.path.join(model_path, f"{vid}-{image_count}{setting.preview_image_ext}")
                            with open(description_img, 'wb') as f:
                                img_r.raw.decode_content = True
                                shutil.copyfileobj(img_r.raw, f)
                    except Exception as e:
                        pass              
    return model_info

def delete_model_information(modelid:str):
    if not modelid:
        return 
    
    model_path = os.path.join(setting.shortcut_info_folder, modelid)
    if setting.shortcut_info_folder != model_path:
        if os.path.exists(model_path):
            shutil.rmtree(model_path)

def update_thumbnail_images(progress):
    preISC = load()                           
    if not preISC:
        return
    
    for k, v in progress.tqdm(preISC.items(),desc="Update Shortcut's Thumbnails"):
        if v:
            version_info = civitai.get_latest_version_info_by_model_id(v['id'])
            if not version_info:
                continue
            
            if 'images' not in version_info.keys():
                continue
            
            if len(version_info['images']) > 0:                    
                v['imageurl'] = version_info['images'][0]['url']
                download_thumbnail_image(v['id'], v['imageurl'])
                
    # 중간에 변동이 있을수 있으므로 병합한다.                
    ISC = load()
    if ISC:
        ISC.update(preISC)
    else:
        ISC = preISC            
    save(ISC)
    
# def get_thumbnail_list2(shortcut_types=None, only_downloaded=False):
    
#     shortlist =  get_image_list(shortcut_types)
#     if not shortlist:
#         return None
    
#     if only_downloaded:
#         if model.Downloaded_Models:                
#             downloaded_list = list()            
#             for short in shortlist:
#                 sc_name = short[1]
#                 mid = str(sc_name[0:sc_name.find(':')])
#                 if mid in model.Downloaded_Models.keys():
#                     downloaded_list.append(short)
#             return downloaded_list
#     else:
#         return shortlist
#     return None  
        
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
                    
    return shotcutlist

def get_image_list2(shortcut_types=None)->str:
    
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
                        shotcutlist.append((os.path.join(setting.shortcut_thumnail_folder,f"{v['id']}.png"),f"{v['id']}:{v['name']}"))
                    else:
                        shotcutlist.append((setting.no_card_preview_image,f"{v['id']}:{v['name']}"))
            else:           
                if is_sc_image(v['id']):
                    shotcutlist.append((os.path.join(setting.shortcut_thumnail_folder,f"{v['id']}.png"),f"{v['id']}:{v['name']}"))
                else:
                    shotcutlist.append((setting.no_card_preview_image,f"{v['id']}:{v['name']}"))
    
    return shotcutlist 
    
def get_image_list(shortcut_types=None, search=None)->str:
    
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
            
    
    search_list= list()
    # type 을 걸러내자
    for k, v in ISC.items():
        # util.printD(ISC[k])
        if v:
            if tmp_types:
                if v['type'] in tmp_types:
                    search_list.append(v)                    
            else:
                search_list.append(v)
    
    # search를 걸러내자
    result_list=list()
    for v in search_list:
        if v:
            if search:
                if search.lower() in v['name'].lower():
                    result_list.append(v)
            else:
                result_list.append(v)
                
    # 썸네일이 있는지 판단해서 대체 이미지 작업
    shotcutlist = list()
    for v in result_list:
        if v:
            if is_sc_image(v['id']):
                shotcutlist.append((os.path.join(setting.shortcut_thumnail_folder,f"{v['id']}{setting.preview_image_ext}"),f"{v['id']}:{v['name']}"))
            else:
                shotcutlist.append((setting.no_card_preview_image,f"{v['id']}:{v['name']}"))

    return shotcutlist                

def delete_thumbnail_image(model_id):
    if is_sc_image(model_id):
        try:
            os.remove(os.path.join(setting.shortcut_thumnail_folder,f"{model_id}{setting.preview_image_ext}"))
        except:
            return 
        
def download_thumbnail_image(model_id, url):
    if not model_id:    
        return False

    if not url:    
        return False
    
    if not os.path.exists(setting.shortcut_thumnail_folder):
        os.makedirs(setting.shortcut_thumnail_folder)    
        
    # if os.path.isfile(os.path.join(setting.shortcut_thumnail_folder,f"{model_id}{setting.preview_image_ext}")):
    #     return True
    
    try:
        # get image
        with requests.get(url, stream=True) as img_r:
            if not img_r.ok:
                return False
            
            shotcut_img = os.path.join(setting.shortcut_thumnail_folder,f"{model_id}{setting.preview_image_ext}")                                                                   
            with open(shotcut_img, 'wb') as f:
                img_r.raw.decode_content = True
                shutil.copyfileobj(img_r.raw, f)                            
    except Exception as e:
        return False
    
    return True                    

def is_sc_image(model_id):
    if not model_id:    
        return False
            
    if os.path.isfile(os.path.join(setting.shortcut_thumnail_folder,f"{model_id}{setting.preview_image_ext}")):
        return True
    
    return False        

def add(ISC:dict, model_id)->dict:

    if not model_id:
        return ISC   
        
    if not ISC:
        ISC = dict()
    
    model_info = write_model_information(model_id)
    
    if model_info:        
        if "modelVersions" in model_info.keys():            
            def_version = model_info["modelVersions"][0]
            def_id = def_version['id']
                
            if 'images' in def_version.keys():
                if len(def_version["images"]) > 0:
                    img_dict = def_version["images"][0]
                    def_image = img_dict["url"]                
                        
        cis = {
                "id" : model_info['id'],
                "type" : model_info['type'],
                "name": model_info['name'],
                "url": f"{civitai.Url_ModelId()}{model_id}",
                "versionid" : def_id,
                "imageurl" : def_image
        }

        ISC[str(model_id)] = cis
        
        cis_to_file(cis)
        
        download_thumbnail_image(model_id, def_image)

    return ISC

def delete(ISC:dict, model_id)->dict:
    if not model_id:
        return 
    
    if not ISC:
        return 
           
    cis = ISC.pop(str(model_id),None)
    
    cis_to_file(cis)
    
    delete_thumbnail_image(model_id)
    
    delete_model_information(model_id)
    
    return ISC

def cis_to_file(cis):
    if cis: 
        if "name" in cis.keys() and 'id' in cis.keys():
                if not os.path.exists(setting.shortcut_save_folder):
                    os.makedirs(setting.shortcut_save_folder)              
                util.write_InternetShortcut(os.path.join(setting.shortcut_save_folder,f"{util.replace_filename(cis['name'])}.url"),f"{civitai.Url_ModelId()}{cis['id']}")
    
def save(ISC:dict):
    #print("Saving Civitai Internet Shortcut to: " + setting.shortcut)

    output = ""
    
    #write to file
    try:
        with open(setting.shortcut, 'w') as f:
            json.dump(ISC, f, indent=4)
    except Exception as e:
        util.printD("Error when writing file:"+setting.shortcut)
        return output

    output = "Civitai Internet Shortcut saved to: " + setting.shortcut
    #util.printD(output)

    return output

def load()->dict:
    #util.printD("Load Civitai Internet Shortcut from: " + setting.shortcut)

    if not os.path.isfile(setting.shortcut):
        util.printD("No Civitai Internet Shortcut file, use blank")
        return
    
    json_data = None
    try:
        with open(setting.shortcut, 'r') as f:
            json_data = json.load(f)
    except:
        return None            

    # check error
    if not json_data:
        util.printD("load Civitai Internet Shortcut file failed")
        return None

    # check for new key
    return json_data
