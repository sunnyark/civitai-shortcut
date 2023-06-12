import os
import json
import gradio as gr
import datetime
import modules
import shutil

from . import util
from . import model
from . import civitai
from . import ishortcut
from . import setting
from . import classification
from . import downloader

def on_ui(refresh_sc_browser:gr.Textbox(), recipe_input):
    with gr.Column(scale=3):    
        with gr.Accordion("#", open=True) as model_title_name:               
            versions_list = gr.Dropdown(label="Model Version", choices=[setting.NORESULT], interactive=True, value=setting.NORESULT)             

        with gr.Tabs():
            with gr.TabItem("Images" , id="Model_Images"):                                 
                saved_gallery = gr.Gallery(show_label=False, elem_id="saved_gallery").style(grid=[setting.gallery_column],height=setting.information_gallery_height, object_fit=setting.gallery_thumbnail_image_style)    
                with gr.Row():
                    download_images = gr.Button(value="Download Images")
                    open_image_folder = gr.Button(value="Open Download Image Folder") 
                    change_thumbnail_image = gr.Button(value="Change thumbnail to selected image", variant="primary", visible=True)
                    change_preview_image = gr.Button(value="Change preview to selected image", variant="primary", visible=False)                    
            with gr.TabItem("Description" , id="Model_Description"):                             
                description_html = gr.HTML()       
            with gr.TabItem("Download" , id="Model_Download"): 
                # gr.Markdown("Downloadable Files")                
                gr.Markdown("When you click on the file name, an information window appears where you can change the file name.")
                downloadable_files = gr.DataFrame(
                        headers=["","ID","Filename","Type","SizeKB","Primary","DownloadUrl"],
                        datatype=["str","str","str","str","str","str","str"], 
                        col_count=(7,"fixed"),
                        interactive=False,
                        type="array",
                    )                                
                gr.Markdown("The information file and preview file names are generated based on the primary file. Additionally, the information file and preview file will only be saved if the primary file is included in the download.")
                filename_list = gr.CheckboxGroup (show_label=False , label="Model Version File", choices=[], value=[], interactive=True, visible=False)
                
                with gr.Accordion(label='Change File Name', open=True, visible=False) as change_filename:     
                    with gr.Row():                
                        with gr.Column(scale=4):
                            select_filename = gr.Textbox(label='Please enter the file name you want to change.', interactive=True, visible=True)
                        with gr.Column(scale=1):
                            select_fileid = gr.Textbox(label='The ID of the selected file.', interactive=False, visible=True)
                    with gr.Row():
                        close_filename_btn = gr.Button(value="Cancel", visible=True)
                        change_filename_btn = gr.Button(value="Change file name", variant="primary", visible=True)
                
                with gr.Accordion(label='Select Download Folder', open=True, visible=True):     
                    cs_foldername = gr.Dropdown(label='Can select a classification defined by the user or create a new one as the folder to download the model.', multiselect=False, choices=[setting.CREATE_MODEL_FOLDER] + classification.get_list(), value=setting.CREATE_MODEL_FOLDER, interactive=True)
                    with gr.Row():
                        with gr.Column(scale=2):
                            ms_foldername = gr.Textbox(label="Model folder name for the downloaded model. Please set it to the desired name.", value="", interactive=True, lines=1, visible=True).style(container=True)
                            # ms_foldername = gr.Dropdown(label='This is the name for the model folder to be created. You can either choose from the suggested names or enter your own.', multiselect=False, choices=None, value=None, interactive=True, allow_custom_value=True)
                        with gr.Column(scale=1):
                            ms_suggestedname = gr.Dropdown(label='Suggested names', multiselect=False, choices=None, value=None, interactive=True)                            

                    vs_folder = gr.Checkbox(label="Create separate independent folders for each version under the generated model folder.", value=False, visible=True , interactive=True)
                    vs_foldername = gr.Textbox(label="Folder name to create", value="", show_label=False, interactive=True, lines=1, visible=False).style(container=True)

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
                        with gr.Accordion("Classification", open=True):
                            model_classification = gr.Dropdown(label='Classification', show_label=False ,multiselect=True, interactive=True, choices=classification.get_list())
                            model_classification_update_btn = gr.Button(value="Update",variant="primary")

                        with gr.Accordion("Downloaded Version", open=True, visible=False) as downloaded_tab:                             
                            downloaded_info = gr.Textbox(interactive=False,show_label=False)
                            saved_openfolder = gr.Button(value="Open Download Folder", variant="primary", visible=False)

            with gr.TabItem("Image Information" , id="Image_Information"):      
                with gr.Column():            
                    img_file_info = gr.Textbox(label="Generate Info", interactive=True, lines=6).style(container=True, show_copy_button=True)
                    try:
                        send_to_buttons = modules.generation_parameters_copypaste.create_buttons(["txt2img", "img2img", "inpaint", "extras"])
                    except:
                        pass 
                    send_to_recipe = gr.Button(value="Send To Recipe", variant="primary", visible=True)
                    
        # with gr.Row():
        #     with gr.Column():                                                    
        #         refresh_btn = gr.Button(value="Refresh")                                                                                            
        with gr.Row():
            update_information_btn = gr.Button(value="Update Shortcut")       
            with gr.Accordion("Delete Shortcut", open=False):
                shortcut_del_btn = gr.Button(value="Delete")                      
                            
    with gr.Row(visible=False): 
        selected_model_id = gr.Textbox()
        selected_version_id = gr.Textbox()
        
        # saved shortcut information  
        img_index = gr.Number(show_label=False)
        saved_images = gr.State() # 로드된것
        saved_images_url = gr.State() #로드 해야 하는것
        saved_images_meta = gr.State() # 생성 정보 로드
        
        # 트리거를 위한것
        hidden = gr.Image(type="pil")
        
        refresh_information = gr.Textbox()
        refresh_gallery = gr.Textbox()
        
        loaded_modelid = gr.Textbox()
        
    try:
        modules.generation_parameters_copypaste.bind_buttons(send_to_buttons, hidden, img_file_info)
    except:
        pass
   
    send_to_recipe.click(
        fn=on_send_to_recipe_click,
        inputs=[
            img_file_info,
            img_index,
            saved_images
        ],
        outputs=[recipe_input]
    )
    
    downloadable_files.select(
        fn=on_downloadable_files_select,
        inputs=[
            downloadable_files,
            filename_list
        ],
        outputs=[
            downloadable_files,
            filename_list,
            #==============
            select_fileid,
            select_filename,
            change_filename
        ],
        show_progress=False
    ) 

    cs_foldername.select(    
        fn=on_cs_foldername_select,
        inputs=[vs_folder],
        outputs=[
            vs_folder,
            vs_foldername,
            ms_foldername,
            ms_suggestedname
        ]          
    )
    
    download_model.click(
        fn=on_download_model_click,
        inputs=[
            selected_model_id,
            selected_version_id,
            filename_list,            
            vs_folder,
            vs_foldername,
            cs_foldername,
            ms_foldername
        ],
        outputs=[
            refresh_sc_browser,
            downloaded_tab,
            downloaded_info,
            saved_openfolder,
            change_preview_image
            # refresh_information
        ]
    )  
        
    download_images.click(
        fn=on_download_images_click,
        inputs=[
            selected_model_id,
            saved_images_url              
        ],
        outputs=None 
    )
    
    gallery = refresh_gallery.change(
        fn=on_file_gallery_loading,
        inputs=[
            saved_images_url 
        ],
        outputs=[               
            saved_gallery,
            saved_images
        ]          
    )
        
    model_classification_update_btn.click(
        fn=on_model_classification_update_btn_click,
        inputs=[
            model_classification,
            selected_model_id
        ],
        outputs=[
            refresh_sc_browser
        ]
    )
        
    # civitai saved model information start
    shortcut_del_btn.click(
        fn=on_shortcut_del_btn_click,
        inputs=[
            selected_model_id,
        ],
        outputs=[
            refresh_sc_browser
        ]
    )
    
    update_information_btn.click(
        fn=on_update_information_btn_click,
        inputs=[
            selected_model_id,
        ],
        outputs=[
            selected_model_id,
            refresh_sc_browser,
            # 이건 진행 상황을 표시하게 하기 위해 넣어둔것이다.
            saved_gallery,
            refresh_information #information update 용
        ]
    )       
    
    selected_model_id.change(
        fn=on_load_saved_model,
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
            saved_images_url,
            saved_images_meta,
            img_file_info,
            saved_openfolder,
            change_preview_image,
            model_classification,
            vs_folder,
            vs_foldername,            
            cs_foldername,
            ms_foldername,
            change_filename,
            ms_suggestedname            
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
            saved_images_url,
            saved_images_meta,
            img_file_info,
            saved_openfolder,
            change_preview_image,
            model_classification,
            vs_folder,
            vs_foldername,            
            cs_foldername,
            ms_foldername,
            change_filename,
            ms_suggestedname            
        ],
        cancels=gallery
    )    

    #information update 용 start
    refresh_information.change(
        fn=on_load_saved_model,
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
            saved_images_url,
            saved_images_meta,
            img_file_info,
            saved_openfolder,
            change_preview_image,
            model_classification,
            vs_folder,
            vs_foldername,            
            cs_foldername,
            ms_foldername,
            change_filename,
            ms_suggestedname            
        ],
        cancels=gallery
    )
    
    # refresh_btn.click(lambda :datetime.datetime.now(),None,refresh_information,cancels=gallery)    
    saved_gallery.select(on_gallery_select, saved_images, [img_index, hidden, info_tabs])
    hidden.change(on_civitai_hidden_change,[hidden,img_index,saved_images_meta],[img_file_info])
    saved_openfolder.click(on_open_folder_click,[selected_model_id,selected_version_id],None)  
    vs_folder.change(lambda x:gr.update(visible=x),vs_folder,vs_foldername)
    change_preview_image.click(on_change_preview_image_click,[selected_model_id,selected_version_id,img_index,saved_images],None)
    change_thumbnail_image.click(on_change_thumbnail_image_click,[selected_model_id,img_index,saved_images],[refresh_sc_browser])
    open_image_folder.click(on_open_image_folder_click,[selected_model_id],None)
    
    ms_suggestedname.select(lambda x:x,ms_suggestedname,ms_foldername,show_progress=False)
    
    select_filename.submit(
        fn=on_change_filename_submit,
        inputs=[
            select_fileid,
            select_filename,            
            downloadable_files,
            filename_list,            
        ],
        outputs=[
            select_filename,
            downloadable_files,
            filename_list,
            change_filename            
        ],
        show_progress=False
    )
    
    change_filename_btn.click(
        fn=on_change_filename_submit,
        inputs=[
            select_fileid,
            select_filename,            
            downloadable_files,
            filename_list,            
        ],
        outputs=[
            select_filename,
            downloadable_files,
            filename_list,
            change_filename            
        ],
        show_progress=False
    )
    
    close_filename_btn.click(lambda :gr.update(visible=False),None,change_filename,show_progress=False)
    
    return selected_model_id, refresh_information

