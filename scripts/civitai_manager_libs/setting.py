import os
import json
import shutil

from modules import scripts, script_callbacks, shared
from . import util

root_path = os.getcwd()
extension_base = scripts.basedir()
# extension_base = os.path.join("extensions","civitai-shortcut")

headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.68',
         "Authorization": ""}

civitai_api_key = ""
Extensions_Name = "Civitai Shortcut"
Extensions_Version = "v1.6.7"

PLACEHOLDER = "[No Select]"
NORESULT = "[No Result]"
NEWRECIPE = "[New Prompt Recipe]"
NEWCLASSIFICATION = "[New Classification]"

CREATE_MODEL_FOLDER = "Create a model folder to download the model"
# CREATE_MODEL_FOLDER = "Create a model folder with the model name"

model_exts = (".bin", ".pt", ".safetensors", ".ckpt")

# sd_version = ['SD1', 'SD2', 'SDXL', 'Unknown']
model_basemodels = {
    "SD 1.4":"SD1", 
    "SD 1.5":"SD1", 
    "SD 2.0":"SD2", 
    "SD 2.0 768":"SD2", 
    "SD 2.1":"SD2", 
    "SD 2.1 768":"SD2", 
    "SD 2.1 Unclip":"SD2", 
    "SDXL 0.9":"SDXL", 
    "SDXL 1.0":"SDXL", 
    
    "SDXL 1.0 LCM":"SDXL", 
    "SDXL Distilled":"SDXL", 
    "SDXL Turbo":"SDXL", 
    "SDXL Lightning":"SDXL", 
    "Pony":"Pony", 
    "SVD":"SVD", 
    "SVD XT":"SVD", 
    "Stable Cascade":"SC", 
    "Playground V2":"PGV2", 
    "PixArt A":"PixArtA",     
    
    "Other":"Unknown"
}

