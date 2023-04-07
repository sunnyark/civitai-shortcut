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
   
civitai_shortcut = "CivitaiShortCut.json"
civitai_shortcut_thumnail_folder =  "sc_thum_images"
civitai_shortcut_save_folder =  "sc_saves"
civitai_no_card_preview_image = os.path.join(root_path,"html","card-no-preview.png")

