import os
import json
import shutil
from modules import shared
import modules.scripts as scripts

from . import util

root_path = os.getcwd()
extension_base = scripts.basedir()

headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.68'}

Extensions_Name = "Civitai Shortcut"

PLACEHOLDER = "<no select>"
NORESULT = "<no result>"  
    
model_exts = (".bin", ".pt", ".safetensors", ".ckpt")

# define model type name -> civitai model type
# model_types = {
#     'checkpoint':'Checkpoint',
#     'lora':'LORA',
#     'locon':'LoCon',
#     'textualinversion':'TextualInversion',
#     'hypernetwork':'Hypernetwork',
#     'aestheticgradient':'AestheticGradient',
#     'controlnet':'Controlnet',
#     'poses':'Poses',
#     'wildcards':'Wildcards',
#     'other':'Other',
          
#     'vae':'VAE',          
#     "anlora":"ANLORA",
#     "unknown":"Unknown"
# }

# civitai model type -> folder path
model_folders = {
    'Checkpoint': os.path.join("models","Stable-diffusion"),
    'LORA': os.path.join("models","Lora"),
    'LoCon': os.path.join("models","Lora"),    
    'TextualInversion': os.path.join("embeddings"),   
    'Hypernetwork': os.path.join("models","hypernetworks"),         
    'AestheticGradient': os.path.join("extensions","stable-diffusion-webui-aesthetic-gradients","aesthetic_embeddings"),        
    'Controlnet': os.path.join("models","ControlNet"),
    'Poses': os.path.join("models","Poses"),
    'Wildcards': os.path.join("extensions","sd-dynamic-prompts","wildcards"),    
    'Other': os.path.join("models","Other"),    
    
    'VAE': os.path.join("models","VAE"),    
    'ANLORA': os.path.join("extensions","sd-webui-additional-networks","models","lora"),    
    'Unknown': os.path.join("models","Unkonwn"),
}

# UI 쪽에서 변환할때 쓰인다.
# UI model type -> civitai model type
ui_typenames = {
    "Checkpoint" : 'Checkpoint',
    "LoRA" : 'LORA',
    "LyCORIS" : 'LoCon',
    "Textual Inversion" : 'TextualInversion',
    "Hypernetwork" : 'Hypernetwork',
    "Aesthetic Gradient" : 'AestheticGradient',
    "Controlnet" : 'Controlnet',
    "Poses" : 'Poses',
    "Wildcards" : 'Wildcards',
    "Other" : 'Other',
}

#information tab 
civitai_information_tab = 0
saved_information_tab = 1
usergal_information_tab = 2

# civitai helper 호환성
info_ext = ".info"
info_suffix = ".civitai"

triger_ext = ".txt"
triger_suffix = ".triger"

preview_image_ext = ".png"
preview_image_suffix = ".preview"


# 갤러리 ui설정
gallery_column = 4
shortcut_column = 3  
classification_gallery_column = 8
# 유저 갤러리 설정
usergallery_images_column = 5
usergallery_images_page_limit = 10
# usergallery_preload_page_count = 1
# 버전당 최대 다운로드 이미지 수 , 0이면 전체다운 받는다
shortcut_max_download_image_per_version = 0

# 생성되는 폴더 및 파일
shortcut = "CivitaiShortCut.json"
shortcut_setting = "CivitaiShortCutSetting.json"
shortcut_classification = "CivitaiShortCutClassification.json"
shortcut_thumbnail_folder =  "sc_thumb_images"
shortcut_save_folder =  "sc_saves"
shortcut_info_folder =  "sc_infos"
shortcut_gallery_folder =  "sc_gallery"

no_card_preview_image = os.path.join(root_path,"html","card-no-preview.png")


shortcut_env = dict()