def on_send_to_recipe_click(img_file_info, img_index, civitai_images):
    # return img_file_info
    try:
        return civitai_images[int(img_index)]
    except:
        return gr.update(visible=False)

def on_open_image_folder_click(modelid):
    if modelid:                
        model_info = ishortcut.get_model_info(modelid)
        if model_info:  
            model_name = model_info['name']
            image_folder = util.get_download_image_folder(model_name)
            if image_folder:
                util.open_folder(image_folder)

def on_change_filename_submit(select_fileid, select_filename, df, filenames):
    
    if not select_fileid or not select_filename or len(select_filename.strip()) <= 0:
        return gr.update(visible=True), gr.update(visible=True), gr.update(visible=False), gr.update(visible=False)
    
    select_filename = util.replace_filename(select_filename.strip())
    filelist = []
    
    if df:
        for df_row in df:
            
            if str(select_fileid) == str(df_row[1]):
                df_row[2] = select_filename
                
            vid = df_row[1]
            vname = df_row[2]
            dn_name = f"{vid}:{vname}"
            filelist.append(dn_name)
            
    if filenames and select_fileid and select_filename:
        for i, filename in enumerate(filenames): 
            if filename.startswith(f"{select_fileid}:"):
                filenames[i] = f"{select_fileid}:{select_filename}"
        
    return gr.update(visible=True), df, gr.update(choices=filelist, value=filenames), gr.update(visible=False)

