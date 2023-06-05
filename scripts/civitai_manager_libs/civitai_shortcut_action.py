import gradio as gr
import datetime

from . import model
from . import civitai
from . import setting
from . import sc_browser_page

from . import model_action
from . import ishortcut_action
from . import civitai_gallery_action

def on_ui(recipe_input):
    with gr.Row(visible=False):       
        selected_model_id = gr.Textbox()
        selected_information_tabs = gr.State(0)
        
    with gr.Column(scale=setting.shortcut_browser_screen_split_ratio):
        with gr.Tabs() as civitai_shortcut_tabs:
            with gr.TabItem("Upload"):
                with gr.Row(visible=False):                                 
                    register_information_only = gr.Checkbox(label="Register only model information", value=False)
                with gr.Row():
                    with gr.Column():
                        civitai_internet_url_txt = gr.Textbox(placeholder="Copy & Paste or Drag & Drop Civitai Model Url", show_label=False, interactive=True)
                        civitai_internet_url = gr.File(label="Civitai Internet Shortcut", file_count="multiple", file_types=[".url"])
                        update_modelfolder_btn = gr.Button(value="Update Downloaded Model Information", variant="primary")
                        gr.Markdown(value="If you have made direct modifications(e.g. moving or renaming a folder) to the downloaded model during runtime, please execute the \"Update Downloaded Model Information\" function, which rescans the downloaded model and updates its information accordingly. ", visible=True)
                                                    
            with gr.TabItem("Browsing"):    
                with gr.Row():
                    with gr.Column():
                        sc_gallery, refresh_sc_browser, refresh_sc_gallery = sc_browser_page.on_ui()
                        
            with gr.TabItem("Scan New Version"):
                with gr.Row():
                    with gr.Column():
                        shortcut_new_version_type = gr.Dropdown(label='Filter Model type', multiselect=True, choices=[k for k in setting.ui_typenames], interactive=True)                                     
                        scan_new_version_btn = gr.Button(value="Scan new version model", variant="primary")
                        sc_new_version_gallery = gr.Gallery(label="SC New Version Gallery", elem_id="sc_new_version_gallery", show_label=False).style(grid=[setting.shortcut_column], height="fit", object_fit=setting.gallery_thumbnail_image_style)
                        gr.Markdown(value="The feature is to search for new versions of models on Civitai among the downloaded ones.", visible=True)
                
    with gr.Column(scale=(setting.shortcut_browser_screen_split_ratio_max-setting.shortcut_browser_screen_split_ratio)):
        with gr.Tabs() as civitai_information_tabs:
            with gr.TabItem("Model Information" , id="civitai_info"):
                with gr.Row():
                    refresh_civitai_information = ishortcut_action.on_ui(selected_model_id, refresh_sc_browser, recipe_input)

            with gr.TabItem("User Gallery" , id="gallery_info"):
                with gr.Row():
                    civitai_gallery_action.on_ui(selected_model_id, recipe_input)
                    pass

            with gr.TabItem("Downloaded Model Information" , id="download_info"):
                with gr.Row():
                    refresh_download_information = model_action.on_ui(selected_model_id)
                    
    # sc_gallery.select(on_sc_gallery_select, None,[selected_model_id])
    sc_gallery.select(
        fn=on_sc_gallery_select, 
        inputs=selected_information_tabs ,
        outputs=[selected_model_id],
        show_progress=False
    )
    
    sc_new_version_gallery.select(on_sc_new_version_gallery_select, None,[selected_model_id], show_progress=False)

    civitai_information_tabs.select(
        fn=on_civitai_information_tabs_select,
        inputs=None,        
        outputs=[selected_information_tabs, refresh_download_information]
    )
    
    civitai_shortcut_tabs.select(
        fn=on_civitai_shortcut_tabs_select,
        inputs=None,
        outputs=refresh_sc_browser
    )
    
    civitai_internet_url.upload(
        fn=on_civitai_internet_url_upload,
        inputs=[
            civitai_internet_url,
            register_information_only,
        ],
        outputs=[
            selected_model_id,
            refresh_sc_browser,
            civitai_internet_url
        ]
    )
    
    civitai_internet_url_txt.change(
        fn=on_civitai_internet_url_txt_upload,
        inputs=[
            civitai_internet_url_txt,
            register_information_only,
        ],
        outputs=[
            selected_model_id,
            refresh_sc_browser,
            civitai_internet_url_txt
        ]        
    )
       
    update_modelfolder_btn.click(
        fn=on_update_modelfolder_btn_click,
        inputs=None,
        outputs=refresh_sc_browser
    )

    scan_new_version_btn.click(
        fn=on_scan_new_version_btn,
        inputs=[
            shortcut_new_version_type,
        ],
        outputs=[
            sc_new_version_gallery,
        ]                
    )
    
    return refresh_sc_browser, refresh_civitai_information

