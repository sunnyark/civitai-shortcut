import os
import json
import shutil
from modules import shared
import modules.scripts as scripts

root_path = os.getcwd()

PLACEHOLDER = "<no select>"
NORESULT = "<no result>"  
    
# define model type name -> civitai system model type
model_types = {
    'checkpoint':'Checkpoint',
    'lora':'LORA',
    'locon':'LoCon',
    'textualinversion':'TextualInversion',
    'hypernetwork':'Hypernetwork',
    'aestheticgradient':'AestheticGradient',
    'controlnet':'Controlnet',
    'poses':'Poses',
    'wildcards':'Wildcards',
    'other':'Other',
          
    'vae':'VAE',          
    "anlora":"ANLORA",
    "unknown":"Unknown"
}

# civitai system model type -> folder path
model_folders = {
    model_types['checkpoint']: os.path.join("models","Stable-diffusion"),
    model_types['lora']: os.path.join("models","Lora"),
    model_types['locon']: os.path.join("models","Lora"),    
    model_types['textualinversion']: os.path.join("embeddings"),   
    model_types['hypernetwork']: os.path.join("models","hypernetworks"),         
    model_types['aestheticgradient']: os.path.join("extensions","stable-diffusion-webui-aesthetic-gradients","aesthetic_embeddings"),        
    model_types['controlnet']: os.path.join("extensions","sd-webui-controlnet","models"),
    model_types['poses']: os.path.join("models","Poses"),
    model_types['wildcards']: os.path.join("extensions","stable-diffusion-webui-wildcards","Wildcards"),    
    model_types['other']: os.path.join("models","Other"),    
    
    model_types['vae']: os.path.join("models","VAE"),    
    model_types['anlora']: os.path.join("extensions","sd-webui-additional-networks","models","lora"),    
    model_types['unknown']: os.path.join("models","Unkonwn"),
}

# UI 쪽에서 변환할때 쓰인다.
# UI model type -> civitai system model type
ui_model_types = {
    "Checkpoint" : model_types['checkpoint'],
    "LoRA" : model_types['lora'],
    "LyCORIS" : model_types['locon'],
    "Textual Inversion" : model_types['textualinversion'],
    "Hypernetwork" : model_types['hypernetwork'],
    "Aesthetic Gradient" : model_types['aestheticgradient'],
    "Controlnet" : model_types['controlnet'],
    "Poses" : model_types['poses'],
    "Wildcards" : model_types['wildcards'],
    "Other" : model_types['other'],
}

ModelUITypeFolder = { "model_types" : model_types,  "model_folders" : model_folders, "ui_model_types" : ui_model_types }


# content_types_list = ["Checkpoint","LORA","LoCon","TextualInversion","Hypernetwork","AestheticGradient","Controlnet","Poses","Wildcards","Other"]

# # UI 쪽에서 변환할때 쓰인다.
# # UI TYPE -> System Type
# content_types_dict = {
#     "Checkpoint" : content_types_list[0],
#     "LoRA" : content_types_list[1],
#     "LyCORIS" : content_types_list[2],
#     "Textual Inversion" : content_types_list[3],
#     "Hypernetwork" : content_types_list[4],
#     "Aesthetic Gradient" : content_types_list[5],
#     "Controlnet" : content_types_list[6],
#     "Poses" : content_types_list[7],
#     "Wildcards" : content_types_list[8],
#     "Other" : content_types_list[9],
# }

# folders_dict = {
#     content_types_list[0]: os.path.join("models","Stable-diffusion"),
#     content_types_list[1]: os.path.join("models","Lora"),
#     content_types_list[2]: os.path.join("models","Lora"),    
#     content_types_list[3]: os.path.join("embeddings"),   
#     content_types_list[4]: os.path.join("models","hypernetworks"),         
#     content_types_list[5]: os.path.join("extensions","stable-diffusion-webui-aesthetic-gradients","aesthetic_embeddings"),        
#     content_types_list[6]: os.path.join("extensions","sd-webui-controlnet","models"),
#     content_types_list[7]: os.path.join("models","Poses"),
#     content_types_list[8]: os.path.join("extensions","stable-diffusion-webui-wildcards","Wildcards"),    
#     content_types_list[9]: os.path.join("models","Other"),    
#     "VAE": os.path.join("models","VAE"),  
#     "Unknown": os.path.join("models","Unkonwn"),  
#     "ANLORA": os.path.join("extensions","sd-webui-additional-networks","models","lora"),    
# }

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


