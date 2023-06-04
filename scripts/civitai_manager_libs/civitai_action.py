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
from . import ishortcut_action 

from PIL import Image

   
def on_ui(refresh_sc_list:gr.Textbox()):
    with gr.Column(scale=3):
        with gr.Accordion("#", open=True) as model_title_name:            
            versions_list = gr.Dropdown(label="Model Version", choices=[setting.NORESULT], interactive=True, value=setting.NORESULT)
            with gr.Row():
                update_information_btn = gr.Button(value="Update Model Information")
                with gr.Accordion("Delete Civitai Shortcut", open=False):
                    shortcut_del_btn = gr.Button(value="Delete Shortcut")
        with gr.Tabs():    
            with gr.TabItem("Images" , id="Model_Images"): 
                civitai_gallery = gr.Gallery(show_label=False, elem_id="civitai_gallery").style(grid=[setting.gallery_column], height=setting.information_gallery_height, object_fit=setting.gallery_thumbnail_image_style)        
                with gr.Row():
                    download_images = gr.Button(value="Download Images")
                    open_image_folder = gr.Button(value="Open Download Image Folder")
            with gr.TabItem("Description" , id="Model_Description"): 
                description_html = gr.HTML()
            with gr.TabItem("Download" , id="Model_Download"): 
                gr.Markdown("Downloadable Files")
                downloadable_files = gr.DataFrame(
                        headers=["","ID","Filename","Type","SizeKB","DownloadUrl"],
                        datatype=["str","str","str","str","str","str"], 
                        col_count=(6,"fixed"),
                        interactive=False,
                        type="array",
                    )                  
                filename_list = gr.CheckboxGroup (show_label=False , label="Model Version File", choices=[], value=[], interactive=True, visible=False)                 
            
                cs_foldername = gr.Dropdown(label='Download Folder Select', multiselect=None, choices=[setting.CREATE_MODEL_FOLDER] + classification.get_list(), value=setting.CREATE_MODEL_FOLDER, interactive=True)
                vs_folder = gr.Checkbox(label="Create individual version folder", value=False, visible=True , interactive=True)               
                vs_folder_name = gr.Textbox(label="Folder name to create", value="", show_label=False, interactive=True, lines=1, visible=False).style(container=True)
                download_model = gr.Button(value="Download", variant="primary")
                gr.Markdown("Downloading may take some time. Check console log for detail")     
                                                           
    with gr.Column(scale=1):
        with gr.Tabs() as info_tabs:
            with gr.TabItem("Information" , id="Model_Information"):
                model_type = gr.Textbox(label="Model Type", value="", interactive=False, lines=1)
                trigger_words = gr.Textbox(label="Trigger Words", value="", interactive=False, lines=1).style(container=True, show_copy_button=True)
                civitai_model_url_txt = gr.Textbox(label="Model Url", value="", interactive=False , lines=1).style(container=True, show_copy_button=True)

                with gr.Row():                        
                    with gr.Column():
                        with gr.Accordion("Classcification", open=True):
                            model_classification = gr.Dropdown(label='Classification', show_label=False ,multiselect=True, interactive=True, choices=classification.get_list())
                            model_classification_update_btn = gr.Button(value="Update",variant="primary")     
                                                                                    
                        with gr.Accordion("Downloaded Version", open=True, visible=False)  as downloaded_tab:
                            downloaded_info = gr.Textbox(interactive=False,show_label=False)
                            civitai_openfolder = gr.Button(value="Open Download Folder",variant="primary" , visible=False)
                with gr.Row():
                    with gr.Column():   
                        refresh_btn = gr.Button(value="Refresh")
                        
            with gr.TabItem("Image Information" , id="Image_Information"):  
                with gr.Column():
                    img_file_info = gr.Textbox(label="Generate Info", interactive=True, lines=6).style(container=True, show_copy_button=True)
                    try:
                        send_to_buttons = modules.generation_parameters_copypaste.create_buttons(["txt2img", "img2img", "inpaint", "extras"])
                    except:
                        pass
                                                
    with gr.Row(visible=False):
        selected_model_id  = gr.Textbox()
        selected_version_id = gr.Textbox()
        
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

    downloadable_files.select(
        fn=on_downloadable_files_select,
        inputs=[
            downloadable_files,
            filename_list
        ],
        outputs=[
            downloadable_files,
            filename_list,
        ]
    ) 
    
    gallery = refresh_gallery.change(
        fn=on_civitai_gallery_loading,
        inputs=[
            civitai_images_url,
        ],
        outputs=[
            civitai_gallery,
            civitai_images,
        ]     
    )

    # civitai saved model information start
    shortcut_del_btn.click(
        fn=on_shortcut_del_btn_click,
        inputs=[
            selected_model_id,
        ],
        outputs=[
            refresh_sc_list
        ]
    )
    
    update_information_btn.click(
        fn=on_update_information_btn_click,
        inputs=[
            selected_model_id,
        ],
        outputs=[
            selected_model_id,
            refresh_sc_list,
            civitai_gallery,
            refresh_information #information update 용
        ]
    )
        
    model_classification_update_btn.click(
        fn=on_model_classification_update_btn_click,
        inputs=[
            model_classification,
            selected_model_id
        ],
        outputs=[
            refresh_sc_list
        ]
    )        

    cs_foldername.select(    
        fn=on_cs_foldername_select,
        inputs=None,
        outputs=[
            vs_folder,
            vs_folder_name
        ]          
    )
    
    download_model.click(
        fn=on_download_model_click,
        inputs=[
            selected_version_id,
            filename_list,            
            vs_folder,
            vs_folder_name,
            cs_foldername,
        ],
        outputs=[
            refresh_sc_list,
            refresh_information
        ]
    )  

    download_images.click(
        fn=on_download_images_click,
        inputs=[
            selected_version_id,
            civitai_images_url              
        ],
        outputs=None 
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
            model_type, 
            versions_list,
            description_html,
            trigger_words,
            filename_list,
            downloadable_files,
            model_title_name,                        
            refresh_gallery, 
            civitai_images_url,
            civitai_images_meta,
            img_file_info,
            civitai_openfolder,
            vs_folder,
            vs_folder_name,
            model_classification,
            cs_foldername
        ],
        cancels=gallery
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
            model_type, 
            versions_list,
            description_html,
            trigger_words,
            filename_list,
            downloadable_files,
            model_title_name,                        
            refresh_gallery, 
            civitai_images_url,       
            civitai_images_meta,     
            img_file_info,
            civitai_openfolder,
            vs_folder,            
            vs_folder_name,
            model_classification,
            cs_foldername
        ],
        cancels=gallery
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
            model_type, 
            versions_list,
            description_html,
            trigger_words,
            filename_list,
            downloadable_files,
            model_title_name,                        
            refresh_gallery, 
            civitai_images_url,
            civitai_images_meta,
            img_file_info,
            civitai_openfolder,
            vs_folder,            
            vs_folder_name,
            model_classification,
            cs_foldername
        ],
        cancels=gallery
    )

    refresh_btn.click(lambda :datetime.datetime.now(),None,refresh_information,cancels=gallery)             
    civitai_gallery.select(on_gallery_select, civitai_images, [img_index, hidden, info_tabs])    
    hidden.change(on_civitai_hidden_change,[hidden,img_index,civitai_images_meta],[img_file_info])
    civitai_openfolder.click(on_open_folder_click,[selected_model_id,selected_version_id],None)    
    vs_folder.change(lambda x:gr.update(visible=x),vs_folder,vs_folder_name)
    
    open_image_folder.click(on_open_image_folder_click,[selected_model_id],None)
    
    return selected_model_id , refresh_information

