import os
import gradio as gr
import datetime
import requests
import shutil
import json

from . import util
from . import model
from . import setting
from . import civitai

from . import ishortcut
from . import ishortcut_action

# import modules.scripts as scripts   
from modules import scripts, script_callbacks, shared
    
def create_models_information(files, mfolder, vs_folder, register_shortcut, progress=gr.Progress()):
    
    non_list = list()    
    if not files:
        return None
    
    for file_path in progress.tqdm(files, desc=f"Create Models Information"): 
        if os.path.isfile(file_path):                        
            util.printD(f"Generate SHA256: {file_path}")
            hash = util.calculate_sha256(file_path)
            version_info = civitai.get_version_info_by_hash(hash)
            
            if not version_info:
                # These models are not registered with Civitai.
                non_list.append(file_path)
                continue
            
            vfolder , vfile = os.path.split(file_path) 
            basename , ext = os.path.splitext(vfile)
            
            # 저장할 폴더 생성
            if mfolder:
                model_folder = util.make_download_model_folder(version_info, True, vs_folder)
                # 다정하면 임의의 분류뒤에 모델폴더를 생성하고 그뒤에 버전까지 생성가능
                # model_folder = make_download_model_folder(version_info, ms_folder=True, vs_folder=True, vs_foldername=None, cs_foldername=None):
                # model_folder = util.make_version_folder(version_info, vs_folder)
            else:
                model_folder = vfolder
            
            # version info file name 으로 교체시
            # savefile_base = get_save_base_name(version_info)   
            # basename = savefile_base
            # destination = os.path.join(model_folder, f"{basename}{ext}")
            
            # save info
            info_path = os.path.join(model_folder, f"{basename}{setting.info_suffix}{setting.info_ext}")       
            result = civitai.write_version_info(info_path, version_info)
            if result:
                util.printD(f"Wrote version info : {info_path}")
                                                                    
            # save preview            
            if "images" in version_info.keys():
                description_img = os.path.join(model_folder, f"{basename}{setting.preview_image_suffix}{setting.preview_image_ext}")
                try:            
                    img_dict = version_info["images"][0] 
                    if "url" in img_dict:
                        img_url = img_dict["url"]
                        if "width" in img_dict:
                            if img_dict["width"]:
                                img_url =  util.change_width_from_image_url(img_url, img_dict["width"])
                        # get image
                        with requests.get(img_url, stream=True) as img_r:
                            if not img_r.ok:
                                util.printD("Get error code: " + str(img_r.status_code))
                                return

                            with open(description_img, 'wb') as f:
                                img_r.raw.decode_content = True
                                shutil.copyfileobj(img_r.raw, f)
                                util.printD(f"Downloaded preview image : {description_img}")                                
                except Exception as e:
                    pass
                
            # 파일 이동
            if mfolder:
                destination = os.path.join(model_folder, vfile)
                if file_path != destination:
                    if not os.path.isfile(destination):
                        os.rename(file_path, destination)
                    else:
                        util.printD(f"The target file already exists : target {destination}")
            
            # 숏컷 추가
            if register_shortcut:
                if version_info['modelId']:
                    ishortcut.update_shortcut(version_info['modelId'], progress)                    
                    model.update_downloaded_model()
                
    return non_list
                    
def scan_models(fix_information_filename, progress=gr.Progress()):    
    root_dirs = list(set(setting.model_folders.values()))
    file_list = util.search_file(root_dirs,None,setting.model_exts)    

    result = list()
    
    if fix_information_filename:
        # fix_version_information_filename()
        pass
        
    for file_path in progress.tqdm(file_list, desc=f"Scan Models for Civitai"): 
        
        vfolder , vfile = os.path.split(file_path) 
        basename , ext = os.path.splitext(vfile)
        info = os.path.join(vfolder, f"{basename}{setting.info_suffix}{setting.info_ext}")        

        if not os.path.isfile(info):
            result.append(file_path)

    return result

def get_save_base_name(version_info):
    # 이미지 파일명도 primary 이름으로 저장한다.
           
    base = None    
    primary_file = civitai.get_primary_file_by_version_info(version_info)
    if not primary_file:
        base = setting.generate_version_foldername(version_info['model']['name'],version_info['name'],version_info['id'])
    else:
        base, ext = os.path.splitext(primary_file['name'])   
    return base

# def fix_version_information_filename():
#     root_dirs = list(set(setting.model_folders.values()))
#     file_list = util.search_file(root_dirs,None,[setting.info_ext])
    
