import os
import gradio as gr
from . import civitai
from . import civitai_action
from . import setting
from . import util
from . import ishortcut
from . import model
from . import model_action
from tqdm import tqdm

# civitai model information start
# 모델의 정보 불러오게 하는 루틴
def on_selected_model_id_change(modelid):
    is_lora = False
    is_downloaded = False
    model_type = ""
    downloaded_info = ""
    def_name = ""
    model_url = ""
    def_id = ""
    
    if modelid:
        model_type, def_name, def_id, vlist= civitai_action.get_selected_model_info(modelid)
        downloaded_versions_list = model_action.get_model_versions(modelid)

        if downloaded_versions_list:
            downloaded_info = "\n".join(downloaded_versions_list)
            
        if model_type == "LORA":
            is_lora = True   
        
        if downloaded_info:
            is_downloaded = True 

        model_url = civitai.Url_ModelId() + str(modelid)
        
        return gr.update(value=def_id),gr.update(value=model_url),gr.update(visible = is_downloaded),gr.update(value=downloaded_info),gr.update(visible=is_lora),gr.update(value=model_type),gr.update(choices=vlist,value=def_name)
    return gr.update(value=def_id),gr.update(value=model_url),gr.update(visible = is_downloaded),gr.update(value=downloaded_info),gr.update(visible=is_lora),gr.update(value=model_type),gr.Dropdown.update(choices=[setting.NORESULT], value=setting.NORESULT)
    
# 모델의 버전 정보 불러오게 하는 루틴
def on_selected_version_id_change(versionid:str):
    if not versionid:
        return gr.HTML.update(value=""), gr.Textbox.update(value=None), gr.CheckboxGroup.update(choices=[], value=None),None,None,None
    
    version_info = civitai.get_version_info_by_version_id(versionid) 
    
    if not version_info:
        return gr.HTML.update(value=""), gr.Textbox.update(value=None), gr.CheckboxGroup.update(choices=[], value=None),None,None,None
                
    dhtml, triger, flist, mtype = civitai_action.get_version_description_by_version_info(version_info)
    title_name = civitai_action.get_model_title_name_by_version_info(version_info)    
    
    return gr.HTML.update(value=dhtml),gr.Textbox.update(value=triger),gr.CheckboxGroup.update(choices=flist if flist else [], value=flist if flist else []),title_name,None,None
    
def on_description_html_change(versionid):
    return civitai_action.get_version_description_gallery_by_version_id(versionid)
  
def on_versions_list_select(evt: gr.SelectData, modelid:str):       
    
    if not modelid or not evt.value:
        return gr.Textbox.update(value="")
       
    versionid = civitai.get_version_id_by_version_name(modelid, evt.value)        
        
    return gr.Textbox.update(value=versionid)
# civitai model information end 


# download model information start
def on_selected_downloaded_model_id_change(modelid):
    model_type = ""
    def_name = ""
    model_url = ""
    def_id = ""
    
    if modelid:
        downloaded_info, model_type, def_name, def_id, vlist= model_action.get_selected_downloaded_modelinfo(modelid)
        model_url = civitai.Url_ModelId() + str(modelid)
        return gr.update(value=def_id),gr.update(value=model_url),gr.update(value=model_type),gr.update(choices=vlist,value=def_name)
    return gr.update(value=def_id),gr.update(value=model_url),gr.update(value=model_type),gr.Dropdown.update(choices=[setting.NORESULT], value=setting.NORESULT)

def on_selected_downloaded_version_id_change(versionid:str):
    
    if not versionid:
        return gr.HTML.update(value=""), gr.Textbox.update(value=None), gr.Textbox.update(value=None),None,None,None
    
    version_info = model.get_version_info(versionid) 

    if not version_info:
        return gr.HTML.update(value=""), gr.Textbox.update(value=None), gr.Textbox.update(value=None),None,None,None
                    
    dhtml, triger, flist, mtype = model_action.get_version_description(version_info)
    title_name = model_action.get_model_title_name(version_info)    
    
    if flist:
        file_text = "\n".join(flist)
        
    return gr.HTML.update(value=dhtml),gr.Textbox.update(value=triger),gr.Textbox.update(value=file_text),title_name,None,None    
    
def on_downloaded_description_html_change(versionid):
    return model_action.get_version_description_gallery(versionid)

def on_downloaded_versions_list_select(evt: gr.SelectData, model_id:str):       
    
    if not model_id or not evt.value:
        return gr.Textbox.update(value="")
       
    version_id = model.get_version_id_by_version_name(model_id, evt.value)
          
    return gr.Textbox.update(value=version_id)

