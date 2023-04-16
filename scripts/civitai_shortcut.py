import os
import gradio as gr
import modules.extras
import modules.scripts as scripts
from modules import shared
from modules import script_callbacks
from scripts.civitai_manager_libs import setting
from scripts.civitai_manager_libs import model_action
from scripts.civitai_manager_libs import ishortcut_action
from scripts.civitai_manager_libs import civitai_shortcut_action
from scripts.civitai_manager_libs import util

def civitai_shortcut_ui():    
    with gr.Tabs(elem_id="civitai_shortcut_tabs_container") as civitai_tab:
        with gr.TabItem("Civitai Shortcut" , id="civitai01"):
            with gr.Row(): 
                with gr.Column(scale=1):
                    with gr.Tabs() as civitai_shortcut_tabs:
                        with gr.TabItem("Upload"):
                            with gr.Row():
                                civitai_internet_url = gr.File(label="Civitai Internet Shortcut", file_count="multiple", file_types=[".url"])
                            with gr.Row():                                
                                shortcut_saved_update_btn = gr.Button(value="Update Shortcut's Model Information",variant="primary")
                            with gr.Row():
                                scan_to_shortcut_btn = gr.Button(value="Scan Downloaded Models to Shortcut",variant="primary")
                            with gr.Row():
                                with gr.Column():
                                    gr.Markdown(value="Updating and scanning may take a lot of time, which can cause heavy traffic on the site.\nRecommend performing these tasks during off-peak hours when the site traffic is lower and the connection is smoother.\nYou can continue with other tasks.")                            
                                    thumb_progress = gr.Markdown(value="###", visible=True)                                                                                                                                    
                                    scan_progress = gr.Markdown(value="###", visible=True)
                            with gr.Row(visible=False):
                                upload_progress = gr.Markdown(value="###", visible=False)
                                
                        with gr.TabItem("Browsing"):    
                            with gr.Row():
                                shortcut_type = gr.Dropdown(label='Filter Model type', multiselect=True, choices=[k for k in setting.ui_model_types], interactive=True)
                            with gr.Row():
                                sc_search = gr.Textbox(label="Search", value="", placeholder="Search name, #tags ....",interactive=True, lines=1)
                            with gr.Row():
                                sc_gallery = gr.Gallery(label="SC Gallery", elem_id="sc_gallery", show_label=False, value=ishortcut_action.get_thumbnail_list()).style(grid=[setting.shortcut_colunm],height="auto")
                            with gr.Row():
                                show_only_downloaded_sc = gr.Checkbox(label="Show downloaded shortcut only", value=False)
                            with gr.Row():
                                refresh_sc_btn = gr.Button(value="Refresh Shortcut List",variant="primary")                                                              
                                
                        with gr.TabItem("Scan New Version"):
                            with gr.Row():
                                shortcut_new_version_type = gr.Dropdown(label='Filter Model type', multiselect=True, choices=[k for k in setting.ui_model_types], interactive=True)                                     
                            with gr.Row():
                                scan_new_version_btn = gr.Button(value="Scan new version model", variant="primary")
                            with gr.Row():
                                sc_new_version_gallery = gr.Gallery(label="SC New Version Gallery", elem_id="sc_new_version_gallery", show_label=False).style(grid=[setting.shortcut_colunm],height="auto")                                

                with gr.Column(scale=4):
                    with gr.Tabs() as civitai_information_tabs:
                        with gr.TabItem("Civitai Model Information" , id="civitai_info"):
                            with gr.Row():
                                with gr.Column(scale=1):
                                    with gr.Row():
                                        versions_list = gr.Dropdown(label="Model Version", choices=[setting.NORESULT], interactive=True, value=setting.NORESULT)
                                    with gr.Row():
                                        model_type = gr.Textbox(label="Model Type", value="", interactive=False, lines=1)
                                    with gr.Row():
                                        trigger_words = gr.Textbox(label="Trigger Words", value="", interactive=False, lines=1).style(container="True")         
                                    with gr.Row():
                                        civitai_model_url_txt = gr.Textbox(label="Model Url", interactive=False , max_lines=1)

                                    with gr.Row(visible=False) as downloaded_tab:
                                        with gr.Tab("Downloaded Version"):
                                            downloaded_info = gr.Textbox(interactive=False,show_label=False)
                                            civitai_openfolder = gr.Button(value="Open Download Folder",variant="primary")   
                                                    
                                    with gr.Row():
                                        filename_list = gr.CheckboxGroup (label="Model Version File", info="Select the files you want to download", choices=[], value=[], interactive=True)
                                    with gr.Row():
                                        an_lora = gr.Checkbox(label="LoRA to additional-networks", value=False)          
                                    with gr.Row():
                                        vs_folder = gr.Checkbox(label="Create version specific folder", value=True)                                                                  
                                    with gr.Row():
                                        download_model = gr.Button(value="Download", variant="primary")                                                
                                    with gr.Row():
                                        gr.Markdown("Downloading may take some time.\nCheck console log for detail")                                                                         
                                        
                                with gr.Column(scale=4):                                                  
                                    with gr.Row():                                                              
                                        model_title_name = gr.Markdown("###", visible=True)            
                                    with gr.Row():    
                                        version_gallery = gr.Gallery(label="Version Gallery", show_label=False, elem_id="version_gallery").style(grid=[setting.gallery_column],height="auto")
                                    with gr.Row():    
                                        description_html = gr.HTML()                                                                                                   
                                with gr.Column(scale=1):
                                    with gr.Row():                            
                                        img_file_info = gr.Textbox(label="Generate Info", interactive=False, lines=6)                            
                                    with gr.Row():
                                        try:
                                            send_to_buttons = modules.generation_parameters_copypaste.create_buttons(["txt2img", "img2img", "inpaint", "extras"])
                                        except:
                                            pass   
                        with gr.TabItem("Saved Model Information" , id="saved_info"):
                            with gr.Row():
                                with gr.Column(scale=1):
                                    with gr.Row():
                                        saved_versions_list = gr.Dropdown(label="Model Version", choices=[setting.NORESULT], interactive=True, value=setting.NORESULT)
                                    with gr.Row():
                                        saved_model_type = gr.Textbox(label="Model Type", value="", interactive=False, lines=1)
                                    with gr.Row():
                                        saved_trigger_words = gr.Textbox(label="Trigger Words", value="", interactive=False, lines=1).style(container="True")         
                                    with gr.Row():
                                        saved_civitai_model_url_txt = gr.Textbox(label="Model Url", interactive=False , max_lines=1)
                                        
                                    with gr.Row(visible=False) as saved_downloaded_tab:
                                        with gr.Tab("Downloaded Version"):
                                            saved_downloaded_info = gr.Textbox(interactive=False,show_label=False)
                                            saved_openfolder = gr.Button(value="Open Download Folder",variant="primary")                                            

                                    with gr.Row():
                                        saved_filename_list = gr.Textbox(label="Model Version File", interactive=False)
                                    with gr.Row():
                                        saved_update_information_btn = gr.Button(value="Update Model Information")
                                    with gr.Row():
                                        shortcut_del_btn = gr.Button(value="Delete Shortcut")                                    
                                        
                                with gr.Column(scale=4):                                                  
                                    with gr.Row():                                                              
                                        saved_model_title_name = gr.Markdown("###", visible=True)            
                                    with gr.Row():    
                                        saved_version_gallery = gr.Gallery(label="Version Gallery", show_label=False, elem_id="version_gallery").style(grid=[setting.gallery_column],height="auto")
                                    with gr.Row():    
                                        saved_description_html = gr.HTML()                                                                                                   
                                with gr.Column(scale=1):
                                    with gr.Row():                            
                                        saved_img_file_info = gr.Textbox(label="Generate Info", interactive=False, lines=6)                            
                                    with gr.Row():
                                        try:
                                            saved_send_to_buttons = modules.generation_parameters_copypaste.create_buttons(["txt2img", "img2img", "inpaint", "extras"])
                                        except:
                                            pass 
            
        with gr.TabItem("Downloaded Model" , id="civitai02"):
            with gr.Row(): 
                with gr.Column(scale=1):
                    with gr.Tabs() as downloaded_model_tabs:                               
                        with gr.TabItem("Browsing"):
                            with gr.Row():
                                shortcut_downloaded_type = gr.Dropdown(label='Filter Model type', multiselect=True, choices=[k for k in setting.ui_model_types], interactive=True)
                            with gr.Row():
                                sc_downloaded_search = gr.Textbox(label="Search", value="", placeholder="Search name, #tags ...." , interactive=True, lines=1)                                
                            with gr.Row():
                                sc_downloaded_gallery = gr.Gallery(label="SC Downloaded Gallery", elem_id="sc_downloaded_gallery", show_label=False, value=ishortcut_action.get_thumbnail_list(None,True)).style(grid=[setting.shortcut_colunm],height="auto")                         
                            with gr.Row():
                                refresh_downloaded_sc_btn = gr.Button(value="Refresh Shortcut List",variant="primary")
                                                                
                with gr.Column(scale=4):
                    with gr.Tab("Civitai Model Information"):
                        with gr.Row():
                            with gr.Column(scale=1):
                                with gr.Row():
                                    downloaded_versions_list = gr.Dropdown(label="Model Version", choices=[setting.NORESULT], interactive=True, value=setting.NORESULT)
                                with gr.Row():
                                    downloaded_model_type = gr.Textbox(label="Model Type", value="", interactive=False, lines=1)                                                     
                                with gr.Row():
                                    downloaded_trigger_words = gr.Textbox(label="Trigger Words", value="", interactive=False, lines=1).style(container="True")         
                                with gr.Row():
                                    downloaded_civitai_model_url_txt = gr.Textbox(label="Model Url", interactive=False , max_lines=1)
                                with gr.Row():
                                    downloaded_filename_list = gr.Textbox(label="Model Version File", interactive=False)                                    
                                with gr.Row():
                                    goto_civitai_model_tab = gr.Button(value="Goto civitai shortcut tab",variant="primary")
                                with gr.Row():
                                    downloaded_openfolder = gr.Button(value="Open Download Folder",variant="primary")
                                                                                                        
                            with gr.Column(scale=4):                                                  
                                with gr.Row():                                                              
                                    downloaded_model_title_name = gr.Markdown("###", visible=True)            
                                with gr.Row():    
                                    downloaded_version_gallery = gr.Gallery(label="Downloaded Version Gallery", show_label=False, elem_id="downloaded_version_gallery").style(grid=[setting.gallery_column],height="auto")
                                with gr.Row():    
                                    downloaded_description_html = gr.HTML()                                                                                                   
                            with gr.Column(scale=1):
                                with gr.Row():                            
                                    downloaded_img_file_info = gr.Textbox(label="Generate Info", interactive=False, lines=6)                            
                                with gr.Row():
                                    try:
                                        downloaded_send_to_buttons = modules.generation_parameters_copypaste.create_buttons(["txt2img", "img2img", "inpaint", "extras"])
                                    except:
                                        pass     
                                                                                
    with gr.Row(visible=False):
                        
        #civitai model select model
        selected_version_id = gr.Textbox()
        selected_model_id = gr.Textbox()
        
        #civitai model information                
        img_index = gr.Number(show_label=False)
        version_images_url = gr.State()
        hidden = gr.Image(type="pil")
        info1 = gr.Textbox()
        info2 = gr.Textbox()        
        selectecd_civitai_information_tabs = gr.Number(value=0, show_label=False)
        
        #download model select model
        selected_downloaded_version_id = gr.Textbox()
        selected_downloaded_model_id = gr.Textbox()
        
        #download model information                
        downloaded_img_index = gr.Number(show_label=False)
        downloaded_version_images_url = gr.State()
        downloaded_hidden = gr.Image(type="pil")
        downloaded_info1 = gr.Textbox()
        downloaded_info2 = gr.Textbox()  
        
        # download shortcut model select model
        selected_saved_version_id = gr.Textbox()
        selected_saved_model_id = gr.Textbox()
                
        # download shortcut information  
        saved_img_index = gr.Number(show_label=False)
        saved_version_images_url = gr.State()
        saved_hidden = gr.Image(type="pil")
        saved_info1 = gr.Textbox()
        saved_info2 = gr.Textbox()

        refresh_sc_list = gr.Textbox(value="")                         
    try:
        modules.generation_parameters_copypaste.bind_buttons(send_to_buttons, hidden, img_file_info)
        modules.generation_parameters_copypaste.bind_buttons(downloaded_send_to_buttons, downloaded_hidden,downloaded_img_file_info)
        modules.generation_parameters_copypaste.bind_buttons(saved_send_to_buttons, saved_hidden,saved_img_file_info)
    except:
        pass
   
    
    ###### Civitai Tab ######
    # civitai upload tab start
    civitai_internet_url.upload(
        fn=civitai_shortcut_action.on_civitai_internet_url_upload,
        inputs=[
            civitai_internet_url,
            selectecd_civitai_information_tabs
        ],
        outputs=[
            selected_model_id,
            selected_saved_model_id,
            upload_progress,
            civitai_internet_url
        ]
    )
    
    scan_to_shortcut_btn.click(
        fn=civitai_shortcut_action.on_scan_to_shortcut_click,
        inputs=None,
        outputs=[
            scan_progress,
        ]                
    )
    
    shortcut_saved_update_btn.click(
        fn=civitai_shortcut_action.on_shortcut_saved_update_btn,
        inputs=None,
        outputs=[
            thumb_progress,
        ]
    ) 
    
    thumb_progress.change(
        fn=civitai_shortcut_action.on_refresh_progress_change,
        inputs= [
            shortcut_type,
            sc_search,
            show_only_downloaded_sc,
            shortcut_downloaded_type,
            sc_downloaded_search
        ],
        outputs=[
            sc_gallery,
            sc_downloaded_gallery,
            thumb_progress
        ]
    )
    
    scan_progress.change(
        fn=civitai_shortcut_action.on_refresh_progress_change,
        inputs= [
            shortcut_type,
            sc_search,
            show_only_downloaded_sc,
            shortcut_downloaded_type,
            sc_downloaded_search
        ],
        outputs=[
            sc_gallery,
            sc_downloaded_gallery,
            scan_progress
        ]
    )
    
    upload_progress.change(
        fn=civitai_shortcut_action.on_refresh_progress_change,
        inputs= [
            shortcut_type,
            sc_search,
            show_only_downloaded_sc,
            shortcut_downloaded_type,
            sc_downloaded_search
        ],
        outputs=[
            sc_gallery,
            sc_downloaded_gallery,
            upload_progress,
        ]        
    )
    # civitai upload tab end
    
    # civitai browsing tab start
    shortcut_type.change(
        fn=civitai_shortcut_action.on_shortcut_gallery_refresh,
        inputs=[
            shortcut_type,            
            sc_search,
            show_only_downloaded_sc,            
        ],
        outputs=[
            sc_gallery,
        ]
    )  
    
    sc_search.submit(
        fn=civitai_shortcut_action.on_shortcut_gallery_refresh,
        inputs=[            
            shortcut_type,
            sc_search,
            show_only_downloaded_sc,                        
        ],
        outputs=[
            sc_gallery            
        ]        
    )
    
    refresh_sc_btn.click(
        fn=civitai_shortcut_action.on_shortcut_gallery_refresh,
        inputs=[
            shortcut_type,
            sc_search,
            show_only_downloaded_sc,
        ],
        outputs=[
            sc_gallery
        ]
    )    
        
    sc_gallery.select(civitai_shortcut_action.on_sc_gallery_select,selectecd_civitai_information_tabs,[selected_model_id,selected_saved_model_id])    
    
    civitai_information_tabs.select(
        fn=civitai_shortcut_action.on_civitai_information_tabs_select,
        inputs=[
            selected_model_id,
            selected_saved_model_id,
        ],
        outputs=[
            selected_model_id,
            selected_saved_model_id,
            selectecd_civitai_information_tabs
        ]
    )
    
    show_only_downloaded_sc.change(
        fn=civitai_shortcut_action.on_shortcut_gallery_refresh,
        inputs=[
            shortcut_type,
            sc_search,
            show_only_downloaded_sc,
        ],
        outputs=[
            sc_gallery,
        ]
    )    
    # civitai browsing tab end
    
    # civitai scan new version tab start
    scan_new_version_btn.click(
        fn=civitai_shortcut_action.on_scan_new_version_btn,
        inputs=[
            shortcut_new_version_type,
        ],
        outputs=[
            sc_new_version_gallery,
        ]                
    )
    
    sc_new_version_gallery.select(civitai_shortcut_action.on_sc_gallery_select,selectecd_civitai_information_tabs,[selected_model_id,selected_saved_model_id])
    # civitai scan new version tab end

    # civitai model information start
    download_model.click(
        fn=civitai_shortcut_action.on_download_model_click,
        inputs=[
            selected_version_id,
            filename_list,            
            an_lora,
            vs_folder
        ],
        outputs=[refresh_sc_list]
    )  
    
    refresh_sc_list.change(
        fn=civitai_shortcut_action.on_refresh_progress_change,
        inputs= [
            shortcut_type,
            sc_search,
            show_only_downloaded_sc,
            shortcut_downloaded_type,
            sc_downloaded_search
        ],
        outputs=[
            sc_gallery,
            sc_downloaded_gallery,
            refresh_sc_list
        ]
    )

    # civitai model
    selected_model_id.change(
        fn=civitai_shortcut_action.on_load_model,
        inputs=[
            selected_model_id,
        ],
        outputs=[
            selected_version_id,
            civitai_model_url_txt, 
            downloaded_tab, 
            downloaded_info, 
            an_lora, 
            model_type, 
            versions_list,
            description_html,
            trigger_words,
            filename_list,
            model_title_name,                        
            version_gallery, 
            version_images_url,
            img_file_info            
        ] 
    )
    
    versions_list.select(
        fn=civitai_shortcut_action.on_versions_list_select,
        inputs=[
            selected_model_id,
        ],
        outputs=[
            selected_version_id,
            civitai_model_url_txt, 
            downloaded_tab, 
            downloaded_info, 
            an_lora, 
            model_type, 
            versions_list,
            description_html,
            trigger_words,
            filename_list,
            model_title_name,                        
            version_gallery, 
            version_images_url,            
            img_file_info          
        ]
    )    
    
    version_gallery.select(civitai_shortcut_action.on_gallery_select, version_images_url, [img_index, hidden])
    hidden.change(fn=modules.extras.run_pnginfo, inputs=[hidden], outputs=[info1, img_file_info, info2])
    # civitai model information end

    # civitai saved model information start
    selected_saved_model_id.change(
        fn=civitai_shortcut_action.on_load_saved_model,
        inputs=[
            selected_saved_model_id,
        ],
        outputs=[
            selected_saved_version_id,
            saved_civitai_model_url_txt,
            saved_downloaded_tab, 
            saved_downloaded_info, 
            saved_model_type, 
            saved_versions_list,                    
            saved_description_html,
            saved_trigger_words,
            saved_filename_list,
            saved_model_title_name,                        
            saved_version_gallery,
            saved_version_images_url,
            saved_img_file_info   
        ] 
    )
    
    saved_versions_list.select(
        fn=civitai_shortcut_action.on_saved_versions_list_select,
        inputs=[
            selected_saved_model_id,
        ],
        outputs=[
            selected_saved_version_id,
            saved_civitai_model_url_txt,
            saved_downloaded_tab, 
            saved_downloaded_info, 
            saved_model_type, 
            saved_versions_list,                    
            saved_description_html,
            saved_trigger_words,
            saved_filename_list,
            saved_model_title_name,                        
            saved_version_gallery,
            saved_version_images_url,
            saved_img_file_info         
        ]
    )    
    
    # shortcut delete
    shortcut_del_btn.click(
        fn=civitai_shortcut_action.on_shortcut_del_btn_click,
        inputs=[
            selected_saved_model_id,
        ],
        outputs=[refresh_sc_list]               
    )
    
    saved_update_information_btn.click(
        fn=civitai_shortcut_action.on_saved_update_information_btn_click,
        inputs=[
            selected_saved_model_id,
        ],
        outputs=[ 
            selected_saved_model_id,
            refresh_sc_list,
            # 이건 진행 상황을 표시하게 하기 위해 넣어둔것이다.
            saved_version_gallery
        ]                    
    )                 

    # selected_saved_model_id 값을 초기화 시키기 위한 이벤트 헨들러이다.
    # saved_update_information_btn.click 에 두개가 묶여 있지만 이것이 먼저 실행될것이다.
    # 하는게 없으므로
    saved_update_information_btn.click(
        fn=civitai_shortcut_action.on_blank_model_info,
        inputs=None,
        outputs=[selected_saved_model_id]                    
    ) 
    
    saved_version_gallery.select(civitai_shortcut_action.on_gallery_select, saved_version_images_url, [saved_img_index, saved_hidden])
    saved_hidden.change(fn=modules.extras.run_pnginfo, inputs=[saved_hidden], outputs=[saved_info1, saved_img_file_info, saved_info2])    
    # civitai saved model information end
    ###### Civitai Tab ###### 

    ###### Downloaded Tab ######                                                  
    # downloaded browsing tab start        
    shortcut_downloaded_type.change(
        fn=civitai_shortcut_action.on_shortcut_gallery_refresh,
        inputs=[
            shortcut_downloaded_type,
            sc_downloaded_search
        ],
        outputs=[
            sc_downloaded_gallery,
        ]
    )   

    sc_downloaded_search.submit(
        fn=civitai_shortcut_action.on_shortcut_gallery_refresh,
        inputs=[            
            shortcut_downloaded_type,          
            sc_downloaded_search
        ],
        outputs=[
            sc_downloaded_gallery            
        ]        
    )
        
    refresh_downloaded_sc_btn.click(civitai_shortcut_action.on_shortcut_gallery_refresh,[shortcut_downloaded_type,sc_downloaded_search],[sc_downloaded_gallery])
    sc_downloaded_gallery.select(civitai_shortcut_action.on_sc_downloaded_gallery_select,None,selected_downloaded_model_id)
    # downloaded browsing tab end

    # downloaded model information start
    selected_downloaded_model_id.change(
        fn=civitai_shortcut_action.on_load_downloaded_model,
        inputs=[
            selected_downloaded_model_id,
        ],
        outputs=[
            selected_downloaded_version_id,
            downloaded_civitai_model_url_txt,
            downloaded_model_type, 
            downloaded_versions_list,                    
            downloaded_description_html,
            downloaded_trigger_words,
            downloaded_filename_list,
            downloaded_model_title_name,                        
            downloaded_version_gallery,
            downloaded_version_images_url,
            downloaded_img_file_info   
        ] 
    )
    
    downloaded_versions_list.select(
        fn=civitai_shortcut_action.on_downloaded_versions_list_select,
        inputs=[
            selected_downloaded_model_id,
        ],
        outputs=[
            selected_downloaded_version_id,
            downloaded_civitai_model_url_txt,
            downloaded_model_type, 
            downloaded_versions_list,                    
            downloaded_description_html,
            downloaded_trigger_words,
            downloaded_filename_list,
            downloaded_model_title_name,                        
            downloaded_version_gallery,
            downloaded_version_images_url,
            downloaded_img_file_info          
        ]
    ) 
       
    goto_civitai_model_tab.click(
        fn=civitai_shortcut_action.on_goto_civitai_model_tab_click,
        inputs=[
            selected_downloaded_model_id
        ],        
        outputs=[
            civitai_tab,
            civitai_information_tabs,
            selected_model_id,      
        ],        
    )
            
    downloaded_version_gallery.select(civitai_shortcut_action.on_gallery_select, downloaded_version_images_url, [downloaded_img_index, downloaded_hidden])
    downloaded_hidden.change(fn=modules.extras.run_pnginfo, inputs=[downloaded_hidden], outputs=[downloaded_info1, downloaded_img_file_info, downloaded_info2])
    # downloaded model information end
    ###### Downloaded Tab ######                                                  

    ### open folder start
    civitai_openfolder.click(civitai_shortcut_action.on_open_folder_click,selected_version_id,None)
    saved_openfolder.click(civitai_shortcut_action.on_open_folder_click,selected_saved_version_id,None)
    downloaded_openfolder.click(civitai_shortcut_action.on_open_folder_click,selected_downloaded_version_id,None)
    ### open folder end
            
