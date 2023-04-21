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


# def on_vs_folder_change(vs_folder):
#     return gr.update(visible=vs_folder)

def civitai_user_gallery_ui(selected_usergal_model_id:gr.Textbox):
        
    with gr.Column(scale=5):                                                   
        with gr.Row():                  
            with gr.Column(scale=1): 
                with gr.Row():
                    usergal_first_btn = gr.Button(value="First Page")
                    usergal_prev_btn = gr.Button(value="Prev Page")                                        
            with gr.Column(scale=1): 
                    usergal_page_slider = gr.Slider(minimum=1, maximum=1, value=1, step=1, label='Total Pages', interactive=True)
            with gr.Column(scale=1): 
                with gr.Row():
                    usergal_next_btn = gr.Button(value="Next Page")
                    usergal_end_btn = gr.Button(value="End Page")
        with gr.Row():
            with gr.Accordion("#", open=True) as usergal_title_name:
                usergal_gallery = gr.Gallery(label="Civitai User Gallery", show_label=False, elem_id="civitai_user_gallery").style(grid=[5],height="auto")
    with gr.Column(scale=1):
        with gr.Row():                            
            usergal_img_file_info = gr.Textbox(label="Generate Info", interactive=False, lines=6).style(container=True, show_copy_button=True)                            
        with gr.Row():
            try:
                usergal_send_to_buttons = modules.generation_parameters_copypaste.create_buttons(["txt2img", "img2img", "inpaint", "extras"])
            except:
                pass  
        
    with gr.Row(visible=False):                                                           
        # user gallery information  
        usergal_img_index = gr.Number(show_label=False)
        # 이미지 파일명 또는 URL 리스트였다가 이미지 리스트가됨 왔다갔다 함
        usergal_images = gr.State()
        # 트리거를 위한것
        usergal_gallery_url = gr.Textbox(value=None)
        usergal_hidden = gr.Image(type="pil")
        usergal_info1 = gr.Textbox()
        usergal_info2 = gr.Textbox()
        usergal_page = gr.State()
        usergal_page_url = gr.Textbox(value=None)

    try:
        modules.generation_parameters_copypaste.bind_buttons(usergal_send_to_buttons, usergal_hidden,usergal_img_file_info)
    except:
        pass            

    # civitai user gallery information start
    selected_usergal_model_id.change(
        fn=civitai_shortcut_action.on_load_usergal_model,
        inputs=[
            selected_usergal_model_id,            
        ],
        outputs=[            
            usergal_page_url    
        ] 
    )    
    
    usergal_first_btn.click(
        fn=civitai_shortcut_action.on_usergal_first_btn_click,
        inputs=[
            usergal_page_url,
            usergal_page
        ],
        outputs=[            
            usergal_page_url
        ]        
    )

    usergal_end_btn.click(
        fn=civitai_shortcut_action.on_usergal_end_btn_click,
        inputs=[
            usergal_page_url,
            usergal_page
        ],
        outputs=[            
            usergal_page_url
        ]        
    )

    usergal_prev_btn.click(
        fn=civitai_shortcut_action.on_usergal_prev_btn_click,
        inputs=[
            usergal_page_url,
            usergal_page
        ],
        outputs=[            
            usergal_page_url
        ]        
    )
    
    usergal_next_btn.click(
        fn=civitai_shortcut_action.on_usergal_next_btn_click,
        inputs=[
            usergal_page_url,
            usergal_page
        ],
        outputs=[            
            usergal_page_url
        ]        
    )

    usergal_page_slider.release(
        fn=civitai_shortcut_action.on_usergal_page_slider_release,
        inputs=[
            usergal_page_url,
            usergal_page_slider
        ],
        outputs=[            
            usergal_page_url
        ]        
    )
        
    usergal_gallery_url.change(
        fn=civitai_shortcut_action.on_civitai_gallery_loading,
        inputs=[
            usergal_images 
        ],
        outputs=[               
            usergal_gallery,
            usergal_images
        ]                  
    )
    
    usergal_page_url.change(
        fn=civitai_shortcut_action.on_usergal_page_url_change,
        inputs=[
            selected_usergal_model_id,
            usergal_page_url,            
            usergal_page
        ],
        outputs=[               
            usergal_title_name,                               
            usergal_gallery_url,
            usergal_images,
            usergal_page_slider,
            usergal_page,
            usergal_img_file_info   
        ]         
    )
        
    usergal_gallery.select(civitai_shortcut_action.on_gallery_select, usergal_images, [usergal_img_index, usergal_hidden])
    usergal_hidden.change(fn=modules.extras.run_pnginfo, inputs=[usergal_hidden], outputs=[usergal_info1, usergal_img_file_info, usergal_info2])
    
    # civitai user gallery information end
        