def on_open_image_folder_click(modelid):
    if modelid:                
        model_info = civitai.get_model_info(modelid)
        if model_info:  
            model_name = model_info['name']
            image_folder = util.get_download_image_folder(model_name)
            if image_folder:
                util.open_folder(image_folder)
                
def on_downloadable_files_select(evt: gr.SelectData, df, filenames):
    # util.printD(evt.index)
    # index[0] # 행,열
    vid = None
    vname = None
    dn_name = None
    
    if df:
        vid = df[evt.index[0]][1]
        vname = df[evt.index[0]][2]
        dn_name = f"{vid}:{vname}"

    if vid:        
        if filenames:
            if dn_name in filenames:
                filenames.remove(dn_name)
                df[evt.index[0]][0] = '⬜️'
            else:
                filenames.append(dn_name)
                df[evt.index[0]][0] = '✅'
        else:
            filenames = [dn_name]    
            df[evt.index[0]][0] = '✅'

    return df, gr.update(value=filenames)
    
def on_cs_foldername_select(evt: gr.SelectData):
    if evt.value == setting.CREATE_MODEL_FOLDER:
        return gr.update(visible=True,value=False),gr.update(visible=False)
    return gr.update(visible=False,value=False),gr.update(visible=False)

def on_model_classification_update_btn_click(model_classification, modelid):
    
    if modelid:
        classification.clean_classification_shortcut(str(modelid))
        
    if model_classification and modelid:
        for name in model_classification:
            classification.add_classification_shortcut(name, str(modelid))
    current_time = datetime.datetime.now()
    return current_time

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
                            dn_image_list.append(setting.no_card_preview_image)
                            image_list.append(setting.no_card_preview_image)
                        else:
                            img_r.raw.decode_content=True
                            dn_image_list.append(Image.open(img_r.raw))
                            image_list.append(img_url)                     
                except:
                    dn_image_list.append(setting.no_card_preview_image)
                    image_list.append(setting.no_card_preview_image)
            else:
                dn_image_list.append(setting.no_card_preview_image)
                image_list.append(setting.no_card_preview_image)
               
        return dn_image_list, image_list
        # return dn_image_list, dn_image_list
    return None, None    

