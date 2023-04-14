import os
import gradio as gr
from . import util
from . import setting
from . import civitai_action
from . import ishortcut_action
from . import model_action

from tqdm import tqdm


# selected_saved_model_id 값을 초기화 시키기 위한 이벤트 헨들러이다.
# saved_update_information_btn.click 에 두개가 묶여 있지만 이것이 먼저 리턴값을 낼것이다.
# 하는게 없으므로
def on_blank_model_info():
    return gr.update(value=None)
            
def on_saved_update_information_btn_click(modelid):
    if modelid:
        ishortcut_action.update_shortcut_model(modelid)  
    return gr.update(value=modelid),gr.update(value="Done"),gr.update(value=None)

def on_goto_civitai_model_tab_click(selected_downloaded_model_id):    
    return gr.update(selected="civitai01"), gr.update(value=selected_downloaded_model_id), gr.update(value=selected_downloaded_model_id)
# download model information end

# 다운 로드후 shortcut 리스트를 갱신한다.
def on_download_model_click(version_id:str, file_name, lora_an, vs_folder):
    msg = None
    if version_id:    
        # 프리뷰이미지와 파일 모두를 다운 받는다.
        msg = civitai_action.download_file_thread(file_name, version_id, lora_an, vs_folder)
        civitai_action.download_image_files(version_id, lora_an, vs_folder)
        # 다운 받은 모델 정보를 갱신한다.    
        model_action.Load_Downloaded_Models()
    
    return gr.update(value=msg, visible=False)

def on_shortcut_del_btn_click(model_id):
    #util.printD(f"Delete shortcut {model_id} {len(model_id)}")    
    if model_id:
        ishortcut_action.delete_shortcut_model(model_id)            
    return gr.update(value="Delete shortcut is Done", visible=False)
# page download action end

def on_refresh_progress_change(sc_types,sc_search,show_only_downloaded_sc,sc_downloaded_types,sc_downloaded_search):
    return gr.update(value=ishortcut_action.get_thumbnail_list(sc_types,show_only_downloaded_sc,sc_search)),gr.update(value=ishortcut_action.get_thumbnail_list(sc_downloaded_types,True,sc_downloaded_search)),gr.update(value="###",visible=True)

# left menu action start 
def on_shortcut_gallery_refresh(sc_types, sc_search, show_only_downloaded_sc=True):
    return gr.update(value=ishortcut_action.get_thumbnail_list(sc_types,show_only_downloaded_sc,sc_search))

# 갤러리에서 하나 선택할때
def on_gallery_select(evt: gr.SelectData,version_images_url):  
     return evt.index, version_images_url[evt.index]
 
# 갤러리 방식으로 숏컬리스트 표시할때
def on_sc_gallery_select(evt : gr.SelectData):
    if evt.value:
        shortcut = evt.value 
        sc_model_id = shortcut[0:shortcut.find(':')]      
                        
    return gr.update(value=sc_model_id),gr.update(value=sc_model_id)

# 갤러리 방식으로 숏컬리스트 표시할때
def on_sc_downloaded_gallery_select(evt : gr.SelectData):
    if evt.value:
        shortcut = evt.value 
        sc_model_id = shortcut[0:shortcut.find(':')]      
                        
    return gr.update(value=sc_model_id)

def on_civitai_internet_url_upload(files, progress=gr.Progress()):       
    model_id = ""
    if files:
        modelids = ishortcut_action.upload_shortcut_by_files(files,progress)
        if len(modelids) > 0:
            model_id = modelids[0]

    if not model_id:
        return gr.update(value=""),gr.update(value=""),gr.update(value="Upload shortcut is Done"), None
    return gr.update(value=model_id),gr.update(value=model_id),gr.update(value="Upload shortcut is Done"), None
  
def on_scan_to_shortcut_click(progress=gr.Progress()):
    model_action.Load_Downloaded_Models()
    ishortcut_action.scan_downloadedmodel_to_shortcut(progress)
    return gr.update(value="Scan Downloaded Models to Shortcut is Done",visible=False)

def on_shortcut_saved_update_btn(progress=gr.Progress()):
    ishortcut_action.update_all_shortcut_model(progress)
    return gr.update(value="Update Shortcut's Model Information is Done",visible=False)

