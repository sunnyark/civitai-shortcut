import requests
import gradio as gr
from . import civitai
from . import civitai_action
from . import model
from . import setting
from . import util
from PIL import Image

def on_page_btn_click(action, json_state, content_type, sort_type, search_term, show_nsfw):       
    mlist, new_json_data = model.get_search_page_action(action, json_state, content_type, sort_type, search_term, show_nsfw)

    if not mlist:
        return new_json_data,gr.Dropdown.update(choices=[setting.NORESULT], value=setting.NORESULT)
    
    return new_json_data,gr.Dropdown.update(choices=[setting.PLACEHOLDER] + mlist, value=setting.PLACEHOLDER)

def on_models_list_select(evt: gr.SelectData,json_state):       
    if evt.value and evt.value != setting.PLACEHOLDER:
        url = civitai_action.get_url_of_model_by_name(json_state, evt.value)
        
        if url: 
            m_id, vlist, def_vname , def_vid= model.get_selected_model_info_by_url(url)
            if m_id and def_vname and def_vid and vlist:                
                return gr.Textbox.update(value=url),gr.Dropdown.update(choices=vlist, value=def_vname),gr.Textbox.update(value=def_vid),gr.Textbox.update(value=m_id)

    return gr.Textbox.update(value=""),gr.Dropdown.update(choices=[setting.NORESULT], value=setting.NORESULT),gr.Textbox.update(value=""),gr.Textbox.update(value="")

def on_civitai_model_info_btn_click(url:str):  
    if url:                 
        m_id, vlist, def_vname , def_vid= model.get_selected_model_info_by_url(url)
        if m_id and def_vname and def_vid and vlist: 
            return gr.Textbox.update(value=url),gr.Dropdown.update(choices=vlist, value=def_vname),gr.Textbox.update(value=def_vid),gr.Textbox.update(value=m_id)    
                
    return gr.Textbox.update(value=""),gr.Dropdown.update(choices=[setting.NORESULT], value=setting.NORESULT),gr.Textbox.update(value=""),gr.Textbox.update(value="")

def on_versions_list_select(evt: gr.SelectData, model_id:str):       
    
    if not model_id or not evt.value:
        return gr.Textbox.update(value="")
       
    version_id = civitai.get_version_id_by_version_name(model_id, evt.value)        
        
    return gr.Textbox.update(value=version_id)

def on_selected_version_id_change(version_id:str):           
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

def on_civitai_model_url_txt_select(evt: gr.SelectData):
    #util.printD("text select")
    return gr.Textbox.update(value="")
    
   