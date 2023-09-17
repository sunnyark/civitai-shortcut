import os
import json
import shutil
import requests
import gradio as gr
import datetime

from tqdm import tqdm

from . import util
from . import setting
from . import civitai
from . import classification

from PIL import Image

thumbnail_max_size = (400, 400)

def get_model_information(modelid:str=None, versionid:str=None, ver_index:int=None):
    # 현재 모델의 정보를 가져온다.
    model_info = None
    version_info = None
    
    if modelid:
        model_info = get_model_info(modelid)        
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
        model_basemodels = version_info["baseModel"]         
        versions_list = list()            
        for ver in model_info['modelVersions']:
            versions_list.append(ver['name'])
            # model_basemodels.append(ver['baseModel'])
        
        dhtml, triger, files = get_version_description(version_info, model_info)
        
        return model_info,version_info,versionid,version_name,model_type,model_basemodels,versions_list,dhtml,triger,files
    return None,None,None,None,None,None,None,None,None,None
    
def get_version_description_gallery(version_info):
    modelid = None
    versionid = None
    ver_images = dict()
    
            
    if not version_info:
        return None, None

    if "modelId" in version_info.keys():
        modelid = str(version_info['modelId'])   
            
    if "id" in version_info.keys():
        versionid = str(version_info['id'])

    if "images" in version_info.keys():
        ver_images = version_info['images']

    images_url = list()
    images_meta = list()
    
    try:        
        for ver in ver_images:
            description_img = setting.get_image_url_to_shortcut_file(modelid,versionid,ver['url'])
            meta_string = ""
            
            # NSFW filtering ....
            if setting.NSFW_filtering_enable:
                # if not setting.NSFW_level[ver["nsfw"]]:
                if setting.NSFW_levels.index(ver["nsfw"]) > setting.NSFW_levels.index(setting.NSFW_level_user):                
                    description_img = setting.nsfw_disable_image
                    meta_string = ""
                    
            if os.path.isfile(description_img):               
                meta_string = util.convert_civitai_meta_to_stable_meta(ver['meta'])
                images_url.append(description_img)
                images_meta.append(meta_string)
    except:
        return None, None
                
    return images_url, images_meta                  
    
def get_version_description(version_info:dict,model_info:dict=None):
    output_html = ""
    output_training = ""

    files = []
    
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
                model_info = get_model_info(model_id)

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

        
        html_descpart = f"<br><b>Version : {version_info['name']}</b><br> BaseModel : {version_info['baseModel']}<br>"
        
        if 'description' in version_info:  
            if version_info['description']:
                html_descpart = html_descpart + f"<b>Description</b><br>{version_info['description']}<br>"

        if 'tags' in model_info:  
            model_tags = model_info["tags"]
            if len(model_tags) > 0:
                html_model_tags = "<br><b>Model Tags:</b>"
                for tag in model_tags:
                    html_model_tags = html_model_tags + f"<b> [{tag}]</b>"
                                                                
        if 'description' in model_info:  
            if model_info['description']:
                html_descpart = html_descpart + f"<br><b>Description</b><br>{model_info['description']}<br>"
                    
        html_versionpart = f"<br><b>Version:</b> {model_version_name}"        

        if 'files' in version_info:                                
            for file in version_info['files']:
                files.append(file)
                html_dnurlpart = html_dnurlpart + f"<br><a href={file['downloadUrl']}><b>Download << Here</b></a>"     
                            
        output_html = html_typepart + html_modelpart + html_versionpart + html_creatorpart + html_trainingpart + "<br>" +  html_model_tags + "<br>" +  html_modelurlpart + html_dnurlpart + "<br>" + html_descpart + "<br>" + html_imgpart
        
        return output_html, output_training, files            
    
    return "", None, None    
   
def sort_shortcut_by_value(ISC, key, reverse=False):
    sorted_data = sorted(ISC.items(), key=lambda x: x[1][key], reverse=reverse)
    return dict(sorted_data)

def sort_shortcut_by_modelid(ISC, reverse=False):
    sorted_data = {}
    for key in sorted(ISC.keys(), reverse=reverse):
        sorted_data[key] = ISC[key]
    return sorted_data

def get_tags():
    ISC = load()
    if not ISC:
        return  
      
    result = []

    for item in ISC.values():
        name_values = set(tag['name'] for tag in item['tags'])
        result.extend(name_values)        

    result = list(set(result))
    # util.printD(f"{len(result)}:{result}")
    return result