def on_downloadable_files_select(evt: gr.SelectData, df, filenames):
    # util.printD(evt.index)
    # index[0] # 행,열
    vid = None
    vname = None
    dn_name = None
    
    row = evt.index[0]
    col = evt.index[1]
    
    # util.printD(f"row : {row} ,col : {col}")
    if col == 0:
        # 파일 선택    
        if df:
            vid = df[row][1]
            vname = df[row][2]
            dn_name = f"{vid}:{vname}"

        if vid:        
            if filenames:
                if dn_name in filenames:
                    filenames.remove(dn_name)
                    df[row][0] = '⬜️'
                else:
                    filenames.append(dn_name)
                    df[row][0] = '✅'
            else:
                filenames = [dn_name]    
                df[row][0] = '✅'
        
        return df, gr.update(value=filenames), gr.update(visible=True), gr.update(visible=True), gr.update(visible=False)   
    
    elif col == 2:
        # 파일 명 변경
        if df:
            vid = df[row][1]
            vname = df[row][2]
            
        return gr.update(visible=True), gr.update(visible=False), gr.update(value=vid), gr.update(value=vname), gr.update(visible=True)
        
    return df, gr.update(value=filenames), gr.update(visible=True), gr.update(visible=True), gr.update(visible=False)

def on_download_images_click(model_id:str, images_url):
    msg = None
    if model_id:        
        model_info = ishortcut.get_model_info(model_id)              
        if not model_info:
            return

        if "name" not in model_info.keys():
            return
            
        downloader.download_image_file(model_info['name'], images_url)
    current_time = datetime.datetime.now() 

