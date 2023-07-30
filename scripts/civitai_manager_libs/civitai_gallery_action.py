import os
import shutil
import requests
import gradio as gr
import datetime
import modules
import re
import threading
import math

from tqdm import tqdm

from . import util
from . import civitai
from . import setting
from . import ishortcut

def on_ui(recipe_input):
               
    with gr.Column(scale=3):                                                   
        with gr.Accordion("#", open=True) as model_title_name:            
            versions_list = gr.Dropdown(label="Model Version", choices=[setting.PLACEHOLDER], interactive=True, value=setting.PLACEHOLDER)
        usergal_gallery = gr.Gallery(show_label=False, elem_id="user_gallery").style(grid=[setting.usergallery_images_column], height=setting.information_gallery_height, object_fit=setting.gallery_thumbnail_image_style)
        with gr.Row():                  
            with gr.Column(scale=1): 
                with gr.Row():
                    first_btn = gr.Button(value="First Page")
                    prev_btn = gr.Button(value="Prev Page")                                        
            with gr.Column(scale=1): 
                    page_slider = gr.Slider(minimum=1, maximum=1, value=1, step=1, label='Total Pages', interactive=True)
            with gr.Column(scale=1): 
                with gr.Row():
                    next_btn = gr.Button(value="Next Page")
                    end_btn = gr.Button(value="End Page")        
        with gr.Row():
            download_images = gr.Button(value="Download Images")
            open_image_folder = gr.Button(value="Open Download Image Folder")                    

    with gr.Column(scale=1):     
        with gr.Tabs() as info_tabs:
            with gr.TabItem("Image Information" , id="Image_Information"):   
                with gr.Column():
                    img_file_info = gr.Textbox(label="Generate Info", interactive=True, lines=6).style(container=True, show_copy_button=True)                            
                    try:
                        send_to_buttons = modules.generation_parameters_copypaste.create_buttons(["txt2img", "img2img", "inpaint", "extras"])
                    except:
                        pass
                    send_to_recipe = gr.Button(value="Send To Recipe", variant="primary", visible=True)
                        
    with gr.Row(visible=False):
        selected_model_id = gr.Textbox()
        
        # user gallery information  
        img_index = gr.Number(show_label=False)
        
        # 실재 로드된것
        usergal_images = gr.State()
                
        # 로드 해야 할것
        usergal_images_url = gr.State()
        
        usergal_images_meta = gr.State()
        
        # 트리거를 위한것
        hidden = gr.Image(type="pil")
        
        # 페이징 관련 정보
        paging_information = gr.State()
        
        usergal_page_url = gr.Textbox(value=None)
        
        refresh_information = gr.Textbox()
        
        refresh_gallery = gr.Textbox()
        
        # 미리 다음페이지를 로딩한다.
        pre_loading = gr.Textbox()
                
    try:
        modules.generation_parameters_copypaste.bind_buttons(send_to_buttons, hidden,img_file_info)
    except:
        pass            
            
    usergal_gallery.select(on_gallery_select, usergal_images, [img_index, hidden, info_tabs])
    hidden.change(on_civitai_hidden_change,[hidden,img_index,usergal_images_meta],[img_file_info])
    open_image_folder.click(on_open_image_folder_click,[selected_model_id],None)
        
    send_to_recipe.click(
        fn=on_send_to_recipe_click,
        inputs=[
            img_file_info,
            img_index,
            usergal_images
        ],
        outputs=[recipe_input]
    )
        
    download_images.click(
        fn=on_download_images_click,
        inputs=[
            usergal_page_url,
            usergal_images_url       
        ],
        outputs=None 
    )
    
    gallery = refresh_gallery.change(
        fn=on_refresh_gallery_change,
        inputs=[
            usergal_images_url,
        ],
        outputs=[               
            usergal_gallery,
            usergal_images,
            pre_loading
        ]         
    ) 

    gallery_page = usergal_page_url.change(
        fn=on_usergal_page_url_change,
        inputs=[
            usergal_page_url,
            paging_information
        ],
        outputs=[               
            refresh_gallery,
            usergal_images_url,
            usergal_images_meta,
            page_slider,
            img_file_info,            
        ],
        cancels=gallery         
    )   

    refresh_information.change(
        fn=on_usergal_page_url_change,
        inputs=[
            usergal_page_url,
            paging_information
        ],
        outputs=[               
            refresh_gallery,
            usergal_images_url,
            usergal_images_meta,
            page_slider,
            img_file_info,            
        ],
        cancels=gallery  
    )
                
    # civitai user gallery information start
    selected_model_id.change(
        fn=on_selected_model_id_change,
        inputs=[
            selected_model_id,
        ],
        outputs=[   
            model_title_name,             
            usergal_page_url,
            versions_list,
            page_slider,
            paging_information
        ],
        cancels=[gallery, gallery_page]
    )

    versions_list.select(
        fn=on_versions_list_select,
        inputs=[
            selected_model_id,            
        ],
        outputs=[            
            model_title_name,             
            usergal_page_url,
            versions_list,
            page_slider,
            paging_information
        ],
        cancels=[gallery, gallery_page]
    )

    pre_loading.change(
        fn=on_pre_loading_change,
        inputs=[
            usergal_page_url,
            paging_information
        ],
        outputs=None
    )
                    
    first_btn.click(
        fn=on_first_btn_click,
        inputs=[
            usergal_page_url,
            paging_information
        ],
        outputs=[            
            usergal_page_url
        ]        
    )

    end_btn.click(
        fn=on_end_btn_click,
        inputs=[
            usergal_page_url,
            paging_information            
        ],
        outputs=[            
            usergal_page_url
        ]        
    )

    prev_btn.click(
        fn=on_prev_btn_click,
        inputs=[
            usergal_page_url,
            paging_information
        ],
        outputs=[            
            usergal_page_url
        ]        
    )
    
    next_btn.click(
        fn=on_next_btn_click,
        inputs=[
            usergal_page_url,
            paging_information
        ],
        outputs=[            
            usergal_page_url
        ]        
    )

    page_slider.release(
        fn=on_page_slider_release,
        inputs=[
            usergal_page_url,            
            page_slider,
            paging_information
        ],
        outputs=[            
            usergal_page_url
        ]        
    )
    
    return selected_model_id , refresh_information

