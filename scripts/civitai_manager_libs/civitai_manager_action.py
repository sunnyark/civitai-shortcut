import os
import gradio as gr
from . import civitai
from . import civitai_action
from . import setting
from . import util
from . import ishortcut
from . import model
from tqdm import tqdm

# civitai model information start
# 
# sc_gallery_select -> select_modelid -> versionid-> description_html -> gallery 순으로 순차적으로 실행된다.
# 동시헤 하면 교착상태에 자주빠져서 이리했다. 아마 동시에 civitai에 request 를 해서 네트워크가 안좋을때는 문제가 되는듯하다.
# 모델의 정보 불러오게 하는 루틴
def on_selected_model_id_change(modelid):
    is_lora = False
    is_owned = False
    model_type = ""
    owned_info = ""
    def_name = ""
    def_id = ""
    model_url = ""
    
    if modelid:
        owned_info, model_type, def_name, def_id, vlist= civitai_action.get_selected_model_info(modelid)

        if model_type == "LORA":
            is_lora = True   
        
        if owned_info:
            is_owned = True 

        model_url = civitai.Url_ModelId() + str(modelid)
                
        return gr.update(value=def_id), gr.update(value=model_url),gr.update(visible = is_owned),gr.update(value=owned_info),gr.update(visible=is_lora),gr.update(value=model_type),gr.update(choices=vlist,value=def_name)
    return gr.update(value=def_id), gr.update(value=model_url),gr.update(visible = is_owned),gr.update(value=owned_info),gr.update(visible=is_lora),gr.update(value=model_type),gr.Dropdown.update(choices=[setting.NORESULT], value=setting.NORESULT)
    
# 모델의 버전 정보 불러오게 하는 루틴
def on_selected_version_id_change(version_id:str):
    if not version_id:
        return gr.HTML.update(value=""), gr.Textbox.update(value=None), gr.CheckboxGroup.update(choices=[], value=None),None,None,None
    
    version_info = civitai.get_version_info_by_version_id(version_id) 
        
    if not version_info:
        return gr.HTML.update(value=""), gr.Textbox.update(value=None), gr.CheckboxGroup.update(choices=[], value=None),None,None,None
               
    dhtml, triger, flist, mtype = civitai_action.get_version_description_by_version_info(version_info)
    title_name = civitai_action.get_model_title_name_by_version_info(version_info)    
    
    return gr.HTML.update(value=dhtml), gr.Textbox.update(value=triger), gr.CheckboxGroup.update(choices=flist if flist else [], value=flist if flist else []),title_name,None,None
    
def on_description_html_change(version_id):
    return civitai_action.get_version_description_gallery_by_version_id(version_id)

def on_gallery_select(evt: gr.SelectData,version_images_url):  
     return evt.index, version_images_url[evt.index]
 
def on_versions_list_select(evt: gr.SelectData, model_id:str):       
    
    if not model_id or not evt.value:
        return gr.Textbox.update(value="")
       
    version_id = civitai.get_version_id_by_version_name(model_id, evt.value)        
        
    return gr.Textbox.update(value=version_id)
# civitai model information end 
       
# page download action start    
def on_download_images_click(version_id:str, lora_an=False,vs_folder=True):
    msg = None
    if not version_id:
        return msg

    msg = civitai_action.download_image_files(version_id, lora_an, vs_folder)
    return msg

def on_download_model_click(version_id:str, file_name=None, lora_an=False,vs_folder=True):
    msg = None
    if not version_id:
        return
    
    msg = civitai_action.download_file_thread(file_name, version_id, lora_an, vs_folder)
    return msg
# page download action end

# left menu action start
def on_shortcut_thumnail_update_click(sc_types,sc_owned_types):
    ishortcut.update_thumnail_images()
    return gr.Gallery.update(value=ishortcut.get_image_list(sc_types)),gr.Gallery.update(value=ishortcut.get_owned_image_list(sc_owned_types))
     
def on_shortcut_del_btn_click(model_id, sc_types, sc_owned_types):
    if model_id:
        ISC = ishortcut.load()                           
        ISC = ishortcut.delete(ISC, model_id)                        
        ishortcut.save(ISC)
        
    return gr.Gallery.update(value=ishortcut.get_image_list(sc_types)),gr.Gallery.update(value=ishortcut.get_owned_image_list(sc_owned_types))
        
def on_shortcut_type_change(sc_types):       
    return gr.Gallery.update(value=ishortcut.get_image_list(sc_types))

def on_shortcut_owned_type_change(sc_types):       
    return gr.Gallery.update(value=ishortcut.get_owned_image_list(sc_types))

# 갤러리 방식으로 숏컬리스트 표시할때
def on_sc_gallery_select(evt : gr.SelectData):
    def_id = ""
    if evt.value:
        shortcut = evt.value 
        sc_model_id = shortcut[0:shortcut.find(':')]               
    return gr.update(value=sc_model_id)

# civitai_internet_url 필드를 클리어 하기 위한것
def on_civitai_model_url_txt_change():
    return None 

def on_civitai_internet_url_upload(files, sc_types, sc_owned_types):   
    
    if files:
        shortcut = None
        for file in tqdm(files, desc=f"Civitai Shortcut"):                        
            shortcut = util.load_InternetShortcut(file.name)            
            model_id, model_url, def_id = internet_shortcut_upload(shortcut)
            
    if not model_id:
        return gr.update(value=ishortcut.get_image_list(sc_types)),gr.update(value=ishortcut.get_owned_image_list(sc_owned_types)),gr.update(value="")
    return gr.update(value=ishortcut.get_image_list(sc_types)),gr.update(value=ishortcut.get_owned_image_list(sc_owned_types)),gr.update(value=model_id)

def internet_shortcut_upload(url):
    if url:  
        model_id = util.get_model_id_from_url(url) 
        model_name, model_type, model_url, def_id, def_name, def_image = civitai_action.get_shortcut_model_info(model_id)
        
        if model_id:
            ISC = ishortcut.load()                           
            ISC = ishortcut.add(ISC, model_id, model_name, model_type, model_url, def_id, def_image)                        
            ishortcut.save(ISC)
    return model_id, model_url, def_id
    
def on_scan_to_shortcut_click(sc_types, sc_owned_types):
    ishortcut.OwnedModel_to_Shortcut()
    util.printD("Scan Models to Shortcut ended")
    return gr.Gallery.update(value=ishortcut.get_image_list(sc_types)),gr.Gallery.update(value=ishortcut.get_owned_image_list(sc_owned_types))

def on_refresh_sc_btn_click(sc_types, sc_owned_types):    
    return gr.Gallery.update(value=ishortcut.get_image_list(sc_types)),gr.Gallery.update(value=ishortcut.get_owned_image_list(sc_owned_types))
# left menu action end
