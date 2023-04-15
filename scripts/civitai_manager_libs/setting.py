import os
from modules import shared
import modules.scripts as scripts

root_path = os.getcwd()

PLACEHOLDER = "<no select>"
NORESULT = "<no result>"

content_types_list = ["Checkpoint","LORA","LoCon","TextualInversion","Hypernetwork","AestheticGradient","Controlnet","Poses","Wildcards","Other"]

folders_dict = {
    content_types_list[0]: os.path.join("models","Stable-diffusion"),
    content_types_list[1]: os.path.join("models","Lora"),
    content_types_list[2]: os.path.join("models","Lora"),    
    content_types_list[3]: os.path.join("embeddings"),   
    content_types_list[4]: os.path.join("models","hypernetworks"),         
    content_types_list[5]: os.path.join("extensions","stable-diffusion-webui-aesthetic-gradients","aesthetic_embeddings"),        
    content_types_list[6]: os.path.join("extensions","sd-webui-controlnet","models"),
    content_types_list[7]: os.path.join("models","Poses"),
    content_types_list[8]: os.path.join("extensions","stable-diffusion-webui-wildcards","Wildcards"),    
    content_types_list[9]: os.path.join("models","Other"),    
    "VAE": os.path.join("models","VAE"),  
    "Unknown": os.path.join("models","Unkonwn"),  
    "ANLORA": os.path.join("extensions","sd-webui-additional-networks","models","lora"),    
}

# UI 쪽에서 변환할때 쓰인다.
content_types_dict = {
    "Checkpoint" : content_types_list[0],
    "LoRA" : content_types_list[1],
    "LyCORIS" : content_types_list[2],
    "Textual Inversion" : content_types_list[3],
    "Hypernetwork" : content_types_list[4],
    "Aesthetic Gradient" : content_types_list[5],
    "Controlnet" : content_types_list[6],
    "Poses" : content_types_list[7],
    "Wildcards" : content_types_list[8],
    "Other" : content_types_list[9],
}
 
# civitai helper 호환성
info_ext = ".info"
info_suffix = ".civitai"

triger_ext = ".txt"
triger_suffix = ".triger"

preview_image_ext = ".png"
preview_image_suffix = ".preview"

gallery_column = 4
shortcut_colunm = 2  
shortcut = "CivitaiShortCut.json"
shortcut_thumnail_folder =  "sc_thumb_images"
shortcut_save_folder =  "sc_saves"

civitai_information_tab = 0
saved_information_tab = 1
# have model_name subfolder ... 
# add shortcut -> create model_name folder ..
# model_name/ modelid.info , versionid_images... 
# del shortcut --> rm model_name folder ..
# thumbnails update -->  shortcuts update : model_info update
shortcut_info_folder =  "sc_infos"

no_card_preview_image = os.path.join(root_path,"html","card-no-preview.png")