def saved_model_information_ui(selected_saved_version_id:gr.Textbox(),selected_saved_model_id:gr.Textbox(),refresh_sc_list:gr.Textbox()):

    with gr.Column(scale=1):
        with gr.Row():
            saved_versions_list = gr.Dropdown(label="Model Version", choices=[setting.NORESULT], interactive=True, value=setting.NORESULT)
        with gr.Row():
            saved_model_type = gr.Textbox(label="Model Type", value="", interactive=False, lines=1)
        with gr.Row():
            saved_trigger_words = gr.Textbox(label="Trigger Words", value="", interactive=False, lines=1).style(container=True, show_copy_button=True)
        with gr.Row():
            saved_civitai_model_url_txt = gr.Textbox(label="Model Url", value="", interactive=False , lines=1).style(container=True, show_copy_button=True)
            
        with gr.Row(visible=False) as saved_downloaded_tab:
            with gr.Accordion("Downloaded Version", open=False): 
                saved_downloaded_info = gr.Textbox(interactive=False,show_label=False)                

        with gr.Row():
            saved_filename_list = gr.Textbox(label="Model Version File", interactive=False)
        with gr.Row():
            saved_update_information_btn = gr.Button(value="Update Model Information")
        with gr.Row():
            shortcut_del_btn = gr.Button(value="Delete Shortcut")       
        with gr.Row():                          
            saved_openfolder = gr.Button(value="Open Download Folder",variant="primary", visible=False)               
            
    with gr.Column(scale=4):                                                  
        with gr.Row():  
            with gr.Accordion("#", open=True) as saved_model_title_name:   
                saved_gallery = gr.Gallery(label="Civitai Saved Gallery", show_label=False, elem_id="civitai_saved_gallery").style(grid=[setting.gallery_column],height="auto")
        with gr.Row():    
            with gr.Accordion("Model Description", open=True):  
                saved_description_html = gr.HTML()                                                                                                   
    with gr.Column(scale=1):
        with gr.Row():                            
            saved_img_file_info = gr.Textbox(label="Generate Info", interactive=False, lines=6).style(container=True, show_copy_button=True)
        with gr.Row():
            try:
                saved_send_to_buttons = modules.generation_parameters_copypaste.create_buttons(["txt2img", "img2img", "inpaint", "extras"])
            except:
                pass 

    with gr.Row(visible=False): 
        # saved shortcut information  
        saved_img_index = gr.Number(show_label=False)
        # 이미지 파일명리스트 - 파일은 굳이 일부러 로딩할필요가 없다.
        saved_images = gr.State()
        # 트리거를 위한것
        saved_gallery_url = gr.Textbox(value=None)
        saved_hidden = gr.Image(type="pil")
        saved_info1 = gr.Textbox()
        saved_info2 = gr.Textbox()

    try:
        modules.generation_parameters_copypaste.bind_buttons(saved_send_to_buttons, saved_hidden,saved_img_file_info)
    except:
        pass
    
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
            saved_gallery_url,
            saved_images,
            saved_img_file_info,
            saved_openfolder
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
            saved_gallery_url,
            saved_images,
            saved_img_file_info,
            saved_openfolder
        ]
    )    

    saved_gallery_url.change(
        fn=civitai_shortcut_action.on_file_gallery_loading,
        inputs=[
            saved_images 
        ],
        outputs=[               
            saved_gallery
        ]                  
    )

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
            saved_gallery
        ]
    )

    # selected_saved_model_id 값을 초기화 시키기 위한 이벤트 헨들러이다.
    # saved_update_information_btn.click 에 두개가 묶여 있지만 이것이 먼저 실행될것이다.
    saved_update_information_btn.click(lambda :gr.update(value=None),None,selected_saved_model_id)
    
    saved_gallery.select(civitai_shortcut_action.on_gallery_select, saved_images, [saved_img_index, saved_hidden])
    saved_hidden.change(fn=modules.extras.run_pnginfo, inputs=[saved_hidden], outputs=[saved_info1, saved_img_file_info, saved_info2])  
    
    saved_openfolder.click(civitai_shortcut_action.on_open_folder_click,[selected_saved_model_id,selected_saved_version_id],None)  
    # civitai saved model information end
        
