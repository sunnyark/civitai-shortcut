import os
import json
import gradio as gr
import datetime
import modules

from . import util
from . import model
from . import civitai
from . import ishortcut
from . import setting
from . import model_action
from . import classification

def on_ui(selected_saved_version_id:gr.Textbox(),selected_saved_model_id:gr.Textbox(),refresh_sc_list:gr.Textbox()):

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
            with gr.Accordion("Delete Civitai Shortcut", open=False):
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
            saved_img_file_info = gr.Textbox(label="Generate Info", interactive=True, lines=6).style(container=True, show_copy_button=True)
        with gr.Row():
            try:
                saved_send_to_buttons = modules.generation_parameters_copypaste.create_buttons(["txt2img", "img2img", "inpaint", "extras"])
            except:
                pass 

        with gr.Row():
            with gr.Accordion("Model Classcification", open=True):
                model_classification = gr.Dropdown(label='Classcification', multiselect=True, interactive=True, choices=classification.get_list())
                model_classification_update_btn = gr.Button(value="Update",variant="primary")
                
    with gr.Row(visible=False): 
        # saved shortcut information  
        saved_img_index = gr.Number(show_label=False)
        saved_images = gr.State() #실제 다운 로드되질 않으니 여기선 안쓰인다. 그냥 둔것임
        saved_images_url = gr.State()
        saved_images_meta = gr.State() # 생성 정보 로드
        
        # 트리거를 위한것
        saved_hidden = gr.Image(type="pil")
        
        saved_refresh_information = gr.Textbox()
        saved_refresh_gallery = gr.Textbox()
    try:
        modules.generation_parameters_copypaste.bind_buttons(saved_send_to_buttons, saved_hidden,saved_img_file_info)
    except:
        pass
    
    model_classification_update_btn.click(
        fn=on_model_classification_update_btn_click,
        inputs=[
            model_classification,
            selected_saved_model_id
        ],
        outputs=[refresh_sc_list]
    )
        
    # civitai saved model information start
    shortcut_del_btn.click(
        fn=on_shortcut_del_btn_click,
        inputs=[
            selected_saved_model_id,
        ],
        outputs=[refresh_sc_list]
    )
    
    saved_update_information_btn.click(
        fn=on_saved_update_information_btn_click,
        inputs=[
            selected_saved_model_id,
        ],
        outputs=[
            selected_saved_model_id,
            refresh_sc_list,
            # 이건 진행 상황을 표시하게 하기 위해 넣어둔것이다.
            saved_gallery,
            saved_refresh_information, #information update 용
            saved_refresh_gallery
        ]
    )
        
    selected_saved_model_id.change(
        fn=on_load_saved_model,
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
            saved_refresh_gallery,
            saved_images_url,
            saved_images_meta,
            saved_img_file_info,
            saved_openfolder,
            model_classification
        ] 
    )
    
    saved_versions_list.select(
        fn=on_saved_versions_list_select,
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
            saved_refresh_gallery,
            saved_images_url,
            saved_images_meta,
            saved_img_file_info,
            saved_openfolder,
            model_classification
        ]
    )    

    #information update 용 start
    saved_refresh_information.change(
        fn=on_load_saved_model,
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
            saved_refresh_gallery,
            saved_images_url,
            saved_images_meta,
            saved_img_file_info,
            saved_openfolder,
            model_classification
        ]
    )
    
    saved_refresh_gallery.change(
        fn=on_file_gallery_loading,
        inputs=[
            saved_images_url 
        ],
        outputs=[               
            saved_gallery,
            saved_images
        ]          
    )
    
    #information update 용 end    
    
    saved_gallery.select(on_gallery_select, saved_images, [saved_img_index, saved_hidden])
    saved_hidden.change(on_civitai_hidden_change,[saved_hidden,saved_img_index,saved_images_meta],[saved_img_file_info])
   
    saved_openfolder.click(on_open_folder_click,[selected_saved_model_id,selected_saved_version_id],None)  
    # civitai saved model information end

def on_model_classification_update_btn_click(model_classification, modelid):
    
    if modelid:
        classification.clean_classification_shortcut(str(modelid))
        
    if model_classification and modelid:
        for name in model_classification:
            classification.add_classification_shortcut(name, str(modelid))
    current_time = datetime.datetime.now()
    return current_time
                
def on_open_folder_click(mid,vid):
    path = model_action.get_model_folder(vid)
    if path:
        util.open_folder(path)

def on_gallery_select(evt: gr.SelectData, civitai_images):
    return evt.index, civitai_images[evt.index]

def on_civitai_hidden_change(hidden, index, civitai_images_meta):
    
    info1,info2,info3 = modules.extras.run_pnginfo(hidden)
    # 이미지에 메타 데이터가 없으면 info 것을 사용한다.
    if not info2:
        info2 = civitai_images_meta[int(index)]        
    return info2

