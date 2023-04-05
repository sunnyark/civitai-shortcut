import gradio as gr
from . import civitai
from . import civitai_action
from . import setting
from . import util
from . import ishortcut
from . import model
from tqdm import tqdm

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

def on_selected_gallery_change(version_id):
    return civitai_action.get_version_description_gallery_by_version_id(version_id)       

def on_civitai_model_url_txt_change():
    return None 

def on_shortcut_thumnail_update_click(sc_types):
    ishortcut.update_thumnail_images()
    return gr.Gallery.update(value=ishortcut.get_image_list(sc_types))

# 갤러리 방식으로 숏컬리스트 표시할때
def on_get_sc_galery_select(evt : gr.SelectData):
    model_url = "" 
    if evt.value:
        shortcut = evt.value 
        sc_model_id = shortcut[0:shortcut.find(':')]      
        sc_model_url = civitai.Url_ModelId() + sc_model_id  
        #util.printD(f"{model_id} {len(model_id)}")    
        model_id, model_name, model_type, model_url, def_id, def_name, def_image, vlist = civitai_action.get_selected_model_info_by_url(sc_model_url)     
        if def_id:
            return sc_model_url, gr.Dropdown.update(choices=vlist, value=def_name), gr.Textbox.update(value=def_id), gr.Textbox.update(value=sc_model_id)
    return sc_model_url, gr.Dropdown.update(choices=[setting.NORESULT], value=setting.NORESULT), gr.Textbox.update(value=""), gr.Textbox.update(value=sc_model_id)       
     
def on_shortcut_del_btn_click(model_id,sc_types):
    #util.printD(f"Delete shortcut {model_id} {len(model_id)}")    
    if model_id:
        ISC = ishortcut.load()                           
        ISC = ishortcut.delete(ISC, model_id)                        
        ishortcut.save(ISC)
        
    return gr.Gallery.update(value=ishortcut.get_image_list(sc_types))
        
def on_shortcut_type_change(sc_types):       
    return gr.Gallery.update(value=ishortcut.get_image_list(sc_types))

def on_civitai_internet_url_upload(files, sc_types):   
    
    if files:
        shortcut = None
        for file in tqdm(files, desc=f"Civitai Shortcut"):                        
            shortcut = util.load_InternetShortcut(file.name)            
            model_id, model_name, model_type, model_url, def_id, def_name, def_image, vlist = internet_shortcut_upload(shortcut)
        
    if not model_url:
        return "",gr.Gallery.update(value=ishortcut.get_image_list(sc_types)),gr.Dropdown.update(choices=[setting.NORESULT], value=setting.NORESULT),gr.Textbox.update(value=""),gr.Textbox.update(value="")
    
    if not def_id:
        return model_url,gr.Gallery.update(value=ishortcut.get_image_list(sc_types)),gr.Dropdown.update(choices=[setting.NORESULT], value=setting.NORESULT),gr.Textbox.update(value=""),gr.Textbox.update(value="")
    return model_url,gr.Gallery.update(value=ishortcut.get_image_list(sc_types)),gr.Dropdown.update(choices=vlist, value=def_name),gr.Textbox.update(value=def_id),gr.Textbox.update(value=model_id)

def internet_shortcut_upload(url):
    if url:  
        #util.printD(url)
        model_id, model_name, model_type, model_url, def_id, def_name, def_image, vlist = civitai_action.get_selected_model_info_by_url(url)
        if model_id:
            # util.printD(model_id)
            ISC = ishortcut.load()                           
            ISC = ishortcut.add(ISC, model_id, model_name, model_type, model_url, def_id, def_image)                        
            ishortcut.save(ISC)
    return model_id, model_name, model_type, model_url, def_id, def_name, def_image, vlist

def on_scan_to_shortcut_click(sc_types):
    ishortcut.OwnedModel_to_Shortcut()
    util.printD("Scan Models to Shortcut ended")
    return gr.Gallery.update(value=ishortcut.get_image_list(sc_types))

def on_refresh_sc_btn_click(sc_types):
    #model.Test_Models()
    return gr.Gallery.update(value=ishortcut.get_image_list(sc_types))