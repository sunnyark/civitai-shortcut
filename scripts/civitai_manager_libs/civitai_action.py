import os
import shutil
import requests
import threading
import gradio as gr
import datetime
import modules

from . import util
from . import model
from . import civitai
from . import setting
from . import downloader
from . import classification

from tqdm import tqdm
from PIL import Image

def on_ui(selected_version_id:gr.Textbox(),selected_model_id:gr.Textbox(),refresh_sc_list:gr.Textbox()):
    
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
                vs_folder = gr.Checkbox(label="Create individual folders with the following", value=True)               
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
            img_file_info = gr.Textbox(label="Generate Info", interactive=True, lines=6).style(container=True, show_copy_button=True)
        with gr.Row():
            try:
                send_to_buttons = modules.generation_parameters_copypaste.create_buttons(["txt2img", "img2img", "inpaint", "extras"])
            except:
                pass      
        with gr.Row():
            with gr.Accordion("Model Classcification", open=True):
                model_classification = gr.Dropdown(label='Classcification', multiselect=True, interactive=True, choices=classification.get_list())
                model_classification_update_btn = gr.Button(value="Update",variant="primary")
            
            
    with gr.Row(visible=False):
        #civitai model information                
        img_index = gr.Number(value=-1, show_label=False)
        civitai_images = gr.State() # 로드된 image_list
        civitai_images_url = gr.State() # 이미지 로드를 위한 url변수
        civitai_images_meta = gr.State() # 생성 정보 로드

        # 트리거를 위한것
        hidden = gr.Image(type="pil")

        refresh_information = gr.Textbox()
        refresh_gallery = gr.Textbox()
        
    try:
        modules.generation_parameters_copypaste.bind_buttons(send_to_buttons, hidden, img_file_info)
    except:
        pass

    model_classification_update_btn.click(
        fn=on_model_classification_update_btn_click,
        inputs=[
            model_classification,
            selected_model_id
        ],
        outputs=[refresh_sc_list]
    )        

    download_model.click(
        fn=on_download_model_click,
        inputs=[
            selected_version_id,
            filename_list,            
            # an_lora,
            vs_folder,
            vs_folder_name
        ],
        outputs=[refresh_sc_list,refresh_information,refresh_gallery]
    )  

    selected_model_id.change(
        fn=on_load_model,
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
            refresh_gallery, 
            civitai_images_url,
            civitai_images_meta,
            img_file_info,
            civitai_openfolder,
            vs_folder_name,
            model_classification
        ] 
    )
    
    versions_list.select(
        fn=on_versions_list_select,
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
            refresh_gallery, 
            civitai_images_url,       
            civitai_images_meta,     
            img_file_info,
            civitai_openfolder,
            vs_folder_name,
            model_classification
        ]
    )    

    refresh_gallery.change(
        fn=on_civitai_gallery_loading,
        inputs=[
            civitai_images_url,
        ],
        outputs=[
            civitai_gallery,
            civitai_images,
        ]     
    )

    refresh_information.change(
        fn=on_load_model,
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
            refresh_gallery, 
            civitai_images_url,
            civitai_images_meta,
            img_file_info,
            civitai_openfolder,
            vs_folder_name,
            model_classification
        ]         
    )
            
    civitai_gallery.select(on_gallery_select, civitai_images, [img_index, hidden])    
    
    hidden.change(on_civitai_hidden_change,[img_index,civitai_images_meta],[img_file_info])
    
    civitai_openfolder.click(on_open_folder_click,[selected_model_id,selected_version_id],None)    

    vs_folder.change(lambda x:gr.update(visible=x),vs_folder,vs_folder_name)

def on_model_classification_update_btn_click(model_classification, modelid):
    
    if modelid:
        classification.clean_classification_shortcut(str(modelid))
        
    if model_classification and modelid:
        for name in model_classification:
            classification.add_classification_shortcut(name, str(modelid))
    current_time = datetime.datetime.now()
    return current_time
    
def on_load_model(modelid=None, versionid=None):
    return load_model(modelid,versionid)

def on_versions_list_select(evt: gr.SelectData, modelid:str):
    return load_model(modelid,evt.index)