def on_send_to_recipe_click(img_file_info, img_index, usergal_images):
    try:
        return usergal_images[int(img_index)]
    except:
        return gr.update(visible=False)
    
def on_open_image_folder_click(modelid):
    if modelid:                
        # model_info = civitai.get_model_info(modelid)
        model_info = ishortcut.get_model_info(modelid)
        if model_info:  
            model_name = model_info['name']
            image_folder = util.get_download_image_folder(model_name)
            if image_folder:
                util.open_folder(image_folder)
                
def on_download_images_click(page_url,images_url):
    if page_url:
        modelid , versionid = extract_model_info(page_url)
        download_user_gallery_images(modelid,images_url)
    
def on_page_slider_release(usergal_page_url, page_slider, paging_information):
    page_url = usergal_page_url
    
    if paging_information:
        if paging_information["totalPageUrls"]:
            totalPageUrls = paging_information["totalPageUrls"]
            page_url = totalPageUrls[page_slider - 1]

    return page_url
     
def on_first_btn_click(usergal_page_url, paging_information):
    page_url = usergal_page_url

    if paging_information:
        if paging_information["totalPageUrls"]:
            totalPageUrls = paging_information["totalPageUrls"]
            page_url = totalPageUrls[0]
          
    return page_url
            
def on_end_btn_click(usergal_page_url, paging_information):
    page_url = usergal_page_url
    
    if paging_information:
        if paging_information["totalPageUrls"]:
            totalPageUrls = paging_information["totalPageUrls"]
            page_url = totalPageUrls[-1]

    return page_url

def on_next_btn_click(usergal_page_url, paging_information):
    page_url = usergal_page_url  
    
    current_Page = get_current_page(paging_information, usergal_page_url) 
    if paging_information:
        if paging_information["totalPageUrls"]:
            totalPageUrls = paging_information["totalPageUrls"]
            if len(totalPageUrls) > current_Page:
                page_url = totalPageUrls[current_Page]

    return page_url