# 현재 소유한 버전에서 최신 버전을 얻는다.
def get_latest_version_info_by_model_id(id:str) -> dict:

    model_info = get_model_info(id)
    if not model_info:
        return

    if "modelVersions" not in model_info.keys():
        return
            
    def_version = model_info["modelVersions"][0]
    if not def_version:
        return
    
    if "id" not in def_version.keys():
        return
    
    return def_version

def get_model_filenames(modelid:str):
    
    model_info = get_model_info(modelid)    
    if not model_info:
        return None

    filenames = []
    
    if "modelVersions" in model_info.keys():
        for ver in model_info["modelVersions"]:
            for ver_file in ver["files"]:
                filenames.append(ver_file["name"])

    return filenames

def is_baseModel(modelid:str, baseModels):
    
    model_info = get_model_info(modelid)    
    if not model_info:
        return None

    if "modelVersions" in model_info.keys():
        for ver in model_info["modelVersions"]:
            try:
                # util.printD(ver["baseModel"])                
                if ver["baseModel"] in baseModels:
                    return True
            except:
                pass

    return False

def get_model_info(modelid:str):
    if not modelid:
        return    
    contents = None    
    model_path = os.path.join(setting.shortcut_info_folder, modelid, f"{modelid}{setting.info_suffix}{setting.info_ext}")       
    try:
        with open(model_path, 'r') as f:
            contents = json.load(f)            

        if 'id' not in contents.keys():
            return None
    except:
        return None
    
    return contents

def get_version_info(modelid:str, versionid:str):
    
    model_info = get_model_info(modelid)    
    if not model_info:
        return None
        
    if "modelVersions" in model_info.keys():
        for ver in model_info["modelVersions"]:
            if str(versionid) == str(ver["id"]):
                return ver
    return None

def get_version_images(modelid:str, versionid:str):
    
    version_info = get_version_info(modelid, versionid)
    if not version_info:
        return None
    
    if "images" in version_info.keys():
        return version_info["images"]

    return None
                            
def get_version_image_id(filename):
    version_image, ext = os.path.splitext(filename)
    
    ids = version_image.split("-")
    
    if len(ids) > 1 :
        return ids
        
    return None

def get_images_meta(images:dict, imageid):
    
    if not images:
        return None
    
    if not imageid:
        return None
    
    for img in images:
        if imageid in img['url']:
            return img['meta']
    
    return None

# 모델에 해당하는 shortcut에서 note를 변경한다.
def update_shortcut_model_note(modelid, note):
    if modelid:
        ISC = load()            
        try:           
            ISC[str(modelid)]["note"] = str(note)
            save(ISC)
        except:
            pass
        
# 모델에 해당하는 shortcut에서 note를 가져온다
def get_shortcut_model_note(modelid):
    if modelid:
        ISC = load()            
        try:           
            return ISC[str(modelid)]["note"]
        except:
            pass
    return None

# 모델에 해당하는 shortcut 을 가져온다
def get_shortcut_model(modelid):
    if modelid:
        ISC = load()            
        try:           
            return ISC[str(modelid)]
        except:
            pass
    return None
        
# 모델에 해당하는 shortcut 을 지운다
def delete_shortcut_model(modelid):
    if modelid:
        ISC = load()                           
        ISC = delete(ISC, modelid)
        save(ISC) 
        
# 이중으로 하지 않으면 gr.Progress 오류가 난다 아마도 중첩에서 에러가 나는것 같다. progress.tqdm
# 솟컷을 업데이트하며 없으면 해당 아이디의 모델을 새로 생성한다.
def update_shortcut(modelid, progress = None):
    if modelid:
        note = None
        date = datetime.datetime.now()
        date = date.strftime("%Y-%m-%d %H:%M:%S")
                            
        add_ISC = add(None, str(modelid), False, progress)
        ISC = load()
        if ISC:
            if str(modelid) in ISC:
                                
                #만일 civitai 에서 정보를 가져올수 없다면 기존것을 그대로 사용한다.
                if str(modelid) not in add_ISC:
                    add_ISC[str(modelid)] = ISC[str(modelid)]

                # 기존의 개별적으로 저장한 정보를 가져온다.
                if "note" in ISC[str(modelid)]:
                    note = ISC[str(modelid)]["note"]                                    

                # 기존의 등록날짜 정보를 가져온다.
                if "date" in ISC[str(modelid)]:
                    if ISC[str(modelid)]["date"]:
                        date = ISC[str(modelid)]["date"]
                
                add_ISC[str(modelid)]["note"] = str(note)
                add_ISC[str(modelid)]["date"] = date
                
                if 'nsfw' not in add_ISC[str(modelid)].keys():
                    add_ISC[str(modelid)]["nsfw"] = False
                    
            ISC.update(add_ISC)
        else:
            ISC = add_ISC
        save(ISC)
        