def load_model(modelid, versionid):
    if modelid:
        model_info,versionid,version_name,model_url,downloaded_versions_list,model_type,versions_list,dhtml,triger,flist,title_name,images_url,images_meta,vs_foldername = get_model_information(modelid,None,versionid)    
        if model_info:
            # is_lora = False
            downloaded_info = None
            is_downloaded = False            
            is_visible_openfolder = False
            
            # if model_type == setting.model_types['lora'] or model_type == setting.model_types['locon']:
            #     is_lora = True 

            if downloaded_versions_list:
                downloaded_info = "\n".join(downloaded_versions_list.values())
                
                if versionid in downloaded_versions_list:
                    is_visible_openfolder=True                
                        
            if downloaded_info:
                is_downloaded = True 
            
            current_time = datetime.datetime.now()
                
            classification_list = classification.get_classification_names_by_modelid(modelid)
                                
            return gr.update(value=versionid),gr.update(value=model_url),gr.update(visible = is_downloaded),gr.update(value=downloaded_info),\
                gr.update(value=model_type),gr.update(choices=versions_list,value=version_name),gr.update(value=dhtml),\
                gr.update(value=triger),gr.update(choices=flist if flist else [], value=flist if flist else []),gr.update(label=title_name),\
                current_time,images_url,images_meta,gr.update(value=None),gr.update(visible=is_visible_openfolder),gr.update(value=vs_foldername),\
                gr.update(choices=classification.get_list(),value=classification_list)

    # 모델 정보가 없다면 클리어 한다.
    # clear model information
    return gr.update(value=None),gr.update(value=None),gr.update(visible=False),gr.update(value=None),\
        gr.update(value=None),gr.update(choices=[setting.NORESULT], value=setting.NORESULT),gr.update(value=None),\
        gr.update(value=None),gr.update(choices=[], value=None),gr.update(label="#"),\
        None,None,None,gr.update(value=None),gr.update(visible=False),gr.update(value=None),\
        gr.update(choices=classification.get_list(), value=[], interactive=True)

def on_civitai_gallery_loading(image_url, progress=gr.Progress()):
    if image_url:
        dn_image_list = []
        image_list = []
        for i, img_url in enumerate(progress.tqdm(image_url, desc=f"Civitai Images Loading"), start=0):
            
            result = util.is_url_or_filepath(img_url)
            if result == "filepath":
                dn_image_list.append(img_url)
                image_list.append(img_url) 
            elif result == "url":   
                try:
                    with requests.get(img_url,stream=True) as img_r:
                        if not img_r.ok:                        
                            util.printD("Get error code: " + str(img_r.status_code) + ": proceed to the next file")
                            dn_image_list.append(Image.open(setting.no_card_preview_image))
                            image_list.append(setting.no_card_preview_image)
                            continue
                        img_r.raw.decode_content=True
                        dn_image_list.append(Image.open(img_r.raw))
                        image_list.append(img_url)                     
                except:
                    dn_image_list.append(Image.open(setting.no_card_preview_image))
                    image_list.append(setting.no_card_preview_image)
            else:
                dn_image_list.append(Image.open(setting.no_card_preview_image))
                image_list.append(setting.no_card_preview_image)
                
        #return dn_image_list, dn_image_list
        return dn_image_list, image_list
    return None, None    

def on_download_model_click(version_id:str, file_name,vs_folder,vs_foldername):
    msg = None
    if version_id:    
        # 프리뷰이미지와 파일 모두를 다운 받는다.
        msg = download_file_thread(file_name, version_id, False, vs_folder,vs_foldername)
        download_image_files(version_id, False, vs_folder,vs_foldername)
        # 다운 받은 모델 정보를 갱신한다.    
        model.update_downloaded_model()

    current_time = datetime.datetime.now()    
    return gr.update(value=current_time),gr.update(value=current_time),gr.update(value=current_time)    

def on_gallery_select(evt: gr.SelectData, civitai_images):
    return evt.index, civitai_images[evt.index]

def on_open_folder_click(mid,vid):
    path = model.get_model_folder(vid)
    if path:
        util.open_folder(path)

def on_civitai_hidden_change(index, civitai_images_meta):    
    return civitai_images_meta[int(index)]
        
