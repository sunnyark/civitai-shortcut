import os
import gradio as gr
import requests

from PIL import Image
from . import util
from . import setting
from . import civitai_action
from . import ishortcut_action
from . import model_action
from . import civitai_gallery_action

def on_open_folder_click(vid):
    path = model_action.get_model_folder(vid)
    if path:
        util.open_folder(path)

def on_civitai_information_tabs_select(evt: gr.SelectData, selected_civitai_information_tabs , selected_modelid, selected_saved_modelid, selected_usergal_modelid):
    # util.printD(f"{evt.value},{evt.index}")
    active_modleid = selected_modelid
    if selected_civitai_information_tabs == setting.civitai_information_tab:
        active_modleid = selected_modelid
    if selected_civitai_information_tabs == setting.saved_information_tab:
        active_modleid = selected_saved_modelid
    if selected_civitai_information_tabs == setting.usergal_information_tab:
        active_modleid = selected_usergal_modelid
        
    # civitai_information
    if evt.index == setting.civitai_information_tab:
        return evt.index, active_modleid, selected_saved_modelid, selected_usergal_modelid
    
    # saved_information
    if evt.index == setting.saved_information_tab:
        return evt.index, selected_modelid, active_modleid, selected_usergal_modelid

    # usergallery_information
    if evt.index == setting.usergal_information_tab:
        return evt.index, selected_modelid, selected_saved_modelid, active_modleid
        
    return evt.index, selected_modelid, selected_modelid

def on_sc_gallery_select(evt : gr.SelectData, selected_civitai_information_tabs=None):
    if evt.value:
        shortcut = evt.value 
        sc_model_id = shortcut[0:shortcut.find(':')]      
    
    if selected_civitai_information_tabs is not None:
        if selected_civitai_information_tabs == setting.civitai_information_tab:
            return gr.update(value=sc_model_id),gr.update(value=None),gr.update(value=None)
        if selected_civitai_information_tabs == setting.saved_information_tab:
            return gr.update(value=None),gr.update(value=sc_model_id),gr.update(value=None)
        if selected_civitai_information_tabs == setting.usergal_information_tab:
            return gr.update(value=None),gr.update(value=None),gr.update(value=sc_model_id)
                        
    return gr.update(value=sc_model_id),gr.update(value=sc_model_id)

def on_sc_downloaded_gallery_select(evt : gr.SelectData):
    if evt.value:
        shortcut = evt.value 
        sc_model_id = shortcut[0:shortcut.find(':')]      
                        
    return gr.update(value=sc_model_id)

# 이미지를 체크해서 둘다 다시넣어 줘야한다.
def on_civitai_gallery_loading(image_url, progress=gr.Progress()):
    if image_url:
        dn_image_list = []
        image_list = []
        for img_url in progress.tqdm(image_url, desc=f"Civitai Images Loading"):
            try:
                with requests.get(img_url,stream=True) as img_r:
                    if not img_r.ok:                        
                        util.printD("Get error code: " + str(img_r.status_code) + ": proceed to the next file")
                        dn_image_list.append(Image.open(setting.no_card_preview_image))
                        image_list.append(setting.no_card_preview_image)
                        continue
                    img_r.raw.decode_content=True
                    dn_image_list.append(Image.open(img_r.raw))
                    image_list.append(img_url)                     
            except:
                dn_image_list.append(Image.open(setting.no_card_preview_image))
                image_list.append(setting.no_card_preview_image)
        return dn_image_list, image_list
    return None, None

def on_file_gallery_loading(image_url, progress=gr.Progress()):
    if image_url:
        # dn_image_list = []
        # for img_url in progress.tqdm(image_url, desc=f"Images Files Loading"):  
        #     dn_image_list.append(Image.open(img_url))                     
        # return dn_image_list       
        return image_url
    return None

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
    return gr.update(selected="civitai01"), gr.update(selected="civitai_info"),gr.update(value=selected_downloaded_model_id)
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

def on_civitai_internet_url_upload(files, progress=gr.Progress(), selectecd_civitai_information_tabs=None):       
    model_id = ""
    if files:
        modelids = ishortcut_action.upload_shortcut_by_files(files,progress)
        if len(modelids) > 0:
            model_id = modelids[0]

    if not model_id:
        return gr.update(value=""),gr.update(value=""),gr.update(value="Upload shortcut is Done"), None

    if selectecd_civitai_information_tabs is not None:
        if selectecd_civitai_information_tabs == setting.civitai_information_tab:
            return gr.update(value=model_id),gr.update(value=None),gr.update(value="Upload shortcut is Done"), None
        if selectecd_civitai_information_tabs == setting.saved_information_tab:
            return gr.update(value=None),gr.update(value=model_id),gr.update(value="Upload shortcut is Done"), None

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
              
# user gallery information start
def on_usergal_page_url_change( modelid, usergal_page_url, page_info):
    
    if usergal_page_url:
        page_info, title_name, image_url = civitai_gallery_action.get_model_information( modelid , usergal_page_url, False) 
        if page_info:
            total_page = page_info['totalPages']
            current_Page = page_info['currentPage']
                    
            return gr.update(value=title_name),\
                image_url,\
                image_url,\
                gr.update(minimum=1, maximum=total_page, value=current_Page, step=1, label=f"Total {total_page} Pages"),\
                page_info,\
                gr.update(value=None)
                                                    
    return None,None,None,gr.update(minimum=1, maximum=1, value=1),None,None

def on_load_usergal_model(modelid=None):
    page_url = None
    if modelid:
        page_url = civitai_gallery_action. get_default_page_url(modelid,False)    
    return page_url
    
def on_usergal_page_slider_release(usergal_page_url, page_slider):
    page_url = usergal_page_url
    if usergal_page_url:       
        page_url = util.update_url(usergal_page_url,"page", page_slider)    
    
    return page_url

def on_usergal_first_btn_click(usergal_page_url, page_info):
    page_url = usergal_page_url
    if page_info:        
        if page_info['prevPage']:
            page_url = util.update_url(page_info['prevPage'],"page",1)
                    
    return page_url

def on_usergal_end_btn_click(usergal_page_url, page_info):
    page_url = usergal_page_url
    if page_info:
        if page_info['nextPage']:            
            page_url = util.update_url(page_info['nextPage'],"page",page_info['totalPages'])

    return page_url

def on_usergal_next_btn_click(usergal_page_url, page_info):
    page_url = usergal_page_url
    if page_info:        
        if page_info['nextPage']:
            page_url = page_info['nextPage']

    return page_url

def on_usergal_prev_btn_click(usergal_page_url, page_info):
    page_url = usergal_page_url
    if page_info:        
        if page_info['prevPage']:
            page_url = page_info['prevPage']

    return page_url
        
# user gallery information end
        
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
        downloaded_info = None
        is_downloaded = False
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
            downloaded_info = None
            is_downloaded = False            
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
        if model_type == setting.model_types['lora'] or model_type == setting.model_types['locon']:
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

            if model_type == setting.model_types['lora'] or model_type == setting.model_types['locon']:
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