def on_prev_btn_click(usergal_page_url, paging_information):
    page_url = usergal_page_url

    current_Page = get_current_page(paging_information, usergal_page_url) 
    if paging_information:
        if paging_information["totalPageUrls"]:
            totalPageUrls = paging_information["totalPageUrls"]
            if current_Page > 1:
                page_url = totalPageUrls[current_Page - 2]    

    return page_url

def on_civitai_hidden_change(hidden, index, civitai_images_meta):
    info1,info2,info3 = modules.extras.run_pnginfo(hidden)
    # 이미지에 메타 데이터가 없으면 info 것을 사용한다.
    if not info2:
        info2 = civitai_images_meta[int(index)]
    return info2

def on_gallery_select(evt: gr.SelectData, civitai_images):
    return evt.index, civitai_images[evt.index], gr.update(selected="Image_Information")

def on_selected_model_id_change(modelid):
    page_url = None
    versions_list = None
    title_name = None
    version_name = None
    paging_information = None
    
    if modelid:
        page_url = get_default_page_url(modelid,None,False)
        title_name, versions_list, version_name, paging_information = get_model_information(page_url)
        if paging_information:
            total_page = paging_information["totalPages"]
        else:
            total_page = 0    
    
    return  gr.update(label=title_name),page_url,gr.update(choices=[setting.PLACEHOLDER] + versions_list if versions_list else None, value=version_name if version_name else setting.PLACEHOLDER), \
        gr.update(minimum=1, maximum=total_page, value=1, step=1, label=f"Total {total_page} Pages"), paging_information

def on_versions_list_select(evt: gr.SelectData, modelid=None): 
    page_url = None
    versions_list = None
    title_name = None
    version_name = None    
    paging_information = None
    
    if modelid:
        if evt.index > 0:
            ver_index = evt.index - 1
            # model_info = civitai.get_model_info(modelid)
            model_info = ishortcut.get_model_info(modelid)
            version_info = dict()
            if model_info:
                if "modelVersions" in model_info.keys():
                    if len(model_info["modelVersions"]) > 0:
                        version_info = model_info["modelVersions"][ver_index]
                        if version_info["id"]:
                            versionid = version_info["id"]
                            page_url = get_default_page_url(modelid,versionid,False)
        else:            
            page_url = get_default_page_url(modelid,None,False)
                         
        title_name, versions_list, version_name, paging_information = get_model_information(page_url)
        if paging_information:
            total_page = paging_information["totalPages"]
        else:
            total_page = 0
        
    return  gr.update(label=title_name),page_url,gr.update(choices=[setting.PLACEHOLDER] + versions_list if versions_list else None, value=version_name if version_name else setting.PLACEHOLDER), \
        gr.update(minimum=1, maximum=total_page, value=1, step=1, label=f"Total {total_page} Pages"), paging_information
        
def get_model_information(page_url=None):
    model_info = None
    version_name = None
    modelid = None
    versionid= None
    
    if page_url:
        modelid , versionid = extract_model_info(page_url)
        
    if modelid:
        # model_info = civitai.get_model_info(modelid)    
        model_info = ishortcut.get_model_info(modelid)    
                                                        
    if model_info:       
        title_name = f"# {model_info['name']}"

        versions_list = list()
        if 'modelVersions' in model_info:
            for ver in model_info['modelVersions']:
                versions_list.append(ver['name'])
                if versionid:
                    if versionid == str(ver['id']):
                        version_name = ver['name']

        # 작업중 2023-07-14 여기서 페이지 정보를 가져오도록 변경한다.
        # paging_information = get_paging_information(modelid,versionid,False)
        paging_information = get_paging_information_working(modelid,versionid,False)
        
        
        return title_name, versions_list, version_name, paging_information
    return None,None,None,None

def on_usergal_page_url_change(usergal_page_url, paging_information):   
    return load_gallery_page(usergal_page_url, paging_information)