def get_model_information(modelid:str=None, versionid:str=None, ver_index:int=None):
    # 현재 모델의 정보를 가져온다.
    
    model_info = None
    version_info = None
    
    if modelid:
        model_info = civitai.get_model_info(modelid)        
        version_info = dict()
        if model_info:
            if not versionid and not ver_index:
                if "modelVersions" in model_info.keys():
                    version_info = model_info["modelVersions"][0]
                    if version_info["id"]:
                        versionid = version_info["id"]
            elif versionid:
                if "modelVersions" in model_info.keys():
                    for ver in model_info["modelVersions"]:                        
                        if versionid == ver["id"]:
                            version_info = ver                
            else:
                if "modelVersions" in model_info.keys():
                    if len(model_info["modelVersions"]) > 0:
                        version_info = model_info["modelVersions"][ver_index]
                        if version_info["id"]:
                            versionid = version_info["id"]

                            
    # 존재 하는지 판별하고 있다면 내용을 얻어낸다.
    if model_info and version_info:        
        version_name = version_info["name"]
        model_type = model_info['type']                    
        downloaded_versions = model.get_model_downloaded_versions(modelid)       
        versions_list = list()            
        for ver in model_info['modelVersions']:
            versions_list.append(ver['name'])
        
        model_url = civitai.Url_Page() + str(modelid)        
        dhtml, triger, flist = get_version_description(version_info,model_info)
        title_name = f"# {model_info['name']} : {version_info['name']}"           
        
        images_url, images_meta = get_version_description_gallery(version_info)
        
        vs_foldername = setting.generate_version_foldername(model_info['name'],version_name,versionid)        
        model_folder = setting.generate_model_foldername(model_info['name'],model_type,False)
        
        # 정리하자... 
        if os.getcwd() in model_folder and os.path.exists(model_folder):
            info_list = util.scan_folder_for_info(model_folder)
            if info_list:
                for info in info_list:
                    info_dir = os.path.dirname(info)
                    info_basename = os.path.basename(info_dir)
                    if info_dir == model_folder:
                        continue
                    ver_info = util.read_json(info)
                    if not ver_info:
                        continue
                    if 'id' not in ver_info.keys():
                        continue
                    if ver_info['id'] == versionid:
                        vs_foldername = info_basename
                        break
                    
        return model_info, versionid,version_name,model_url,downloaded_versions,model_type,versions_list,dhtml,triger,flist,title_name,images_url,images_meta,vs_foldername
    return None, None,None,None,None,None,None,None,None,None,None,None,None,None

def get_version_description_gallery(version_info:dict):       
    if not version_info:
        return None,None

    versionid = version_info['id']
    modelid = version_info['modelId']
    
    images_url = []
    images_meta = []
    
    if 'images' not in version_info:
        return None,None
        
    for pic in version_info["images"]:  
        meta_string = ""    
        if "meta" in pic:
            meta_string = util.convert_civitai_meta_to_stable_meta(pic["meta"])
                
        if "url" in pic:
            img_url = pic["url"]
            # use max width
            # 파일 인포가 있는 원본 이미지.
            if "width" in pic:
                if pic["width"]:
                    img_url = util.change_width_from_image_url(img_url, pic["width"])
                    
            shortcut_img_file = setting.get_image_url_to_shortcut_file(modelid,versionid,img_url)
            if os.path.isfile(shortcut_img_file):
                # 다운 받은 이미지가 있으면 파일로 대체 그리고 이미지 인포역시
                img_url = shortcut_img_file
                info1,info2,info3 = modules.extras.run_pnginfo(Image.open(shortcut_img_file))
                if info2:
                    meta_string = info2

            images_url.append(img_url)
            images_meta.append(meta_string)                
    return images_url, images_meta

          

      
