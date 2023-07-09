import io
import re
import os
import json

import hashlib
import platform
import subprocess

from modules import scripts, script_callbacks, shared

from . import setting
from tqdm import tqdm

# from modules import images
# def run_pnginfo(image, image_path, image_file_name):
#     if image is None:
#         return '', '', '', '', ''
#     try:
#         geninfo, items = images.read_info_from_image(image)
#         items = {**{'parameters': geninfo}, **items}

#         info = ''
#         for key, text in items.items():
#             info += f"""
#                 <div>
#                 <p><b>{plaintext_to_html(str(key))}</b></p>
#                 <p>{plaintext_to_html(str(text))}</p>
#                 </div>
#                 """.strip()+"\n"
#     except UnidentifiedImageError as e:
#         geninfo = None
#         info = ""
    
#     if geninfo is None:
#         try:
#             filename = os.path.splitext(image_file_name)[0] + ".txt"
#             geninfo = ""
#             with open(filename) as f:
#                 for line in f:
#                     geninfo += line
#         except Exception:
#             logger.warning(f"run_pnginfo: No EXIF in image or txt file")

#     if openoutpaint:
#         prompt, neg_prompt = wib_db.select_prompts(image_file_name)
#         if prompt == "0":
#             prompt = ""
#         if neg_prompt == "0":
#             neg_prompt = ""
#     else:
#         prompt = ""
#         neg_prompt = ""

#     return '', geninfo, info, prompt, neg_prompt

def printD(msg):    
    print(f"{setting.Extensions_Name}: {msg}") 

