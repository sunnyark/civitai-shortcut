import re
import os
from . import setting

def printD(msg):    
    print(f"Civitai Manager: {msg}") 
    
def make_new_folder(content_type, model_name, lora_an=False):
    
    if not model_name:
        return
    
    model_name = model_name.strip()
    
    try:
        folder = setting.folders_dict[content_type]
    except: 
        # 알수 없는 타입일경우 언노운 폴더에 저장한다.
        if content_type:
            tmp_type = content_type.replace("|", "-").replace(":", "-").replace("/", "-").replace("\\", "-")
            folder = os.path.join(setting.folders_dict['Unknown'], tmp_type , model_name.replace("|", "-").replace(":", "-").replace("/", "-").replace("\\", "-"))
        else:                    
            folder = os.path.join(setting.folders_dict['Unknown'], content_type, model_name.replace("|", "-").replace(":", "-").replace("/", "-").replace("\\", "-"))
    
    if lora_an and content_type == "LORA":
        folder = setting.folders_dict['ANLORA']        
            
    model_folder = folder  
    #if content_type == "Checkpoint" or content_type == "Hypernetwork" or content_type =="LORA" or content_type == "Poses" or content_type == "TextualInversion" or content_type == "AestheticGradient":
    model_folder = os.path.join(model_folder, model_name.replace("|", "-").replace(":", "-").replace("/", "-").replace("\\", "-"))    
                
    if not os.path.exists(model_folder):
        os.makedirs(model_folder)
                
    return model_folder    

def write_InternetShortcut(path, url):
    with open(path, 'w', newline='\r\n') as f:        
        f.write(f"[InternetShortcut]\nURL={url}")
    return

def load_InternetShortcut(path)->str:
    urls = ""
    with open(path, 'r') as f:
        try:
            InternetShortcut = f.readline()            
            if not InternetShortcut or not "[InternetShortcut]" in InternetShortcut:
                return
            InternetShortcut = f.readline()
            if not InternetShortcut:
                return            
            urls = InternetShortcut[4:]
        except Exception as e:
            printD(e)
            return                
    return urls 

# get image with full size
# width is in number, not string
# 파일 인포가 있는 원본 이미지 주소이다.
def get_full_size_image_url(image_url, width):
    return re.sub('/width=\d+/', '/width=' + str(width) + '/', image_url)

def change_width_from_image_url(image_url, width):
    return re.sub('/width=\d+/', '/width=' + str(width) + '/', image_url)

# get id from url
def get_model_id_from_url(url):
    id = ""

    if not url:
        return ""

    if url.isnumeric():
        # is already an id
        id = str(url)
        return id
    
    s = url.split("/")
    if len(s) < 2:
        return ""
    
    if s[-2].isnumeric():
        id  = s[-2]
    elif s[-1].isnumeric():
        id  = s[-1]
    else:
        return ""
    
    return id