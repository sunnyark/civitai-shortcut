import os
import shutil
import requests
import gradio as gr
import datetime
import modules

from PIL import Image
from . import util
from . import civitai
from . import setting

def on_ui(selected_usergal_model_id:gr.Textbox):
        
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
        usergal_images = gr.State()
        usergal_images_url = gr.State()
        usergal_images_meta = gr.State()
        
        # 트리거를 위한것
        usergal_hidden = gr.Image(type="pil")
        usergal_info1 = gr.Textbox()
        usergal_info2 = gr.Textbox()
        usergal_page = gr.State()
        
        usergal_page_url = gr.Textbox(value=None)
        
        refresh_information = gr.Textbox()
        refresh_gallery = gr.Textbox()
                
    try:
        modules.generation_parameters_copypaste.bind_buttons(usergal_send_to_buttons, usergal_hidden,usergal_img_file_info)
    except:
        pass            

    # civitai user gallery information start
    selected_usergal_model_id.change(
        fn=on_selected_usergal_model_id_change,
        inputs=[
            selected_usergal_model_id,            
        ],
        outputs=[            
            usergal_page_url    
        ] 
    )    

    usergal_page_url.change(
        fn=on_load_usergal_model,
        inputs=[
            selected_usergal_model_id,
            usergal_page_url,            
            usergal_page
        ],
        outputs=[               
            usergal_title_name,                               
            refresh_gallery,
            usergal_images_url,
            usergal_images_meta,
            usergal_page_slider,
            usergal_page,
            usergal_img_file_info   
        ]         
    )
        
    usergal_first_btn.click(
        fn=on_usergal_first_btn_click,
        inputs=[
            usergal_page_url,
            usergal_page
        ],
        outputs=[            
            usergal_page_url
        ]        
    )

    usergal_end_btn.click(
        fn=on_usergal_end_btn_click,
        inputs=[
            usergal_page_url,
            usergal_page
        ],
        outputs=[            
            usergal_page_url
        ]        
    )

    usergal_prev_btn.click(
        fn=on_usergal_prev_btn_click,
        inputs=[
            usergal_page_url,
            usergal_page
        ],
        outputs=[            
            usergal_page_url
        ]        
    )
    
    usergal_next_btn.click(
        fn=on_usergal_next_btn_click,
        inputs=[
            usergal_page_url,
            usergal_page
        ],
        outputs=[            
            usergal_page_url
        ]        
    )

    usergal_page_slider.release(
        fn=on_usergal_page_slider_release,
        inputs=[
            usergal_page_url,
            usergal_page_slider
        ],
        outputs=[            
            usergal_page_url
        ]        
    )

    refresh_information.change(
        fn=on_load_usergal_model,
        inputs=[
            selected_usergal_model_id,
            usergal_page_url,            
            usergal_page
        ],
        outputs=[               
            usergal_title_name,                               
            refresh_gallery,
            usergal_images_url,
            usergal_images_meta,
            usergal_page_slider,
            usergal_page,
            usergal_img_file_info   
        ]        
    )
    
    refresh_gallery.change(
        fn=on_user_gallery_loading,
        inputs=[
            usergal_images_url 
        ],
        outputs=[               
            usergal_gallery,
            usergal_images
        ]         
    )
            
    usergal_gallery.select(on_gallery_select, usergal_images, [usergal_img_index, usergal_hidden])
    # usergal_hidden.change(fn=modules.extras.run_pnginfo, inputs=[usergal_hidden], outputs=[usergal_info1, usergal_img_file_info, usergal_info2])
    usergal_hidden.change(on_civitai_hidden_change,[usergal_hidden,usergal_img_index,usergal_images_meta],[usergal_info1, usergal_img_file_info, usergal_info2])

def on_civitai_hidden_change(hidden, index, civitai_images_meta):
    
    info1,info2,info3 = modules.extras.run_pnginfo(hidden)
    # 이미지에 메타 데이터가 없으면 info 것을 사용한다.
    if not info2:
        info2 = civitai_images_meta[int(index)]        
    return info1, info2, info3

def on_gallery_select(evt: gr.SelectData, civitai_images):
    return evt.index, civitai_images[evt.index]

def on_load_usergal_model( modelid, usergal_page_url, page_info):

    if not usergal_page_url:
        if modelid:
            usergal_page_url = get_default_page_url(modelid,False)    
            
    if usergal_page_url:
        page_info, title_name, image_url, images_meta = get_model_information( modelid , usergal_page_url, False) 
        if page_info:
            total_page = page_info['totalPages']
            current_Page = page_info['currentPage']
            
            current_time = datetime.datetime.now()
                                
            return gr.update(label=title_name),\
                current_time,\
                image_url,\
                images_meta,\
                gr.update(minimum=1, maximum=total_page, value=current_Page, step=1, label=f"Total {total_page} Pages"),\
                page_info,\
                gr.update(value=None)
                                                    
    return gr.update(label="#"),None,None,None,gr.update(minimum=1, maximum=1, value=1),None,None

