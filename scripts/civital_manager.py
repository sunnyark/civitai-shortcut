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

def civitai_manager_ui():                 
    with gr.Row(): 
        with gr.Column(scale=1):
            with gr.Tabs(): 
                with gr.TabItem("Shortcut"):
                    with gr.Row():
                        civitai_internet_url = gr.File(label="Civitai Internet Shortcut", file_count="multiple", file_types=[".url"])
                    with gr.Row():                        
                        scan_sc_btn = gr.Button(value="Scan Models to Shortcut",variant="primary")    
                with gr.TabItem("Browsing Shortcut"):    
                    with gr.Row():
                        shortcut_type = gr.Dropdown(label='Filter Model type', multiselect=True, choices=[k for k in setting.content_types_dict], interactive=True)         
                    with gr.Row():
                        sc_gallery = gr.Gallery(show_label=False, value=ishortcut.get_image_list()).style(grid=1)
                    with gr.Row():
                        refresh_sc_btn = gr.Button(value="Refressh Shortcut",variant="primary")                        
                    with gr.Row():
                        update_sc_btn = gr.Button(value="Update Thumnails",variant="primary")
                with gr.TabItem("Browsing Owned"):
                    with gr.Row():
                        shortcut_owned_type = gr.Dropdown(label='Filter Model type', multiselect=True, choices=[k for k in setting.content_types_dict], interactive=True)         
                    with gr.Row():
                        sc_owned_gallery = gr.Gallery(show_label=False, value=ishortcut.get_owned_image_list()).style(grid=1)
        with gr.Column(scale=4):
            with gr.Tab("Civitai Model Infomation"):
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

                        with gr.Row(visible=False) as owned_tab: 
                            with gr.Tabs(visible=True) as owtabs:
                                with gr.TabItem("Owned Version"):
                                    with gr.Row():                            
                                        owned_info = gr.Textbox(interactive=False,show_label=False)
                            
                            
                            
                        # with gr.Row():
                        #     with gr.Tabs():                                
                        #         with gr.TabItem("Tese"):
                        #             pass
                        #         with gr.TabItem("Tese"):
                        #             pass
                        #         with gr.TabItem("Tese"):
                        #             pass
                            
                            
                        # with gr.Row():
                        #     with gr.Tab("Download"):                                 

                        with gr.Row():
                            filename_list = gr.CheckboxGroup (label="Model Version File", info="Select the files you want to download", choices=[], value=[], interactive=True)
                        with gr.Row():
                            an_lora = gr.Checkbox(label="LoRA to additional-networks", value=False)          
                        with gr.Row():
                            vs_folder = gr.Checkbox(label="Create version specific folder", value=True)                                                                  
                        with gr.Row():
                            download_model = gr.Button(value="Download", variant="primary")                                                
                        with gr.Row():
                            download_images = gr.Button(value="Download Images",variant="primary")      
                            
                                                    
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
                            version_description_html = gr.HTML()                                                                                                   
                    with gr.Column(scale=1):
                        with gr.Row():                            
                            img_file_info = gr.Textbox(label="Generate Info", interactive=False, lines=6)                            
                        with gr.Row():
                            try:
                                send_to_buttons = modules.generation_parameters_copypaste.create_buttons(["txt2img", "img2img", "inpaint", "extras"])
                            except:
                                pass   
            with gr.Tab("Downloaded Model Information"):
                pass
    with gr.Row(visible=False):                                         
                
        
        #civitai model select model
        selected_version_id = gr.Textbox()
        selected_model_id = gr.Textbox()
        selected_gallery = gr.Textbox()
        
        #civitai model information                
        img_index = gr.Number(show_label=False)
        version_images_url = gr.State()
        hidden = gr.Image(type="pil")
        info1 = gr.Textbox()
        info2 = gr.Textbox()        



        #download model informaton ui
        owned_versions_list = gr.Dropdown(label="Model Version", choices=[setting.NORESULT], interactive=True, value=setting.NORESULT)
        owned_model_type = gr.Textbox(label="Model Type", value="", interactive=False, lines=1)                                                     
        owned_trigger_words = gr.Textbox(label="Trigger Words", value="", interactive=False, lines=1).style(container="True")         
        owned_civitai_model_url_txt = gr.Textbox(label="Model Url", interactive=False , max_lines=1)
        owned_filename_list = gr.CheckboxGroup (label="Model Version File", info="Select the files you want to download", choices=[], value=[], interactive=True)
                                            
        owned_img_file_info = gr.Textbox(label="Generate Info", interactive=False, lines=6)
        owned_version_description_html = gr.HTML()
        owned_model_title_name = gr.Markdown("###", visible=True)            
        owned_version_gallery = gr.Gallery(show_label=False).style(grid=4)

        #download model select model
        owned_selected_version_id = gr.Textbox()
        owned_selected_model_id = gr.Textbox()
        owned_selected_gallery = gr.Textbox()
        
        #download model information                
        owned_img_index = gr.Number(show_label=False)
        owned_version_images_url = gr.State()
        owned_hidden = gr.Image(type="pil")
        owned_info1 = gr.Textbox()
        owned_info2 = gr.Textbox()  
                        
    try:
        modules.generation_parameters_copypaste.bind_buttons(send_to_buttons, hidden, img_file_info)
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
        ],
        outputs=[message_log]
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
        inputs=selected_model_id,
        outputs=[civitai_model_url_txt, owned_tab, owned_info, an_lora, model_type, versions_list] 
    )
  
    selected_version_id.change(
        fn=civitai_manager_action.on_selected_version_id_change,
        inputs=[
            selected_version_id,
        ],
        outputs=[
            version_description_html,
            trigger_words,
            filename_list,
            model_title_name,                        
            selected_gallery,
            version_gallery,
            img_file_info      
        ]
    )
        
    selected_gallery.change(
        fn=civitai_manager_action.on_selected_gallery_change,
        inputs=[selected_gallery],
        outputs=[version_gallery, version_images_url]
    )

    version_gallery.select(civitai_manager_action.on_gallery_select, version_images_url, [img_index, hidden])    
    hidden.change(fn=modules.extras.run_pnginfo, inputs=[hidden], outputs=[info1, img_file_info, info2])      
    # civitai model information
    
    
    # # download model information
    # # 버전을 하나 선택
    # # 동일 이벤트에 여러개 연결하면 많이 늦어지는듯함..  따로 만듧시다.
    # owned_versions_list.select(
    #     fn=civitai_manager_action.on_owned_versions_list_select,
    #     inputs=[
    #         owned_selected_model_id, 
    #     ],
    #     outputs=[
    #         owned_selected_version_id,            
    #     ]
    # )    

    # owned_selected_model_id.change(
    #     fn=civitai_manager_action.on_selected_owned_model_id_change,   
    #     inputs=owned_selected_model_id,
    #     outputs=None,
    #     # outputs=[
    #     #     owned_civitai_model_url_txt
    #     #     owned_model_type, 
    #     #     owned_versions_list
    #     # ] 
    # )
    
    # owned_selected_version_id.change(
    #     fn=civitai_manager_action.on_selected_owned_version_id_change,
    #     inputs=[
    #         owned_selected_version_id,
    #     ],
    #     outputs=None,
    #     # outputs=[
    #     #     owned_version_description_html,
    #     #     owned_trigger_words,
    #     #     owned_filename_list,
    #     #     owned_model_title_name,                        
    #     #     owned_selected_gallery,
    #     #     owned_version_gallery,
    #     #     owned_img_file_info      
    #     # ]
    # )
    
    # owned_selected_gallery.change(
    #     fn=civitai_manager_action.on_selected_owned_gallery_change,
    #     inputs=[
    #         owned_selected_gallery
    #     ],
    #     outputs=None,
    #     # outputs=[
    #     #     owned_version_gallery, 
    #     #     owned_version_images_url
    #     # ]
    # )
    
    # owned_version_gallery.select(civitai_manager_action.on_owned_gallery_select, owned_version_images_url, [owned_img_index, owned_hidden])
    # owned_hidden.change(fn=modules.extras.run_pnginfo, inputs=[owned_hidden], outputs=[owned_info1, owned_img_file_info, owned_info2])
    # # download model information
                
    
    
    civitai_model_url_txt.change(civitai_manager_action.on_civitai_model_url_txt_change,None,[civitai_internet_url])
    
    # shortcut delete
    shortcut_del_btn.click(
        fn=civitai_manager_action.on_shortcut_del_btn_click,
        inputs=[
            selected_model_id,
            shortcut_type,
            shortcut_owned_type
        ],
        outputs=[
            sc_gallery,
            sc_owned_gallery,
        ]                
    )

    # shortcut tab
    civitai_internet_url.upload(
        fn=civitai_manager_action.on_civitai_internet_url_upload,
        inputs=[
            civitai_internet_url,
            shortcut_type,
            shortcut_owned_type            
        ],
        outputs=[
            sc_gallery,
            sc_owned_gallery,
            selected_version_id, 
            selected_model_id,            
            owned_selected_version_id,
            owned_selected_model_id,
        ]
    )  
        
    scan_sc_btn.click(
        fn=civitai_manager_action.on_scan_to_shortcut_click,
        inputs=[
            shortcut_type,
            shortcut_owned_type
        ],
        outputs=[
            sc_gallery,
            sc_owned_gallery
        ]                
    )
    # shortcut tab
    
    # total gallery tab
    shortcut_type.change(
        fn=civitai_manager_action.on_shortcut_type_change,
        inputs=[
            shortcut_type,
        ],
        outputs=[
            sc_gallery,
        ]
    )  

    sc_gallery.select(
        fn=civitai_manager_action.on_sc_gallery_select,
        inputs=None,
        outputs=[
            selected_version_id, 
            selected_model_id,            
            owned_selected_version_id, 
            owned_selected_model_id,                                   
        ]
    )

    update_sc_btn.click(
        fn=civitai_manager_action.on_shortcut_thumnail_update_click,
        inputs=[
            shortcut_type,
            shortcut_owned_type,
        ],
        outputs=[
            sc_gallery,
            sc_owned_gallery
        ]
    )
            
    refresh_sc_btn.click(civitai_manager_action.on_refresh_sc_btn_click,[shortcut_type,shortcut_owned_type],[sc_gallery,sc_owned_gallery])
    # total gallery tab

    # owned gallery tab
    # 여러군데에 갱신하는 부분을 넣어줘야 한다.
    # sc_gallery 가 참조되는 부분을 보자
    shortcut_owned_type.change(
        fn=civitai_manager_action.on_shortcut_owned_type_change,
        inputs=[
            shortcut_owned_type,
        ],
        outputs=[
            sc_owned_gallery,
        ]
    )   
    
    sc_owned_gallery.select(
        #같이씀
        fn=civitai_manager_action.on_sc_gallery_select,
        inputs=None,
        outputs=[
            selected_version_id, 
            selected_model_id,   
            owned_selected_version_id, 
            owned_selected_model_id,                       
        ]
    )
    # owned gallery tab
    
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
    setting.civitai_shortcut_thumnail_folder = os.path.join(scripts.basedir(),"sc_thum_images")
    setting.civitai_shortcut_save_folder = os.path.join(scripts.basedir(),"sc_saves")
    
    # 소유한 모델을 스캔하여 저장한다.
    model.Load_Owned_Models()
               
# init
init_civitai_manager()
        
def on_ui_tabs():
    with gr.Blocks() as civitai_manager:
    	civitai_manager_ui()
    
    return (civitai_manager, "Civitai", "civitai_manager"),


script_callbacks.on_ui_tabs(on_ui_tabs)