def init():
    global root_path
    global extension_base
    global model_folders
    
    global shortcut
    global shortcut_setting
    global shortcut_classification
    global shortcut_thumbnail_folder
    global shortcut_save_folder
    global shortcut_info_folder
    global shortcut_gallery_folder
    
    global shortcut_column
    global gallery_column
    global classification_gallery_column
    global usergallery_images_column
    global usergallery_images_page_limit
    global shortcut_max_download_image_per_version
        
    root_path = os.getcwd()
       
    shortcut = os.path.join(extension_base,shortcut)
    shortcut_setting = os.path.join(extension_base,shortcut_setting)
    shortcut_classification = os.path.join(extension_base,shortcut_classification)
    shortcut_thumbnail_folder = os.path.join(extension_base,shortcut_thumbnail_folder)
    shortcut_save_folder = os.path.join(extension_base,shortcut_save_folder)
    shortcut_info_folder = os.path.join(extension_base,shortcut_info_folder)
    shortcut_gallery_folder = os.path.join(extension_base,shortcut_gallery_folder)
        
    if shared.cmd_opts.embeddings_dir:
        model_folders['TextualInversion'] = shared.cmd_opts.embeddings_dir

    if shared.cmd_opts.hypernetwork_dir :
        model_folders['Hypernetwork'] = shared.cmd_opts.hypernetwork_dir

    if shared.cmd_opts.ckpt_dir:
        model_folders['Checkpoint'] = shared.cmd_opts.ckpt_dir

    if shared.cmd_opts.lora_dir:
        model_folders['LORA'] = shared.cmd_opts.lora_dir
        model_folders['LoCon'] = shared.cmd_opts.lora_dir
    
    environment = load()
    if environment:
        if "shortcut_column" in environment.keys():
            shortcut_column = int(environment['shortcut_column'])
        if "gallery_column" in environment.keys():            
            gallery_column = int(environment['gallery_column'])
        if "classification_gallery_column" in environment.keys():
            classification_gallery_column = int(environment['classification_gallery_column'])
        if "usergallery_images_column" in environment.keys():
            usergallery_images_column = int(environment['usergallery_images_column'])
        if "usergallery_images_page_limit" in environment.keys():
            usergallery_images_page_limit = int(environment['usergallery_images_page_limit'])
        if "shortcut_max_download_image_per_version" in environment.keys():
            shortcut_max_download_image_per_version = int(environment['shortcut_max_download_image_per_version'])

        if "model_folders" in environment.keys():
                
            user_folders = environment['model_folders']
            
            if 'Wildcards' in user_folders.keys():
                model_folders['Wildcards'] = user_folders['Wildcards']
                
            if 'Controlnet' in user_folders.keys():
                model_folders['Controlnet'] = user_folders['Controlnet']

            if 'AestheticGradient' in user_folders.keys():
                model_folders['AestheticGradient'] = user_folders['AestheticGradient']

            if 'Poses' in user_folders.keys():
                model_folders['Poses'] = user_folders['Poses']

            if 'Other' in user_folders.keys():
                model_folders['Other'] = user_folders['Other']
                
def generate_version_foldername(model_name,ver_name,ver_id):      
    # return f"{model_name}-{ver_name}-{ver_id}"
    return f"{model_name}-{ver_name}"

def generate_model_foldername(content_type, model_name=None):
    
    if not model_name:
        return
    
    model_name = model_name.strip()
    if len(model_name) <= 0:
        return
            
    if content_type in model_folders.keys():
        model_folder = model_folders[content_type]        
    elif content_type:
        model_folder = os.path.join(model_folders['Unknown'], util.replace_dirname(content_type))
    else:
        model_folder = os.path.join(model_folders['Unknown'])
                     
    model_folder = os.path.join(model_folder, util.replace_dirname(model_name))
                
    return model_folder 
    
def get_model_folders():
    return model_folders.values()

def get_ui_typename(model_type):
    for k,v in ui_typenames.items():
        if v == model_type:
            return k
    return model_type
    
def get_modelid_from_shortcutname(sc_name):
    if sc_name:
        return sc_name[sc_name.rfind(':') + 1:]

def set_shortcutname(modelname,modelid):
    if modelname and modelid:
        return f"{modelname}:{modelid}"
    
def get_image_url_to_shortcut_file(modelid, versionid, image_url):
    if image_url:
        version_image_prefix = f"{versionid}-"
        model_path = os.path.join(shortcut_info_folder, str(modelid))      
        image_id, ext = os.path.splitext(os.path.basename(image_url))
        description_img = os.path.join(model_path, f"{version_image_prefix}{image_id}{preview_image_ext}")
        return description_img
    return None  

def get_image_url_to_gallery_file(image_url):
    if image_url:
        image_id, ext = os.path.splitext(os.path.basename(image_url))
        description_img = os.path.join(shortcut_gallery_folder, f"{image_id}{preview_image_ext}")
        return description_img
    return None  

def save(env):
    try:
        with open(shortcut_setting, 'w') as f:
            json.dump(env, f, indent=4)
    except Exception as e:
        return False
    
    return True

def load():
    if not os.path.isfile(shortcut_setting):        
        save({})
        return
    
    json_data = None
    try:
        with open(shortcut_setting, 'r') as f:
            json_data = json.load(f)
    except:
        pass

    return json_data
    
# def add_custom_type(custom_types):
    
#     global model_folders,ui_typenames        
    
#     model_folders[custom_types['model_type']] = custom_types['model_folder']
#     ui_typenames[custom_types['ui_typename']] = custom_types['model_type']