# civitai model type -> folder path
model_folders = {
    'Checkpoint': os.path.join("models","Stable-diffusion"),
    'LORA': os.path.join("models","Lora"),
    'LoCon': os.path.join("models","LyCORIS"),
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

# UI type 하나에 다중의 civitai type을 대입할때 대상이 되는것은  get_ui_typename 함수와 ishortcut->get_image_list 와 get_list 뿐이다.
# 나머지는 key로만 쓰이기 때문에 value 값이 배열이라 해도문제가 안될듯한다.
# ishortcut 부분은 여기를
# tmp_types.append(setting.ui_typenames[sc_type])
# ->
# for type_name in setting.ui_typenames[sc_type]:
#     tmp_types.append(type_name)
# 이리 하면 될듯

# get_ui_typename는 이렇게 수정해도 문제 없을것 같다. 대신 모두 "" : ["",""] 형식으로 바꿔야 할듯(안해도 되나?)
# def get_ui_typename(model_type):
#     for k,v in ui_typenames.items():
#         if model_type in v:
#             return k
#     return model_type

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
usergal_information_tab = 1
download_information_tab = 2

# civitai helper 호환성
info_ext = ".info"
info_suffix = ".civitai"

triger_ext = ".txt"
triger_suffix = ".triger"

preview_image_ext = ".png"
preview_image_suffix = ".preview"

# 임시설정

# 갤러리 height 설정
information_gallery_height = "auto" # auto , fit

# 화면 분할 비율
shortcut_browser_screen_split_ratio = 3
shortcut_browser_screen_split_ratio_max  = 10

shortcut_browser_search_up = False

# 갤러리 ui설정
# model browser 설정
shortcut_column = 5
shortcut_rows_per_page = 4
gallery_column = 7

# 유저 갤러리 설정
usergallery_images_column = 6
usergallery_images_rows_per_page = 2

# prompt recipe 설정
prompt_shortcut_column = 5
prompt_shortcut_rows_per_page = 4
prompt_reference_shortcut_column = 8
prompt_reference_shortcut_rows_per_page = 4

# classification 설정
classification_shortcut_column = 5
classification_shortcut_rows_per_page = 4

classification_gallery_column = 8
classification_gallery_rows_per_page = 4

shortcut_max_download_image_per_version = 0 # 버전당 최대 다운로드 이미지 수 , 0이면 전체다운 받는다
gallery_thumbnail_image_style = "scale-down"

# 다운로드 설정
download_images_folder = os.path.join("outputs","download-images")

# background thread 설정
# shortcut_auto_update = True
shortcut_update_when_start = True
usergallery_preloading = False

# 생성되는 폴더 및 파일
shortcut = "CivitaiShortCut.json"
shortcut_setting = "CivitaiShortCutSetting.json"
shortcut_classification = "CivitaiShortCutClassification.json"
shortcut_civitai_internet_shortcut_url = "CivitaiShortCutBackupUrl.json"
shortcut_recipe = "CivitaiShortCutRecipeCollection.json"

# shortcut_thumbnail_folder =  "sc_thumb"
shortcut_thumbnail_folder =  "sc_thumb_images"
shortcut_recipe_folder =  "sc_recipes"
shortcut_info_folder =  "sc_infos"
shortcut_gallery_folder =  "sc_gallery"

no_card_preview_image = os.path.join(extension_base,"img","card-no-preview.png")
nsfw_disable_image = os.path.join(extension_base,"img","nsfw-no-preview.png")

NSFW_filtering_enable = True
# NSFW_level = { "None":True, "Soft":False, "Mature":False, "X":False } # None, Soft, Mature, X
NSFW_levels = ("None","Soft","Mature","X","XX") # None, Soft, Mature, X
NSFW_level_user = "None"

shortcut_env = dict()

def set_NSFW(enable, level="None"):
    # global NSFW_level
    global NSFW_filtering_enable
    global NSFW_level_user

    NSFW_filtering_enable = enable
    NSFW_level_user = level

def save_NSFW():
    global NSFW_filtering_enable
    global NSFW_level_user

    environment = load()
    if not environment:
         environment = dict()

    nsfw_filter = dict()
    nsfw_filter['nsfw_filter_enable'] = NSFW_filtering_enable
    nsfw_filter['nsfw_level'] = NSFW_level_user
    environment['NSFW_filter'] = nsfw_filter

    save(environment)

def init():
    global extension_base

    global shortcut
    global shortcut_setting
    global shortcut_classification
    global shortcut_civitai_internet_shortcut_url
    global shortcut_recipe

    global shortcut_thumbnail_folder
    global shortcut_recipe_folder
    global shortcut_info_folder
    global shortcut_gallery_folder

    shortcut = os.path.join(extension_base,shortcut)
    shortcut_setting = os.path.join(extension_base,shortcut_setting)
    shortcut_classification = os.path.join(extension_base,shortcut_classification)
    shortcut_recipe = os.path.join(extension_base,shortcut_recipe)
    shortcut_civitai_internet_shortcut_url = os.path.join(extension_base,shortcut_civitai_internet_shortcut_url)

    shortcut_thumbnail_folder = os.path.join(extension_base,shortcut_thumbnail_folder)
    shortcut_recipe_folder = os.path.join(extension_base,shortcut_recipe_folder)
    shortcut_info_folder = os.path.join(extension_base,shortcut_info_folder)
    shortcut_gallery_folder = os.path.join(extension_base,shortcut_gallery_folder)

    load_data()

def load_data():
    global model_folders

    global shortcut_column
    global shortcut_rows_per_page
    global gallery_column
    global classification_shortcut_column
    global classification_shortcut_rows_per_page
    global classification_gallery_column
    global classification_gallery_rows_per_page
    global usergallery_images_column
    global usergallery_images_rows_per_page

    global prompt_shortcut_column
    global prompt_shortcut_rows_per_page
    global prompt_reference_shortcut_column
    global prompt_reference_shortcut_rows_per_page

    global shortcut_max_download_image_per_version
    global gallery_thumbnail_image_style
    global shortcut_browser_search_up

    global download_images_folder
    global shortcut_browser_screen_split_ratio
    global information_gallery_height

    global shortcut_update_when_start
    global civitai_api_key

    if shared.cmd_opts.embeddings_dir:
        model_folders['TextualInversion'] = shared.cmd_opts.embeddings_dir

    if shared.cmd_opts.hypernetwork_dir :
        model_folders['Hypernetwork'] = shared.cmd_opts.hypernetwork_dir

    if shared.cmd_opts.ckpt_dir:
        model_folders['Checkpoint'] = shared.cmd_opts.ckpt_dir

    if shared.cmd_opts.lora_dir:
        model_folders['LORA'] = shared.cmd_opts.lora_dir

    environment = load()
    if environment:
        if "NSFW_filter" in  environment.keys():
            nsfw_filter = environment['NSFW_filter']
            filtering_enable = True
            if 'nsfw_filter_enable' in nsfw_filter.keys():
                filtering_enable = bool(nsfw_filter['nsfw_filter_enable'])

            if 'nsfw_level' in  nsfw_filter.keys():
                set_NSFW(filtering_enable, nsfw_filter['nsfw_level'])

        if "application_allow" in environment.keys():
            application_allow = environment['application_allow']

            if "civitai_api_key" in application_allow.keys():
                civitai_api_key = application_allow['civitai_api_key']
            if "shortcut_update_when_start" in application_allow.keys():
                shortcut_update_when_start = bool(application_allow['shortcut_update_when_start'])
            if "shortcut_max_download_image_per_version" in application_allow.keys():
                shortcut_max_download_image_per_version = int(application_allow['shortcut_max_download_image_per_version'])

        if "screen_style" in environment.keys():
            screen_style = environment['screen_style']

            if "shortcut_browser_screen_split_ratio" in screen_style.keys():
                shortcut_browser_screen_split_ratio = int(screen_style['shortcut_browser_screen_split_ratio'])
            if "information_gallery_height" in screen_style.keys():
                if screen_style['information_gallery_height'].strip():
                    information_gallery_height = screen_style['information_gallery_height']
            if "gallery_thumbnail_image_style" in screen_style.keys():
                gallery_thumbnail_image_style = screen_style['gallery_thumbnail_image_style']
            if "shortcut_browser_search_up" in screen_style.keys():
                shortcut_browser_search_up = bool(screen_style['shortcut_browser_search_up'])

        if "image_style" in environment.keys():
            image_style = environment['image_style']

            if "shortcut_column" in image_style.keys():
                shortcut_column = int(image_style['shortcut_column'])
            if "shortcut_rows_per_page" in image_style.keys():
                shortcut_rows_per_page = int(image_style['shortcut_rows_per_page'])

            if "gallery_column" in image_style.keys():
                gallery_column = int(image_style['gallery_column'])

            if "classification_shortcut_column" in image_style.keys():
                classification_shortcut_column = int(image_style['classification_shortcut_column'])
            if "classification_shortcut_rows_per_page" in image_style.keys():
                classification_shortcut_rows_per_page = int(image_style['classification_shortcut_rows_per_page'])
            if "classification_gallery_column" in image_style.keys():
                classification_gallery_column = int(image_style['classification_gallery_column'])
            if "classification_gallery_rows_per_page" in image_style.keys():
                classification_gallery_rows_per_page = int(image_style['classification_gallery_rows_per_page'])

            if "usergallery_images_column" in image_style.keys():
                usergallery_images_column = int(image_style['usergallery_images_column'])
            if "usergallery_images_rows_per_page" in image_style.keys():
                usergallery_images_rows_per_page = int(image_style['usergallery_images_rows_per_page'])

            if "prompt_shortcut_column" in image_style.keys():
                prompt_shortcut_column = int(image_style['prompt_shortcut_column'])
            if "prompt_shortcut_rows_per_page" in image_style.keys():
                prompt_shortcut_rows_per_page = int(image_style['prompt_shortcut_rows_per_page'])
            if "prompt_reference_shortcut_column" in image_style.keys():
                prompt_reference_shortcut_column = int(image_style['prompt_reference_shortcut_column'])
            if "prompt_reference_shortcut_rows_per_page" in image_style.keys():
                prompt_reference_shortcut_rows_per_page = int(image_style['prompt_reference_shortcut_rows_per_page'])

        if "model_folders" in environment.keys():

            user_folders = environment['model_folders']

            if 'LoCon' in user_folders.keys():
                model_folders['LoCon'] = user_folders['LoCon']

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

        if "download_folders" in environment.keys():

            download_folders = environment['download_folders']
            if 'download_images' in download_folders.keys():
                download_images_folder = download_folders['download_images']

        if "temporary" in environment.keys():
            temporary = environment['temporary']

def generate_type_basefolder(content_type):

    if content_type in model_folders.keys():
        model_folder = model_folders[content_type]
    elif content_type:
        model_folder = os.path.join(model_folders['Unknown'], util.replace_dirname(content_type))
    else:
        model_folder = os.path.join(model_folders['Unknown'])

    return model_folder

def generate_version_foldername(model_name,ver_name,ver_id):
    return f"{model_name}-{ver_name}"

def get_model_folders():
    return model_folders.values()

def get_ui_typename(model_type):
    for k,v in ui_typenames.items():
        if v == model_type:
            return k
    return model_type

def get_imagefn_and_shortcutid_from_recipe_image(recipe_image):
    if recipe_image:
        result = recipe_image.split(":", 1)
        if len(result) > 1:
            return result[0], result[1]
        return None, None

def set_imagefn_and_shortcutid_for_recipe_image( shortcutid,image_fn):
    if image_fn and shortcutid:
        return f"{shortcutid}:{image_fn}"

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
