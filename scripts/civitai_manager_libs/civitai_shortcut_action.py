import os
import gradio as gr
import datetime

from . import util

from . import model
from . import civitai
from . import setting
from . import sc_browser_page

from . import civitai_action
from . import ishortcut_action
from . import civitai_gallery_action
from . import model_action

def is_latest(modelid:str)->bool:
    if not modelid:
        return False
   
    if modelid in model.Downloaded_Models.keys():
        # civitai 에서 최신 모델 정보를 가져온다.
        version_info = civitai.get_latest_version_info_by_model_id(modelid)
        if version_info:
            latest_versionid = str(version_info['id']).strip()                
            
            # 현재 가지고 있는 버전들을 가져온다.                
            dnver_list = list()                
            for vid, version_paths in model.Downloaded_Models[str(modelid)]:
                dnver_list.append(str(vid).strip())
                
            if latest_versionid in dnver_list:                        
                return True
    return False

def on_refresh_shortcut_change():
    current_time = datetime.datetime.now()
    return current_time

def on_civitai_shortcut_tabs_select(evt: gr.SelectData):
    if evt.index == 1:      
        current_time = datetime.datetime.now()  
        return current_time
        
    return gr.update(visible=False)
   
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

##### sc_gallery 함수 정의 #####
def on_sc_gallery_select(evt : gr.SelectData, selected_civitai_information_tabs=None):
    if evt.value:
        shortcut = evt.value 
        sc_model_id = setting.get_modelid_from_shortcutname(shortcut) #shortcut[0:shortcut.find(':')]      
        
    if selected_civitai_information_tabs is not None:
        if selected_civitai_information_tabs == setting.civitai_information_tab:
            return gr.update(value=sc_model_id),gr.update(value=None),gr.update(value=None)
        if selected_civitai_information_tabs == setting.saved_information_tab:
            return gr.update(value=None),gr.update(value=sc_model_id),gr.update(value=None)
        if selected_civitai_information_tabs == setting.usergal_information_tab:
            return gr.update(value=None),gr.update(value=None),gr.update(value=sc_model_id)
                        
    return gr.update(value=sc_model_id),gr.update(value=sc_model_id),gr.update(value=sc_model_id)

def on_civitai_internet_url_upload(files, register_information_only, selected_civitai_information_tabs=None, progress=gr.Progress()):       
    model_id = None    
    if files:
        modelids = ishortcut_action.upload_shortcut_by_files(files, register_information_only, progress)
        if len(modelids) > 0:
            model_id = modelids[0]

    current_time = datetime.datetime.now()
    
    if not model_id:
        return gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), None

    if selected_civitai_information_tabs is not None:
        if selected_civitai_information_tabs == setting.civitai_information_tab:
            return gr.update(value=model_id),gr.update(value=None),gr.update(value=None),current_time, None
        if selected_civitai_information_tabs == setting.saved_information_tab:
            return gr.update(value=None),gr.update(value=model_id),gr.update(value=None),current_time, None
        if selected_civitai_information_tabs == setting.usergal_information_tab:
            return gr.update(value=None),gr.update(value=None),gr.update(value=model_id),current_time, None
        
    return gr.update(value=model_id),gr.update(value=model_id),gr.update(value=model_id),current_time, None

def on_civitai_internet_url_txt_upload(url, register_information_only, selected_civitai_information_tabs=None, progress=gr.Progress()):       
    model_id = None    
    if url:
        if len(url.strip()) > 0:
            modelids = ishortcut_action.upload_shortcut_by_urls([url], register_information_only, progress)
            if len(modelids) > 0:
                model_id = modelids[0]        
    
    current_time = datetime.datetime.now()
    
    if not model_id:
        return gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), None

    if selected_civitai_information_tabs is not None:
        if selected_civitai_information_tabs == setting.civitai_information_tab:
            return gr.update(value=model_id),gr.update(value=None),gr.update(value=None),current_time, None
        if selected_civitai_information_tabs == setting.saved_information_tab:
            return gr.update(value=None),gr.update(value=model_id),gr.update(value=None),current_time, None
        if selected_civitai_information_tabs == setting.usergal_information_tab:
            return gr.update(value=None),gr.update(value=None),gr.update(value=model_id),current_time, None
        
    return gr.update(value=model_id),gr.update(value=model_id),gr.update(value=model_id),current_time, None

def on_update_modelfolder_btn_click():
    model.update_downloaded_model()
    current_time = datetime.datetime.now()
    return current_time

# 새 버전이 있는지 스캔한다
def on_scan_new_version_btn(sc_types, progress=gr.Progress()):
    model.update_downloaded_model()

    scan_list = list()
    # shortlist =  sc_browser.get_thumbnail_list(sc_types,True)
    shortlist, thumb_totals, thumb_max_page =  sc_browser_page.get_thumbnail_list(sc_types,True)
    if shortlist:
        for short in progress.tqdm(shortlist, desc="Scanning new version model"):
            sc_name = short[1]
            mid = setting.get_modelid_from_shortcutname(sc_name) # str(sc_name[0:sc_name.find(':')])
            if not is_latest(mid):
                scan_list.append(short)

    return gr.update(value=scan_list)

