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
            with gr.Tab("Shortcut and Search"):                           
                with gr.Column():
                    with gr.Row():
                        civitai_internet_url = gr.File(label="Civitai Internet Shortcut", file_count="multiple", file_types=[".url"])
                    with gr.Row():                        
                        scan_sc_btn = gr.Button(value="Scan Models to Shortcut",variant="primary")    
            with gr.Tab("Browsing Shortcut"):        
                    with gr.Row():
                        shortcut_type = gr.Dropdown(label='Filter Model type', multiselect=True, choices=[k for k in setting.content_types_dict], interactive=True)         
                    with gr.Row():
                        sc_gallery = gr.Gallery(show_label=False, value=ishortcut.get_image_list()).style(grid=1)
                    with gr.Row():                        
                        refresh_sc_btn = gr.Button(value="Refressh Shortcut",variant="primary")                        
                    with gr.Row():                        
                        update_sc_btn = gr.Button(value="Update Thumnails",variant="primary")
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
    with gr.Row(visible=False):                                         
        img_index = gr.Number(show_label=False)
        version_images_url = gr.State()
        hidden = gr.Image(type="pil")
        info1 = gr.Textbox()
        info2 = gr.Textbox()        
        selected_version_id = gr.Textbox()
        selected_model_id = gr.Textbox()
        selected_gallery = gr.Textbox()
                                                                             
    hidden.change(fn=modules.extras.run_pnginfo, inputs=[hidden], outputs=[info1, img_file_info, info2])      

    try:
        modules.generation_parameters_copypaste.bind_buttons(send_to_buttons, hidden, img_file_info)
    except:
        pass
                          
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
            vs_folder,
        ],
        outputs=[message_log]
    )
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
        fn=civitai_manager_action.on_scan_to_shortcut_click,
        inputs=[
            shortcut_type,
        ],
        outputs=[
            sc_gallery,
        ]                
    )
    
    refresh_sc_btn.click(civitai_manager_action.on_refresh_sc_btn_click,shortcut_type,sc_gallery)

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
    
    # 소유한 모델 데이터를 저장한다.
    model.Load_Owned_ModelInfo()
               
# init
init_civitai_manager()
        
def on_ui_tabs():
    with gr.Blocks() as civitai_manager:
    	civitai_manager_ui()
    
    return (civitai_manager, "Civitai", "civitai_manager"),


script_callbacks.on_ui_tabs(on_ui_tabs)