def on_refresh_gallery_change(images_url, progress=gr.Progress()):    
    return gallery_loading(images_url, progress)

def on_pre_loading_change(usergal_page_url, paging_information):
    if setting.usergallery_preloading:
        pre_loading(usergal_page_url, paging_information)
   
def pre_loading(usergal_page_url, paging_information):
    page_url = usergal_page_url

    current_Page = get_current_page(paging_information, usergal_page_url) 
    
    if paging_information:
        if paging_information["totalPageUrls"]:
            totalPageUrls = paging_information["totalPageUrls"]
            if len(totalPageUrls) > current_Page:
                page_url = totalPageUrls[current_Page]
                    
    if page_url:        
        image_data = None
        json_data = civitai.request_models(fix_page_url_cursor(page_url))
        try:
            image_data = json_data['items']
        except Exception as e:
            util.printD(e)
            return

        dn_image_list = list()
        
        if image_data:                    
            for image_info in image_data:                          
                if "url" in image_info:
                    img_url = image_info['url']                    
                    gallery_img_file = setting.get_image_url_to_gallery_file(image_info['url'])
                    if not os.path.isfile(gallery_img_file):
                        dn_image_list.append(img_url)

        if len(dn_image_list) > 0:                     
            try:
                thread = threading.Thread(target=download_images,args=(dn_image_list,))
                thread.start()                
            except Exception as e:
                util.printD(e)
                pass
    return

def download_images(dn_image_list:list):        
    if dn_image_list:
        # for img_url in tqdm(dn_image_list,desc=f"{setting.Extensions_Name} preloading"):            
        for img_url in dn_image_list:
            gallery_img_file = setting.get_image_url_to_gallery_file(img_url)              
            # util.printD(gallery_img_file)
            if not os.path.isfile(gallery_img_file):                
                with requests.get(img_url,stream=True) as img_r:
                    if not img_r.ok:
                        continue

                    with open(gallery_img_file, 'wb') as f:
                        img_r.raw.decode_content = True
                        shutil.copyfileobj(img_r.raw, f)
                                    
def load_gallery_page(usergal_page_url, paging_information):           
    if usergal_page_url:
        image_url, images_meta = get_gallery_information(usergal_page_url, False)
            
        current_Page = get_current_page(paging_information, usergal_page_url) 
        
        current_time = datetime.datetime.now()                            
        
        return current_time,\
            image_url,\
            images_meta,\
            gr.update(value=current_Page),\
            gr.update(value=None)
    
    return None,None,None,gr.update(minimum=1, maximum=1, value=1),None                                                    

def get_gallery_information(page_url=None, show_nsfw=False):
    modelid = None       
    if page_url:
        modelid, versionid = extract_model_info(page_url)
        
    if modelid:
        images_url = None        
        images_meta = None
        
        images_url, images_meta , images_list = get_user_gallery(modelid, page_url, show_nsfw)

        return images_url, images_meta
    return None,None

def get_user_gallery(modelid, page_url, show_nsfw):    
    if not modelid:
        return None,None    
    
    image_data = get_image_page(modelid, page_url, show_nsfw)

    images_list = {}
    images_url = []
    images_meta = []
    if image_data:
        for image_info in image_data:       
            meta_string = ""  
            if "meta" in image_info:     
                meta_string = util.convert_civitai_meta_to_stable_meta(image_info['meta'])
                
            if "url" in image_info:                
                img_url = image_info['url']
                
                gallery_img_file = setting.get_image_url_to_gallery_file(image_info['url'])
                
                # NSFW filtering ....
                if setting.NSFW_filtering_enable:
                    if not setting.NSFW_level[image_info["nsfwLevel"]]:
                        gallery_img_file = setting.nsfw_disable_image
                        meta_string = ""
                                    
                if os.path.isfile(gallery_img_file):
                    img_url = gallery_img_file
                                     
                images_url.append(img_url)
                images_meta.append(meta_string)
                
        images_list = {image_info['id']:image_info for image_info in image_data}
        
    return images_url, images_meta , images_list
           
