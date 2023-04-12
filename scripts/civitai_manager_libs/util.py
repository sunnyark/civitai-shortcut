import re
import os
import json
from . import setting

def printD(msg):    
    print(f"Civitai Manager: {msg}") 
    
def read_json(path)->dict:
    contents = None
    if not path:
        return None    
    try:
        with open(path, 'r') as f:
            contents = json.load(f)            
    except:
        return None
                
    return contents

def write_json(contents, path):
    if not path:
        return
    
    if not contents:
        return
        
    try:
        with open(path, 'w') as f:
            f.write(json.dumps(contents, indent=4))
    except Exception as e:
        return
        
  
def make_folder(version_info, lora_an=False, vs_folder=True):
    
    if not version_info:
        return
                
    if "model" not in version_info.keys():
        return
                       
    content_type = version_info['model']['type']
    model_name = version_info['model']['name']
    
    if not model_name:
        return
    
    model_name = model_name.strip()

    if lora_an and content_type == "LORA":
        model_folder = setting.folders_dict['ANLORA']
    elif content_type in setting.folders_dict.keys():
        model_folder = setting.folders_dict[content_type]        
    elif content_type:
        model_folder = os.path.join(setting.folders_dict['Unknown'], replace_dirname(content_type))
    else:
        model_folder = os.path.join(setting.folders_dict['Unknown'])
         
    if vs_folder:  

        vs_folder_name = None
        primary_file = None
        
        if len(version_info['files']) > 0:
            primary_file = version_info['files'][0]
                        
        if not primary_file:
            vs_folder_name = replace_filename(version_info['model']['name'] + "." + version_info['name'])
        vs_folder_name, ext = os.path.splitext(primary_file['name'])                 

        model_folder = os.path.join(model_folder, replace_dirname(model_name), replace_dirname(vs_folder_name))
    else:        
        model_folder = os.path.join(model_folder, replace_dirname(model_name))
                
    if not os.path.exists(model_folder):
        os.makedirs(model_folder)
                
    return model_folder  

def replace_filename(file_name):
    if file_name and len(file_name.strip()) > 0:
        return file_name.replace("*", "-").replace("?", "-").replace("\"", "-").replace("|", "-").replace(":", "-").replace("/", "-").replace("\\", "-").replace("<", "-").replace(">", "-")    
    return None

def replace_dirname(dir_name):
    if dir_name and len(dir_name.strip()) > 0:
        return dir_name.replace("*", "-").replace("?", "-").replace("\"", "-").replace("|", "-").replace(":", "-").replace("/", "-").replace("\\", "-").replace("<", "-").replace(">", "-")
    return None
    
def write_InternetShortcut(path, url):
    try:
        with open(path, 'w', newline='\r\n') as f:        
            f.write(f"[InternetShortcut]\nURL={url}")        
    except:
        return False    
    return True
    
def load_InternetShortcut(path)->str:
    urls = ""
    try:    
        with open(path, 'r') as f:
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
        file_list = list(set(file_list))
        return file_list
    return None