def on_download_model_click(model_id, version_id, file_name, vs_folder, vs_foldername, cs_foldername=None, ms_foldername=None):
    msg = None
    if version_id and model_id:    
        # 프리뷰이미지와 파일 모두를 다운 받는다.
        if cs_foldername == setting.CREATE_MODEL_FOLDER:
            msg = downloader.download_file_thread(file_name, version_id, True, vs_folder, vs_foldername, None, ms_foldername)
        else:
            msg = downloader.download_file_thread(file_name, version_id, False, False, None , cs_foldername, ms_foldername)
            
        # 다운 받은 모델 정보를 갱신한다.    
        model.update_downloaded_model()

        downloaded_info = None
        is_downloaded = False       
        is_visible_openfolder = False
        is_visible_changepreview = False
        downloaded_versions = model.get_model_downloaded_versions(model_id)
        if downloaded_versions:
                
            downloaded_info = "\n".join(downloaded_versions.values())

            if str(version_id) in downloaded_versions:
                is_visible_openfolder=True
                is_visible_changepreview = True

        if downloaded_info:
            is_downloaded = True 
                                            
        current_time = datetime.datetime.now()
        
        return gr.update(value=current_time),gr.update(visible = is_downloaded),gr.update(value=downloaded_info),gr.update(visible=is_visible_openfolder),gr.update(visible=is_visible_changepreview)
    return gr.update(visible=True),gr.update(visible=False),gr.update(value=None),gr.update(visible=False),gr.update(visible=False)

def on_cs_foldername_select(evt: gr.SelectData, is_vsfolder):
    if evt.value == setting.CREATE_MODEL_FOLDER:
        return gr.update(visible=True), gr.update(visible=is_vsfolder), gr.update(visible=True), gr.update(visible=True)
    return gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False)
    
def on_model_classification_update_btn_click(model_classification, modelid):
    
    if modelid:
        classification.clean_classification_shortcut(str(modelid))
        
    if model_classification and modelid:
        for name in model_classification:
            classification.add_classification_shortcut(name, str(modelid))
    current_time = datetime.datetime.now()
    return current_time
                
def on_open_folder_click(mid,vid):
    path = model.get_default_version_folder(vid)
    if path:
        util.open_folder(path)