# 갤럴리 ui설정
gallery_column = 4
shortcut_colunm = 2  

# 
gallery_images_page_limit = 10

# 생성되는 폴더 및 파일
shortcut = "CivitaiShortCut.json"
shortcut_classification = "CivitaiShortCutClassification.json"
shortcut_thumbnail_folder =  "sc_thumb_images"
shortcut_save_folder =  "sc_saves"
# have model_name subfolder ... 
# add shortcut -> create model_name folder ..
# model_name/ modelid.info , versionid_images... 
# del shortcut --> rm model_name folder ..
# thumbnails update -->  shortcuts update : model_info update
shortcut_info_folder =  "sc_infos"

no_card_preview_image = os.path.join(root_path,"html","card-no-preview.png")


setting_file = "CivitaiShortCut_Setting.json"

Extensions_Name = "Civitai Shortcut"

# CivitaiShortCut_Setting.json
# {
#     "ModelUITypeFolder" : { "model_types" : model_types,  "model_folders" : model_folders, "ui_model_types" : ui_model_types }
# }


def write(ui_type_folder):
    SettingData = dict()    
    SettingData["ModelUITypeFolder"] = ui_type_folder
    
    path = os.path.join(scripts.basedir(), setting_file)
    try:
        with open(path, 'w') as f:
            json.dump(SettingData, f, indent=4)
    except Exception as e:
        return False
    
    return True

def read()->dict:
    path = os.path.join(scripts.basedir(), setting_file)
    
    if not os.path.isfile(path):
        return None
    
    m_types = None    
    m_folders = None
    ui_types = None
    
    ui_type_folder = None
    try:
        json_data = None
        with open(path, 'r') as f:
            json_data = json.load(f)            
            ui_type_folder = json_data["ModelUITypeFolder"]
            if "model_types" in ui_type_folder:
                m_types = ui_type_folder["model_types"]
            if "ui_model_types" in ui_type_folder:
                ui_types = ui_type_folder["ui_model_types"]
            if "model_folders" in ui_type_folder:
                m_folders = ui_type_folder["model_folders"]
            
            ui_type_folder = { "model_types" : m_types, "ui_model_types" : ui_types, "model_folders" : m_folders }
    except:
        return None
    
    return ui_type_folder
    
def load(ui_type_folder:dict):
    global model_types, ui_model_types, model_folders

    if not ui_type_folder:
        return False
    
    if "model_types" in ui_type_folder.keys():
        model_types.update(ui_type_folder['model_types'])

    if "model_folders" in ui_type_folder.keys():
        model_folders.update(ui_type_folder['model_folders'])

    if "ui_model_types" in ui_type_folder.keys():
        ui_model_types.update(ui_type_folder['ui_model_types'])
    
    return True
    
def make_model_type(civitai_type:str, ui_type:str, m_folder:str)->dict:
    
    if not civitai_type:
        return

    if not ui_type:
        return
    
    if not m_folder:
        return

    define_type = civitai_type.lower()

    m_types = dict()
    ui_types = dict()
    m_folders = dict()
    
    m_types[define_type] = civitai_type
    ui_types[ui_type] = civitai_type
    m_folders[civitai_type] = m_folder
    
    ui_type_folder = { "model_types" : m_types, "ui_model_types" : ui_types, "model_folders" : m_folders }
    
    return ui_type_folder
    
def add_model_type(ui_type_folder:dict, civitai_type:str, ui_type:str, m_folder:str)->dict:
    if not ui_type_folder:
        return None
    
    utf = make_model_type(civitai_type, ui_type, m_folder)
    
    if utf:
        ui_type_folder.update(utf)    
    
    return ui_type_folder
   
def delete_model_type(ui_type_folder:dict, civitai_type, ui_type):
    if not ui_type_folder:
        return None
    
    if not civitai_type:
        return ui_type_folder

    if not ui_type:
        return ui_type_folder    
    
    m_types = dict()
    ui_types = dict()
    m_folders = dict()
        
    if "model_types" in ui_type_folder.keys():
        m_types = ui_type_folder['model_types']

    if "model_folders" in ui_type_folder.keys():
        m_folders = ui_type_folder['model_folders']

    if "ui_model_types" in ui_type_folder.keys():
        ui_types = ui_type_folder['ui_model_types']
        
    define_type = civitai_type.lower()
        
    m_types.pop(define_type,None)    
    ui_types.pop(ui_type,None)
    m_folders.pop(civitai_type,None)
    
    return ui_type_folder