def civitai_model_information_ui(selected_version_id:gr.Textbox(),selected_model_id:gr.Textbox(),refresh_sc_list:gr.Textbox()):
    
    with gr.Column(scale=1):
        with gr.Row():
            versions_list = gr.Dropdown(label="Model Version", choices=[setting.NORESULT], interactive=True, value=setting.NORESULT)
        with gr.Row():
            model_type = gr.Textbox(label="Model Type", value="", interactive=False, lines=1)
        with gr.Row():
            trigger_words = gr.Textbox(label="Trigger Words", value="", interactive=False, lines=1).style(container=True, show_copy_button=True)
        with gr.Row():
            civitai_model_url_txt = gr.Textbox(label="Model Url", value="", interactive=False , lines=1).style(container=True, show_copy_button=True)

        with gr.Row(visible=False) as downloaded_tab:
            with gr.Accordion("Downloaded Version", open=False):
                downloaded_info = gr.Textbox(interactive=False,show_label=False)                

        with gr.Accordion("Download", open=True):
            with gr.Row():
                filename_list = gr.CheckboxGroup (label="Model Version File", info="Select the files you want to download", choices=[], value=[], interactive=True)
            # with gr.Row():
            #     an_lora = gr.Checkbox(label="Download to additional-networks folder", value=False)          
            with gr.Row():
                vs_folder = gr.Checkbox(label="Create specific folders with the following", value=True)               
            with gr.Row():
                vs_folder_name = gr.Textbox(label="Folder name to create", value="", show_label=False, interactive=True, lines=1, visible=True).style(container=True)
                download_model = gr.Button(value="Download", variant="primary")
            with gr.Row():
                civitai_openfolder = gr.Button(value="Open Download Folder",variant="primary" , visible=False)
            with gr.Row():
                gr.Markdown("Downloading may take some time.\nCheck console log for detail")
            
    with gr.Column(scale=4):    
        with gr.Row(): 
            with gr.Accordion("#", open=True) as model_title_name:   
                civitai_gallery = gr.Gallery(label="Civitai Gallery", show_label=False, elem_id="civitai_gallery").style(grid=[setting.gallery_column],height="auto")
        with gr.Row():  
            with gr.Accordion("Model Description", open=True):  
                description_html = gr.HTML()

    with gr.Column(scale=1):
        with gr.Row():                            
            img_file_info = gr.Textbox(label="Generate Info", interactive=False, lines=6).style(container=True, show_copy_button=True)
        with gr.Row():
            try:
                send_to_buttons = modules.generation_parameters_copypaste.create_buttons(["txt2img", "img2img", "inpaint", "extras"])
            except:
                pass      
            
    with gr.Row(visible=False):
        #civitai model information                
        img_index = gr.Number(show_label=False)
        # 이미지 파일명 또는 URL 리스트였다가 이미지 리스트가됨 왔다갔다 함
        civitai_images = gr.State()
        # 트리거를 위한것
        civitai_gallery_url = gr.Textbox(value=None)
        hidden = gr.Image(type="pil")
        info1 = gr.Textbox()
        info2 = gr.Textbox() 

    try:
        modules.generation_parameters_copypaste.bind_buttons(send_to_buttons, hidden, img_file_info)
    except:
        pass
        
    download_model.click(
        fn=civitai_shortcut_action.on_download_model_click,
        inputs=[
            selected_version_id,
            filename_list,            
            # an_lora,
            vs_folder,
            vs_folder_name
        ],
        outputs=[refresh_sc_list]
    )  
    
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
            # an_lora, 
            model_type, 
            versions_list,
            description_html,
            trigger_words,
            filename_list,
            model_title_name,                        
            civitai_gallery_url, 
            civitai_images,
            img_file_info,
            civitai_openfolder,
            vs_folder_name            
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
            # an_lora, 
            model_type, 
            versions_list,
            description_html,
            trigger_words,
            filename_list,
            model_title_name,                        
            civitai_gallery_url, 
            civitai_images,            
            img_file_info,
            civitai_openfolder,
            vs_folder_name
        ]
    )    
    
    civitai_gallery_url.change(
        fn=civitai_shortcut_action.on_civitai_gallery_loading,
        inputs=[
            civitai_images,
        ],
        outputs=[
            civitai_gallery,
            civitai_images
        ]                
    )
    
    # civitai_gallery.select(lambda evt, version_images_url : evt.index, version_images_url[evt.index], civitai_images, [img_index, hidden])
    civitai_gallery.select(civitai_shortcut_action.on_gallery_select, civitai_images, [img_index, hidden])
    hidden.change(fn=modules.extras.run_pnginfo, inputs=[hidden], outputs=[info1, img_file_info, info2])
    civitai_openfolder.click(civitai_shortcut_action.on_open_folder_click,[selected_model_id,selected_version_id],None)    
    
    # vs_folder.change(
    #     fn=on_vs_folder_change,
    #     inputs=[vs_folder],
    #     outputs=[vs_folder_name]
    # )
    
    vs_folder.change(lambda x:gr.update(visible=x),vs_folder,vs_folder_name)
                