def on_change_thumbnail_image_click(mid, img_idx:int, civitai_images):
    if civitai_images and mid:
        if len(civitai_images) > int(img_idx):
            selected_image_filepath = civitai_images[int(img_idx)]
            
            if not os.path.isfile(selected_image_filepath):
                return gr.update(visible=False)
            
            ishortcut.create_thumbnail(mid, selected_image_filepath)
            
            current_time = datetime.datetime.now()
            return current_time
        
    return gr.update(visible=False)

def on_change_preview_image_click(mid,vid,img_idx:int,civitai_images):
    if civitai_images and vid and mid:
        if len(civitai_images) > int(img_idx):
            selected_image_filepath = civitai_images[int(img_idx)]
            
            if not os.path.isfile(selected_image_filepath):
                return

            #=====================================================
            infopath = model.get_default_version_infopath(vid)
                        
            if not infopath:
                util.printD("The selected version of the model has not been downloaded. The model must be downloaded first.")
                return 
            
            path , infofile = os.path.split(infopath)

            if not path or not os.path.isdir(path):
                util.printD("The selected version of the model has not been downloaded. The model must be downloaded first.")
                return
                        
            if not f"{setting.info_suffix}{setting.info_ext}" in infofile:
                util.printD("The selected version of the model has not been downloaded. The model must be downloaded first.")
                return
            
            savefile_base = infofile[:infofile.rfind(f"{setting.info_suffix}{setting.info_ext}")]
            
            if not savefile_base:
                util.printD("The selected version of the model has not been downloaded. The model must be downloaded first.")
                return

            preview_img_filepath = os.path.join(path, f"{util.replace_filename(savefile_base)}{setting.preview_image_suffix}{setting.preview_image_ext}")
            
            shutil.copy(selected_image_filepath, preview_img_filepath)
            #========================================================
            # path = model.get_default_version_folder(vid)
                
            # if not path:
            #     util.printD("The selected version of the model has not been downloaded. The model must be downloaded first.")
            #     return
            
            # if not os.path.isdir(path):
            #     util.printD("The selected version of the model has not been downloaded. The model must be downloaded first.")
            #     return
            
            # version_info = ishortcut.get_version_info(mid,vid)
            # if not version_info:
            #     util.printD("The model information does not exist.")
            #     return
            
            # savefile_base = downloader.get_save_base_name(version_info)
            # preview_img_filepath = os.path.join(path, f"{util.replace_filename(savefile_base)}{setting.preview_image_suffix}{setting.preview_image_ext}")
            
            # shutil.copy(selected_image_filepath, preview_img_filepath)
            #=========================================================

def on_gallery_select(evt: gr.SelectData, civitai_images):
    return evt.index, civitai_images[evt.index], gr.update(selected="Image_Information")

def on_civitai_hidden_change(hidden, index, civitai_images_meta):
    info1,info2,info3 = modules.extras.run_pnginfo(hidden)
    if not info2:
        info2 = civitai_images_meta[int(index)]        
    return info2

def on_shortcut_del_btn_click(model_id):
    if model_id:
        ishortcut.delete_shortcut_model(model_id)            
    current_time = datetime.datetime.now()
    return current_time

def on_update_information_btn_click(modelid, progress=gr.Progress()):
    if modelid:
        ishortcut.update_shortcut_models([modelid], progress)  
                
        current_time = datetime.datetime.now()
        return gr.update(value=modelid),gr.update(value=current_time),gr.update(value=None),gr.update(value=current_time)
    return gr.update(value=modelid),gr.update(visible=True),gr.update(value=None),gr.update(visible=True)

def on_load_saved_model(modelid=None, ver_index=None):
    return load_saved_model(modelid, ver_index)

def on_versions_list_select(evt: gr.SelectData, modelid:str):
    return load_saved_model(modelid, evt.index)

def on_file_gallery_loading(image_url):
    chk_image_url = image_url
    if image_url:
        chk_image_url = [img if os.path.isfile(img) else setting.no_card_preview_image for img in image_url]   
        return chk_image_url, chk_image_url
    return None, None 
        