def on_download_model_click(version_id, file_name, vs_folder, vs_foldername, cs_foldername=None):
    msg = None
    if version_id:    
        # 프리뷰이미지와 파일 모두를 다운 받는다.
        if cs_foldername == setting.CREATE_MODEL_FOLDER:
            msg = download_file_thread(file_name, version_id, True, vs_folder, vs_foldername, None)
        else:
            msg = download_file_thread(file_name, version_id, False, False, None , cs_foldername)
            
        # 다운 받은 모델 정보를 갱신한다.    
        model.update_downloaded_model()

        current_time = datetime.datetime.now()    
        return gr.update(value=current_time),gr.update(value=current_time)    
    return gr.update(visible=True),gr.update(visible=True)

def on_download_images_click(version_id:str, images_url):
    msg = None
    if version_id:        
        version_info = civitai.get_version_info_by_version_id(version_id)              
        if not version_info:
            return

        if "model" not in version_info.keys():
            return
            
        downloader.download_image_file(version_info['model']['name'], images_url)
    current_time = datetime.datetime.now()    

def on_gallery_select(evt: gr.SelectData, civitai_images):
    return evt.index, civitai_images[evt.index], gr.update(selected="Image_Information")

def on_open_folder_click(mid,vid):
    path = model.get_default_version_folder(vid)
    if path:
        util.open_folder(path)

def on_shortcut_del_btn_click(model_id):
    if model_id:
        ishortcut_action.delete_shortcut_model(model_id)            
    current_time = datetime.datetime.now()
    return current_time

def on_update_information_btn_click(modelid, progress=gr.Progress()):
    if modelid:
        ishortcut_action.update_shortcut_models([modelid],progress)  
    
        current_time = datetime.datetime.now()
        return gr.update(value=modelid),gr.update(value=current_time),gr.update(value=None),gr.update(value=current_time)
    return gr.update(value=modelid),gr.update(visible=True),gr.update(value=None),gr.update(visible=True)

def on_civitai_hidden_change(hidden, index, civitai_images_meta):    
    info1,info2,info3 = modules.extras.run_pnginfo(hidden)
    # 이미지에 메타 데이터가 없으면 info 것을 사용한다.
    if not info2:
        info2 = civitai_images_meta[int(index)]        
    return info2

def on_load_model(modelid=None, ver_index=None):
    return load_model(modelid, ver_index)

def on_versions_list_select(evt: gr.SelectData, modelid:str):
    return load_model(modelid, evt.index)

