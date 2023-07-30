import os
import gradio as gr
import shutil

from . import util
from . import setting

# import modules.scripts as scripts   
from modules import scripts, script_callbacks, shared    
            
def on_setting_ui():
    with gr.Column(): 
        with gr.Row():
            with gr.Accordion("Option", open=False):    
                with gr.Row():
                    shortcut_update_when_start = gr.Checkbox(value=setting.shortcut_update_when_start, label="Startup : The program performs 'Update the model information for the shortcut' when it starts.",info="At program startup, the registered shortcuts are updated with the latest data. This process operates in the background. To update manually, you can uncheck that option and use the 'Scans and Model Updates -> Update the model information for the shortcut' feature.", interactive=True)
                    shortcut_max_download_image_per_version = gr.Slider(minimum=0, maximum=30, value=setting.shortcut_max_download_image_per_version, step=1,info="When registering a shortcut of a model, you can specify the maximum number of images to download. \n This is the maximum per version, and setting it to 0 means unlimited downloads.", label='Maximum number of download images per version', interactive=True)
                with gr.Row():
                    classification_preview_mode_disable = gr.Checkbox(value=setting.classification_preview_mode_disable, label="Deactivate the preview mode of the classification gallery." , info="Deactivate the preview mode of the classification gallery. It is a temporary feature implemented using a expedient. Please use it only if necessary." , interactive=True)
        with gr.Row():
            with gr.Accordion("Screen Style", open=False):    
                with gr.Row():
                    scbrowser_screen_split_ratio = gr.Slider(minimum=0, maximum=setting.shortcut_browser_screen_split_ratio_max, value=setting.shortcut_browser_screen_split_ratio, step=1, info="You can specify the size ratio between the shortcut browser and the information screen.", label='Shortcut Browser screen ratio', interactive=True)              
                with gr.Row():                                                
                    info_gallery_height = gr.Dropdown(choices=["auto"], value=setting.information_gallery_height, allow_custom_value=True, interactive=True, info="You can also specify a specific size other than 'auto'" , label="Information Gallery Height")                    
                    gallery_thumbnail_image_style = gr.Dropdown(choices=["scale-down","cover","contain","fill","none"], value=setting.gallery_thumbnail_image_style, interactive=True, info="This specifies the shape of the displayed thumbnail." , label="Gallery Thumbnail Image Style")
                    shortcut_browser_search_up = gr.Dropdown(choices=["Up","Down"], value="Up" if setting.shortcut_browser_search_up else "Down", interactive=True, label="Set the position of the search bar in the shortcut browser.", info="If you select 'Up', the search bar will be placed above the thumbnail pane.")
                    
        with gr.Row():
            with gr.Accordion("Shortcut Browser and Information Images", open=False):    
                with gr.Row():
                    shortcut_column = gr.Slider(minimum=1, maximum=12, value=setting.shortcut_column, step=1, label='Shortcut Browser Column Count', interactive=True)
                    shortcut_rows_per_page = gr.Slider(minimum=0, maximum=10, value=setting.shortcut_rows_per_page, step=1, label='Shortcut Browser Thumbnail Rows per Page : setting it to 0 means displaying the entire list without a page.', interactive=True)
                with gr.Row():                    
                    gallery_column = gr.Slider(minimum=1, maximum=24, value=setting.gallery_column, step=1, label='Model Information Column Count', interactive=True)
                    classification_gallery_column = gr.Slider(minimum=1, maximum=24, value=setting.classification_gallery_column, step=1, label='Classification Model Column Count', interactive=True)
                # with gr.Row():                        
                #     shortcut_max_download_image_per_version = gr.Slider(minimum=0, maximum=30, value=setting.shortcut_max_download_image_per_version, step=1,info="When registering a shortcut of a model, you can specify the maximum number of images to download. \n This is the maximum per version, and setting it to 0 means unlimited downloads.", label='Maximum number of download images per version', interactive=True)
                #     gr.Markdown(value="When registering a shortcut of a model, you can specify the maximum number of images to download. \n This is the maximum per version, and setting it to 0 means unlimited downloads.", visible=True)    
                                                                
        with gr.Row():
            with gr.Accordion("User Gallery Images", open=False):    
                with gr.Row():
                    usergallery_images_column = gr.Slider(minimum=1, maximum=20, value=setting.usergallery_images_column, step=1, label='User Gallery Column Count', interactive=True)
                    usergallery_images_page_limit = gr.Slider(minimum=1, maximum=48, value=setting.usergallery_images_page_limit, step=1, label='User Gallery Images Count Per Page', interactive=True)
                with gr.Row():                    
                    usergallery_openfolder_btn = gr.Button(value="Open User Gallery Cache Folder", variant="primary")
                    with gr.Accordion("Clean User Gallery Cache", open=False):
                        usergallery_cleangallery_btn = gr.Button(value="Clean User Gallery Cache", variant="primary")

        with gr.Row():
            with gr.Accordion("Download Folder for Extensions", open=False):
                with gr.Column():
                    extension_locon_folder = gr.Textbox(value=setting.model_folders['LoCon'], label="LyCORIS", interactive=True)
                    extension_wildcards_folder = gr.Textbox(value=setting.model_folders['Wildcards'], label="Wildcards", interactive=True)
                    extension_controlnet_folder = gr.Textbox(value=setting.model_folders['Controlnet'], label="Controlnet", interactive=True)
                    extension_aestheticgradient_folder = gr.Textbox(value=setting.model_folders['AestheticGradient'], label="Aesthetic Gradient", interactive=True)
                    extension_poses_folder = gr.Textbox(value=setting.model_folders['Poses'], label="Poses", interactive=True)
                    extension_other_folder = gr.Textbox(value=setting.model_folders['Other'], label="Other", interactive=True)                    
                    download_images_folder = gr.Textbox(value=setting.download_images_folder, label="Download Images Folder", interactive=True)                    
                    
        with gr.Row():
            save_btn = gr.Button(value="Save Setting", variant="primary")
            reload_btn = gr.Button(value="Reload UI")
            refresh_setting = gr.Textbox(visible=False)        

    refresh_setting.change(
        fn=on_refresh_setting_change,
        inputs=None,
        outputs=[
            shortcut_update_when_start,
            scbrowser_screen_split_ratio,
            info_gallery_height,
            shortcut_column,
            shortcut_rows_per_page,
            gallery_column,
            classification_gallery_column,
            usergallery_images_column,
            usergallery_images_page_limit,            
            shortcut_max_download_image_per_version,
            gallery_thumbnail_image_style,
            shortcut_browser_search_up,
            extension_locon_folder,
            extension_wildcards_folder,
            extension_controlnet_folder,
            extension_aestheticgradient_folder,
            extension_poses_folder,
            extension_other_folder,
            download_images_folder,
            classification_preview_mode_disable             
        ],
        show_progress=False
    )

    # reload the page
    reload_btn.click(fn=on_reload_btn_click, _js='restart_reload', inputs=None, outputs=None)
                            
    usergallery_openfolder_btn.click(
        fn=on_usergallery_openfolder_btn_click,
        inputs=None,
        outputs=None    
    )
    
    usergallery_cleangallery_btn.click(
        fn=on_usergallery_cleangallery_btn_click,
        inputs=None,
        outputs=None    
    )
                            
    save_btn.click(
        fn=on_save_btn_click,
        inputs=[
            shortcut_update_when_start,
            scbrowser_screen_split_ratio,
            info_gallery_height,
            shortcut_column,
            shortcut_rows_per_page,
            gallery_column,
            classification_gallery_column,
            usergallery_images_column,
            usergallery_images_page_limit,            
            shortcut_max_download_image_per_version,
            gallery_thumbnail_image_style,
            shortcut_browser_search_up,
            extension_locon_folder,
            extension_wildcards_folder,
            extension_controlnet_folder,
            extension_aestheticgradient_folder,
            extension_poses_folder,
            extension_other_folder,
            download_images_folder,
            classification_preview_mode_disable            
        ],
        outputs=None    
    )   
    
    return refresh_setting