def downloaded_model_information_ui(selected_downloaded_version_id:gr.Textbox(),selected_downloaded_model_id:gr.Textbox(),civitai_tab:gr.Tabs(),civitai_information_tabs:gr.Tabs(),selected_civitai_information_tabs: gr.Number(),selected_model_id: gr.Textbox()):
    with gr.Column(scale=1):
        with gr.Row():
            downloaded_versions_list = gr.Dropdown(label="Model Version", choices=[setting.NORESULT], interactive=True, value=setting.NORESULT)
        with gr.Row():
            downloaded_model_type = gr.Textbox(label="Model Type", value="", interactive=False, lines=1)                                                     
        with gr.Row():
            downloaded_trigger_words = gr.Textbox(label="Trigger Words", value="", interactive=False, lines=1).style(container=True, show_copy_button=True)
        with gr.Row():
            downloaded_civitai_model_url_txt = gr.Textbox(label="Model Url", interactive=False , lines=1).style(container=True, show_copy_button=True)
        with gr.Row():
            downloaded_filename_list = gr.Textbox(label="Model Version File", interactive=False)                                    
        with gr.Row():
            goto_civitai_model_tab = gr.Button(value="Goto civitai shortcut tab",variant="primary")
        with gr.Row():
            downloaded_openfolder = gr.Button(value="Open Download Folder",variant="primary")
                                                                                
    with gr.Column(scale=4):
        with gr.Row():
            with gr.Accordion("#", open=True) as downloaded_model_title_name:
                downloaded_gallery = gr.Gallery(label="Downloaded Version Gallery", show_label=False, elem_id="downloaded_version_gallery").style(grid=[setting.gallery_column],height="auto")
        with gr.Row():    
            with gr.Accordion("Model Description", open=True):  
                downloaded_description_html = gr.HTML()                                                                                                   
    with gr.Column(scale=1):
        with gr.Row():                            
            downloaded_img_file_info = gr.Textbox(label="Generate Info", interactive=False, lines=6).style(container=True, show_copy_button=True)
        with gr.Row():
            try:
                downloaded_send_to_buttons = modules.generation_parameters_copypaste.create_buttons(["txt2img", "img2img", "inpaint", "extras"])
            except:
                pass 
            
    with gr.Row(visible=False):  
        #download model information                
        downloaded_img_index = gr.Number(show_label=False)
        # 이미지 파일명리스트 - 파일은 굳이 일부러 로딩할필요가 없다.
        downloaded_images = gr.State()
        # 트리거를 위한것
        downloaded_gallery_url = gr.Textbox(value=None)
        downloaded_hidden = gr.Image(type="pil")
        downloaded_info1 = gr.Textbox()
        downloaded_info2 = gr.Textbox()  
                        
    try:
        modules.generation_parameters_copypaste.bind_buttons(downloaded_send_to_buttons, downloaded_hidden,downloaded_img_file_info)
    except:
        pass

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
            downloaded_gallery_url,
            downloaded_images,
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
            downloaded_gallery_url,
            downloaded_images,
            downloaded_img_file_info          
        ]
    ) 

    downloaded_gallery_url.change(
        fn=civitai_shortcut_action.on_file_gallery_loading,
        inputs=[
            downloaded_images 
        ],
        outputs=[               
            downloaded_gallery
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
            selected_civitai_information_tabs,
            selected_model_id,      
        ],        
    )
                    
    downloaded_gallery.select(civitai_shortcut_action.on_gallery_select, downloaded_images, [downloaded_img_index, downloaded_hidden])
    downloaded_hidden.change(fn=modules.extras.run_pnginfo, inputs=[downloaded_hidden], outputs=[downloaded_info1, downloaded_img_file_info, downloaded_info2])
    # downloaded model information end
    ###### Downloaded Tab ######                                                  

    ### open folder start    
    downloaded_openfolder.click(civitai_shortcut_action.on_open_folder_click,[selected_downloaded_model_id,selected_downloaded_version_id],None)
                
