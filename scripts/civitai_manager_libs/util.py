import re
import os
import json
from . import setting

import hashlib
import io
import platform
import subprocess

from modules import shared
import modules.scripts as scripts

def printD(msg):    
    print(f"{setting.Extensions_Name}: {msg}") 

# # Now, hashing use the same way as pip's source code.
# def gen_file_sha256(filname):
#     printD("Use Memory Optimized SHA256")
#     blocksize=1 << 20
#     h = hashlib.sha256()
#     length = 0
#     with open(os.path.realpath(filname), 'rb') as f:
#         for block in read_chunks(f, size=blocksize):
#             length += len(block)
#             h.update(block)

#     hash_value =  h.hexdigest()
#     printD("sha256: " + hash_value)
#     printD("length: " + str(length))
#     return hash_value

# def read_chunks(file, size=io.DEFAULT_BUFFER_SIZE):
#     """Yield pieces of data from a file-like object until EOF."""
#     while True:
#         chunk = file.read(size)
#         if not chunk:
#             break
#         yield chunk

def update_url(url, param_name, new_value):
    if param_name not in url:
        # If the parameter is not found in the URL, add it to the end with the new value
        if "?" in url:
            # If there are already other parameters in the URL, add the new parameter with "&" separator
            updated_url = url + "&" + param_name + "=" + str(new_value)
        else:
            # If there are no parameters in the URL, add the new parameter with "?" separator
            updated_url = url + "?" + param_name + "=" + str(new_value)
    else:
        # If the parameter is found in the URL, update its value with the new value
        prefix, suffix = url.split(param_name + "=")
        if "&" in suffix:
            current_value, remainder = suffix.split("&", 1)
            updated_suffix = param_name + "=" + str(new_value) + "&" + remainder
        else:
            updated_suffix = param_name + "=" + str(new_value)
        updated_url = prefix + updated_suffix

    return updated_url

def add_number_to_duplicate_files(filenames):    
    counts = {}
    for i, filename in enumerate(filenames):        
        if filename in counts:
            name, ext = os.path.splitext(filename)
            counts[filename] += 1
            filenames[i] = f"{name} ({counts[filename]}){ext}"
        else:
            counts[filename] = 0
    return filenames
    
def open_folder(path):
    if os.path.exists(path):
        # Code from ui_common.py
        if not shared.cmd_opts.hide_ui_dir_config:
            if platform.system() == "Windows":
                os.startfile(path)
            elif platform.system() == "Darwin":
                subprocess.Popen(["open", path])
            elif "microsoft-standard-WSL2" in platform.uname().release:
                subprocess.Popen(["wsl-open", path])
            else:
                subprocess.Popen(["xdg-open", path])
                
def get_search_keyword(search:str):
    tags = []
    keys = []
    
    if not search:
        return None , None
    
    for word in search.split(","):
        word = word.strip().lower()
        if word.startswith("#"):
            if len(word) > 1:
                tag = word[1:]
                if tag not in tags:
                    tags.append(tag)
        else:
            if word not in keys:
                keys.append(word)
                    
    return keys if len(keys) > 0 else None, tags if len(tags) > 0 else None
    
    
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

    if lora_an and content_type == setting.model_types['lora']:
        model_folder = setting.model_folders[setting.model_types['anlora']]
    elif content_type in setting.model_folders.keys():
        model_folder = setting.model_folders[content_type]        
    elif content_type:
        model_folder = os.path.join(setting.model_folders[setting.model_types['unknown']], replace_dirname(content_type))
    else:
        model_folder = os.path.join(setting.model_folders[setting.model_types['unknown']])
         
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