import gradio as gr
import modules.extras
from modules import script_callbacks
from scripts.civitai_manager_libs import civitai
from scripts.civitai_manager_libs import setting
from scripts.civitai_manager_libs import civitai_manager_action

def civitai_manager_ui():
    with gr.Row():    
        with gr.Column(scale=1):        
            gr.Markdown("###")       
        with gr.Column(scale=5):                
            with gr.Row():         
                with gr.Column(scale=1):
                    gr.Markdown("###")  
                with gr.Column(scale=4):                    
                    civitai_model_url_txt = gr.Textbox(label="Model Url", show_label=False , placeholder="Enter your civitai url or model id", max_lines=1)
                with gr.Column(scale=1):                    
                    civitai_model_info_btn = gr.Button(value="Get Model Info",variant="primary")                                       
    with gr.Row(): 
        with gr.Column(scale=1):            
            with gr.Tab("Search"):  
                with gr.Column():                    
                    with gr.Row():
                        content_type = gr.Dropdown(label='Content type', choices=[k for k in civitai.content_types_dict], value="All", type="value")                                                        
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
        with gr.Column(scale=5):                                                    
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
                            filename_list = gr.CheckboxGroup (label="Model Version File", choices=[], value=[], interactive=True)                                                                            
                        with gr.Row():                            
                            an_lora = gr.Checkbox(label="LoRA to additional-networks", value=False)                                 
                        with gr.Row():
                            download_model = gr.Button(value="Download", variant="primary")                                                
                        with gr.Row():
                            download_images = gr.Button(value="Download Images",variant="primary")                            
                        with gr.Row():    
                            message_log = gr.Markdown("###")
                    with gr.Column(scale=4):                                                  
                        with gr.Row():                                                              
                            model_title_name = gr.Markdown("###", visible=True)            
                        with gr.Row():    
                            version_gallery = gr.Gallery(show_label=False).style(grid=[4])   
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
                   
    # model의 정보 표시
    civitai_model_info_btn.click(
        fn=civitai_manager_action.on_civitai_model_info_btn_click,
        inputs=[
            civitai_model_url_txt,
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
    
    # civitai_model_url_txt.select(civitai_manager_action.on_civitai_model_url_txt_select,None,[civitai_model_url_txt])
            
# init
setting.init_civitai_manager()
    
def on_ui_tabs():
    with gr.Blocks() as civitai_manager:
    	civitai_manager_ui()
    
    return (civitai_manager, "Civitai", "civitai_manager"),


script_callbacks.on_ui_tabs(on_ui_tabs)