def get_version_description(version_info:dict,model_info:dict=None):
    output_html = ""
    output_training = ""

    files_name = []
    
    html_typepart = ""
    html_creatorpart = ""
    html_trainingpart = ""
    html_modelpart = ""
    html_versionpart = ""
    html_descpart = ""
    html_dnurlpart = ""
    html_imgpart = ""
    html_modelurlpart = ""
    html_model_tags = ""
        
    model_id = None

    if version_info:        
        if 'modelId' in version_info:            
            model_id = version_info['modelId']  
            if not model_info:            
                model_info = civitai.get_model_info(model_id)

    if version_info and model_info:
        
        html_typepart = f"<br><b>Type: {model_info['type']}</b>"    
        model_url = civitai.Url_Page()+str(model_id)

        html_modelpart = f'<br><b>Model: <a href="{model_url}" target="_blank">{model_info["name"]}</a></b>'
        html_modelurlpart = f'<br><b><a href="{model_url}" target="_blank">Civitai Hompage << Here</a></b><br>'

        model_version_name = version_info['name']

        if 'trainedWords' in version_info:  
            output_training = ", ".join(version_info['trainedWords'])
            html_trainingpart = f'<br><b>Training Tags:</b> {output_training}'

        model_uploader = model_info['creator']['username']
        html_creatorpart = f"<br><b>Uploaded by:</b> {model_uploader}"

        if 'description' in version_info:  
            if version_info['description']:
                html_descpart = f"<br><b>Version : {version_info['name']} Description</b><br>{version_info['description']}<br>"

        if 'tags' in model_info:  
            if model_info['tags']:
                model_tags = [tag["name"] for tag in model_info["tags"]]
                if len(model_tags) > 0:
                    html_model_tags = "<br><b>Model Tags:</b>"
                    for tag in model_tags:
                        html_model_tags = html_model_tags + f"<b> [{tag}] </b>"
                                        
        if 'description' in model_info:  
            if model_info['description']:
                html_descpart = html_descpart + f"<br><b>Description</b><br>{model_info['description']}<br>"
                    
        html_versionpart = f"<br><b>Version:</b> {model_version_name}"

        if 'files' in version_info:                                
            for file in version_info['files']:
                files_name.append(f"{file['id']}:{file['name']}")
                html_dnurlpart = html_dnurlpart + f"<br><a href={file['downloadUrl']}><b>Download << Here</b></a>"     
                            
        output_html = html_typepart + html_modelpart + html_versionpart + html_creatorpart + html_trainingpart + "<br>" +  html_model_tags + "<br>" +  html_modelurlpart + html_dnurlpart + "<br>" + html_descpart + "<br>" + html_imgpart
        
        return output_html, output_training, files_name             
    
    return "",None,None

def add_number_to_duplicate_files(filenames)->dict:    
    counts = {}
    dup_file = {}
    
    for file in filenames:     
        file_info = file.split(":", 1)
        if len(file_info) > 1:
            if file_info[1] in counts:
                name, ext = os.path.splitext(file_info[1])
                counts[file_info[1]] += 1
                file_info[1] = f"{name} ({counts[file_info[1]]}){ext}"
            else:
                counts[file_info[1]] = 0        
            dup_file[file_info[0]] = file_info[1]
    return dup_file
    
def download_file_thread(file_name, version_id, lora_an, vs_folder, vs_foldername=None):               
    if not file_name:
        return

    if not version_id:
        return
    
    version_info = civitai.get_version_info_by_version_id(version_id)
    
    if not version_info:
        return 
       
    download_files = civitai.get_files_by_version_info(version_info)
    
    if not download_files:
        return

    model_folder = util.make_version_folder(version_info, lora_an , vs_folder, vs_foldername)
    
    if not model_folder:
        return

    dup_names = add_number_to_duplicate_files(file_name)
    
    for fid, file in dup_names.items():                    
        try:
            #모델 파일 저장
            path_dl_file = os.path.join(model_folder, file)            
            thread = threading.Thread(target=downloader.download_file,args=(download_files[str(fid)]['downloadUrl'], path_dl_file))
            # Start the thread
            thread.start()                
        except Exception as e:
            util.printD(e)
            pass
        
    # 저장할 파일명을 생성한다.
    savefile_base = get_save_base_name(version_info)
                                
    path_file = os.path.join(model_folder, f"{util.replace_filename(savefile_base)}{setting.info_suffix}{setting.info_ext}")
    info_file = civitai.write_version_info(path_file, version_info)
    if info_file:
        util.printD(f"Wrote version info : {path_file}")

    path_file = os.path.join(model_folder, f"{util.replace_filename(savefile_base)}{setting.triger_suffix}{setting.triger_ext}")
    triger_file = civitai.write_triger_words_by_version_info(path_file, version_info)
    if triger_file:
         util.printD(f"Wrote triger words : {path_file}")

    return f"Download started"