def init_civitai_shortcut():
   
    setting.root_path = os.getcwd()
    
    if shared.cmd_opts.embeddings_dir:
        setting.model_folders[setting.model_types['textualinversion']] = shared.cmd_opts.embeddings_dir

    if shared.cmd_opts.hypernetwork_dir :
        setting.model_folders[setting.model_types['hypernetwork']] = shared.cmd_opts.hypernetwork_dir

    if shared.cmd_opts.ckpt_dir:
        setting.model_folders[setting.model_types['checkpoint']] = shared.cmd_opts.ckpt_dir

    if shared.cmd_opts.lora_dir:
        setting.model_folders[setting.model_types['lora']] = shared.cmd_opts.lora_dir
        setting.model_folders[setting.model_types['locon']] = shared.cmd_opts.lora_dir
    
    setting.shortcut = os.path.join(scripts.basedir(),setting.shortcut)
    setting.shortcut_thumbnail_folder = os.path.join(scripts.basedir(),setting.shortcut_thumbnail_folder)
    setting.shortcut_save_folder = os.path.join(scripts.basedir(),setting.shortcut_save_folder)
    setting.shortcut_info_folder = os.path.join(scripts.basedir(),setting.shortcut_info_folder)
    
    # 소유한 모델을 스캔하여 저장한다.
    model_action.Load_Downloaded_Models()
               
# init
init_civitai_shortcut()

def on_ui_tabs():
    with gr.Blocks() as civitai_shortcut:
        civitai_shortcut_ui()
    
    return (civitai_shortcut, "Civitai Shortcut", "civitai_shortcut"),


script_callbacks.on_ui_tabs(on_ui_tabs)