def get_image_page(modelid, page_url, show_nsfw=False):
    json_data = {}

    if not page_url:
       page_url = get_default_page_url(modelid, None, show_nsfw)

    # util.printD(page_url)
    json_data = civitai.request_models(fix_page_url_cursor(page_url))
    # util.printD("here")
    
    try:
        json_data['items']
    except TypeError:
        return None,None
                        
    return json_data['items']

def get_paging_information(modelId, modelVersionId = None, show_nsfw=False):
    totalPages = 0
    
    page_url = get_default_page_url(modelId, modelVersionId, show_nsfw)    
    
    total_page_urls = list()    
    while page_url is not None:
        total_page_urls.append(page_url)
        # util.printD(page_url)
        json_data = civitai.request_models(fix_page_url_cursor(page_url))
        
        try:
            page_url = json_data['metadata']['nextPage']
        except:
            page_url = None
            
        totalPages = totalPages + 1
                           
    paging_information = dict()
    paging_information["totalPages"] = totalPages
    paging_information["totalPageUrls"] = total_page_urls
    
    return paging_information

# cursor로 쿼리를 보내면 그 다음것부터 검색되어 리턴되고 있다. 
# 명확해 질때까지 대기....
# 페잊 수에 오류가 난다.
def get_paging_information_working(modelId, modelVersionId = None, show_nsfw=False):
    totalPages = 0
    
    # 한번에 가져올수 있는 최대량은 200 이다.
    page_url = get_default_page_url(modelId, modelVersionId, show_nsfw, 200)    
    
    item_list = list()    
    total_page_urls = list()    

    while page_url is not None:
        # util.printD(page_url)
        json_data = civitai.request_models(fix_page_url_cursor(page_url))
        try:  
            item_list.extend(json_data['items'])
        except:
            pass
        
        try:
            page_url = json_data['metadata']['nextPage']
        except:
            page_url = None
               
    # totalItems = len(item_list)
        
    # try:
    #     totalPages = math.ceil(totalItems / setting.usergallery_images_page_limit)
    # except:
    #     totalPages = 0        

    # import json

    # output_file = 'item_list.json'
    # with open(output_file, 'w') as f:
    #     json.dump(item_list, f, indent=4)

    initial_url = get_default_page_url(modelId, modelVersionId, show_nsfw)
    total_page_urls.append(initial_url)    
    page_items = item_list[::setting.usergallery_images_page_limit]
    totalPages = len(page_items)
    
    # util.printD(page_items)
    # util.printD(f"{totalItems} , {totalItems2} , {len(page_items)}")
    
    for index, item in enumerate(page_items):        
        if index > 0:
            total_page_urls.append(util.update_url(initial_url,"cursor",item["id"]))
                       
    paging_information = dict()
    paging_information["totalPages"] = totalPages
    paging_information["totalPageUrls"] = total_page_urls
    
    # for pags_url in total_page_urls:
    #     util.printD(pags_url)
    
    return paging_information

# 현재 pageurl 의 cursor에서 page를 계산한다.
def get_current_page(paging_information, page_url):
    current_cursor = extract_url_cursor(page_url)
    # util.printD(f"current {current_cursor}")
    # util.printD(page_url)

    if paging_information:
        total_page_urls = paging_information["totalPageUrls"]
        for cur_page, p_url in enumerate(total_page_urls, start=1):
            p_cursor = extract_url_cursor(p_url)
            # util.printD(p_cursor)
            
            if not p_cursor:
                continue 
                
            if str(current_cursor) == str(p_cursor):
                # util.printD(f"select {p_cursor}")
                return cur_page
    return 1