def on_user_gallery_loading(images_url, progress=gr.Progress()):
    if images_url:
        # image_url = [image_info['url'] for image_info in images_infos.values()]
        dn_image_list = []
        image_list = []
        for img_url in progress.tqdm(images_url, desc=f"Civitai Images Loading"):
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
        return dn_image_list, dn_image_list # 어떤 때에는 갤러리가 이미지 생성 정보가 사라지게 한다 그레도 이리하면 이미지 선택시 다시 로딩할 필요가 없다. 오프라인에서 로딩할때는 이럴 필요가 없다.
        #return dn_image_list, image_list
    return None, None

def on_selected_usergal_model_id_change(modelid=None):
    page_url = None
    if modelid:
        page_url = get_default_page_url(modelid,False)    
    return page_url
    
def on_usergal_page_slider_release(usergal_page_url, page_slider):
    page_url = usergal_page_url
    if usergal_page_url:       
        page_url = util.update_url(usergal_page_url,"page", page_slider)    
    
    return page_url

def on_usergal_first_btn_click(usergal_page_url, page_info):
    page_url = usergal_page_url
    if page_info:        
        if page_info['prevPage']:
            page_url = util.update_url(page_info['prevPage'],"page",1)
                    
    return page_url

def on_usergal_end_btn_click(usergal_page_url, page_info):
    page_url = usergal_page_url
    if page_info:
        if page_info['nextPage']:            
            page_url = util.update_url(page_info['nextPage'],"page",page_info['totalPages'])

    return page_url

def on_usergal_next_btn_click(usergal_page_url, page_info):
    page_url = usergal_page_url
    if page_info:        
        if page_info['nextPage']:
            page_url = page_info['nextPage']

    return page_url

def on_usergal_prev_btn_click(usergal_page_url, page_info):
    page_url = usergal_page_url
    if page_info:        
        if page_info['prevPage']:
            page_url = page_info['prevPage']

    return page_url
    
def get_default_page_url(modelid, show_nsfw=False):
    page_url = f"{civitai.Url_ImagePage()}?limit={setting.gallery_images_page_limit}&modelId={modelid}&sort=Newest&page=1"
    if not show_nsfw:    
        page_url = f"{page_url}&nsfw=false"
               
    return page_url

def get_model_information( modelid:str=None, page_url=None, show_nsfw=False,):
    # 현재 모델의 정보를 가져온다.

    model_info = None
    
    if modelid:
        model_info = civitai.get_model_info(modelid)        
                            
    # 존재 하는지 판별하고 있다면 내용을 얻어낸다.
    if model_info:
        images_url = None        
        images_meta = None
        
        title_name = f"# {model_info['name']}"

        page_info , images_infos = get_user_gallery(modelid, page_url, show_nsfw)
        images_url = [image_info['url'] for image_info in images_infos.values()]
        #images_url = images_infos
        
        images_meta = [util.convert_civitai_meta_to_stable_meta(image_info['meta']) for image_info in images_infos.values()]

        return page_info, title_name, images_url, images_meta
    return None,None,None,None

def get_user_gallery(modelid, page_url, show_nsfw):
    
    if not modelid:
        return None,None
    
    images_list = {}
    page_info , image_data = get_image_page(modelid, page_url, show_nsfw)

    if image_data:
        images_list = {image_info['id']:image_info for image_info in image_data}
    
    return page_info, images_list
           
def get_image_page(modelid, page_url, show_nsfw=False):
    json_data = {}
    prev_page_url = None
    next_page_url = None
        
    if not page_url:
       page_url = get_default_page_url(modelid, show_nsfw)

    json_data = civitai.request_models(page_url)
        
    try:
        json_data['items']
    except TypeError:
        return None,None

    page_info = dict()
    try:
        if json_data['metadata']['nextPage'] is not None:
            next_page_url = json_data['metadata']['nextPage']
    except:
        pass

    try:
        if json_data['metadata']['prevPage'] is not None:
            prev_page_url = json_data['metadata']['prevPage']
    except:
        pass


    page_info['prevPage'] =  prev_page_url
    page_info['nextPage'] =  next_page_url
    page_info['currentPage'] = json_data['metadata']['currentPage']
    page_info['pageSize'] =  json_data['metadata']['pageSize']
    page_info['totalItems'] =  json_data['metadata']['totalItems']
    page_info['totalPages'] =  json_data['metadata']['totalPages']
                        
    return page_info, json_data['items']
    