def on_save_btn_click(shortcut_update_when_start,
                      scbrowser_screen_split_ratio, info_gallery_height, 
                      shortcut_column, shortcut_rows_per_page,
                      gallery_column, classification_gallery_column, usergallery_images_column, usergallery_images_page_limit,
                      shortcut_max_download_image_per_version,
                      gallery_thumbnail_image_style,
                      shortcut_browser_search_up,
                      locon,wildcards,controlnet,aestheticgradient,poses,other,download_images_folder,
                      classification_preview_mode_disable
                      ):    
    
    save_setting(shortcut_update_when_start,
                      scbrowser_screen_split_ratio, info_gallery_height, 
                      shortcut_column, shortcut_rows_per_page,
                      gallery_column, classification_gallery_column, usergallery_images_column, usergallery_images_page_limit,
                      shortcut_max_download_image_per_version,
                      gallery_thumbnail_image_style,
                      shortcut_browser_search_up,
                      locon,wildcards,controlnet,aestheticgradient,poses,other,download_images_folder,
                      classification_preview_mode_disable
                      )    

def save_setting(shortcut_update_when_start,
                      scbrowser_screen_split_ratio, info_gallery_height, 
                      shortcut_column, shortcut_rows_per_page,
                      gallery_column, classification_gallery_column, usergallery_images_column, usergallery_images_page_limit,
                      shortcut_max_download_image_per_version,
                      gallery_thumbnail_image_style,
                      shortcut_browser_search_up,
                      locon,wildcards,controlnet,aestheticgradient,poses,other,download_images_folder,
                      classification_preview_mode_disable
                      ):    
    
    environment = setting.load()
    if not environment:
         environment = dict()        
         
    application_allow = dict()    
    application_allow['shortcut_update_when_start'] = shortcut_update_when_start
    application_allow['shortcut_max_download_image_per_version'] = shortcut_max_download_image_per_version
    environment['application_allow'] = application_allow
                
    screen_style = dict()
    screen_style['shortcut_browser_screen_split_ratio'] = scbrowser_screen_split_ratio
    screen_style['information_gallery_height'] = info_gallery_height
    screen_style['gallery_thumbnail_image_style'] = gallery_thumbnail_image_style
    screen_style['shortcut_browser_search_up'] = True if shortcut_browser_search_up == "Up" else False
    environment['screen_style'] = screen_style
    
    image_style = dict()
    image_style['shortcut_column'] = shortcut_column
    image_style['shortcut_rows_per_page'] = shortcut_rows_per_page

    image_style['gallery_column'] = gallery_column
    image_style['classification_gallery_column'] = classification_gallery_column
        
    image_style['usergallery_images_column'] = usergallery_images_column
    image_style['usergallery_images_page_limit'] = usergallery_images_page_limit           
    environment['image_style'] = image_style
    
    model_folders = dict()
    if locon:
        model_folders['LoCon'] = locon    
    if wildcards:
        model_folders['Wildcards'] = wildcards
    if controlnet:
        model_folders['Controlnet'] = controlnet
    if aestheticgradient:        
        model_folders['AestheticGradient'] = aestheticgradient
    if poses:        
        model_folders['Poses'] = poses
    if other:        
        model_folders['Other'] = other
    
    environment['model_folders'] = model_folders
    
    download_folders = dict()
    if download_images_folder:
        download_folders['download_images'] = download_images_folder        
                
    environment['download_folders'] = download_folders
    
    temporary = dict()
    temporary['classification_preview_mode_disable'] = classification_preview_mode_disable  
    
    environment['temporary'] = temporary
    
    setting.save(environment)
    setting.load_data()
    
    util.printD("Save setting. Reload UI is needed")
                   
