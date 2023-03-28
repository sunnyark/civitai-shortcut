import gradio as gr
import modules.extras
from modules import script_callbacks
from scripts.civitai_manager_libs import civitai
from scripts.civitai_manager_libs import setting
from scripts.civitai_manager_libs import civitai_manager_action
from scripts.civitai_manager_libs import util
from scripts.civitai_manager_libs import ishortcut

def civitai_manager_ui():
    # with gr.Row():    
    #     with gr.Column(scale=1):        
    #         gr.Markdown("###")       
    #     with gr.Column(scale=5):                
    #         with gr.Row():         
    #             with gr.Column(scale=1):
    #                 gr.Markdown("###")                                      
    #             with gr.Column(scale=4):                       
    #                 civitai_model_url_txt = gr.Textbox(label="Model Url", show_label=False , placeholder="Enter your civitai url or model id", max_lines=1)
    #             with gr.Column(scale=1):                    
    #                 civitai_model_info_btn = gr.Button(value="Get Model Info",variant="primary")                                       
    with gr.Row(): 
        with gr.Column(scale=1):            
            with gr.Tab("Civitai Shortcut"):                           
                with gr.Column():
                    with gr.Row():
                        civitai_model_url_txt = gr.Textbox(label="Model Url", show_label=False , placeholder="Enter your civitai url or model id", max_lines=1)
                    with gr.Row():
                        civitai_model_info_btn = gr.Button(value="Get Model Info",variant="primary")    
                    with gr.Row():
                        civitai_internet_url = gr.File(label="Civitai Internet Shortcut")
                    with gr.Row():
                        shortcut_list = gr.Dropdown(label="Civitai Shortcut List", choices=[setting.PLACEHOLDER] + get_Internet_Shortcut_list(), interactive=True, value=setting.PLACEHOLDER)   
                    with gr.Row():
                        shortcut_del_btn = gr.Button(value="Delete Civitai Shortcut") 
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
                            filename_list = gr.CheckboxGroup (label="Model Version File", info="Select the files you want to download", choices=[], value=[], interactive=True)
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
        


    civitai_internet_url.upload(
        fn=civitai_internet_url_upload,
        inputs=[
            civitai_internet_url
        ],
        outputs=[
            civitai_model_url_txt,
            shortcut_list,
            versions_list,
            selected_version_id, 
            selected_model_id,            
        ]
    )                  
         
    civitai_model_url_txt.change(civitai_model_url_txt_change,None,[civitai_internet_url])
    
    shortcut_list.select(shortcut_list_select,shortcut_list,[civitai_model_url_txt])        
    
    shortcut_del_btn.click(shortcut_del_btn_click,shortcut_list,shortcut_list)


def shortcut_del_btn_click(shortcut):
    if shortcut and shortcut != setting.PLACEHOLDER:
        model_id = shortcut[0:shortcut.find(':')]
        util.printD(f"{model_id} {len(model_id)}")    
        if model_id:
            ISC = ishortcut.load()                           
            ISC = ishortcut.delete(ISC, model_id)                        
            ishortcut.save(ISC)
        
    return gr.Dropdown.update(choices=[setting.PLACEHOLDER] + get_Internet_Shortcut_list(), value=setting.PLACEHOLDER)

def civitai_model_url_txt_change():
    return None 
        
def shortcut_list_select(shortcut):
    url = ""
    
    if shortcut and shortcut != setting.PLACEHOLDER:
        model_id = shortcut[0:shortcut.find(':')]
        #util.printD(f"{model_id} {len(model_id)}")    
        url = civitai.Url_ModelId() + model_id    
        
    return url   
    
def civitai_internet_url_upload(file_obj):
    if not file_obj:
        return ""
    
    shortcut = util.load_InternetShortcut(file_obj.name)
    if shortcut:        
        model_id = util.get_model_id_from_url(shortcut) 
        if model_id:
            model_info = civitai.get_model_info_by_model_id(model_id)
            if model_info:
                model_image = ""
                def_id = ""
                def_name = ""
                versions_list = []
                model_url = civitai.Url_ModelId() + model_id
                
                if "modelVersions" in model_info.keys():            
                    def_version = model_info["modelVersions"][0]
                    def_id = def_version['id']
                    def_name = def_version['name']
                            
                    if 'images' in def_version.keys():
                        img_dict = def_version["images"][0]
                        model_image = img_dict["url"]
                        
                    for version_info in model_info['modelVersions']:
                        versions_list.append(version_info['name'])                        
        
                #util.printD(f"{model_info['id']} {model_info['name']} {model_info['type']} {civitai.Url_ModelId()}{model_id}")
                
                ISC = ishortcut.load()                           
                ISC = ishortcut.add(ISC, model_info['id'] ,model_info['name'], model_info['type'], model_url, def_id , model_image)                        
                ishortcut.save(ISC)
            
                #util.printD(ISC)    
                
                return shortcut,gr.Dropdown.update(choices=[setting.PLACEHOLDER] + get_Internet_Shortcut_list(), value=setting.PLACEHOLDER),gr.Dropdown.update(choices=[v for v in versions_list], value=def_name),gr.Textbox.update(value=def_id),gr.Textbox.update(value=model_id)
            
            return shortcut,gr.Dropdown.update(choices=[setting.PLACEHOLDER] + get_Internet_Shortcut_list(), value=setting.PLACEHOLDER),gr.Dropdown.update(choices=[setting.NORESULT], value=setting.NORESULT),gr.Textbox.update(value=""),gr.Textbox.update(value="")
        
    return "",gr.Dropdown.update(choices=[setting.PLACEHOLDER] + get_Internet_Shortcut_list(), value=setting.PLACEHOLDER),gr.Dropdown.update(choices=[setting.NORESULT], value=setting.NORESULT),gr.Textbox.update(value=""),gr.Textbox.update(value="")
            
            
def get_Internet_Shortcut_list()->str:
    
    ISC = ishortcut.load()                           
    if not ISC:
        return
    if "IShortCut" not in ISC.keys():
        return    
    
    shotcutlist = []
    for k, v in ISC["IShortCut"].items():
        # util.printD(ISC["IShortCut"][k])
        if v:
            shotcutlist.append(f"{v['id']}:{v['name']}")
                    
    return [v for v in shotcutlist]

# init
setting.init_civitai_manager()
    
def on_ui_tabs():
    with gr.Blocks() as civitai_manager:
    	civitai_manager_ui()
    
    return (civitai_manager, "Civitai", "civitai_manager"),


script_callbacks.on_ui_tabs(on_ui_tabs)