def get_save_base_name(version_info):
    # 이미지 파일명도 primary 이름으로 저장한다.
           
    base = None    
    primary_file = civitai.get_primary_file_by_version_info(version_info)
    if not primary_file:
        base = setting.generate_version_foldername(version_info['model']['name'],version_info['name'],version_info['id'])
    else:
        base, ext = os.path.splitext(primary_file['name'])   
    return base

# def download_preview_image(version_id, lora_an, vs_folder, vs_foldername=None):
#     message =""
#     base = None
    
#     if not version_id:                
#         return         
    
#     version_info = civitai.get_version_info_by_version_id(version_id)          
    
#     if not version_info:
#         return
    
#     if 'images' not in version_info.keys():
#         return
        
#     model_folder = util.make_version_folder(version_info, lora_an , vs_folder,vs_foldername)
    
#     if not model_folder:
#         return

#     base = get_save_base_name(version_info)
#     base = os.path.join(setting.root_path, model_folder, util.replace_filename(base))
    
#     if base and len(base.strip()) > 0:  
#         if "images" in version_info.keys():
#             try:            
#                 img_dict = version_info["images"][0] 
#                 if "url" in img_dict:
#                     img_url = img_dict["url"]
#                     # use max width
#                     if "width" in img_dict:
#                         if img_dict["width"]:
#                             img_url =  util.change_width_from_image_url(img_url, img_dict["width"])
#                     # get image
#                     with requests.get(img_url, stream=True) as img_r:
#                         if not img_r.ok:
#                             util.printD("Get error code: " + str(img_r.status_code))
#                             return
#                         # write to file
#                         description_img = f"{base}{setting.preview_image_suffix}{setting.preview_image_ext}"

#                         with open(description_img, 'wb') as f:
#                             img_r.raw.decode_content = True
#                             shutil.copyfileobj(img_r.raw, f)
#             except Exception as e:
#                 return
#     return

def download_image_files(version_id, lora_an, vs_folder,vs_foldername=None):
    message =""
    base = None
    preview_base = None
    
    if not version_id:                
        return         
    
    version_info = civitai.get_version_info_by_version_id(version_id)          
    
    if not version_info:
        return
    
    if 'images' not in version_info.keys():
        return
        
    model_folder = util.make_version_folder(version_info, lora_an , vs_folder,vs_foldername)
    
    if not model_folder:
        return

    base = get_save_base_name(version_info)
    base = os.path.join(setting.root_path, model_folder, util.replace_filename(base))
    
    if base and len(base.strip()) > 0:                                           
        #image_count = 0 
        
        for image_count, img_dict in enumerate(tqdm(version_info["images"], desc=f"Download image"), start=0):
            # if "nsfw" in img_dict:
            #     if img_dict["nsfw"]:
            #         printD("This image is NSFW")

            if "url" in img_dict:
                img_url = img_dict["url"]
                # use max width
                if "width" in img_dict:
                    if img_dict["width"]:
                        img_url =  util.change_width_from_image_url(img_url, img_dict["width"])
                
                try:
                    # get image
                    with requests.get(img_url, stream=True) as img_r:
                        if not img_r.ok:
                            util.printD("Get error code: " + str(img_r.status_code) + ": proceed to the next file")
                            continue
                        
                        image_id, ext = os.path.splitext(os.path.basename(img_url))

                        # write to file
                        description_img = f'{base}-{version_id}-{image_id}{setting.preview_image_suffix}{setting.preview_image_ext}'
                        with open(description_img, 'wb') as f:
                            img_r.raw.decode_content = True
                            shutil.copyfileobj(img_r.raw, f)
                                                    
                        if image_count == 0:
                            #프리뷰는 호환성 때문에 filename에 따라간다. 둘다 가지고 있자
                            preview_img = f'{base}{setting.preview_image_suffix}{setting.preview_image_ext}'                           
                            shutil.copyfile(description_img, preview_img)

                except Exception as e:
                    pass
                
                # set image_counter
                image_count = image_count + 1
            
        message = f"Downloaded images"
    return message       
