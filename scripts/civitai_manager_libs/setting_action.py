import os
import gradio as gr
import datetime
import requests
import shutil

from . import util
from . import model
from . import setting
from . import civitai

from . import ishortcut_action

def create_models_information(files, mfolder, vs_folder,register_shortcut, progress=gr.Progress()):
    
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
                model_folder = util.make_version_folder(version_info, False , vs_folder)
            else:
                model_folder = vfolder
            
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
                    os.rename(file_path, destination)
            
            # 숏컷 추가
            if register_shortcut:
                if version_info['modelId']:
                    ishortcut_action.add_shortcut(version_info['modelId'],progress)
                    model.update_downloaded_model()
                
    return non_list
                    
def scan_models(progress=gr.Progress()):    
    root_dirs = list(set(setting.model_folders.values()))
    file_list = util.search_file(root_dirs,None,setting.model_exts)    

    result = list()
    
    for file_path in progress.tqdm(file_list, desc=f"Scan Models for Civitai"): 
        
        vfolder , vfile = os.path.split(file_path) 
        basename , ext = os.path.splitext(vfile)
        info = os.path.join(vfolder, f"{basename}{setting.info_suffix}{setting.info_ext}")        

        if not os.path.isfile(info):
            result.append(file_path)

    return result

def on_create_models_info_btn_click(files, mfolder, vsfolder, register_shortcut, progress=gr.Progress()):
    remain_files = create_models_information(files,mfolder,vsfolder,register_shortcut, progress)
    if remain_files and len(remain_files) > 0:
        return gr.update(choices=remain_files, value=remain_files, interactive=True, label="These models are not registered with Civitai."),gr.update(visible=True),gr.update(visible=True)    
    return gr.update(choices=[], value=[], interactive=True),gr.update(visible=False),gr.update(visible=False)  
         
def on_thumb_progress_change():
    current_time = datetime.datetime.now()
    return gr.update(value="###")

def on_scan_progress_change():
    current_time = datetime.datetime.now()
    return gr.update(value="###")

def on_scan_models_btn_click(progress=gr.Progress()):
    files = scan_models(progress)
    return gr.update(choices=files,value=files,interactive=True,label="Scanned Model List"),gr.update(visible=True),gr.update(visible=True),gr.update(value=True, interactive=True),gr.update(value=True, interactive=True)
    
def on_scan_to_shortcut_click(progress=gr.Progress()):
    model.update_downloaded_model()
    ishortcut_action.scan_downloadedmodel_to_shortcut(progress)
    return gr.update(value="Scan downloaded models for shortcut registration is Done")

def on_shortcut_saved_update_btn(progress=gr.Progress()):
    ishortcut_action.update_all_shortcut_model(progress)
    return gr.update(value="Update the model information for the shortcut is Done")

def on_scan_save_modelfolder_change(scan_save_modelfolder):
    if scan_save_modelfolder:
        return gr.update(value=True, interactive=True)
    return gr.update(value=False, interactive=False)

def on_scan_ui():
    with gr.Column():      
        with gr.Row():
            with gr.Accordion("Scan models for Civitai", open=True):    
                with gr.Row():
                    with gr.Column():
                        scan_models_btn = gr.Button(value="Scan Models",variant="primary") 
                        with gr.Box(elem_classes="cs_box", visible=False) as scanned_result:  
                            scan_models_result = gr.CheckboxGroup(visible=True, label="Scanned Model List").style(item_container=True,container=True)
                with gr.Row(visible=False) as update_information:
                    with gr.Column():
                        with gr.Row():
                            with gr.Column(size=1):
                                scan_register_shortcut = gr.Checkbox(label="Register a shortcut when creating the model information file.", value=True)
                            with gr.Column(size=1):
                                with gr.Row():
                                    scan_save_modelfolder = gr.Checkbox(label="Create a model folder corresponding to the model type.", value=True)
                                    scan_save_vsfolder = gr.Checkbox(label="Create individual model version folder.", value=True) 
                        with gr.Row():
                            with gr.Column():
                                create_models_info_btn = gr.Button(value="Create Model Information",variant="primary")                                                       
        with gr.Row():
            with gr.Accordion("Update Shortcuts", open=True):    
                with gr.Row():
                    with gr.Column():
                        shortcut_saved_update_btn = gr.Button(value="Update the model information for the shortcut",variant="primary")
                        thumb_progress = gr.Markdown(value="###", visible=True)
                    with gr.Column(): 
                        scan_to_shortcut_btn = gr.Button(value="Scan downloaded models for shortcut registration",variant="primary")                    
                        scan_progress = gr.Markdown(value="###", visible=True)

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
        inputs=None,
        outputs=[
            scan_models_result,
            scanned_result,
            update_information,
            scan_save_modelfolder,
            scan_save_vsfolder
        ]                
    )
                 
    scan_to_shortcut_btn.click(
        fn=on_scan_to_shortcut_click,
        inputs=None,
        outputs=[
            scan_progress,
        ]                
    )
    
    shortcut_saved_update_btn.click(
        fn=on_shortcut_saved_update_btn,
        inputs=None,
        outputs=[
            thumb_progress,
        ]
    ) 
    
    thumb_progress.change(
        fn=on_thumb_progress_change,
        inputs=None,
        outputs=[thumb_progress]
    )
    
    scan_progress.change(
        fn=on_scan_progress_change,
        inputs=None,
        outputs=[scan_progress]
    ) 
    
def on_save_btn_click(shortcut_column, gallery_column, classification_gallery_column, usergallery_images_column, usergallery_images_page_limit):    
    environment = dict()
    environment['shortcut_column'] = shortcut_column
    environment['gallery_column'] = gallery_column
    environment['classification_gallery_column'] = classification_gallery_column
    environment['usergallery_images_column'] = usergallery_images_column
    environment['usergallery_images_page_limit'] = usergallery_images_page_limit
    setting.save(environment)
    
    util.printD("Save setting. Reload UI is needed")
                                    
def on_setting_ui():
            
    with gr.Column():       
        with gr.Row():
            with gr.Accordion("Shortcut Browser and Information Images", open=True):    
                with gr.Row():
                    shortcut_column = gr.Slider(minimum=1, maximum=6, value=setting.shortcut_column, step=1, label='Shortcut Browser Column Count', interactive=True)
                    gallery_column = gr.Slider(minimum=1, maximum=12, value=setting.gallery_column, step=1, label='Model Information Column Count', interactive=True)
                    classification_gallery_column = gr.Slider(minimum=1, maximum=12, value=setting.classification_gallery_column, step=1, label='Classification Model Column Count', interactive=True)

        with gr.Row():
            with gr.Accordion("User Gallery Images", open=True):    
                with gr.Row():
                    usergallery_images_column = gr.Slider(minimum=1, maximum=10, value=setting.usergallery_images_column, step=1, label='User Gallery Column Count', interactive=True)
                    usergallery_images_page_limit = gr.Slider(minimum=1, maximum=24, value=setting.usergallery_images_page_limit, step=1, label='User Gallery Images Count Per Page', interactive=True)
                    
        with gr.Row():
            save_btn = gr.Button(value="Save Setting", variant="primary")
                        
    save_btn.click(
        fn=on_save_btn_click,
        inputs=[
            shortcut_column,
            gallery_column,
            classification_gallery_column,
            usergallery_images_column,
            usergallery_images_page_limit
        ],
        outputs=None    
    )   
           


       