def update_shortcut_models(modelid_list:list, progress):
    if not modelid_list:       
        return
      
    for k in progress.tqdm(modelid_list, desc="Updating Shortcut"):        
        update_shortcut(k, progress)
    
def update_shortcut_informations(modelid_list:list, progress):
    if not modelid_list:
        return 
    
    # shortcut 의 데이터만 새로 갱신한다.    
    # for modelid in progress.tqdm(modelid_list, desc="Updating Shortcut Information"):
    #     write_model_information(modelid, False, progress) 

    for modelid in progress.tqdm(modelid_list,desc="Updating Models Information"):        
        if modelid:                
            note = None
            date = datetime.datetime.now()
            date = date.strftime("%Y-%m-%d %H:%M:%S")
            add_ISC = add(None,str(modelid),False,progress)

            ISC = load()

            if str(modelid) in ISC:
                
                #만일 civitai 에서 정보를 가져올수 없다면 기존것을 그대로 사용한다.
                if str(modelid) not in add_ISC:
                    add_ISC[str(modelid)] = ISC[str(modelid)]
                                    
                # 개별적으로 저장한 정보를 가져온다.
                if "note" in ISC[str(modelid)]:
                    note = ISC[str(modelid)]["note"]

                # 기존의 등록날짜 정보를 가져온다.
                if "date" in ISC[str(modelid)]:
                    if ISC[str(modelid)]["date"]:
                        date = ISC[str(modelid)]["date"]
                    
                add_ISC[str(modelid)]["note"] = str(note)
                add_ISC[str(modelid)]["date"] = date

                if 'nsfw' not in add_ISC[str(modelid)].keys():
                    add_ISC[str(modelid)]["nsfw"] = False
                    
                # hot fix and delete model
                # civitiai 에서 제거된 모델때문임
                # tags 를 변경해줘야함
                # 이슈가 해결되면 제거할코드
                # ISC[str(modelid)]["tags"]=[]
                
            if ISC:
                ISC.update(add_ISC)
            else:
                ISC = add_ISC
            save(ISC)
                            
def update_all_shortcut_informations(progress):
    preISC = load()                           
    if not preISC:
        return
    
    modelid_list = [k for k in preISC]
    update_shortcut_informations(modelid_list, progress)
            
