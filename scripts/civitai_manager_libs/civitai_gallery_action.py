import os
import shutil
import requests
from . import util
from . import civitai
from . import setting

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

        title_name = f"### {model_info['name']}"
        page_info , images_url = get_user_gallery(modelid, page_url, show_nsfw)

        return page_info, title_name, images_url
    return None,None,None

def get_user_gallery(modelid, page_url, show_nsfw):
    
    if not modelid:
        return None,None
    
    images_list = []
    page_info , image_data = get_image_page(modelid, page_url, show_nsfw)

    if image_data:
        images_list = [image_info['url'] for image_info in image_data]
    
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
    
