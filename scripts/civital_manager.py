import gradio as gr
import modules.extras
from modules.shared import opts
from modules import script_callbacks
from scripts.civitai_manager_libs import setting
from scripts.civitai_manager_libs import civitai_manager_action
from scripts.civitai_manager_libs import ishortcut
from scripts.civitai_manager_libs import civitai
from scripts.civitai_manager_libs import civitai_action
from scripts.civitai_manager_libs import util

def on_scan_to_shortcut_click(sc_types):
    ishortcut.OwnedModel_to_Shortcut()
    util.printD("Scan & Update Shortcut ended")
    return gr.Gallery.update(value=ishortcut.get_image_list(sc_types))

import threading

def scan_owned_to_shortcut_thread():               
    
    thread = threading.Thread(target=ishortcut.OwnedModel_to_Shortcut(),args=None)                        
    # Start the thread
    thread.start()                
    
    return f"Scan started"
        
def civitai_manager_ui():                             
    with gr.Row(): 
        with gr.Column(scale=1):            
            with gr.Tab("Shortcut and Search"):                           
                with gr.Column():
                    with gr.Row():
                        civitai_internet_url = gr.File(label="Civitai Internet Shortcut")
                    # with gr.Row():
                    #     shortcut_type = gr.Dropdown(label='Filter Model type', multiselect=True, choices=[k for k in setting.content_types_dict], interactive=True)         
                    # with gr.Row():
                    #     shortcut_list = gr.Dropdown(label="Civitai Shortcut List", choices=[setting.PLACEHOLDER] + ishortcut.get_list(), interactive=True, value=setting.PLACEHOLDER)   
                    with gr.Tab("Search"):                
                        with gr.Row():
                            content_type = gr.Dropdown(label='Model type', multiselect=True, choices=[k for k in setting.content_types_dict], value=[], type="value") 
                        with gr.Row():                                                           
                            sort_type = gr.Dropdown(label='Sort List by', choices=["Newest", "Most Downloaded", "Highest Rated", "Most Liked"], value="Newest", type="value")                        
                        with gr.Row():                        
                            search_term = gr.Textbox(label="Search Term", placeholder="Enter your prompt", max_lines=1)
                        with gr.Row():                        
                            search_btn = gr.Button(value=setting.page_action_dict['search'],variant="primary")
                        with gr.Row():  
                            prev_page_btn = gr.Button(value=setting.page_action_dict['prevPage'])                              
                            next_page_btn = gr.Button(value=setting.page_action_dict['nextPage']) 
                        with gr.Row():                    
                            models_list = gr.Dropdown(label="Model List", choices=[setting.NORESULT], interactive=True, value=setting.NORESULT)   
                        with gr.Row():       
                            show_nsfw = gr.Checkbox(label="Show NSFW", value=True)  
            with gr.Tab("Browsing Shortcut"):   
                    with gr.Row():
                        shortcut_type = gr.Dropdown(label='Filter Model type', multiselect=True, choices=[k for k in setting.content_types_dict], interactive=True)         
                    with gr.Row():
                        sc_gallery = gr.Gallery(show_label=False, value=ishortcut.get_image_list()).style(grid=1)
                    with gr.Row():                        
                        update_sc_btn = gr.Button(value="Update Thumnails",variant="primary")
                    with gr.Row():                        
                        scan_sc_btn = gr.Button(value="Scan & Update Shortcut",variant="primary")
        with gr.Column(scale=4):                                                          
            with gr.Tab("Model Info"):
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
                        with gr.Row():
                            filename_list = gr.CheckboxGroup (label="Model Version File", info="Select the files you want to download", choices=[], value=[], interactive=True)
                        with gr.Row():                            
                            an_lora = gr.Checkbox(label="LoRA to additional-networks", value=False)                                 
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
    with gr.Row(visible=False):                                         
        img_index = gr.Number(show_label=False)
        version_images_url = gr.State()
        hidden = gr.Image(type="pil")
        info1 = gr.Textbox()
        info2 = gr.Textbox()        
        selected_version_id = gr.Textbox()
        selected_model_id = gr.Textbox()
        selected_gallery = gr.Textbox()
        
        up_shortcut = gr.Textbox()
        
        # 검색한 모델들의 정보와 선택한 모델정보를 저장하는 변수
        # 페이지가 새로고침 되기전까지 정보를 저장한다.
        json_state  = gr.State()  #검색한 모델들의 정보
        #model_state  = gr.State() #선택한 모델정보
                                                                             
    hidden.change(fn=modules.extras.run_pnginfo, inputs=[hidden], outputs=[info1, img_file_info, info2])      

    try:
        modules.generation_parameters_copypaste.bind_buttons(send_to_buttons, hidden, img_file_info)
    except:
        pass

    show_nsfw.change(
        fn=civitai_manager_action.on_page_btn_click,
        inputs=[  
            show_nsfw,              
            json_state,
            content_type,
            sort_type,
            search_term,
            show_nsfw,            
        ],
        outputs=[
            json_state,
            models_list,
        ]
    )                      
    search_btn.click(
        fn=civitai_manager_action.on_page_btn_click,
        inputs=[  
            search_btn,              
            json_state,
            content_type,
            sort_type,
            search_term,
            show_nsfw,            
        ],
        outputs=[
            json_state,
            models_list,
        ]
    )
    next_page_btn.click(
        fn=civitai_manager_action.on_page_btn_click,
        inputs=[
            next_page_btn,
            json_state,
            content_type,
            sort_type,
            search_term,
            show_nsfw,      
        ],
        outputs=[
            json_state,            
            models_list,
        ]
    )
    prev_page_btn.click(
        fn=civitai_manager_action.on_page_btn_click,
        inputs=[
            prev_page_btn,
            json_state,
            content_type,
            sort_type,
            search_term,
            show_nsfw,      
        ],
        outputs=[
            json_state,            
            models_list,
        ]
    )     

    models_list.select(
        fn=civitai_manager_action.on_models_list_select,
        inputs=[
            json_state,            
        ],
        outputs=[
            civitai_model_url_txt,
            versions_list,
            selected_version_id, 
            selected_model_id,                                     
        ]
    )
                          
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
       
    # 다운로드
    download_images.click(
        fn=civitai_manager_action.on_download_images_click,
        inputs=[
            selected_version_id,
            an_lora,
        ],
        outputs=[message_log]
    )
    download_model.click(
        fn=civitai_manager_action.on_download_model_click,
        inputs=[
            selected_version_id,
            filename_list,            
            an_lora,            
        ],
        outputs=[message_log]
    )     

    selected_version_id.change(
        fn=civitai_manager_action.on_selected_version_id_change,
        inputs=[
            selected_version_id,
            selected_model_id, 
        ],
        outputs=[
            version_description_html,
            trigger_words,
            filename_list,
            model_title_name,            
            model_type,      
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
        
    version_gallery.select(civitai_manager_action.on_get_gallery_select, version_images_url, [img_index, hidden])
    
    civitai_model_url_txt.change(civitai_manager_action.on_civitai_model_url_txt_change,None,[civitai_internet_url])

    # shortcut_list.select(
    #     fn=civitai_manager_action.on_shortcut_list_select,
    #     inputs=[
    #         shortcut_list
    #     ],
    #     outputs=[
    #         civitai_model_url_txt,
    #         versions_list,
    #         selected_version_id, 
    #         selected_model_id,            
    #     ]
    # )  
                
    # civitai_internet_url.upload(
    #     fn=civitai_manager_action.on_civitai_internet_url_upload,
    #     inputs=[
    #         civitai_internet_url,
    #         shortcut_type            
    #     ],
    #     outputs=[
    #         civitai_model_url_txt,
    #         shortcut_list,
    #         versions_list,
    #         selected_version_id, 
    #         selected_model_id,            
    #     ]
    # )                                  
    
    # shortcut_del_btn.click(
    #     fn=civitai_manager_action.on_shortcut_del_btn_click,
    #     inputs=[
    #         shortcut_list,
    #         shortcut_type,
    #     ],
    #     outputs=[
    #         shortcut_list,            
    #     ]                
    # )

    # shortcut_type.change(
    #     fn=civitai_manager_action.on_shortcut_type_change,
    #     inputs=[
    #         shortcut_type,
    #     ],
    #     outputs=[
    #         shortcut_list,
    #     ]
    # )
    
    #sc_gallery,shortcut_list를 갱신 시켜야 되는 3가지 이벤트 civitai_internet_url,shortcut_del_btn,shortcut_type
    sc_gallery.select(
        fn=civitai_manager_action.on_get_sc_galery_select,
        inputs=None,
        outputs=[
            civitai_model_url_txt,
            versions_list,
            selected_version_id, 
            selected_model_id,            
        ]
    )
    civitai_internet_url.upload(
        fn=civitai_manager_action.on_civitai_internet_url_upload,
        inputs=[
            civitai_internet_url,
            shortcut_type            
        ],
        outputs=[
            civitai_model_url_txt,
            sc_gallery,
            versions_list,
            selected_version_id, 
            selected_model_id,            
        ]
    )                                  
    
    shortcut_del_btn.click(
        fn=civitai_manager_action.on_shortcut_del_btn_click,
        inputs=[
            selected_model_id,
            shortcut_type,
        ],
        outputs=[
            sc_gallery,
        ]                
    )

    shortcut_type.change(
        fn=civitai_manager_action.on_shortcut_type_change,
        inputs=[
            shortcut_type,
        ],
        outputs=[
            sc_gallery,
        ]
    )    
        
    update_sc_btn.click(
        fn=civitai_manager_action.on_shortcut_thumnail_update_click,
        inputs=[
            shortcut_type,
        ],
        outputs=[
            sc_gallery,
        ]
    )
    
    scan_sc_btn.click(
        fn=on_scan_to_shortcut_click,
        inputs=[
            shortcut_type,
        ],
        outputs=[
            sc_gallery,
        ]                
    )
    

            
# init
setting.init_civitai_manager()
    
def on_ui_tabs():
    with gr.Blocks() as civitai_manager:
    	civitai_manager_ui()
    
    return (civitai_manager, "Civitai", "civitai_manager"),


script_callbacks.on_ui_tabs(on_ui_tabs)