def write_model_information(modelid:str, register_only_information=False, progress=None):    
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
        except Exception as e:
            return
        
        try:            
            # model info 저장            
            tmp_info_file = os.path.join(model_path, f"tmp{setting.info_suffix}{setting.info_ext}")
            model_info_file = os.path.join(model_path, f"{modelid}{setting.info_suffix}{setting.info_ext}")            
            with open(tmp_info_file, 'w') as f:
                f.write(json.dumps(model_info, indent=4))
            os.replace(tmp_info_file, model_info_file)
        except Exception as e:
            return
                        
        # 이미지 다운로드    
        if not register_only_information and len(version_list) > 0:
            if progress:
                for image_list in progress.tqdm(version_list, desc="downloading model images"):
                    dn_count = 0 # 진짜로 다운 받은 이미지를 뜻한다.
                    for image_count, (vid, url) in enumerate(progress.tqdm(image_list),start=0):
                        
                        # 0이면 전체를 지정수를 넘어가면 스킵한다.
                        if setting.shortcut_max_download_image_per_version != 0:
                            if dn_count >= setting.shortcut_max_download_image_per_version:
                                continue
                            
                        try:
                            # get image
                            description_img = setting.get_image_url_to_shortcut_file(modelid,vid,url)
                            if os.path.exists(description_img):
                                dn_count = dn_count + 1
                                continue
                                
                            with requests.get(url, stream=True) as img_r:
                                if not img_r.ok:
                                    util.printD("Get error code: " + str(img_r.status_code) + ": proceed to the next file")
                                    continue
                                                                
                                # write to file
                                with open(description_img, 'wb') as f:
                                    img_r.raw.decode_content = True
                                    shutil.copyfileobj(img_r.raw, f)
                                    dn_count = dn_count + 1
                        except Exception as e:
                            pass
            else:
                for image_list in version_list:
                    dn_count = 0 # 진짜로 다운 받은 이미지를 뜻한다.
                    
                    for image_count, (vid, url) in enumerate(image_list,start=0):
                        
                        # 0이면 전체를 지정수를 넘어가면 스킵한다.
                        if setting.shortcut_max_download_image_per_version != 0:
                            if dn_count >= setting.shortcut_max_download_image_per_version:
                                continue
                        
                        try:
                            # get image
                            description_img = setting.get_image_url_to_shortcut_file(modelid,vid,url)
                            if os.path.exists(description_img):
                                dn_count = dn_count + 1
                                continue
                            
                            with requests.get(url, stream=True) as img_r:
                                if not img_r.ok:
                                    util.printD("Get error code: " + str(img_r.status_code) + ": proceed to the next file")
                                    continue

                                # write to file
                                with open(description_img, 'wb') as f:
                                    img_r.raw.decode_content = True
                                    shutil.copyfileobj(img_r.raw, f)
                                    dn_count = dn_count + 1
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

    # nsfw_levels = setting.NSFW_levels #[nsfw_level for nsfw_level in setting.NSFW_level.keys()]
    
    for k, v in progress.tqdm(preISC.items(),desc="Update Shortcut's Thumbnails"):
        if v:
            # 사이트에서 최신 정보를 가져온다.
            version_info = civitai.get_latest_version_info_by_model_id(v['id'])
            if not version_info:
                continue
            
            if 'images' not in version_info.keys():
                continue
            
            # if len(version_info['images']) > 0:                    
            #     v['imageurl'] = version_info['images'][0]['url']
            #     download_thumbnail_image(v['id'], v['imageurl'])
                
            # nsfw 검색해서 최대한 건전한 이미지를 골라낸다.
            if len(version_info["images"]) > 0:
                cur_nsfw_level = len(setting.NSFW_levels)
                def_image = None
                for img_dict in version_info["images"]:
                    if setting.NSFW_levels.index(img_dict["nsfw"]) < cur_nsfw_level:
                        cur_nsfw_level = setting.NSFW_levels.index(img_dict["nsfw"])
                        def_image = img_dict["url"]
                        
                if not def_image:
                    def_image = version_info["images"][0]["url"]
                
                v['imageurl'] = def_image                                        
                download_thumbnail_image(v['id'], v['imageurl'])
                
    # 중간에 변동이 있을수 있으므로 병합한다.                
    ISC = load()
    if ISC:
        ISC.update(preISC)
    else:
        ISC = preISC            
    save(ISC)
    
def get_list(shortcut_types=None)->str:
    
    ISC = load()                           
    if not ISC:
        return
    
    tmp_types = list()
    if shortcut_types:
        for sc_type in shortcut_types:
            try:
                tmp_types.append(setting.ui_typenames[sc_type])
            except:
                pass
            
    shotcutlist = list()
    for k, v in ISC.items():
        # util.printD(ISC[k])
        if v:
            if tmp_types:
                if v['type'] in tmp_types:
                    shotcutlist.append(setting.set_shortcutname(v['name'],v['id']))
            else:                                
                shotcutlist.append(setting.set_shortcutname(v['name'],v['id']))                
                    
    return shotcutlist