def on_civitai_shortcut_tabs_select(evt: gr.SelectData):
    if evt.index == 1:      
        current_time = datetime.datetime.now()  
        return current_time
    return gr.update(visible=False)

def on_civitai_information_tabs_select(evt: gr.SelectData):
    current_time = datetime.datetime.now()
    if evt.index == 2:
        # return current_time if setting.changed_model_status else gr.update(visible=True)
        pass
    return gr.update(value=evt.index),gr.update(visible=True)

##### sc_gallery 함수 정의 #####
def on_sc_gallery_select(evt : gr.SelectData, selected_information_tabs):
    if evt.value:
        shortcut = evt.value 
        sc_model_id = setting.get_modelid_from_shortcutname(shortcut) #shortcut[0:shortcut.find(':')]      
        
        # 최신버전이 있으면 업데이트한다. 백그라운드에서 수행되므로 다음에 번에 반영된다.
        # update_shortcut_thread(sc_model_id)
        current_time = datetime.datetime.now()
    return gr.update(value=sc_model_id)

def on_sc_new_version_gallery_select(evt : gr.SelectData):
    if evt.value:
        shortcut = evt.value 
        sc_model_id = setting.get_modelid_from_shortcutname(shortcut) #shortcut[0:shortcut.find(':')]      
        
        # 최신버전이 있으면 업데이트한다. 백그라운드에서 수행되므로 다음에 번에 반영된다.
        # update_shortcut_thread(sc_model_id)
                                
    return gr.update(value=sc_model_id)

def on_civitai_internet_url_upload(files, register_information_only, progress=gr.Progress()):       
    model_id = None    
    if files:
        modelids = ishortcut_action.upload_shortcut_by_files(files, register_information_only, progress)
        if len(modelids) > 0:
            model_id = modelids[0]

    current_time = datetime.datetime.now()
    
    if not model_id:
        return gr.update(visible=False), gr.update(visible=False), None
                
    return gr.update(value=model_id), current_time, None

def on_civitai_internet_url_txt_upload(url, register_information_only, progress=gr.Progress()):       
    model_id = None    
    if url:
        if len(url.strip()) > 0:
            modelids = ishortcut_action.upload_shortcut_by_urls([url], register_information_only, progress)
            if len(modelids) > 0:
                model_id = modelids[0]        
    
    current_time = datetime.datetime.now()
    
    if not model_id:
        return gr.update(visible=False), gr.update(visible=False), None
                
    return gr.update(value=model_id), current_time, None

def on_update_modelfolder_btn_click():
    model.update_downloaded_model()
    current_time = datetime.datetime.now()
    return current_time

# 새 버전이 있는지 스캔한다
def on_scan_new_version_btn(sc_types, progress=gr.Progress()):
    model.update_downloaded_model()

    scan_list = list()
    shortlist, thumb_totals, thumb_max_page =  sc_browser_page.get_thumbnail_list(sc_types,True)
    if shortlist:        
        for short in progress.tqdm(shortlist, desc="Scanning new version model"):
            sc_name = short[1]
            mid = setting.get_modelid_from_shortcutname(sc_name) # str(sc_name[0:sc_name.find(':')])
            # util.printD(mid)
            if not is_latest(mid):
                scan_list.append(short)
    #             util.printD(short)
    # util.printD("end")
    return gr.update(value=scan_list)

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

# def update_shortcut_information(modelid):
#     if not modelid:    
#         return    
#     try:
#         if setting.shortcut_auto_update:
#             ishortcut.write_model_information(modelid, False, None)
#     except:
#         return    
#     return
    
# def update_shortcut_thread(modelid):
#     try:
#         thread = threading.Thread(target=update_shortcut_information, args=(modelid,))
#         thread.start()                
#     except Exception as e:
#         util.printD(e)
#         pass