#     version_info = None
#     if not file_list:             
#         return
    
#     for file_path in file_list:        
        
#         try:
#             with open(file_path, 'r') as f:
#                 json_data = json.load(f)
            
#                 if 'id' in json_data.keys():
#                     version_info = json_data
                    
#             file_path = file_path.strip()
#             vfolder , vfile = os.path.split(file_path)                     
#             savefile_base = get_save_base_name(version_info)                                
#             info_file = os.path.join(vfolder, f"{util.replace_filename(savefile_base)}{setting.info_suffix}{setting.info_ext}")        
                        
#             if file_path != info_file:
#                 if not os.path.isfile(info_file):
#                     os.rename(file_path, info_file)

#         except:
#             pass
    
        
def on_create_models_info_btn_click(files, mfolder, vsfolder, register_shortcut, progress=gr.Progress()):
    remain_files = create_models_information(files,mfolder,vsfolder,register_shortcut, progress)
    if remain_files and len(remain_files) > 0:
        return gr.update(choices=remain_files, value=remain_files, interactive=True, label="These models are not registered with Civitai."),gr.update(visible=True),gr.update(visible=True)    
    return gr.update(choices=[], value=[], interactive=True),gr.update(visible=False),gr.update(visible=False)  
         
def on_update_progress_change():
    current_time = datetime.datetime.now()
    return gr.update(value=current_time)

def on_scan_progress_change():
    current_time = datetime.datetime.now()
    return gr.update(value=current_time)

def on_scan_models_btn_click(fix_information_filename, progress=gr.Progress()):
    files = scan_models(fix_information_filename, progress)
    return gr.update(choices=files,value=files,interactive=True,label="Scanned Model List"),gr.update(visible=True),gr.update(visible=True),gr.update(value=False, interactive=True),gr.update(value=False, interactive=False)
    
def on_scan_to_shortcut_click(progress=gr.Progress()):
    model.update_downloaded_model()
    ishortcut_action.scan_downloadedmodel_to_shortcut(progress)
    return gr.update(value="This feature scans for models that have information files available and registers a shortcut for them, downloading any necessary images in the process. If there is no information available for a particular model, please use the 'Scan Models' feature.")

def on_update_all_shortcuts_btn(progress=gr.Progress()):
    ishortcut.update_all_shortcut_informations(progress)
    return gr.update(value="This feature updates registered shortcuts with the latest information and downloads any new images if available.")

def on_scan_save_modelfolder_change(scan_save_modelfolder):
    if scan_save_modelfolder:
        return gr.update(interactive=True)
    return gr.update(value=False, interactive=False)
    