# 새 버전이 있는지 스캔한다
def on_scan_new_version_btn(sc_types, progress=gr.Progress()):
    model_action.Load_Downloaded_Models()

    scan_list = list()
    shortlist =  ishortcut_action.get_thumbnail_list(sc_types,True)
    if shortlist:
        for short in progress.tqdm(shortlist, desc="Scanning new version model"):
            sc_name = short[1]
            mid = str(sc_name[0:sc_name.find(':')])
            if not model_action.is_latest(mid):
                scan_list.append(short)

    return gr.update(value=scan_list)
# left menu action end


# downloaded model information start
def on_load_downloaded_model(modelid=None, versionid=None):
    model_info,versionid,version_name,model_url,model_type,versions_list,dhtml,triger,flist,title_name, gallery_url, images_url = model_action.get_model_information(modelid, versionid)    
    if model_info:
        file_text = ""
    
        if flist:
            file_text = "\n".join(flist)
                            
        return gr.update(value=versionid),gr.update(value=model_url),\
            gr.update(value=model_type),gr.update(choices=versions_list,value=version_name),gr.update(value=dhtml),\
            gr.update(value=triger),gr.update(value=file_text),gr.update(value=title_name),\
            gallery_url,images_url,gr.update(value=None)

    # 모델 정보가 없다면 클리어 한다.
    # clear model information
    return gr.update(value=None),gr.update(value=None),\
        gr.update(value=None),gr.update(choices=[setting.NORESULT], value=setting.NORESULT),gr.update(value=None),\
        gr.update(value=None),gr.update(value=None),gr.update(value=None),\
        None,None,gr.update(value=None)   

def on_downloaded_versions_list_select(evt: gr.SelectData, modelid:str):
    if modelid:
        model_info,versionid,version_name,model_url,model_type,versions_list,dhtml,triger,flist,title_name,gallery_url,images_url = model_action.get_model_information(modelid,None,evt.index)
        if model_info:
            file_text = ""
        
            if flist:
                file_text = "\n".join(flist)
                
            return gr.update(value=versionid),gr.update(value=model_url),\
                gr.update(value=model_type),gr.update(choices=versions_list,value=version_name),gr.update(value=dhtml),\
                gr.update(value=triger),gr.update(value=file_text),gr.update(value=title_name),\
                gallery_url,images_url,gr.update(value=None)

    # 모델 정보가 없다면 클리어 한다.
    # clear model information
    return gr.update(value=None),gr.update(value=None),\
        gr.update(value=None),gr.update(choices=[setting.NORESULT], value=setting.NORESULT),gr.update(value=None),\
        gr.update(value=None),gr.update(value=None),gr.update(value=None),\
        None,None,gr.update(value=None)  
# downloaded model information end

# saved model information start
def on_load_saved_model(modelid=None, versionid=None):
    model_info,versionid,version_name,model_url,downloaded_versions_list,model_type,versions_list,dhtml,triger,flist,title_name, gallery_url, images_url = ishortcut_action.get_model_information(modelid, versionid)    
    if model_info:
        is_lora = False
        downloaded_info = None
        is_downloaded = False
        if model_type == "LORA":
            is_lora = True 

        if downloaded_versions_list:
            downloaded_info = "\n".join(downloaded_versions_list)
                    
        if downloaded_info:
            is_downloaded = True 

        file_text = ""
    
        if flist:
            file_text = "\n".join(flist)
                            
        return gr.update(value=versionid),gr.update(value=model_url),\
            gr.update(visible = is_downloaded),gr.update(value=downloaded_info),\
            gr.update(value=model_type),gr.update(choices=versions_list,value=version_name),gr.update(value=dhtml),\
            gr.update(value=triger),gr.update(value=file_text),gr.update(value=title_name),\
            gallery_url,images_url,gr.update(value=None)

    # 모델 정보가 없다면 클리어 한다.
    # clear model information
    return gr.update(value=None),gr.update(value=None),\
        gr.update(visible=False),gr.update(value=None),\
        gr.update(value=None),gr.update(choices=[setting.NORESULT], value=setting.NORESULT),gr.update(value=None),\
        gr.update(value=None),gr.update(value=None),gr.update(value=None),\
        None,None,gr.update(value=None)   