def load_saved_model(modelid=None, ver_index=None):
    if modelid:
        model_info,versionid,version_name,model_url,downloaded_versions,model_type,versions_list,dhtml,triger,files,title_name,images_url,images_meta,vs_foldername = get_model_information(modelid,None,ver_index)    
        if model_info:
            downloaded_info = None
            is_downloaded = False       
            is_visible_openfolder = False
            is_visible_changepreview = False
            flist = list()
            downloadable = list()
            current_time = datetime.datetime.now()
            
            classification_list = classification.get_classification_names_by_modelid(modelid)
            ms_foldername = model_info['name']
            cs_foldername = setting.CREATE_MODEL_FOLDER
            is_vsfolder = False
                        
            try:
                # 현재 다운로드된 폴더를 찾고 그 형식을 찾는다.
                # 문제가 발생한다면 그냥 기본으로 내보낸다.
                if versionid:
                    version_path = model.get_default_version_folder(str(versionid))

                    # 다운로드한 이력이 있는 모델의 경우 다운 로드도니 버전에서 폴더 경로 정보를 가져온다.
                    model_path = model.get_default_model_folder(modelid)
                    use_default_folder = False                    
                    if not version_path and model_path:
                        version_path = model_path
                        use_default_folder = True
                    
                    if version_path:
                        download_classification = None
                        version_parent_path = os.path.dirname(version_path)
                        model_base_folder = os.path.abspath(setting.generate_type_basefolder(model_type))
                        download_foldername = os.path.basename(version_path)
                        download_parent_foldername = os.path.basename(version_parent_path)
                                   
                        if model_base_folder in version_path:
                            if version_path == model_base_folder:
                                # 현재 다운로드 폴더가 type 베이스 폴더이다.
                                pass
                            elif model_base_folder == version_parent_path:
                                # 현재 다운로드된 폴더가 모델명 폴더거나 classification 폴더이다.                                
                                for v in classification_list:
                                    if download_foldername == util.replace_dirname(v.strip()):
                                        download_classification = v
                                        break
                                    
                                if download_classification:
                                    cs_foldername = download_classification
                                else:
                                    ms_foldername = download_foldername
                            else:
                                # 현재 다운로드된 폴더가 개별 버전폴더이다.                               
                                ms_foldername = download_parent_foldername
                                
                                # 개별폴더를 선택한경우에는 개별 폴더를 생성할수 있도록 해준다.
                                # 개별폴더이므로 이름이 같아서는 안된다.
                                if not use_default_folder:
                                    vs_foldername = download_foldername 
                                    
                                # vs_foldername = download_foldername
                                is_vsfolder = True
            except:
                ms_foldername = model_info['name']
                cs_foldername = setting.CREATE_MODEL_FOLDER
                is_vsfolder = False

            # 작성자와 tag를 이름으로 추천
            suggested_names = [ms_foldername]
            
            if "creator" in model_info.keys():
                creator = model_info['creator']['username']
                suggested_names.append(creator)
                
            if "tags" in model_info.keys():
                #혹시몰라서
                tags = [tag for tag in model_info['tags']]
                suggested_names.extend(tags)
            
            # util.printD(suggested_names)
            
            if downloaded_versions:
                downloaded_info = "\n".join(downloaded_versions.values())
                
                if str(versionid) in downloaded_versions:
                    is_visible_openfolder=True     
                    is_visible_changepreview = True           
                        
            if downloaded_info:
                is_downloaded = True 
            
            for file in files:            
                flist.append(f"{file['id']}:{file['name']}")
                
                primary = False
                if "primary" in file:
                    primary = file['primary']
                    
                downloadable.append(['✅',file['id'],file['name'],file['type'],round(file['sizeKB']),primary,file['downloadUrl']])
                                
            return gr.update(value=versionid),gr.update(value=model_url),\
                gr.update(visible = is_downloaded),gr.update(value=downloaded_info),\
                gr.update(value=setting.get_ui_typename(model_type)),gr.update(choices=versions_list,value=version_name),gr.update(value=dhtml),\
                gr.update(value=triger),gr.update(choices=flist if flist else [], value=flist if flist else []), downloadable if len(downloadable) > 0 else None,\
                gr.update(label=title_name),\
                current_time,images_url,images_meta,gr.update(value=None),gr.update(visible=is_visible_openfolder),gr.update(visible=is_visible_changepreview),\
                gr.update(choices=classification.get_list(), value=classification_list, interactive=True),\
                gr.update(value=is_vsfolder, visible=True if cs_foldername == setting.CREATE_MODEL_FOLDER else False), gr.update(value=vs_foldername, visible=is_vsfolder),\
                gr.update(choices=[setting.CREATE_MODEL_FOLDER] + classification.get_list(), value=cs_foldername),\
                gr.update(value=ms_foldername, visible=True if cs_foldername == setting.CREATE_MODEL_FOLDER else False),\
                gr.update(visible=False),\
                gr.update(choices=suggested_names, value=ms_foldername, visible=True if cs_foldername == setting.CREATE_MODEL_FOLDER else False)
                
    # 모델 정보가 없다면 클리어 한다.
    # clear model information
    return gr.update(value=None),gr.update(value=None),\
        gr.update(visible=False),gr.update(value=None),\
        gr.update(value=None),gr.update(choices=[setting.NORESULT], value=setting.NORESULT),gr.update(value=None),\
        gr.update(value=None),gr.update(value=None),None,\
        gr.update(label="#"),\
        None,None,None,gr.update(value=None),gr.update(visible=False),gr.update(visible=False),\
        gr.update(choices=classification.get_list(),value=[], interactive=True),\
        gr.update(value=False, visible=True),gr.update(value="",visible=False),\
        gr.update(choices=[setting.CREATE_MODEL_FOLDER] + classification.get_list(), value=setting.CREATE_MODEL_FOLDER),\
        gr.update(value=None),\
        gr.update(visible=False),\
        gr.update(choices=None, value=None)

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
        dhtml, triger, files = get_version_description(version_info,model_info)
        title_name = f"# {model_info['name']} : {version_info['name']}"
        images_url, images_meta = get_version_description_gallery(version_info)
        
        vs_foldername = setting.generate_version_foldername(model_info['name'],version_name,versionid)
                        
        return model_info,versionid,version_name,model_url,downloaded_versions,model_type,versions_list,dhtml,triger,files,title_name,images_url,images_meta, vs_foldername
    return None,None,None,None,None,None,None,None,None,None,None,None,None,None     
    
