import os
import gradio as gr
import requests
import datetime
import modules.extras

from PIL import Image
from . import util
from . import setting
from . import civitai_action
from . import ishortcut_action
from . import model_action

def on_civitai_information_tabs_select(evt: gr.SelectData, selected_civitai_information_tabs , selected_modelid, selected_saved_modelid, selected_usergal_modelid):
    # util.printD(f"{evt.value},{evt.index}")
    active_modelid = selected_modelid
    if selected_civitai_information_tabs == setting.civitai_information_tab:
        active_modelid = selected_modelid
    if selected_civitai_information_tabs == setting.saved_information_tab:
        active_modelid = selected_saved_modelid
    if selected_civitai_information_tabs == setting.usergal_information_tab:
        active_modelid = selected_usergal_modelid
        
    # civitai_information
    if evt.index == setting.civitai_information_tab:
        return evt.index, active_modelid, selected_saved_modelid, selected_usergal_modelid
    
    # saved_information
    if evt.index == setting.saved_information_tab:
        return evt.index, selected_modelid, active_modelid, selected_usergal_modelid

    # usergallery_information
    if evt.index == setting.usergal_information_tab:
        return evt.index, selected_modelid, selected_saved_modelid, active_modelid

    return evt.index, selected_modelid, selected_modelid, selected_modelid

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
                        
    return gr.update(value=sc_model_id),gr.update(value=sc_model_id),gr.update(value=sc_model_id)

def on_refresh_progress_change(sc_types,sc_search,show_only_downloaded_sc):
    return gr.update(value=ishortcut_action.get_thumbnail_list(sc_types,show_only_downloaded_sc,sc_search)),gr.update(value="###",visible=True)

# left menu action start 
def on_shortcut_gallery_refresh(sc_types, sc_search, show_only_downloaded_sc=True):
    return gr.update(value=ishortcut_action.get_thumbnail_list(sc_types,show_only_downloaded_sc,sc_search))
    
def on_civitai_internet_url_upload(files, register_information_only, selected_civitai_information_tabs=None, progress=gr.Progress()):       
    model_id = ""
    if files:
        modelids = ishortcut_action.upload_shortcut_by_files(files, register_information_only, progress)
        if len(modelids) > 0:
            model_id = modelids[0]

    if not model_id:
        return gr.update(value=""),gr.update(value=""),gr.update(value=""),gr.update(value="Upload shortcut is Done"), None

    if selected_civitai_information_tabs is not None:
        if selected_civitai_information_tabs == setting.civitai_information_tab:
            return gr.update(value=model_id),gr.update(value=None),gr.update(value=None),gr.update(value="Upload shortcut is Done"), None
        if selected_civitai_information_tabs == setting.saved_information_tab:
            return gr.update(value=None),gr.update(value=model_id),gr.update(value=None),gr.update(value="Upload shortcut is Done"), None
        if selected_civitai_information_tabs == setting.usergal_information_tab:
            return gr.update(value=None),gr.update(value=None),gr.update(value=model_id),gr.update(value="Upload shortcut is Done"), None
        
    return gr.update(value=model_id),gr.update(value=model_id),gr.update(value=model_id),gr.update(value="Upload shortcut is Done"), None
  
def on_scan_to_shortcut_click(progress=gr.Progress()):
    model_action.Load_Downloaded_Models()
    ishortcut_action.scan_downloadedmodel_to_shortcut(progress)
    return gr.update(value="Scan Downloaded Models to Shortcut is Done", visible=True)

def on_shortcut_saved_update_btn(progress=gr.Progress()):
    ishortcut_action.update_all_shortcut_model(progress)
    return gr.update(value="Update Shortcut's Model Information is Done", visible=True)

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

def on_update_modelfolder_btn_click():
    model_action.Load_Downloaded_Models()
    return gr.update(value="model folder refresh",visible=False)
# left menu action end
    