def on_goto_civitai_model_tab_click(selected_downloaded_model_id):    
    return gr.update(selected="civitai01"), gr.update(value=selected_downloaded_model_id)
# download model information end

    
    
# page download action start
def on_download_images_click(version_id:str, lora_an=False, vs_folder=True):
    msg = None
    if not version_id:
        return msg

    msg = civitai_action.download_image_files(version_id, lora_an, vs_folder)
    return gr.update(value=msg, visible=False)

# 다운 로드후 shortcut 리스트를 갱신한다.
def on_download_model_click(version_id:str, file_name, lora_an, vs_folder):
    msg = None
    if version_id:    
        # 이미지와 파일 모두를 다운 받는다.
        msg = civitai_action.download_file_thread(file_name, version_id, lora_an, vs_folder)
        civitai_action.download_image_files(version_id, lora_an, vs_folder)
        # 다운 받은 모델 정보를 갱신한다.    
        model.Load_Downloaded_Models()
    
    return gr.update(value=msg, visible=False)

def on_shortcut_del_btn_click(model_id):
    #util.printD(f"Delete shortcut {model_id} {len(model_id)}")    
    if model_id:
        ISC = ishortcut.load()                           
        ISC = ishortcut.delete(ISC, model_id)                        
        ishortcut.save(ISC)
            
    return gr.update(value="Delete shortcut is Done", visible=False)
# page download action end

def on_refresh_progress_change(sc_types,show_only_downloaded_sc,sc_downloaded_types):
    return gr.update(value=ishortcut.get_thumbnail_list(sc_types,show_only_downloaded_sc)),gr.update(value=ishortcut.get_thumbnail_list(sc_downloaded_types,True)),gr.update(value="###",visible=True)

# left menu action start 
def on_shortcut_gallery_refresh(sc_types,show_only_downloaded_sc=True):
    return gr.update(value=ishortcut.get_thumbnail_list(sc_types,show_only_downloaded_sc))

# 갤러리에서 하나 선택할때
def on_gallery_select(evt: gr.SelectData,version_images_url):  
     return evt.index, version_images_url[evt.index]
 
# 갤러리 방식으로 숏컬리스트 표시할때
def on_sc_gallery_select(evt : gr.SelectData):
    if evt.value:
        shortcut = evt.value 
        sc_model_id = shortcut[0:shortcut.find(':')]      
                        
    return gr.update(value=sc_model_id)

def on_civitai_internet_url_upload(files, progress=gr.Progress()):       
    if files:
        shortcut = None
        add_ISC = dict()
        for file in progress.tqdm(files, desc=f"Civitai Shortcut"):                        
            shortcut = util.load_InternetShortcut(file.name)            
            if shortcut:  
                model_id = util.get_model_id_from_url(shortcut) 
                model_name, model_type, model_url, def_id, def_name, def_image = civitai_action.get_shortcut_model_info(model_id)
                
                if model_id:                    
                    add_ISC = ishortcut.add(add_ISC, model_id, model_name, model_type, model_url, def_id, def_image)                        
                    
        ISC = ishortcut.load()
        if ISC:
            ISC.update(add_ISC)
        else:
            ISC = add_ISC            
        ishortcut.save(ISC)                     

    if not model_id:
        return gr.update(value=""),gr.update(value="Upload shortcut is Done"), None
    return gr.update(value=model_id),gr.update(value="Upload shortcut is Done"), None
  
def on_scan_to_shortcut_click(progress=gr.Progress()):
    ishortcut.DownloadedModel_to_Shortcut(progress)
    return gr.update(value="Scan Downloaded Models to Shortcut is Done",visible=False)

def on_shortcut_thumbnail_update_click(progress=gr.Progress()):
    ishortcut.update_thumbnail_images(progress)
    return gr.update(value="Update Shortcut's Thumbnails is Done",visible=False)

# 새 버전이 있는지 스캔한다
def on_scan_new_version_btn(sc_types, progress=gr.Progress()):
    model.Load_Downloaded_Models()

    scan_list = list()
    shortlist =  ishortcut.get_thumbnail_list(sc_types,True)
    if shortlist:
        for short in progress.tqdm(shortlist, desc="Scanning new version model"):
            sc_name = short[1]
            mid = str(sc_name[0:sc_name.find(':')])
            if not model_action.is_latest(mid):
                scan_list.append(short)

    return gr.update(value=scan_list)
# left menu action end