import re
import os
from . import setting

def printD(msg):    
    print(f"Civitai Manager: {msg}") 
    
def make_model_folder(content_type, model_name, lora_an=False):
    
    if not model_name:
        return
    
    model_name = model_name.strip()

    if lora_an and content_type == "LORA":
        model_folder = setting.folders_dict['ANLORA']
    elif content_type in setting.folders_dict.keys():
        model_folder = setting.folders_dict[content_type]        
    elif content_type:
        model_folder = os.path.join(setting.folders_dict['Unknown'], content_type.replace("|", "-").replace(":", "-").replace("/", "-").replace("\\", "-"))
    else:
        model_folder = os.path.join(setting.folders_dict['Unknown'])
         
    model_folder = os.path.join(model_folder, model_name.replace("|", "-").replace(":", "-").replace("/", "-").replace("\\", "-"))    
                
    if not os.path.exists(model_folder):
        os.makedirs(model_folder)
                
    return model_folder   
 
def replace_filename(file_name):
    if file_name and len(file_name.strip()) > 0:
        return file_name.replace("*", "-").replace("?", "-").replace("\"", "-").replace("|", "-").replace(":", "-").replace("/", "-").replace("\\", "-")    
    return None

def replace_dirname(dir_name):
    if dir_name and len(dir_name.strip()) > 0:
        return dir_name.replace("|", "-").replace(":", "-").replace("/", "-").replace("\\", "-")
    return None
    
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
    return urls.strip()

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

def search_file(root_dirs:list,base,ext)->list:
    file_list = list()
    #root_path = "D:\\AI\\stable-diffusion-webui"
    root_path = os.getcwd()
        
    for root_dir in root_dirs:
        #print(f"{os.path.join(root_path,root_dir)}\n")
        for (root,dirs,files) in os.walk(os.path.join(root_path,root_dir)):
            # if len(dirs) > 0:
            #     for dir_name in dirs:
            #         print("dir: " + dir_name)        
            if len(files) > 0:
                for file_name in files:               
                    b, e = os.path.splitext(file_name) 
                    if base and ext:
                        if e == ext and b == base:
                            file_list.append(os.path.join(root,file_name))                        
                    elif base:
                        if b == base:
                            file_list.append(os.path.join(root,file_name))
                    elif ext:
                        if e == ext:
                            file_list.append(os.path.join(root,file_name))
                    else:       
                        file_list.append(os.path.join(root,file_name))                        
                    
    if len(file_list) > 0:
        return file_list
    return None