def load_model(modelid, ver_index):
    if modelid:
        model_info,versionid,version_name,model_url,downloaded_versions_list,model_type,versions_list,dhtml,triger,files,title_name,images_url,images_meta,vs_foldername = get_model_information(modelid,None,ver_index)    
        if model_info:
            downloaded_info = None
            is_downloaded = False            
            is_visible_openfolder = False

            if downloaded_versions_list:
                downloaded_info = "\n".join(downloaded_versions_list.values())
                
                if versionid in downloaded_versions_list:
                    is_visible_openfolder=True                
                        
            if downloaded_info:
                is_downloaded = True 
            
            current_time = datetime.datetime.now()
                
            classification_list = classification.get_classification_names_by_modelid(modelid)
                
            flist = list()
            downloadable = list()
            for file in files:            
                flist.append(f"{file['id']}:{file['name']}")
                downloadable.append(['✅',file['id'],file['name'],file['type'],round(file['sizeKB']),file['downloadUrl']])
                                                                            
            return gr.update(value=versionid),gr.update(value=model_url),gr.update(visible = is_downloaded),gr.update(value=downloaded_info),\
                gr.update(value=setting.get_ui_typename(model_type)),gr.update(choices=versions_list,value=version_name),gr.update(value=dhtml),\
                gr.update(value=triger),gr.update(choices=flist if flist else [], value=flist if flist else []), downloadable if len(downloadable) > 0 else None,\
                gr.update(label=title_name),\
                current_time,images_url,images_meta,gr.update(value=None),gr.update(visible=is_visible_openfolder),gr.update(value=False, visible=True),gr.update(value=vs_foldername, visible=False),\
                gr.update(choices=classification.get_list(),value=classification_list),\
                gr.update(choices=[setting.CREATE_MODEL_FOLDER] + classification.get_list(), value=setting.CREATE_MODEL_FOLDER)

    # 모델 정보가 없다면 클리어 한다.
    # clear model information
    return gr.update(value=None),gr.update(value=None),gr.update(visible=False),gr.update(value=None),\
        gr.update(value=None),gr.update(choices=[setting.NORESULT], value=setting.NORESULT),gr.update(value=None),\
        gr.update(value=None),gr.update(choices=[], value=None),None,\
        gr.update(label="#"),\
        None,None,None,gr.update(value=None),gr.update(visible=False),gr.update(value=False, visible=True),gr.update(value="",visible=False),\
        gr.update(choices=classification.get_list(), value=[]),\
        gr.update(choices=[setting.CREATE_MODEL_FOLDER] + classification.get_list(), value=setting.CREATE_MODEL_FOLDER)

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
        dhtml, triger, files = get_version_description(version_info,model_info)
        title_name = f"# {model_info['name']} : {version_info['name']}"           
        
        images_url, images_meta = get_version_description_gallery(version_info)
        
        vs_foldername = setting.generate_version_foldername(model_info['name'],version_name,versionid)

        return model_info, versionid,version_name,model_url,downloaded_versions,model_type,versions_list,dhtml,triger,files,title_name,images_url,images_meta,vs_foldername
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
                img_url = shortcut_img_file
                # info1,info2,info3 = modules.extras.run_pnginfo(Image.open(shortcut_img_file))
                # if info2:
                #     meta_string = info2

            images_url.append(img_url)
            images_meta.append(meta_string)                
    return images_url, images_meta
      
def get_version_description(version_info:dict,model_info:dict=None):
    output_html = ""
    output_training = ""

    files = []
    
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
            model_tags = model_info["tags"]
            if len(model_tags) > 0:
                html_model_tags = "<br><b>Model Tags:</b>"
                for tag in model_tags:
                    html_model_tags = html_model_tags + f"<b> [{tag}]</b>"
                    
        # if 'tags' in model_info:  
        #     if model_info['tags']:
        #         model_tags = [tag["name"] for tag in model_info["tags"]]
        #         if len(model_tags) > 0:
        #             html_model_tags = "<br><b>Model Tags:</b>"
        #             for tag in model_tags:
        #                 html_model_tags = html_model_tags + f"<b> [{tag}] </b>"
                                        
        if 'description' in model_info:  
            if model_info['description']:
                html_descpart = html_descpart + f"<br><b>Description</b><br>{model_info['description']}<br>"
                    
        html_versionpart = f"<br><b>Version:</b> {model_version_name}"

        if 'files' in version_info:                                
            for file in version_info['files']:
                files.append(file)
                # files_name.append(f"{file['id']}:{file['name']}")
                html_dnurlpart = html_dnurlpart + f"<br><a href={file['downloadUrl']}><b>Download << Here</b></a>"     
                            
        output_html = html_typepart + html_modelpart + html_versionpart + html_creatorpart + html_trainingpart + "<br>" +  html_model_tags + "<br>" +  html_modelurlpart + html_dnurlpart + "<br>" + html_descpart + "<br>" + html_imgpart
        
        return output_html, output_training, files            
    
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