def on_saved_versions_list_select(evt: gr.SelectData, modelid:str):
    if modelid:
        model_info,versionid,version_name,model_url,downloaded_versions_list,model_type,versions_list,dhtml,triger,flist,title_name,gallery_url,images_url = ishortcut_action.get_model_information(modelid,None,evt.index)    
        if model_info:
            is_lora = False
            downloaded_info = None
            is_downloaded = False            
            if model_type == "LORA":
                is_lora = True 

            if downloaded_versions_list:
                downloaded_info = "\n".join(downloaded_versions_list)
                        
            if downloaded_info:
                is_downloaded = True 
                
            file_text = ""
        
            if flist:
                file_text = "\n".join(flist)
                
            return gr.update(value=versionid),gr.update(value=model_url),\
                gr.update(visible = is_downloaded),gr.update(value=downloaded_info),\
                gr.update(value=model_type),gr.update(choices=versions_list,value=version_name),gr.update(value=dhtml),\
                gr.update(value=triger),gr.update(value=file_text),gr.update(value=title_name),\
                gallery_url,images_url,gr.update(value=None)

    # 모델 정보가 없다면 클리어 한다.
    # clear model information
    return gr.update(value=None),gr.update(value=None),\
        gr.update(visible=False),gr.update(value=None),\
        gr.update(value=None),gr.update(choices=[setting.NORESULT], value=setting.NORESULT),gr.update(value=None),\
        gr.update(value=None),gr.update(value=None),gr.update(value=None),\
        None,None,gr.update(value=None)  
# saved model information end                    

# civitai model information start
def on_load_model(modelid=None, versionid=None):
    model_info,versionid,version_name,model_url,downloaded_versions_list,model_type,versions_list,dhtml,triger,flist,title_name, gallery_url, images_url = civitai_action.get_model_information(modelid, versionid)    
    if model_info:
        is_lora = False
        downloaded_info = None
        is_downloaded = False
        if model_type == "LORA":
            is_lora = True 

        if downloaded_versions_list:
            downloaded_info = "\n".join(downloaded_versions_list)
                    
        if downloaded_info:
            is_downloaded = True 
                    
        return gr.update(value=versionid),gr.update(value=model_url),gr.update(visible = is_downloaded),gr.update(value=downloaded_info),\
            gr.update(visible=is_lora),gr.update(value=model_type),gr.update(choices=versions_list,value=version_name),gr.update(value=dhtml),\
            gr.update(value=triger),gr.update(choices=flist if flist else [], value=flist if flist else []),gr.update(value=title_name),\
            gallery_url,images_url,gr.update(value=None)

    # 모델 정보가 없다면 클리어 한다.
    # clear model information
    return gr.update(value=None),gr.update(value=None),gr.update(visible=False),gr.update(value=None),\
        gr.update(visible=False),gr.update(value=None),gr.update(choices=[setting.NORESULT], value=setting.NORESULT),gr.update(value=None),\
        gr.update(value=None),gr.update(choices=[], value=None),gr.update(value=None),\
        None,None,gr.update(value=None)       

def on_versions_list_select(evt: gr.SelectData, modelid:str):
    if modelid:
        model_info,versionid,version_name,model_url,downloaded_versions_list,model_type,versions_list,dhtml,triger,flist,title_name,gallery_url,images_url = civitai_action.get_model_information(modelid,None,evt.index)    
        if model_info:
            is_lora = False
            downloaded_info = None
            is_downloaded = False            
            if model_type == "LORA":
                is_lora = True 

            if downloaded_versions_list:
                downloaded_info = "\n".join(downloaded_versions_list)
                        
            if downloaded_info:
                is_downloaded = True 
                        
            return gr.update(value=versionid),gr.update(value=model_url),gr.update(visible = is_downloaded),gr.update(value=downloaded_info),\
                gr.update(visible=is_lora),gr.update(value=model_type),gr.update(choices=versions_list,value=version_name),gr.update(value=dhtml),\
                gr.update(value=triger),gr.update(choices=flist if flist else [], value=flist if flist else []),gr.update(value=title_name),\
                gallery_url,images_url,gr.update(value=None)

    # 모델 정보가 없다면 클리어 한다.
    # clear model information
    return gr.update(value=None),gr.update(value=None),gr.update(visible=False),gr.update(value=None),\
        gr.update(visible=False),gr.update(value=None),gr.update(choices=[setting.NORESULT], value=setting.NORESULT),gr.update(value=None),\
        gr.update(value=None),gr.update(choices=[], value=None),gr.update(value=None),\
        None,None,gr.update(value=None)  
# civitai model information end
