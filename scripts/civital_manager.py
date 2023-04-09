import os
import gradio as gr
import modules.extras
import modules.scripts as scripts
from modules import shared
from modules import script_callbacks
from scripts.civitai_manager_libs import setting
from scripts.civitai_manager_libs import civitai_manager_action
from scripts.civitai_manager_libs import ishortcut
from scripts.civitai_manager_libs import civitai
from scripts.civitai_manager_libs import civitai_action
from scripts.civitai_manager_libs import util
from scripts.civitai_manager_libs import model   

def tab_test():
    return gr.update(selected="civitai01")

def on_goto_civitai_model_tab_click(selected_downloaded_model_id):    
    return gr.update(selected="civitai01"),gr.update(value=selected_downloaded_model_id)

def civitai_manager_ui():      
    with gr.Tabs() as civitai_tab:
        with gr.TabItem("Civitai Shortcut" , id="civitai01"):
            with gr.Row(): 
                with gr.Column(scale=1):
                    with gr.Tabs() as civitai_shortcut_tabs:
                        with gr.TabItem("Upload"):
                            with gr.Row():
                                civitai_internet_url = gr.File(label="Civitai Internet Shortcut", file_count="multiple", file_types=[".url"]) 
                            with gr.Row():
                                update_sc_btn = gr.Button(value="Update Shortcut's Thumbnails",variant="primary")
                            with gr.Row():                        
                                scan_sc_btn = gr.Button(value="Scan Downloaded Models to Shortcut",variant="primary")                             
                        with gr.TabItem("Browsing"):    
                            with gr.Row():
                                shortcut_type = gr.Dropdown(label='Filter Model type', multiselect=True, choices=[k for k in setting.content_types_dict], interactive=True)
                            with gr.Row():
                                sc_gallery = gr.Gallery(show_label=False, value=ishortcut.get_thumbnail_list()).style(grid=1)
                            with gr.Row():
                                show_only_downloaded_sc = gr.Checkbox(label="Show downloaded shortcut only", value=False)                        
                            with gr.Row():
                                refresh_sc_btn = gr.Button(value="Refresh Shortcut List",variant="primary")                        

                with gr.Column(scale=4):
                    with gr.Tab("Model Information"):
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
                                        with gr.TabItem("Downloaded Version"):
                                            with gr.Row():                            
                                                downloaded_info = gr.Textbox(interactive=False,show_label=False)
                                                
                                with gr.Row():
                                    filename_list = gr.CheckboxGroup (label="Model Version File", info="Select the files you want to download", choices=[], value=[], interactive=True)
                                with gr.Row():
                                    an_lora = gr.Checkbox(label="LoRA to additional-networks", value=False)          
                                with gr.Row():
                                    vs_folder = gr.Checkbox(label="Create version specific folder", value=True)                                                                  
                                with gr.Row():
                                    download_model = gr.Button(value="Download", variant="primary")                                                
                                with gr.Row():
                                    download_images = gr.Button(value="Download Images Only",variant="primary")                                                              
                                with gr.Row():
                                    shortcut_del_btn = gr.Button(value="Delete Shortcut")                                                   
                                with gr.Row():    
                                    message_log = gr.Markdown("###")
                            with gr.Column(scale=4):                                                  
                                with gr.Row():                                                              
                                    model_title_name = gr.Markdown("###", visible=True)            
                                with gr.Row():    
                                    version_gallery = gr.Gallery(show_label=False).style(grid=4)
                                    #version_gallery = gr.Gallery(show_label=False).style(grid=opts.images_history_page_columns)
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
                
                    

            
        with gr.TabItem("Downloaded Shortcut" , id="civitai02"):
            with gr.Row(): 
                with gr.Column(scale=1):
                    with gr.Tabs() as downloaded_shortcut_tabs:
                        with gr.TabItem("Browsing"):                    
                            with gr.Row():
                                shortcut_downloaded_type = gr.Dropdown(label='Filter Model type', multiselect=True, choices=[k for k in setting.content_types_dict], interactive=True)         
                            with gr.Row():
                                sc_downloaded_gallery = gr.Gallery(show_label=False, value=ishortcut.get_thumbnail_list(None,True)).style(grid=1)
                            with gr.Row():
                                refresh_downloaded_sc_btn = gr.Button(value="Refresh Shortcut List",variant="primary")
                                
                            # with gr.Row():
                            #     select_tab_test = gr.Button(value="goto tabs",variant="primary")  
                                                                
                with gr.Column(scale=4):
                    with gr.Tab("Model Information"):
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
                                                                    
                            with gr.Column(scale=4):                                                  
                                with gr.Row():                                                              
                                    downloaded_model_title_name = gr.Markdown("###", visible=True)            
                                with gr.Row():    
                                    downloaded_version_gallery = gr.Gallery(show_label=False).style(grid=4)
                                    #owned_version_gallery = gr.Gallery(show_label=False).style(grid=opts.images_history_page_columns)
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
        # with gr.TabItem("Browsing Downloaded Images" , id="civitai03"):
        #     pass
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

        #download model select model
        selected_downloaded_version_id = gr.Textbox()
        selected_downloaded_model_id = gr.Textbox()
        
        #download model information                
        downloaded_img_index = gr.Number(show_label=False)
        downloaded_version_images_url = gr.State()
        downloaded_hidden = gr.Image(type="pil")
        downloaded_info1 = gr.Textbox()
        downloaded_info2 = gr.Textbox()  
                                                
    try:
        modules.generation_parameters_copypaste.bind_buttons(send_to_buttons, hidden, img_file_info)
        modules.generation_parameters_copypaste.bind_buttons(downloaded_send_to_buttons, downloaded_hidden,downloaded_img_file_info)
    except:
        pass
              
    # 다운로드
    download_model.click(
        fn=civitai_manager_action.on_download_model_click,
        inputs=[
            selected_version_id,
            filename_list,            
            an_lora,
            vs_folder,         
            shortcut_type,
            show_only_downloaded_sc,
            shortcut_downloaded_type               
        ],
        outputs=[
            message_log,
            sc_gallery,
            sc_downloaded_gallery,            
        ]
    )  
        
    download_images.click(
        fn=civitai_manager_action.on_download_images_click,
        inputs=[
            selected_version_id,
            an_lora,
            vs_folder,
        ],
        outputs=[message_log]
    )
    
    # civitai model information
    # 버전을 하나 선택
    versions_list.select(
        fn=civitai_manager_action.on_versions_list_select,
        inputs=[
            selected_model_id, 
        ],
        outputs=[
            selected_version_id,            
        ]
    )
    
    selected_model_id.change(
        fn=civitai_manager_action.on_selected_model_id_change,   
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
        ] 
    )
  
    selected_version_id.change(
        fn=civitai_manager_action.on_selected_version_id_change,
        inputs=[
            selected_version_id,
        ],
        outputs=[
            description_html,
            trigger_words,
            filename_list,
            model_title_name,                        
            version_gallery,
            img_file_info      
        ]
    )
        
    description_html.change(
        fn=civitai_manager_action.on_description_html_change,
        inputs=[
            selected_version_id
        ],
        outputs=[
            version_gallery, 
            version_images_url
        ]
    )

    version_gallery.select(civitai_manager_action.on_gallery_select, version_images_url, [img_index, hidden])    
    hidden.change(fn=modules.extras.run_pnginfo, inputs=[hidden], outputs=[info1, img_file_info, info2])      
    # civitai model information
    
    
    # download model information start
    # 버전을 하나 선택
    # 동일 이벤트에 여러개 연결하면 많이 늦어지는듯함..  따로 만듧시다.
    downloaded_versions_list.select(
        fn=civitai_manager_action.on_downloaded_versions_list_select,
        inputs=[
            selected_downloaded_model_id, 
        ],
        outputs=[
            selected_downloaded_version_id,            
        ]
    )    

    selected_downloaded_model_id.change(
        fn=civitai_manager_action.on_selected_downloaded_model_id_change,   
        inputs=[
            selected_downloaded_model_id,
        ],
        outputs=[
            selected_downloaded_version_id,
            downloaded_civitai_model_url_txt,
            downloaded_model_type, 
            downloaded_versions_list,
        ] 
    )
    
    selected_downloaded_version_id.change(
        fn=civitai_manager_action.on_selected_downloaded_version_id_change,
        inputs=[
            selected_downloaded_version_id,
        ],
        outputs=[
            downloaded_description_html,
            downloaded_trigger_words,
            downloaded_filename_list,
            downloaded_model_title_name,                                    
            downloaded_version_gallery,
            downloaded_img_file_info      
        ]
    )
    
    downloaded_description_html.change(
        fn=civitai_manager_action.on_downloaded_description_html_change,
        inputs=[
            selected_downloaded_version_id
        ],
        outputs=[
            downloaded_version_gallery, 
            downloaded_version_images_url
        ]
    )
    

    goto_civitai_model_tab.click(
        fn=on_goto_civitai_model_tab_click,
        inputs=[
            selected_downloaded_model_id
        ],        
        outputs=[
            civitai_tab,
            selected_model_id
        ],        
    )
        
    downloaded_version_gallery.select(civitai_manager_action.on_gallery_select, downloaded_version_images_url, [downloaded_img_index, downloaded_hidden])
    downloaded_hidden.change(fn=modules.extras.run_pnginfo, inputs=[downloaded_hidden], outputs=[downloaded_info1, downloaded_img_file_info, downloaded_info2])
    # # download model information end
    
    civitai_model_url_txt.change(civitai_manager_action.on_civitai_model_url_txt_change,None,[civitai_internet_url])
    
    # shortcut delete
    shortcut_del_btn.click(
        fn=civitai_manager_action.on_shortcut_del_btn_click,
        inputs=[
            selected_model_id,
            shortcut_type,
            show_only_downloaded_sc,
            shortcut_downloaded_type
        ],
        outputs=[
            sc_gallery,
            sc_downloaded_gallery,
        ]                
    )

    # shortcut tab
    civitai_internet_url.upload(
        fn=civitai_manager_action.on_civitai_internet_url_upload,
        inputs=[
            civitai_internet_url,
            shortcut_type,
            show_only_downloaded_sc,
            shortcut_downloaded_type            
        ],
        outputs=[
            sc_gallery,
            sc_downloaded_gallery,
            selected_model_id,
        ]
    )  
        
    scan_sc_btn.click(
        fn=civitai_manager_action.on_scan_to_shortcut_click,
        inputs=[
            shortcut_type,
            show_only_downloaded_sc,
            shortcut_downloaded_type
        ],
        outputs=[
            sc_gallery,
            sc_downloaded_gallery
        ]                
    )
    
    update_sc_btn.click(
        fn=civitai_manager_action.on_shortcut_thumbnail_update_click,
        inputs=[
            shortcut_type,
            show_only_downloaded_sc,
            shortcut_downloaded_type,
        ],
        outputs=[
            sc_gallery,
            sc_downloaded_gallery
        ]
    )    
    # shortcut tab
    
    # total gallery tab
    shortcut_type.change(
        fn=civitai_manager_action.on_shortcut_gallery_refresh,
        inputs=[
            shortcut_type,
            show_only_downloaded_sc,
        ],
        outputs=[
            sc_gallery,
        ]
    )  

    show_only_downloaded_sc.change(
        fn=civitai_manager_action.on_shortcut_gallery_refresh,
        inputs=[
            shortcut_type,
            show_only_downloaded_sc,
        ],
        outputs=[
            sc_gallery,
        ]
    ) 
                    
    refresh_sc_btn.click(
        fn=civitai_manager_action.on_shortcut_gallery_refresh,
        inputs=[
            shortcut_type,
            show_only_downloaded_sc,
        ],
        outputs=[
            sc_gallery
        ]
    )    
        
    sc_gallery.select(civitai_manager_action.on_sc_gallery_select,None,selected_model_id)
    # total gallery tab

    # downloaded gallery tab start
    shortcut_downloaded_type.change(
        fn=civitai_manager_action.on_shortcut_gallery_refresh,
        inputs=[
            shortcut_downloaded_type,
        ],
        outputs=[
            sc_downloaded_gallery,
        ]
    )   
    
    refresh_downloaded_sc_btn.click(civitai_manager_action.on_shortcut_gallery_refresh,[shortcut_downloaded_type],[sc_downloaded_gallery])
    sc_downloaded_gallery.select(civitai_manager_action.on_sc_gallery_select,None,selected_downloaded_model_id)
    # downloaded gallery tab end
    