def on_shortcut_del_btn_click(model_id):
    if model_id:
        delete_shortcut_model(model_id)            
    current_time = datetime.datetime.now()
    return current_time

def on_saved_update_information_btn_click(modelid, progress=gr.Progress()):
    if modelid:
        update_shortcut_models([modelid],progress)  
    
    current_time = datetime.datetime.now()
    return gr.update(value=modelid),gr.update(value=current_time),gr.update(value=None),gr.update(value=current_time),gr.update(value=current_time)

def on_load_saved_model(modelid=None, versionid=None):
    return load_saved_model(modelid, versionid)

def on_saved_versions_list_select(evt: gr.SelectData, modelid:str):
    return load_saved_model(modelid, evt.index)
        
def load_saved_model(modelid=None, versionid=None):
    if modelid:
        model_info,versionid,version_name,model_url,downloaded_versions,model_type,versions_list,dhtml,triger,flist,title_name,images_url,images_meta = get_model_information(modelid,None,versionid)    
        if model_info:
            downloaded_info = None
            is_downloaded = False       
            is_visible_openfolder = False
                 
            if downloaded_versions:
                downloaded_info = "\n".join(downloaded_versions.values())
                
                if versionid in downloaded_versions:
                    is_visible_openfolder=True                
                        
            if downloaded_info:
                is_downloaded = True 
                            
            file_text = ""
        
            if flist:
                file_text = "\n".join(flist)
            
            current_time = datetime.datetime.now()
            
            classification_list = classification.get_classification_names_by_modelid(modelid)
                
            return gr.update(value=versionid),gr.update(value=model_url),\
                gr.update(visible = is_downloaded),gr.update(value=downloaded_info),\
                gr.update(value=model_type),gr.update(choices=versions_list,value=version_name),gr.update(value=dhtml),\
                gr.update(value=triger),gr.update(value=file_text),gr.update(label=title_name),\
                current_time,images_url,images_meta,gr.update(value=None),gr.update(visible=is_visible_openfolder),\
                gr.update(choices=classification.get_list(),value=classification_list, interactive=True)

    # 모델 정보가 없다면 클리어 한다.
    # clear model information
    return gr.update(value=None),gr.update(value=None),\
        gr.update(visible=False),gr.update(value=None),\
        gr.update(value=None),gr.update(choices=[setting.NORESULT], value=setting.NORESULT),gr.update(value=None),\
        gr.update(value=None),gr.update(value=None),gr.update(label="#"),\
        None,None,None,gr.update(value=None),gr.update(visible=False),\
        gr.update(choices=classification.get_list(),value=[], interactive=True)

def on_file_gallery_loading(image_url, progress=gr.Progress()):
    chk_image_url = image_url
    if image_url:
        chk_image_url = [img if os.path.isfile(img) else setting.no_card_preview_image for img in image_url]
        # dn_image_list = []
        # for img_url in progress.tqdm(image_url, desc=f"Images Files Loading"):  
        #     dn_image_list.append(Image.open(img_url))                     
        # return dn_image_list       
        return chk_image_url, chk_image_url
    return None, None    

def get_model_information(modelid:str=None, versionid:str=None, ver_index:int=None):
    # 현재 모델의 정보를 가져온다.
    model_info = None
    version_info = None
    
    if modelid:
        model_info = ishortcut.get_model_info(modelid)        
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
                
        return model_info, versionid,version_name,model_url,downloaded_versions,model_type,versions_list,dhtml,triger,flist,title_name,images_url,images_meta
    return None, None,None,None,None,None,None,None,None,None,None,None,None     
    
def get_version_description_gallery(version_info):
    modelid = None
    versionid = None
    ver_images = dict()
    
            
    if not version_info:
        return None,None

    if "modelId" in version_info.keys():
        modelid = str(version_info['modelId'])   
            
    if "id" in version_info.keys():
        versionid = str(version_info['id'])

    if "images" in version_info.keys():
        ver_images = version_info['images']

    images_url = list()
    images_meta = list()
    
    try:        
        for ver in ver_images:
            description_img = setting.get_image_url_to_shortcut_file(modelid,versionid,ver['url'])
            meta_string = ""
            if os.path.isfile(description_img):               
                meta_string = util.convert_civitai_meta_to_stable_meta(ver['meta'])
                images_url.append(description_img)
                images_meta.append(meta_string)                    
    except:
        return None,None
                
    return images_url,images_meta                  
    
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
                model_info = ishortcut.get_model_info(model_id)

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
                files_name.append(file['name'])
                html_dnurlpart = html_dnurlpart + f"<br><a href={file['downloadUrl']}><b>Download << Here</b></a>"     
                            
        output_html = html_typepart + html_modelpart + html_versionpart + html_creatorpart + html_trainingpart + "<br>" +  html_model_tags + "<br>" +  html_modelurlpart + html_dnurlpart + "<br>" + html_descpart + "<br>" + html_imgpart
        
        return output_html, output_training, files_name             
    
    return "",None,None    