def civitai_shortcut_ui():    
    with gr.Tabs(elem_id="civitai_shortcut_tabs_container") as civitai_tab:
        with gr.TabItem("Civitai Shortcut" , id="civitai01"):
            with gr.Row(visible=False):
                #변수형 컨트롤
                #civitai model select model
                selected_version_id = gr.Textbox()
                selected_model_id = gr.Textbox()
                                
                # saved shortcut model select model
                selected_saved_version_id = gr.Textbox()
                selected_saved_model_id = gr.Textbox()

                # user gallery select model                        
                selected_usergal_model_id = gr.Textbox()

                # download model select model
                selected_downloaded_version_id = gr.Textbox()
                selected_downloaded_model_id = gr.Textbox()
        
                # common                 
                refresh_sc_list = gr.Textbox(value="")                     
                selected_civitai_information_tabs = gr.Number(value=0, show_label=False)
                
            with gr.Row(): 
                with gr.Column(scale=1):
                    with gr.Tabs() as civitai_shortcut_tabs:
                        with gr.TabItem("Upload"):
                            with gr.Row(visible=False):                                 
                                register_information_only = gr.Checkbox(label="Register only model information", value=False)
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
                            with gr.Row():
                                update_modelfolder_btn = gr.Button(value="Update Downloaded Model Information", variant="primary")                                                                    
                            with gr.Row(visible=False):
                                upload_progress = gr.Markdown(value="###", visible=False)
                                
                        with gr.TabItem("Browsing"):    
                            with gr.Row():
                                shortcut_type = gr.Dropdown(label='Filter Model type', multiselect=True, choices=[k for k in setting.ui_model_types], interactive=True)
                            with gr.Row():
                                sc_search = gr.Textbox(label="Search", value="", placeholder="Search name, #tags ....",interactive=True, lines=1)
                            with gr.Row():
                                sc_gallery = gr.Gallery(label="SC Gallery", elem_id="sc_gallery", show_label=False, value=ishortcut_action.get_thumbnail_list()).style(grid=[setting.shortcut_colunm], height="auto")
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
                                civitai_model_information_ui(selected_version_id,selected_model_id,refresh_sc_list)
                                
                        with gr.TabItem("Saved Model Information" , id="saved_info"):
                            with gr.Row():
                                saved_model_information_ui(selected_saved_version_id,selected_saved_model_id,refresh_sc_list)
                                
                        with gr.TabItem("Civitai User Gallery" , id="gallery_info"):
                            with gr.Row():
                                civitai_user_gallery_ui(selected_usergal_model_id)      
                                        
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
                    with gr.Tab("Downloaded Model Information"):
                        with gr.Row():
                            downloaded_model_information_ui(selected_downloaded_version_id, selected_downloaded_model_id, civitai_tab, civitai_information_tabs, selected_civitai_information_tabs, selected_model_id)
    
    ###### Civitai Tab ######
    # civitai upload tab start
    civitai_internet_url.upload(
        fn=civitai_shortcut_action.on_civitai_internet_url_upload,
        inputs=[
            civitai_internet_url,
            register_information_only,
            selected_civitai_information_tabs
        ],
        outputs=[
            selected_model_id,
            selected_saved_model_id,
            selected_usergal_model_id,
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
    
    update_modelfolder_btn.click(
        fn=civitai_shortcut_action.on_update_modelfolder_btn_click,
        inputs=None,
        outputs=refresh_sc_list
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
        
    sc_gallery.select(civitai_shortcut_action.on_sc_gallery_select,selected_civitai_information_tabs,[selected_model_id,selected_saved_model_id,selected_usergal_model_id])    
    
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
    
    sc_new_version_gallery.select(civitai_shortcut_action.on_sc_gallery_select,selected_civitai_information_tabs,[selected_model_id,selected_saved_model_id,selected_usergal_model_id])
    # civitai scan new version tab end

    # Common start
    civitai_information_tabs.select(
        fn=civitai_shortcut_action.on_civitai_information_tabs_select,
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
    
    # sc 메류를 갱신시킨다.
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
    # Common end
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