def get_version_description_gallery(version_info):
    modelid = None
    versionid = None
    ver_images = dict()
    
            
    if not version_info:
        return None, None

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
        return None, None
                
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
            model_tags = model_info["tags"]
            if len(model_tags) > 0:
                html_model_tags = "<br><b>Model Tags:</b>"
                for tag in model_tags:
                    html_model_tags = html_model_tags + f"<b> [{tag}]</b>"
                                                                
        if 'description' in model_info:  
            if model_info['description']:
                html_descpart = html_descpart + f"<br><b>Description</b><br>{model_info['description']}<br>"
                    
        html_versionpart = f"<br><b>Version:</b> {model_version_name}"

        if 'files' in version_info:                                
            for file in version_info['files']:
                files.append(file)
                html_dnurlpart = html_dnurlpart + f"<br><a href={file['downloadUrl']}><b>Download << Here</b></a>"     
                            
        output_html = html_typepart + html_modelpart + html_versionpart + html_creatorpart + html_trainingpart + "<br>" +  html_model_tags + "<br>" +  html_modelurlpart + html_dnurlpart + "<br>" + html_descpart + "<br>" + html_imgpart
        
        return output_html, output_training, files            
    
    return "", None, None    

def upload_shortcut_by_files(files, register_information_only, progress):
    modelids = list()
    if files:
        shortcuts = []
        add_ISC = dict()

        for file in files:
            shortcuts = util.load_InternetShortcut(file.name)
            if shortcuts:
                for shortcut in shortcuts:
                    model_id = util.get_model_id_from_url(shortcut)
                    if model_id:                    
                        modelids.append(model_id)                    
        
        for model_id in progress.tqdm(modelids, desc=f"Civitai Shortcut"): 
            if model_id:                    
                add_ISC = ishortcut.add(add_ISC, model_id, register_information_only, progress)
                      
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

def scan_downloadedmodel_to_shortcut(progress):        
    # util.printD(len(model.Downloaded_Models))
    if model.Downloaded_Models:
        modelid_list = [k for k in model.Downloaded_Models]
        ishortcut.update_shortcut_models(modelid_list,progress)    