def init_civitai_manager():
   
    setting.root_path = os.getcwd()
    
    if shared.cmd_opts.embeddings_dir:
        setting.folders_dict["TextualInversion"] = shared.cmd_opts.embeddings_dir

    if shared.cmd_opts.hypernetwork_dir :
        setting.folders_dict["Hypernetwork"] = shared.cmd_opts.hypernetwork_dir

    if shared.cmd_opts.ckpt_dir:
        setting.folders_dict["Checkpoint"] = shared.cmd_opts.ckpt_dir

    if shared.cmd_opts.lora_dir:
        setting.folders_dict["LORA"] = shared.cmd_opts.lora_dir
        setting.folders_dict["LoCon"] = shared.cmd_opts.lora_dir
    
    setting.civitai_shortcut = os.path.join(scripts.basedir(),"CivitaiShortCut.json")
    setting.civitai_shortcut_thumnail_folder = os.path.join(scripts.basedir(),"sc_thumb_images")
    setting.civitai_shortcut_save_folder = os.path.join(scripts.basedir(),"sc_saves")
    
    # 소유한 모델을 스캔하여 저장한다.
    model.Load_Downloaded_Models()
               
# init
init_civitai_manager()
        
def on_ui_tabs():
    with gr.Blocks() as civitai_manager:
    	civitai_manager_ui()
    
    return (civitai_manager, "Civitai", "civitai_manager"),


script_callbacks.on_ui_tabs(on_ui_tabs)