def on_usergallery_openfolder_btn_click():
    if os.path.exists(setting.shortcut_gallery_folder):
        util.open_folder(setting.shortcut_gallery_folder)   

def on_usergallery_cleangallery_btn_click():
    if os.path.exists(setting.shortcut_gallery_folder):
        shutil.rmtree(setting.shortcut_gallery_folder)        

def on_reload_btn_click():
    request_restart()

def request_restart():
    shared.state.interrupt()
    shared.state.need_restart = True            

# def on_update_btn_click():
#     git = os.environ.get('GIT', "git")

#     subdir = os.path.dirname(os.path.abspath(__file__))

#     # perform git pull in the extension folder
#     output = subprocess.check_output([git, '-C', subdir, 'pull', '--autostash'])
#     print(output.decode('utf-8'))

def on_refresh_setting_change():
    return setting.shortcut_update_when_start,\
            setting.shortcut_browser_screen_split_ratio,\
            setting.information_gallery_height,\
            setting.shortcut_column,\
            setting.shortcut_rows_per_page,\
            setting.gallery_column,\
            setting.classification_gallery_column,\
            setting.usergallery_images_column,\
            setting.usergallery_images_page_limit,\
            setting.shortcut_max_download_image_per_version,\
            setting.gallery_thumbnail_image_style,\
            "Up" if setting.shortcut_browser_search_up else "Down",\
            setting.model_folders['LoCon'],\
            setting.model_folders['Wildcards'],\
            setting.model_folders['Controlnet'],\
            setting.model_folders['AestheticGradient'],\
            setting.model_folders['Poses'],\
            setting.model_folders['Other'],\
            setting.download_images_folder,\
            setting.classification_preview_mode_disable 