def on_scan_ui():
    with gr.Column():      
        with gr.Row():
            with gr.Accordion("Scan models for Civitai", open=True):    
                with gr.Row():
                    with gr.Column():
                        fix_information_filename = gr.Checkbox(label="Fix version information filename", value=False , visible=False) 
                        scan_models_btn = gr.Button(value="Scan Models",variant="primary") 
                        gr.Markdown(value="This feature targets models that do not have information files available in the saved models. It calculates the hash value and searches for the model in Civitai, registering it as a shortcut. Calculating the hash value can take a significant amount of time.", visible=True)
                        with gr.Box(elem_classes="cs_box", visible=False) as scanned_result:  
                            scan_models_result = gr.CheckboxGroup(visible=True, label="Scanned Model List").style(item_container=True,container=True)
                with gr.Row(visible=False) as update_information:
                    with gr.Column():
                        with gr.Row():
                            with gr.Column(scale=1):
                                scan_register_shortcut = gr.Checkbox(label="Register a shortcut when creating the model information file.", value=True)
                            with gr.Column(scale=1):
                                with gr.Row():
                                    scan_save_modelfolder = gr.Checkbox(label="Create a model folder corresponding to the model type.", value=False)
                                    scan_save_vsfolder = gr.Checkbox(label="Create individual model version folder.", value=False, interactive=False) 
                        with gr.Row():
                            with gr.Column():
                                create_models_info_btn = gr.Button(value="Create Model Information",variant="primary")                                                       
        with gr.Row():
            with gr.Accordion("Update Shortcuts", open=True):   
                with gr.Row():
                    with gr.Column():
                        update_all_shortcuts_btn = gr.Button(value="Update the model information for the shortcut",variant="primary")
                        update_progress = gr.Markdown(value="This feature updates registered shortcuts with the latest information and downloads any new images if available.", visible=True)
                    with gr.Column(): 
                        scan_to_shortcut_btn = gr.Button(value="Scan downloaded models for shortcut registration",variant="primary")                    
                        scan_progress = gr.Markdown(value="This feature scans for models that have information files available and registers a shortcut for them, downloading any necessary images in the process. If there is no information available for a particular model, please use the 'Scan Models' feature.", visible=True)
    
    scan_save_modelfolder.change(
        fn=on_scan_save_modelfolder_change,
        inputs=[
            scan_save_modelfolder
        ],
        outputs=[
            scan_save_vsfolder
        ]
    )
    
    create_models_info_btn.click(
        fn=on_create_models_info_btn_click,
        inputs=[
            scan_models_result,
            scan_save_modelfolder,
            scan_save_vsfolder,
            scan_register_shortcut
        ],
        outputs=[
            scan_models_result,
            scanned_result,
            update_information            
        ]
    )   
         
    scan_models_btn.click(
        fn=on_scan_models_btn_click,
        inputs=[fix_information_filename],
        outputs=[
            scan_models_result,
            scanned_result,
            update_information,
            scan_save_modelfolder,
            scan_save_vsfolder
        ]                
    )
                  
    update_all_shortcuts_btn.click(
        fn=on_update_all_shortcuts_btn,
        inputs=None,
        outputs=[
            update_progress,
        ]
    ) 
    
    update_progress.change(
        fn=on_update_progress_change,
        inputs=None,
        outputs=[update_progress]
    )

    scan_to_shortcut_btn.click(
        fn=on_scan_to_shortcut_click,
        inputs=None,
        outputs=[
            scan_progress,
        ]                
    )
        
    scan_progress.change(
        fn=on_scan_progress_change,
        inputs=None,
        outputs=[scan_progress]
    ) 
    
def on_save_btn_click(shortcut_update_when_start,
                      scbrowser_screen_split_ratio, info_gallery_height, 
                      shortcut_column, shortcut_count_per_page,
                      gallery_column, classification_gallery_column, usergallery_images_column, usergallery_images_page_limit,
                      shortcut_max_download_image_per_version,
                      gallery_thumbnail_image_style,
                      locon,wildcards,controlnet,aestheticgradient,poses,other,download_images_folder,
                      classification_preview_mode_disable
                      ):    
    
    environment = dict()    
    
    application_allow = dict()    
    application_allow['shortcut_update_when_start'] = shortcut_update_when_start
    application_allow['shortcut_max_download_image_per_version'] = shortcut_max_download_image_per_version
    environment['application_allow'] = application_allow
                
    screen_style = dict()
    screen_style['shortcut_browser_screen_split_ratio'] = scbrowser_screen_split_ratio
    screen_style['information_gallery_height'] = info_gallery_height
    screen_style['gallery_thumbnail_image_style'] = gallery_thumbnail_image_style
    environment['screen_style'] = screen_style
    
    image_style = dict()
    image_style['shortcut_column'] = shortcut_column
    image_style['shortcut_count_per_page'] = shortcut_count_per_page

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
                    info_gallery_height = gr.Dropdown(choices=["auto","fit"], value=setting.information_gallery_height, allow_custom_value=True, interactive=True, info="You can also specify a specific size other than 'auto' or 'fit'" , label="Information Gallery Height")                    
                    gallery_thumbnail_image_style = gr.Dropdown(choices=["scale-down","cover","contain","fill","none"], value=setting.gallery_thumbnail_image_style, interactive=True, info="This specifies the shape of the displayed thumbnail." , label="Gallery Thumbnail Image Style")
                                        
        with gr.Row():
            with gr.Accordion("Shortcut Browser and Information Images", open=False):    
                with gr.Row():
                    shortcut_column = gr.Slider(minimum=1, maximum=12, value=setting.shortcut_column, step=1, label='Shortcut Browser Column Count', interactive=True)
                    shortcut_count_per_page = gr.Slider(minimum=0, maximum=100, value=setting.shortcut_count_per_page, step=1, label='Shortcut Browser Thumbnail Count per Page : setting it to 0 means displaying the entire list without a page.', interactive=True)
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
            shortcut_count_per_page,
            gallery_column,
            classification_gallery_column,
            usergallery_images_column,
            usergallery_images_page_limit,            
            shortcut_max_download_image_per_version,
            gallery_thumbnail_image_style,
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
           


       