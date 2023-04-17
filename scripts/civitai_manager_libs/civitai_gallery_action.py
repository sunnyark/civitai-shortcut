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
        gallery_url = None
        images_url = None        

        title_name = f"### {model_info['name']}"
        page_info , gallery_url, images_url = get_user_gallery(modelid, page_url, show_nsfw)
        
        return page_info, title_name, gallery_url
    return None,None,None

def get_user_gallery(modelid, page_url, show_nsfw):
    
    if not modelid:
        return None,None,None,None
    
    images_list = []
    page_info , image_data = get_image_page(modelid, page_url, show_nsfw)

    if image_data:
        images_list = [image_info['url'] for image_info in image_data]
    
    return page_info, images_list, images_list
           
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

# image_data_sample = \
# {
#   "items": [
#     {
#       "id": 469632,
#       "url": "https://imagecache.civitai.com/xG1nkqKTMzGDvpLrqFT7WA/cc5caabb-e05f-4976-ff3c-7058598c4e00/width=1024/cc5caabb-e05f-4976-ff3c-7058598c4e00.jpeg",
#       "hash": "UKHU@6H?_ND*_3M{t84o^+%MD%xuXSxasAt7",
#       "width": 1024,
#       "height": 1536,
#       "nsfw": false,
#       "createdAt": "2023-04-11T15:33:12.500Z",
#       "postId": 138779,
#       "stats": {
#         "cryCount": 0,
#         "laughCount": 0,
#         "likeCount": 0,
#         "dislikeCount": 0,
#         "heartCount": 0,
#         "commentCount": 0
#       },
#       "meta": {
#         "Size": "512x768",
#         "seed": 234871805,
#         "Model": "Meina",
#         "steps": 35,
#         "prompt": "<lora:setsunaTokage_v10:0.6>, green hair, long hair, standing, (ribbed dress), zettai ryouiki, choker, (black eyes), looking at viewer, adjusting hair, hand in own hair, street, grin, sharp teeth, high ponytail, [Style of boku no hero academia]",
#         "sampler": "DPM++ SDE Karras",
#         "cfgScale": 7,
#         "Clip skip": "2",
#         "Hires upscale": "2",
#         "Hires upscaler": "4x-AnimeSharp",
#         "negativePrompt": "(worst quality, low quality, extra digits:1.3), easynegative,",
#         "Denoising strength": "0.4"
#       },
#       "username": "Cooler_Rider"
#     }
#   ],
#   "metadata": {
#     "totalItems": 181278,
#     "currentPage": 1,
#     "pageSize": 1,
#     "totalPages": 181278,
#     "nextPage": "http://civitai.com/api/v1/images?limit=1&sort=Newest&nsfw=false&page=2"
#   }
# }

# def update_next_page(next_page_url, show_nsfw):
#     global json_data
#     tmp_json_data = api_next_page()
    
#     if tmp_json_data:
#         json_data = tmp_json_data
            
#     models_name = []
#     try:
#         json_data['items']
#     except TypeError:
#         return None
#     if show_nsfw:
#         for model in json_data['items']:
#             models_name.append(model['name'])
#     else:
#         for model in json_data['items']:
#             temp_nsfw = model['nsfw']
#             if not temp_nsfw:
#                 models_name.append(model['name'])
#     return [v for v in models_name]


# def update_models_list_nsfw(show_nsfw):
#     global json_data
#     models_name = []
#     try:
#         json_data['items']
#     except TypeError:
#         return None
#     if show_nsfw:
#         for model in json_data['items']:
#             models_name.append(model['name'])
#     else:
#         for model in json_data['items']:
#             temp_nsfw = model['nsfw']
#             if not temp_nsfw:
#                 models_name.append(model['name'])
#     return [v for v in models_name]

    
# def update_models_list(content_type, sort_type, search_term, show_nsfw):
#     global json_data
#     json_data = api_to_data(content_type, sort_type, search_term)
#     models_name=[]
#     if show_nsfw:
#         for model in json_data['items']:
#             models_name.append(model['name'])
#     else:
#         for model in json_data['items']:
#             temp_nsfw = model['nsfw']
#             if not temp_nsfw:
#                 models_name.append(model['name'])
#     return [v for v in models_name]

    
# def update_model_versions(model_name=None):
#     if model_name is not None and model_name != PLACEHOLDER:
#         global json_data
#         versions_name = []
#         for model in json_data['items']:
#             if model['name'] == model_name:
#                 for model_version in model['modelVersions']:
#                     versions_name.append(model_version['name'])
        
#         return [v for v in versions_name]                    
#     else:
#         return None
    