def get_image_list(shortcut_types=None, search=None, shortcut_basemodels=None, shortcut_classification=None)->str:
    
    ISC = load()
    if not ISC:
        return
    
    result_list = list()        

    keys, tags, notes = util.get_search_keyword(search)
    # util.printD(f"keys:{keys} ,tags:{tags},notes:{notes}")
    
    # classification # and 연산으로 변경한다.  
    if shortcut_classification:        
        clfs_list = list()
        CISC = classification.load()
        if CISC:
            for name in shortcut_classification:
                name_list = classification.get_shortcut_list(CISC,name)
                if name_list:
                    if len(clfs_list) > 0:
                        clfs_list = list(set(clfs_list) & set(name_list))
                    else:
                        clfs_list = name_list
                else:
                    clfs_list = list()
                    # 결과가 없다면 교집합으로 나올수 있는것이 없으므로 
                    break
                    
            clfs_list = list(set(clfs_list))
            
        if len(clfs_list) > 0:
            for mid in clfs_list:
                if str(mid) in ISC.keys():
                    result_list.append(ISC[str(mid)])
    else:
        result_list = ISC.values()
            
    # filtering type
    tmp_types = list()
    if shortcut_types:
        for sc_type in shortcut_types:
            try:
                tmp_types.append(setting.ui_typenames[sc_type])
            except:
                pass
                
    if tmp_types:
        result_list = [v for v in result_list if v['type'] in tmp_types]
          
    # filtering key
    if keys:
        key_list = list()
        for v in result_list:
            if v:
                for key in keys:
                    if key in v['name'].lower():
                        key_list.append(v)
                        break                    
        result_list = key_list

    # filtering tags
    if tags:
        tags_list = list()
        for v in result_list:
            if v:
                if "tags" not in v.keys():
                    continue                     
                # v_tags = [tag["name"].lower() for tag in v["tags"]]
                v_tags = [tag.lower() for tag in v["tags"]]
                common_tags = set(v_tags) & set(tags)
                if common_tags:
                    tags_list.append(v)
        result_list = tags_list

    # filtering personal note key
    if notes:
        note_list = list()
        for v in result_list:
            if v:
                if "note" not in v.keys():
                    continue
                
                if not v['note']:
                    continue

                for note in notes:                    
                    if note in v['note'].lower():
                        note_list.append(v)
                        break                    
        result_list = note_list
        
    # basemodel 검색
    tmp_basemodels = list()
    if shortcut_basemodels:
        tmp_basemodels.extend(shortcut_basemodels)
        result_list = [v for v in result_list if is_baseModel(str(v['id']), tmp_basemodels)]        
            
    # filename검색
    # if filenames:
    #     filenames_list = list()
    #     for v in result_list:
    #         if v:
    #             if "id" not in v.keys():
    #                 continue
                
    #             v_filenames = get_model_filenames(v["id"])
    #             common_filenames = set(v_filenames) & set(filenames)
    #             if common_filenames:
    #                 filenames_list.append(v)
    #     result_list = filenames_list    
    
    return result_list              

def create_thumbnail(model_id, input_image_path):
    global thumbnail_max_size

    if not model_id:
        return False    
    
    thumbnail_path = os.path.join(setting.shortcut_thumbnail_folder, f"{model_id}{setting.preview_image_ext}")
    # shutil.copy(input_image_path, thumbnail_path)
    try:
        with Image.open(input_image_path) as image:
            image.thumbnail(thumbnail_max_size)
            image.save(thumbnail_path)
    except Exception as e:
        return False
        
    return True
        
def delete_thumbnail_image(model_id):
    if is_sc_image(model_id):
        try:
            os.remove(os.path.join(setting.shortcut_thumbnail_folder,f"{model_id}{setting.preview_image_ext}"))
        except:
            return 
        
def download_thumbnail_image_old(model_id, url):   
    if not model_id or not url:
        return False
    
    if not os.path.exists(setting.shortcut_thumbnail_folder):
        os.makedirs(setting.shortcut_thumbnail_folder)    
    
    try:
        # get image
        with requests.get(url, stream=True) as img_r:
            if not img_r.ok:
                return False
            
            shotcut_img = os.path.join(setting.shortcut_thumbnail_folder,f"{model_id}{setting.preview_image_ext}")                                                                   
            with open(shotcut_img, 'wb') as f:
                img_r.raw.decode_content = True
                shutil.copyfileobj(img_r.raw, f)
            
    except Exception as e:
        return False
    
    return True                    

def download_thumbnail_image(model_id, url):   
    global thumbnail_max_size
    
    if not model_id or not url:
        return False
    
    if not os.path.exists(setting.shortcut_thumbnail_folder):
        os.makedirs(setting.shortcut_thumbnail_folder)    
    
    try:
        # Get image
        with requests.get(url, stream=True) as img_r:
            if not img_r.ok:
                return False

            # Create thumbnail
            with Image.open(img_r.raw) as image:
                image.thumbnail(thumbnail_max_size)
                thumbnail_path = os.path.join(setting.shortcut_thumbnail_folder, f"{model_id}{setting.preview_image_ext}")
                image.save(thumbnail_path)
            
    except Exception as e:
        return False
    
    return True   