def calculate_sha256(filname):
    """
    Calculate the SHA256 hash for a file.
    """
    block_size = 1024 * 1024 # 1MB
    length = 0
    with open(filname, 'rb') as file:
        hash = hashlib.sha256()
        for chunk in tqdm(iter(lambda: file.read(block_size), b""), total=(os.path.getsize(filname)//block_size)+1):
            length += len(chunk)
            hash.update(chunk)

        hash_value = hash.hexdigest()
        printD("sha256: " + hash_value)
        printD("length: " + str(length))
        return hash_value
    
def is_url_or_filepath(input_string):
    if not input_string:
        return "unknown"
    
    if os.path.exists(input_string):
        return "filepath"
    elif input_string.lower().startswith("http://") or input_string.lower().startswith("https://"):
        return "url"
    else:
        return "unknown"
    
def convert_civitai_meta_to_stable_meta(meta:dict):
    meta_string = ""
    different_key=['prompt', 'negativePrompt','steps','sampler','cfgScale','seed','resources','hashes']
    if meta:
        if "prompt" in meta:
            meta_string = f"""{meta['prompt']}""" + "\n"
        if "negativePrompt" in meta:
            meta_string = meta_string + f"""Negative prompt:{meta['negativePrompt']}""" + "\n"
        if "steps" in meta:
            meta_string = meta_string + f",Steps:{meta['steps']}"                
        if "sampler" in meta:
            meta_string = meta_string + f",Sampler:{meta['sampler']}"
        if "cfgScale" in meta:
            meta_string = meta_string + f",CFG scale:{meta['cfgScale']}"
        if "seed" in meta:
            meta_string = meta_string + f",Seed:{meta['seed']}"
            
        addistion_string = ','.join([f'{key}:{value}' for key, value in meta.items() if key not in different_key])
        meta_string = meta_string + "," + addistion_string       
                    
    return meta_string  

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

def add_number_to_duplicate_files(filenames)->dict:
    counts = {}
    for i, filename in enumerate(filenames):        
        if filename in counts:
            name, ext = os.path.splitext(filename)
            counts[filename] += 1
            filenames[i] = f"{name} ({counts[filename]}){ext}"
        else:
            counts[filename] = 0
            
    # 굳이 안해도 dict가 되네???? 
    # result = dict()
    # if filenames:
    #     for filename in filenames:
    #         file = filename[filename.lfind(':') + 1:]
    #         id = filename[:filename.lfind(':')]
    #         result[str(id)] = file
    #     return result
            
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
                
def get_search_keyword_o(search:str):
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
    
def get_search_keyword(search:str):
    tags = []
    keys = []
    clfs = []
        
    if not search:
        return None , None, None
    
    for word in search.split(","):
        word = word.strip()
        if word.startswith("#"):
            if len(word) > 1:
                tag = word[1:].lower()
                if tag not in tags:
                    tags.append(tag)
        elif word.startswith("@"):
            if len(word) > 1:
                clf = word[1:]
                if clf not in clfs:
                    clfs.append(clf)
        else:
            word = word.lower()
            if word not in keys:                
                keys.append(word)
                    
    return keys if len(keys) > 0 else None, tags if len(tags) > 0 else None, clfs if len(clfs) > 0 else None    

# def get_search_keyword(search:str):
#     tags = []
#     keys = []
#     clfs = []
#     filenames = []
    
#     if not search:
#         return None , None, None
    
#     for word in search.split(","):
#         word = word.strip()
#         if word.startswith("#"):
#             if len(word) > 1:
#                 tag = word[1:].lower()
#                 if tag not in tags:
#                     tags.append(tag)
#         elif word.startswith("@"):
#             if len(word) > 1:
#                 clf = word[1:]
#                 if clf not in clfs:
#                     clfs.append(clf)
#         elif word.startswith("!"):
#             if len(word) > 1:
#                 filename = word[1:].lower()
#                 if filename not in filenames:
#                     filenames.append(filename)                    
#         else:
#             word = word.lower()
#             if word not in keys:                
#                 keys.append(word)
                    
#     return keys if len(keys) > 0 else None, tags if len(tags) > 0 else None, clfs if len(clfs) > 0 else None, filenames if len(filenames) > 0 else None    

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

def scan_folder_for_info(folder):
    info_list = search_file([folder],None,[setting.info_ext])
    
    if not info_list:             
        return None
    
    return info_list
            
# def make_version_folder(version_info, vs_folder=True, vs_foldername=None, ms_foldername=None):
    
#     if not version_info:
#         return
                
#     if "model" not in version_info.keys():
#         return
                       
#     content_type = version_info['model']['type']
    
#     if not ms_foldername:
#         ms_foldername = version_info['model']['name']
#     elif len(ms_foldername.strip()) <= 0:
#         ms_foldername = version_info['model']['name']
#     ms_foldername = ms_foldername.strip()
        
#     model_folder = setting.generate_model_foldername(content_type, ms_foldername)                     
    
#     if not model_folder:
#         return
    
#     if vs_folder:        
#         if not vs_foldername:
#             vs_foldername = setting.generate_version_foldername(ms_foldername,version_info['name'],version_info['id'])
#         elif len(vs_foldername.strip()) <= 0:
#             vs_foldername = setting.generate_version_foldername(ms_foldername,version_info['name'],version_info['id'])

#         model_folder = os.path.join(model_folder, replace_dirname(vs_foldername.strip()))
                
#     if not os.path.exists(model_folder):
#         os.makedirs(model_folder)
                
#     return model_folder  

def get_download_image_folder(ms_foldername):

    if not ms_foldername:
        return

    if not setting.download_images_folder:
        return
                        
    model_folder = os.path.join(setting.download_images_folder.strip(), replace_dirname(ms_foldername.strip()))
                
    if not os.path.exists(model_folder):
        return None
                
    return model_folder  

def make_download_image_folder(ms_foldername):

    if not ms_foldername:
        return

    if not setting.download_images_folder:
        return
                        
    model_folder = os.path.join(setting.download_images_folder.strip(), replace_dirname(ms_foldername.strip()))
                
    if not os.path.exists(model_folder):
        os.makedirs(model_folder)
                
    return model_folder  

# 다정하면 임의의 분류뒤에 모델폴더를 생성하고 그뒤에 버전까지 생성가능
# def make_download_model_folder(version_info, ms_folder=True, vs_folder=True, vs_foldername=None, cs_foldername=None):
    
#     if not version_info:
#         return
                
#     if "model" not in version_info.keys():
#         return
                       
#     content_type = version_info['model']['type']
#     ms_foldername = version_info['model']['name']
               
#     model_folder = setting.generate_type_basefolder(content_type)
    
#     if not model_folder:
#         return
    
#     if not cs_foldername and not ms_folder:
#         return
    
#     if cs_foldername:
#         model_folder = os.path.join(model_folder, replace_dirname(cs_foldername.strip()))
                
#     if ms_folder:
#         model_folder = os.path.join(model_folder, replace_dirname(ms_foldername.strip()))
        
#     if vs_folder:        
#         if not vs_foldername:
#             vs_foldername = setting.generate_version_foldername(ms_foldername,version_info['name'],version_info['id'])
#         elif len(vs_foldername.strip()) <= 0:
#             vs_foldername = setting.generate_version_foldername(ms_foldername,version_info['name'],version_info['id'])

#         model_folder = os.path.join(model_folder, replace_dirname(vs_foldername.strip()))
                
#     if not os.path.exists(model_folder):
#         os.makedirs(model_folder)
                
#     return model_folder  

def make_download_model_folder(version_info, ms_folder=True, vs_folder=True, vs_foldername=None, cs_foldername=None, ms_foldername=None):
    
    if not version_info:
        return
                
    if "model" not in version_info.keys():
        return
                       
    content_type = version_info['model']['type']                   
    model_folder = setting.generate_type_basefolder(content_type)
    
    if not model_folder:
        return
    
    if not cs_foldername and not ms_folder:
        return
    
    if cs_foldername:
        model_folder = os.path.join(model_folder, replace_dirname(cs_foldername.strip()))
                
    if ms_folder:
        if not ms_foldername or len(ms_foldername.strip()) <= 0:
            ms_foldername = version_info['model']['name']
        
        model_folder = os.path.join(model_folder, replace_dirname(ms_foldername.strip()))
        
    if vs_folder:        
        if not vs_foldername or len(vs_foldername.strip()) <= 0:
            vs_foldername = setting.generate_version_foldername(ms_foldername, version_info['name'], version_info['id'])

        model_folder = os.path.join(model_folder, replace_dirname(vs_foldername.strip()))
                
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
    
# def load_InternetShortcut(path)->str:
#     urls = ""
#     try:    
#         with open(path, 'r') as f:
#         #with open(path, 'r', encoding='utf8') as f:            
#             content = f.readlines()
#             for line in content:
#                 if line.startswith('URL='):
#                     urls = line[4:]
#     except Exception as e:
#         printD(e)
#         return

#     return urls.strip()

def load_InternetShortcut(path)->str:
    urls = list()
    try:    
        with open(path, 'r') as f:
            content = f.read()
            # urls = re.findall("(?P<url>https?://[^\s]+)", content)
            urls = re.findall('(?P<url>https?://[^\s:"]+)', content)
    except Exception as e:
        printD(e)
        return
    # printD(urls)
    return urls

# get image with full size
# width is in number, not string
# 파일 인포가 있는 원본 이미지 주소이다.
def get_full_size_image_url(image_url, width):
    return re.sub('/width=\d+/', '/width=' + str(width) + '/', image_url)

def change_width_from_image_url(image_url, width):
    return re.sub('/width=\d+/', '/width=' + str(width) + '/', image_url)

# get id from url
# def get_model_id_from_url(url):
#     id = ""

#     if not url:
#         return ""

#     if url.isnumeric():
#         # is already an id
#         id = str(url)
#         return id
    
#     s = url.split("/")
#     if len(s) < 2:
#         return ""
    
#     if s[-2].isnumeric():
#         id  = s[-2]
#     elif s[-1].isnumeric():
#         id  = s[-1]
#     else:
#         return ""
    
#     return id

def get_model_id_from_url(url):
    if not url:
        return ""

    if url.isnumeric():
        return str(url)
    
    s = url.split("/")
    if len(s) < 2:
        return ""
    
    for i in range(len(s)):
        if s[i] == "models" and i < len(s)-1:
            id_str = s[i+1].split("?")[0]
            if id_str.isnumeric():
                return id_str
    
    return ""

def search_file(root_dirs:list,base:list,exts:list)->list:
    file_list = list()
    root_path = os.getcwd()
        
    for root_dir in root_dirs:
        for (root,dirs,files) in os.walk(os.path.join(root_path,root_dir)):
            if len(files) > 0:
                for file_name in files:               
                    b, e = os.path.splitext(file_name) 
                    if base and exts:
                        if e in exts and b in base:
                            file_list.append(os.path.join(root,file_name))                        
                    elif base:
                        if b in base:
                            file_list.append(os.path.join(root,file_name))
                    elif exts:
                        if e in exts:
                            file_list.append(os.path.join(root,file_name))
                    else:       
                        file_list.append(os.path.join(root,file_name))                        
                    
    return file_list if len(file_list) > 0 else None
