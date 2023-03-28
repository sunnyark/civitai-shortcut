import requests
import gradio as gr
from . import civitai
from . import civitai_action
from . import model
from . import setting
from . import util
from . import model
from PIL import Image

def on_page_btn_click(action, json_state, content_type, sort_type, search_term, show_nsfw):       
    mlist, new_json_data = get_search_page_action(action, json_state, content_type, sort_type, search_term, show_nsfw)

    if not mlist:
        return new_json_data,gr.Dropdown.update(choices=[setting.NORESULT], value=setting.NORESULT)
    
    return new_json_data,gr.Dropdown.update(choices=[setting.PLACEHOLDER] + mlist, value=setting.PLACEHOLDER)

def on_models_list_select(evt: gr.SelectData,json_state):       
    if evt.value and evt.value != setting.PLACEHOLDER:
        url = get_url_of_model_by_name(json_state, evt.value)
        
        if url: 
            m_id, vlist, def_vname , def_vid= get_selected_model_info_by_url(url)
            if m_id and def_vname and def_vid and vlist:                
                return gr.Textbox.update(value=url),gr.Dropdown.update(choices=vlist, value=def_vname),gr.Textbox.update(value=def_vid),gr.Textbox.update(value=m_id)

    return gr.Textbox.update(value=""),gr.Dropdown.update(choices=[setting.NORESULT], value=setting.NORESULT),gr.Textbox.update(value=""),gr.Textbox.update(value="")

def on_civitai_model_info_btn_click(url:str):  
    if url:                 
        m_id, vlist, def_vname , def_vid= get_selected_model_info_by_url(url)
        if m_id and def_vname and def_vid and vlist: 
            return gr.Textbox.update(value=url),gr.Dropdown.update(choices=vlist, value=def_vname),gr.Textbox.update(value=def_vid),gr.Textbox.update(value=m_id)    
                
    return gr.Textbox.update(value=""),gr.Dropdown.update(choices=[setting.NORESULT], value=setting.NORESULT),gr.Textbox.update(value=""),gr.Textbox.update(value="")

def on_versions_list_select(evt: gr.SelectData, model_id:str):       
    
    if not model_id or not evt.value:
        return gr.Textbox.update(value="")
       
    version_id = civitai.get_version_id_by_version_name(model_id, evt.value)        
        
    return gr.Textbox.update(value=version_id)

def on_selected_version_id_change(version_id:str,selected_model_id:str):           
    if not version_id:
        return gr.HTML.update(value=""), gr.Textbox.update(value=None), gr.CheckboxGroup.update(choices=[], value=None),None,None,None,None,None
    
    version_info = civitai.get_version_info_by_version_id(version_id) 
    
    if not version_info:
        return gr.HTML.update(value=""), gr.Textbox.update(value=None), gr.CheckboxGroup.update(choices=[], value=None),None,None,None,None,None
        
    dhtml, triger, flist, mtype = civitai_action.get_version_description_by_version_info(version_info)
    title_name = civitai_action.get_model_title_name_by_version_info(version_info)    
    return gr.HTML.update(value=dhtml),gr.Textbox.update(value=triger),gr.CheckboxGroup.update(choices=flist if flist else [], value=flist if flist else []),title_name,mtype,version_id,None,None
    
def on_get_gallery_select(evt: gr.SelectData,version_images_url):  
     return evt.index, version_images_url[evt.index]

def on_download_images_click(version_id:str, lora_an=False):
    msg = None
    if not version_id:
        return msg

    msg = civitai_action.download_image_files(version_id, lora_an)        
    return msg

def on_download_model_click(version_id:str, file_name=None, lora_an=False):
    msg = None
    if not version_id:
        return
    
    msg = civitai_action.download_file_thread(file_name, version_id, lora_an)
    return msg

def on_selected_gallery_change(version_id):
    return civitai_action.get_version_description_gallery_by_version_id(version_id)

# 현재 검색된 리스트에서 모델의 이름을 찾아 url을 알려준다.
def get_url_of_model_by_name(model_list:dict,name):    
    model_url = None
    
    if model_list is not None and name:
        for model in model_list['items']:
            if model['name'] == name:
                model_url = f"{civitai.Url_ModelId()}{model['id']}" 
                break
       
    return model_url 

# url에서 model info 정보를 반환한다
def get_selected_model_info_by_url(url:str):
    model = None
    versions_list = []
    def_version = None
    
    if not url:
        return None,None,None,None
    
    model_id = util.get_model_id_from_url(url)    
    
    if not model_id:
        return None,None,None,None
    
    model_url = f"{civitai.Url_ModelId()}{model_id}"             
    
    try:
        r = requests.get(model_url)
        model = r.json()
    except Exception as e:
        util.printD("Load failed")
        return None,None,None,None

    if not model:
        return None,None,None,None   
        
    if "modelVersions" not in model.keys():
        return None,None,None,None
    
    def_version = model["modelVersions"][0]
    
    if not def_version:
        return None,None,None,None
                    
    for version_info in model['modelVersions']:
        versions_list.append(version_info['name'])
    
    return model_id, [v for v in versions_list], def_version['name'], def_version['id']   
                        
def get_search_page_action(action:str, json_state:dict, content_type, sort_type, search_term, show_nsfw=True):
    json_data = json_state
    if action == setting.page_action_dict['search']:
        if search_term:
            search_term = search_term.strip().replace(" ", "%20")
        
        c_types = civitai.content_types_dict[content_type]
        urls = f"{civitai.Url_ModelId()}?limit={setting.page_dict['limit']}"             
        if c_types and len(c_types) > 0:        
            urls = f"{urls}&types={c_types}"
        urls = f"{urls}&sort={sort_type}&query={search_term}"    
        json_data = civitai.request_models(urls)
        
    elif action == setting.page_action_dict['prevPage']:
        try:        
            json_data = civitai.request_models(json_state['metadata']['prevPage'])
        except:   
            pass
    elif action == setting.page_action_dict['nextPage']:
        try:        
            json_data = civitai.request_models(json_state['metadata']['nextPage'])
        except:   
            pass

    if json_data:
        json_state = json_data
                
    try:
        json_state['items']
    except:
        return None,None    
                            
    models_name=[]
        
    if show_nsfw:
        for model in json_state['items']:
            models_name.append(model['name'])
    else:
        for model in json_state['items']:
            temp_nsfw = model['nsfw']
            if not temp_nsfw:
                models_name.append(model['name'])
    return [v for v in models_name],json_state