def on_ui():
    with gr.Row(visible=False):       
        # information select tab 
        selected_civitai_information_tabs = gr.Number(value=0, show_label=False)
        refresh_shortcut = gr.Textbox()
                        
    with gr.Column(scale=1):
        with gr.Tabs() as civitai_shortcut_tabs:
            with gr.TabItem("Upload"):
                with gr.Row(visible=False):                                 
                    register_information_only = gr.Checkbox(label="Register only model information", value=False)
                with gr.Row():
                    with gr.Column():
                        # with gr.Box(elem_classes="cs_box"):
                        civitai_internet_url_txt = gr.Textbox(placeholder="Copy & Paste or Drag & Drop Civitai Model Url", show_label=False, interactive=True)
                        civitai_internet_url = gr.File(label="Civitai Internet Shortcut", file_count="multiple", file_types=[".url"])
                        update_modelfolder_btn = gr.Button(value="Update Downloaded Model Information", variant="primary")
                        gr.Markdown(value="If you have made direct modifications(e.g. moving or renaming a folder) to the downloaded model during runtime, please execute the \"Update Downloaded Model Information\" function, which rescans the downloaded model and updates its information accordingly. ", visible=True)
                                                    
            with gr.TabItem("Browsing"):    
                with gr.Row():
                    with gr.Column():
                        # sc_gallery, refresh_sc_list = sc_browser.on_ui()
                        sc_gallery, refresh_sc_list = sc_browser_page.on_ui()
                        
            with gr.TabItem("Scan New Version"):
                with gr.Row():
                    with gr.Column():
                        shortcut_new_version_type = gr.Dropdown(label='Filter Model type', multiselect=True, choices=[k for k in setting.ui_typenames], interactive=True)                                     
                        scan_new_version_btn = gr.Button(value="Scan new version model", variant="primary")
                        sc_new_version_gallery = gr.Gallery(label="SC New Version Gallery", elem_id="sc_new_version_gallery", show_label=False).style(grid=[setting.shortcut_column],height="auto")
                        gr.Markdown(value="The feature is to search for new versions of models on Civitai among the downloaded ones.", visible=True)
                
    with gr.Column(scale=4):
        with gr.Tabs() as civitai_information_tabs:
            with gr.TabItem("Civitai Model Information" , id="civitai_info"):
                with gr.Row():
                    selected_model_id , refresh_civitai_information = civitai_action.on_ui(refresh_sc_list)
                    
            with gr.TabItem("Saved Model Information" , id="saved_info"):
                with gr.Row():
                    selected_saved_model_id , refresh_saved_information = ishortcut_action.on_ui(refresh_sc_list)
                    
            with gr.TabItem("Civitai User Gallery" , id="gallery_info"):
                with gr.Row():
                    selected_usergal_model_id = civitai_gallery_action.on_ui()

            # with gr.TabItem("Downloaded Model Information" , id="download_info"):
            #     with gr.Row():
            #         selected_download_model_id = model_action.on_ui()
                                                        
    sc_gallery.select(on_sc_gallery_select, selected_civitai_information_tabs,[selected_model_id,selected_saved_model_id,selected_usergal_model_id])    
    sc_new_version_gallery.select(on_sc_gallery_select,selected_civitai_information_tabs,[selected_model_id,selected_saved_model_id,selected_usergal_model_id])

    refresh_shortcut.change(
        fn=on_refresh_shortcut_change,
        inputs=None,
        outputs=[
            refresh_sc_list,
        ]
    )
    
    civitai_shortcut_tabs.select(
        fn=on_civitai_shortcut_tabs_select,
        inputs=None,
        outputs=refresh_sc_list
    )

    civitai_information_tabs.select(
        fn=on_civitai_information_tabs_select,
        inputs=[
            selected_civitai_information_tabs,
            selected_model_id,
            selected_saved_model_id,
            selected_usergal_model_id
        ],
        outputs=[
            selected_civitai_information_tabs,
            selected_model_id,
            selected_saved_model_id,
            selected_usergal_model_id     
        ]
    )
     
    # civitai upload tab start
    civitai_internet_url.upload(
        fn=on_civitai_internet_url_upload,
        inputs=[
            civitai_internet_url,
            register_information_only,
            selected_civitai_information_tabs
        ],
        outputs=[
            selected_model_id,
            selected_saved_model_id,
            selected_usergal_model_id,
            refresh_sc_list,
            civitai_internet_url
        ]
    )
    
    civitai_internet_url_txt.change(
        fn=on_civitai_internet_url_txt_upload,
        inputs=[
            civitai_internet_url_txt,
            register_information_only,
            selected_civitai_information_tabs
        ],
        outputs=[
            selected_model_id,
            selected_saved_model_id,
            selected_usergal_model_id,
            refresh_sc_list,
            civitai_internet_url_txt
        ]        
    )
       
    update_modelfolder_btn.click(
        fn=on_update_modelfolder_btn_click,
        inputs=None,
        outputs=refresh_sc_list
    )
    
    # civitai upload tab end
    
    # civitai scan new version tab start
    scan_new_version_btn.click(
        fn=on_scan_new_version_btn,
        inputs=[
            shortcut_new_version_type,
        ],
        outputs=[
            sc_new_version_gallery,
        ]                
    )
    # civitai scan new version tab end    
    
    return refresh_shortcut, refresh_civitai_information , refresh_saved_information