def get_thumbnail_list(shortcut_types=None, only_downloaded=False, search=None):
    
    shortlist =  ishortcut.get_image_list(shortcut_types, search)
    if not shortlist:
        return None
    
    if only_downloaded:
        if model.Downloaded_Models:                
            downloaded_list = list()            
            for short in shortlist:
                sc_name = short[1]
                mid = setting.get_modelid_from_shortcutname(sc_name)
                if mid in model.Downloaded_Models.keys():
                    downloaded_list.append(short)
            return downloaded_list
    else:
        return shortlist
    return None

def get_thumbnail_list2(shortcut_types=None, show_downloaded=None, search=None):
    
    shortlist =  ishortcut.get_image_list(shortcut_types, search)
    if not shortlist:
        return None
    
    if show_downloaded:
        if show_downloaded == 'Downloaded':
            if model.Downloaded_Models:                
                downloaded_list = list()            
                for short in shortlist:
                    sc_name = short[1]
                    mid = setting.get_modelid_from_shortcutname(sc_name)
                    if mid in model.Downloaded_Models.keys():
                        downloaded_list.append(short)
                return downloaded_list
        elif show_downloaded == 'Not Downloaded':   
            if model.Downloaded_Models:                
                downloaded_list = list()            
                for short in shortlist:
                    sc_name = short[1]
                    mid = setting.get_modelid_from_shortcutname(sc_name)
                    if mid not in model.Downloaded_Models.keys():
                        downloaded_list.append(short)
                return downloaded_list
            return shortlist
        else:
            return shortlist        
    else:
        return shortlist
    return None
    
def upload_shortcut_by_files(files, register_information_only, progress):
    modelids = list()
    if files:
        shortcut = None
        add_ISC = dict()
        for file in progress.tqdm(files, desc=f"Civitai Shortcut"):                        
            shortcut = util.load_InternetShortcut(file.name)            
            if shortcut:                                  
                model_id = util.get_model_id_from_url(shortcut)                
                if model_id:                    
                    add_ISC = ishortcut.add(add_ISC, model_id, register_information_only, progress)
                    modelids.append(model_id)
                      
        ISC = ishortcut.load()
        if ISC:
            ISC.update(add_ISC)
        else:
            ISC = add_ISC            
        ishortcut.save(ISC)
        
    return modelids

def upload_shortcut_by_urls(urls, register_information_only, progress):
    modelids = list()
    if urls:
        add_ISC = dict()
        for url in progress.tqdm(urls, desc=f"Civitai Shortcut"):                        
            if url:                                  
                model_id = util.get_model_id_from_url(url)
                if model_id:                    
                    add_ISC = ishortcut.add(add_ISC, model_id, register_information_only, progress)
                    modelids.append(model_id)
                      
        ISC = ishortcut.load()
        if ISC:
            ISC.update(add_ISC)
        else:
            ISC = add_ISC            
        ishortcut.save(ISC)
        
    return modelids

def update_shortcut_model(modelid):
    if modelid:
        add_ISC = dict()                
        add_ISC = ishortcut.add(add_ISC, modelid)           
        
        ISC = ishortcut.load()
        if ISC:
            ISC.update(add_ISC)
        else:
            ISC = add_ISC            
        ishortcut.save(ISC)

def update_shortcut_models(modelid_list, progress):
    if not modelid_list:       
        return
    
    add_ISC = dict()                
    for k in progress.tqdm(modelid_list,desc="Updating Models Information"):        
        if k:
            # ishortcut.delete_model_information(str(k))
            add_ISC = ishortcut.add(add_ISC,str(k),False,progress)
                    
        ISC = ishortcut.load()
        if ISC:
            ISC.update(add_ISC)
        else:
            ISC = add_ISC            
        ishortcut.save(ISC)

def update_all_shortcut_model(progress):
    preISC = ishortcut.load()                           
    if not preISC:
        return
    
    modelid_list = [k for k in preISC]
    update_shortcut_models(modelid_list,progress)
                    
def delete_shortcut_model(modelid):
    if modelid:
        ISC = ishortcut.load()                           
        ISC = ishortcut.delete(ISC, modelid)
        ishortcut.save(ISC) 
            
def scan_downloadedmodel_to_shortcut(progress):        
    add_ISC = dict()

    # util.printD(len(model.Downloaded_Models))
    if model.Downloaded_Models:
        modelid_list = [k for k in model.Downloaded_Models]
        for modelid in progress.tqdm(modelid_list, desc=f"Scanning Models"):        
            if modelid:
                # ishortcut.delete_model_information(str(modelid))
                add_ISC = ishortcut.add(add_ISC, str(modelid),False,progress)
            
    ISC = ishortcut.load()
    if ISC:
        ISC.update(add_ISC)
    else:
        ISC = add_ISC            
    ishortcut.save(ISC) 
        