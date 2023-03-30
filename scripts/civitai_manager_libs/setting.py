import os
from modules import shared
import modules.scripts as scripts
from . import util
from . import model

root_path = os.getcwd()

PLACEHOLDER = "<no select>"
NORESULT = "<no result>"

page_dict = {
    "limit" : 50,
}

page_action_dict = {
    "search" : "Search", 
    "prevPage" : "Prev Page",
    "nextPage" : "Next Page",    
}

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
           
# get cusomter model path
def init_civitai_manager():
    global root_path
    global folders_dict
    global civitai_shortcut

    root_path = os.getcwd()
    
    if shared.cmd_opts.embeddings_dir:
        folders_dict["TextualInversion"] = shared.cmd_opts.embeddings_dir

    if shared.cmd_opts.hypernetwork_dir :
        folders_dict["Hypernetwork"] = shared.cmd_opts.hypernetwork_dir

    if shared.cmd_opts.ckpt_dir:
        folders_dict["Checkpoint"] = shared.cmd_opts.ckpt_dir

    if shared.cmd_opts.lora_dir:
        folders_dict["LORA"] = shared.cmd_opts.lora_dir
        folders_dict["LoCon"] = shared.cmd_opts.lora_dir
    
    civitai_shortcut = os.path.join(scripts.basedir(),civitai_shortcut)


    # if not os.path.exists(folders_custom_dict["INTERNETSHORTCUT"]):
    #     os.makedirs(folders_custom_dict["INTERNETSHORTCUT"])
                    
    # util.printD(f"Check ok! : Civitai Internet shortcut save folder : {folders_custom_dict['INTERNETSHORTCUT']}")
        
        