def get_save_base_name(version_info):
    # 이미지 파일명도 primary 이름으로 저장한다.
           
    base = None    
    primary_file = civitai.get_primary_file_by_version_info(version_info)
    if not primary_file:
        base = setting.generate_version_foldername(version_info['model']['name'],version_info['name'],version_info['id'])
    else:
        base, ext = os.path.splitext(primary_file['name'])   
    return base
    
def download_file_thread(file_name, version_id, ms_folder, vs_folder, vs_foldername, cs_foldername):               
    # if not file_name:
    #     return

    if not version_id:
        return
    
    version_info = civitai.get_version_info_by_version_id(version_id)
    
    if not version_info:
        return 
       
    download_files = civitai.get_files_by_version_info(version_info)
    
    if not download_files:
        return

    # model_folder = util.make_version_folder(version_info, vs_folder, vs_foldername, ms_foldername)
    model_folder = util.make_download_model_folder(version_info, ms_folder, vs_folder, vs_foldername, cs_foldername)
    
    if not model_folder:
        return

    if file_name:
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

    path_img = os.path.join(model_folder, f"{util.replace_filename(savefile_base)}{setting.preview_image_suffix}{setting.preview_image_ext}")
    preview_file = download_preview_image(path_img, version_info)
    if preview_file:
         util.printD(f"Wrote preview image : {path_img}")
        
    # path_file = os.path.join(model_folder, f"{util.replace_filename(savefile_base)}{setting.triger_suffix}{setting.triger_ext}")
    # triger_file = civitai.write_triger_words_by_version_info(path_file, version_info)
    # if triger_file:
    #      util.printD(f"Wrote triger words : {path_file}")

    return f"Download started"

def download_preview_image(filepath, version_info):
    if not version_info:
        return False
    # save preview            
    if "images" in version_info.keys():
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
                        return False

                    with open(filepath, 'wb') as f:
                        img_r.raw.decode_content = True
                        shutil.copyfileobj(img_r.raw, f)                                                    
        except Exception as e:
            pass
                    
    return True                    

# def download_image_files(version_id, image_urls):    
#     if not version_id:                
#         return      
    
#     version_info = civitai.get_version_info_by_version_id(version_id)          
    
#     if not version_info:
#         return

#     if "model" not in version_info.keys():
#         return

#     model_folder = util.make_download_image_folder(version_info['model']['name'])
    
#     if not model_folder:
#         return
    
#     # save_folder = os.path.join(setting.root_path, model_folder, "images")
#     save_folder = os.path.join(model_folder, "images")
    
#     if not os.path.exists(save_folder):
#         os.makedirs(save_folder)        
        
#     if image_urls and len(image_urls) > 0:                
#         for image_count, img_url in enumerate(tqdm(image_urls, desc=f"Download images"), start=0):

#             result = util.is_url_or_filepath(img_url)
#             if result == "filepath":
#                 if os.path.basename(img_url) != setting.no_card_preview_image:
#                     description_img = os.path.join(save_folder,os.path.basename(img_url))
#                     shutil.copyfile(img_url,description_img)
#             elif result == "url":
#                 try:
#                     # get image
#                     with requests.get(img_url, stream=True) as img_r:
#                         if not img_r.ok:
#                             util.printD("Get error code: " + str(img_r.status_code) + ": proceed to the next file")
#                         else:
#                             # write to file
#                             image_id, ext = os.path.splitext(os.path.basename(img_url))
#                             description_img = os.path.join(save_folder,f'{image_id}{setting.preview_image_suffix}{setting.preview_image_ext}')
#                             with open(description_img, 'wb') as f:
#                                 img_r.raw.decode_content = True
#                                 shutil.copyfileobj(img_r.raw, f)
#                 except Exception as e:
#                     pass
#     return 