# 섬네일이 있는지 체크한다.
def is_sc_image(model_id):
    if not model_id:    
        return False
            
    if os.path.isfile(os.path.join(setting.shortcut_thumbnail_folder,f"{model_id}{setting.preview_image_ext}")):
        return True
    
    return False        

def add(ISC:dict, model_id, register_information_only=False, progress=None)->dict:

    if not model_id:
        return ISC   
        
    if not ISC:
        ISC = dict()
    
    model_info = write_model_information(model_id, register_information_only, progress)    
    
    def_id = None
    def_image = None
    
    if model_info:        
        filenames = list()

        if "modelVersions" in model_info.keys() and len(model_info["modelVersions"]) > 0:
            def_version = model_info["modelVersions"][0]
            def_id = def_version['id']
                
            if 'images' in def_version.keys():
                # if len(def_version["images"]) > 0:
                #     def_image = def_version["images"][0]["url"]
                    
                # nsfw 검색해서 최대한 건전한 이미지를 골라낸다.
                if len(def_version["images"]) > 0:
                    # nsfw_levels = [nsfw_level for nsfw_level in setting.NSFW_level.keys()]
                    cur_nsfw_level = len(setting.NSFW_levels)
                    def_image = None
                    for img_dict in def_version["images"]:
                        if setting.NSFW_levels.index(img_dict["nsfw"]) < cur_nsfw_level:
                            cur_nsfw_level = setting.NSFW_levels.index(img_dict["nsfw"])
                            def_image = img_dict["url"]
                            
                    if not def_image:
                        def_image = def_version["images"][0]["url"]
                                        
            # 현재 모델의 모델 파일 정보를 추출한다.
            # for ver in model_info["modelVersions"]:
            #     for ver_file in ver["files"]:
            #         filenames.append(ver_file["name"])

        # 모델정보가 바뀌어도 피해를 줄이기 위함
        tags = list()
        try:
            if model_info['tags']:           
                tags = [tag for tag in model_info['tags']]
        except:
            pass
        
        date = datetime.datetime.now()
        ISC[str(model_id)] = {
                "id" : model_info['id'],
                "type" : model_info['type'],
                "name": model_info['name'],
                "tags" : tags,
                "nsfw" : model_info['nsfw'],
                "url": f"{civitai.Url_ModelId()}{model_id}",
                "versionid" : def_id,
                "imageurl" : def_image,
                "note" : "",
                "date" : date.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        cis_to_file(ISC[str(model_id)])
        
        # 섬네일이 없을때만 새로 다운받는다.
        if not is_sc_image(model_id):            
            download_thumbnail_image(model_id, def_image)
        
        # download_thumbnail_image(model_id, def_image)
            
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
    if not cis: 
        return 
    
    if "name" in cis.keys() and 'id' in cis.keys():
        backup_cis(cis['name'], f"{civitai.Url_Page()}{cis['id']}")
        # if not os.path.exists(setting.shortcut_save_folder):
        #     os.makedirs(setting.shortcut_save_folder)              
        # util.write_InternetShortcut(os.path.join(setting.shortcut_save_folder,f"{util.replace_filename(cis['name'])}.url"),f"{civitai.Url_Page()}{cis['id']}")
        
def backup_cis(name, url):
    
    if not name or not url:
        return

    backup_dict = None
    try:
        with open(setting.shortcut_civitai_internet_shortcut_url, 'r') as f:
            backup_dict = json.load(f)            
    except:
        backup_dict = dict()
    
    backup_dict[f"url={url}"] = name
            
    try:        
        with open(setting.shortcut_civitai_internet_shortcut_url, 'w') as f:
            json.dump(backup_dict, f, indent=4)
    except Exception as e:
        util.printD("Error when writing file:" + setting.shortcut_civitai_internet_shortcut_url)
        pass
 
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
        util.printD("Unable to load the shortcut file. Starting with an empty file.")
        save({})
        return
    
    json_data = None
    try:
        with open(setting.shortcut, 'r') as f:
            json_data = json.load(f)
    except:
        return None            

    # check error
    if not json_data:
        util.printD("There are no registered shortcuts.")
        return None

    # check for new key
    return json_data