def gallery_loading(images_url, progress):
    if images_url:
        dn_image_list = []
        image_list = []
        
        if not os.path.exists(setting.shortcut_gallery_folder):
            os.makedirs(setting.shortcut_gallery_folder)
                            
        for i,  img_url in enumerate(progress.tqdm(images_url, desc=f"Civitai Images Loading")):
            result = util.is_url_or_filepath(img_url) 
            description_img = setting.get_image_url_to_gallery_file(img_url)             
            if result == "filepath":
                description_img = img_url
            elif result == "url":                   
                try:
                    with requests.get(img_url,stream=True) as img_r:
                        if not img_r.ok:                        
                            util.printD("Get error code: " + str(img_r.status_code) + ": proceed to the next file")                            
                            description_img = setting.no_card_preview_image
                        else:                                                                        
                            # sc_gallery 에 저장한다.                        
                            with open(description_img, 'wb') as f:
                                img_r.raw.decode_content = True
                                shutil.copyfileobj(img_r.raw, f)      
                except:
                    description_img = setting.no_card_preview_image
            else:
                description_img = setting.no_card_preview_image

            dn_image_list.append(description_img)
            image_list.append(description_img)
                                        
            current_time = datetime.datetime.now()     
        return dn_image_list, image_list , current_time       
    return None, None, gr.update(visible=False)

def download_user_gallery_images(model_id, image_urls):
    base = None
    
    if not model_id:                
        return         
    
    # model_info = civitai.get_model_info(model_id)
    model_info = ishortcut.get_model_info(model_id)
    
    if not model_info:
        return 
                      
    model_folder = util.make_download_image_folder(model_info['name'])    
    
    if not model_folder:
        return
    
    save_folder = os.path.join(model_folder ,"user_gallery_images")
    
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)        
    
    if image_urls and len(image_urls) > 0:                                           
        for image_count, img_url in enumerate(tqdm(image_urls, desc=f"Download user gallery image"), start=0):       

            result = util.is_url_or_filepath(img_url)          
            if result == "filepath":
                if os.path.basename(img_url) != setting.no_card_preview_image:
                    description_img = os.path.join(save_folder,os.path.basename(img_url))
                    shutil.copyfile(img_url,description_img)
            elif result == "url":                                
                try:
                    # get image
                    with requests.get(img_url, stream=True) as img_r:
                        if not img_r.ok:
                            util.printD("Get error code: " + str(img_r.status_code) + ": proceed to the next file")
                        else:
                            # write to file
                            image_id, ext = os.path.splitext(os.path.basename(img_url))
                            description_img = os.path.join(save_folder,f'{image_id}{setting.preview_image_suffix}{setting.preview_image_ext}')
                            with open(description_img, 'wb') as f:
                                img_r.raw.decode_content = True
                                shutil.copyfileobj(img_r.raw, f)

                except Exception as e:
                    pass
    return 

def extract_model_info(url):
    model_id_match = re.search(r'modelId=(\d+)', url)
    model_version_id_match = re.search(r'modelVersionId=(\d+)', url)
    
    model_id = model_id_match.group(1) if model_id_match else None
    model_version_id = model_version_id_match.group(1) if model_version_id_match else None
    
    return (model_id, model_version_id)

# def extract_url_page(url):
#     model_page_match = re.search(r'page=(\d+)', url)
    
#     page = int(model_page_match.group(1)) if model_page_match else 0
    
#     return (page)

def extract_url_cursor(url):
    model_cursor_match = re.search(r'cursor=(\d+)', url)
    
    cursor = int(model_cursor_match.group(1)) if model_cursor_match else 0
    
    return (cursor)
    
def get_default_page_url(modelId, modelVersionId = None, show_nsfw=False, limit=setting.usergallery_images_page_limit):
    page_url = f"{civitai.Url_ImagePage()}?limit={limit}&modelId={modelId}"
    
    if modelVersionId:
        page_url = f"{page_url}&modelVersionId={modelVersionId}"
        
    if not show_nsfw:    
        page_url = f"{page_url}&nsfw=false"

    page_url = f"{page_url}&sort=Newest"
    
    return page_url

# cursor + 1 로 만들어 준다
# civitai 에서 cursor 를 수정 한다면 필요 없다.
def fix_page_url_cursor(page_url):
    cursor = int(extract_url_cursor(page_url))
    if cursor > 0:
        page_url = util.update_url(page_url,"cursor", cursor + 1)        
    return page_url