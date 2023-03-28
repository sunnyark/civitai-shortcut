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

folders_dict = {
    "Checkpoint": os.path.join("models","Stable-diffusion"),
    "LORA": os.path.join("models","Lora"),
    "LoCon": os.path.join("models","Lora"),
    "Hypernetwork": os.path.join("models","hypernetworks"),
    "TextualInversion": os.path.join("embeddings"),            
    "AestheticGradient": os.path.join("extensions","stable-diffusion-webui-aesthetic-gradients","aesthetic_embeddings"),
    "VAE": os.path.join("models","VAE"),        
    "Controlnet" : os.path.join("extensions","sd-webui-controlnet","models"),
    "Poses" : os.path.join("models","Poses"),
    "ANLORA": os.path.join("extensions","sd-webui-additional-networks","models","lora"),
    "Unknown": os.path.join("models","Unknown"),
}

# 아니다. json 파일에 저장하자
# folders_custom_dict = {
#     "INTERNETSHORTCUT" : "InternetShortCut",
# }

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
        
        