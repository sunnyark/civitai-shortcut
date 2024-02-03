import os
import re
import time
import requests
import threading
import shutil
import json

from . import util
from . import setting
from . import civitai

from tqdm import tqdm

def add_number_to_duplicate_files(filenames)->dict:    
    counts = {}
    dup_file = {}
    
    for file in filenames:     
        file_info = file.split(":", 1)
        if len(file_info) > 1:
            if file_info[1] in counts:
                name, ext = os.path.splitext(file_info[1])
                counts[file_info[1]] += 1
                file_info[1] = f"{name} ({counts[file_info[1]]}){ext}"
            else:
                counts[file_info[1]] = 0        
            dup_file[file_info[0]] = file_info[1]
    return dup_file

def get_save_base_name(version_info):
    # 이미지 파일명도 primary 이름으로 저장한다.
           
    base = None    
    primary_file = civitai.get_primary_file_by_version_info(version_info)
    if not primary_file:
        base = setting.generate_version_foldername(version_info['model']['name'],version_info['name'],version_info['id'])
    else:
        base, ext = os.path.splitext(primary_file['name'])   
    return base
    
def download_file_thread(file_name, version_id, ms_folder, vs_folder, vs_foldername, cs_foldername, ms_foldername):
                
    if not file_name or not version_id:
        return
    
    version_info = civitai.get_version_info_by_version_id(version_id)
    
    if not version_info:
        return 
       
    download_files = civitai.get_files_by_version_info(version_info)
    
    if not download_files:
        return

    model_folder = util.make_download_model_folder(version_info, ms_folder, vs_folder, vs_foldername, cs_foldername, ms_foldername)
    
    if not model_folder:
        return

    savefile_base = None
    
    # version_info 에서 파일부분을 가져온다.
    # 파일명이 변경되었을때 정보를 수정한다.
    if "files" in version_info:    
        info_files = version_info["files"]
    
    dup_names = add_number_to_duplicate_files(file_name)
    
    for fid, file in dup_names.items():                    
        try:
            #모델 파일 저장
            path_dl_file = os.path.join(model_folder, file)            
            thread = threading.Thread(target=download_file,args=(download_files[str(fid)]['downloadUrl'], path_dl_file))
            thread.start()                

            # 파일 아이디에 해당하는 파일명을 변경한다.
            # 실제 다운 로드 되는 파일명으로 변경한다.
            # 베이스 파일명도 얻어온다.
            if not info_files:
                continue

            for info_file in info_files:
                if str(info_file['id']) == str(fid):
                    info_file['name'] = file

                    if savefile_base:
                        continue

                    if 'primary' in info_file.keys():
                        if info_file['primary']:
                            savefile_base , ext = os.path.splitext(file)

        except Exception as e:
            util.printD(e)
        # finally:
        #     pass    
    
    # savefile_base 이름이 없다는 것은 primary 파일이 아닌것이다.
    # 다운로드할 파일 목록중에 primary 파일이 있을때만 버전 인포파일과 프리뷰 이미지를 다운로드한다.
    # 프리뷰 파일이 아닐때는 단순히 파일만 다운로드한다.
    if savefile_base:
        path_file = os.path.join(model_folder, f"{util.replace_filename(savefile_base)}{setting.info_suffix}{setting.info_ext}")
        info_file = civitai.write_version_info(path_file, version_info)
        if info_file:
            util.printD(f"Wrote version info : {path_file}")

        path_img = os.path.join(model_folder, f"{util.replace_filename(savefile_base)}{setting.preview_image_suffix}{setting.preview_image_ext}")
        preview_file = download_preview_image(path_img, version_info)
        if preview_file:
            util.printD(f"Wrote preview image : {path_img}")

        # LoRa_metadata_file 을 생성한다.
        path_file = os.path.join(model_folder, f"{util.replace_filename(savefile_base)}.json")
        LoRa_metadata_file = civitai.write_LoRa_metadata(path_file, version_info)
        # LoRa_metadata_file = generate_LoRa_metadata(path_file, version_info)
        if LoRa_metadata_file:
            util.printD(f"Wrote LoRa metadata : {path_file}")
            
    # savefile_base 이름이 없다면 모델인포에서 프라이머리 파일을 찾는다.
    # if not savefile_base:
    #     savefile_base = get_save_base_name(version_info)
        
    # path_file = os.path.join(model_folder, f"{util.replace_filename(savefile_base)}{setting.info_suffix}{setting.info_ext}")
    # info_file = civitai.write_version_info(path_file, version_info)
    # if info_file:
    #     util.printD(f"Wrote version info : {path_file}")

    # path_img = os.path.join(model_folder, f"{util.replace_filename(savefile_base)}{setting.preview_image_suffix}{setting.preview_image_ext}")
    # preview_file = download_preview_image(path_img, version_info)
    # if preview_file:
    #      util.printD(f"Wrote preview image : {path_img}")

    return f"Download started"

def download_preview_image(filepath, version_info):
    if not version_info:
        return False
    # save preview            
    if "images" in version_info.keys():
        try:            
            img_dict = version_info["images"][0] 
            if "url" in img_dict:
                img_url = img_dict["url"]
                if "width" in img_dict:
                    if img_dict["width"]:
                        img_url =  util.change_width_from_image_url(img_url, img_dict["width"])
                # get image
                with requests.get(img_url, stream=True) as img_r:
                    if not img_r.ok:
                        util.printD("Get error code: " + str(img_r.status_code))
                        return False

                    with open(filepath, 'wb') as f:
                        img_r.raw.decode_content = True
                        shutil.copyfileobj(img_r.raw, f)                                                    
        except Exception as e:
            pass
                    
    return True  

# def generate_LoRa_metadata(filepath, version_info):

#     LoRa_metadata = {
# 	    "description": None,
# 	    "sd version": None,
# 	    "activation text": None,
# 	    "preferred weight": 0,
# 	    "notes": None
#     }
    
#     if not version_info:
#         return False
    
#     if os.path.isfile(filepath):        
#         return False
#         # try:
#         #     with open(filepath, 'r') as f:
#         #         LoRa_metadata = json.load(f)
#         # except:
#         #     pass
    
#     if "description" in version_info.keys():
#         LoRa_metadata['description'] = version_info["description"]

#     if "baseModel" in version_info.keys():
#         baseModel = version_info["baseModel"]
#         if baseModel in setting.model_basemodels.keys():            
#             LoRa_metadata['sd version'] = setting.model_basemodels[baseModel]
#         else:
#             LoRa_metadata['sd version'] = 'Unknown'
        
#     if "trainedWords" in version_info.keys():    
#         LoRa_metadata['activation text'] = ", ".join(version_info['trainedWords']) 
    
#     notes = list()
#     if "modelId" in version_info.keys():                
#         notes.append(f"https://civitai.com/models/{version_info['modelId']}")
    
#     if "downloadUrl" in version_info.keys():
#         notes.append(version_info['downloadUrl'])

#     if len(notes) > 0:    
#         LoRa_metadata['notes'] = ", ".join(notes) 

#     try:
#         with open(filepath, 'w') as f:
#             json.dump(LoRa_metadata, f, indent=4)
#     except Exception as e:
#         return False

#     return True                    

def download_image_file(model_name, image_urls, progress_gr=None):    
    if not model_name:                
        return      

    model_folder = util.make_download_image_folder(model_name)
    
    if not model_folder:
        return
    
    save_folder = os.path.join(model_folder, "images")
    
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)        
        
    if image_urls and len(image_urls) > 0:                
        for image_count, img_url in enumerate(tqdm(image_urls, desc=f"Download images"), start=0):

            result = util.is_url_or_filepath(img_url)
            if result == "filepath":
                if os.path.basename(img_url) != setting.no_card_preview_image:
                    description_img = os.path.join(save_folder,os.path.basename(img_url))
                    shutil.copyfile(img_url,description_img)
            elif result == "url":
                try:
                    # get image
                    with requests.get(img_url, stream=True) as img_r:
                        if not img_r.ok:
                            util.printD("Get error code: " + str(img_r.status_code) + ": proceed to the next file")
                        else:
                            # write to file
                            image_id, ext = os.path.splitext(os.path.basename(img_url))
                            description_img = os.path.join(save_folder,f'{image_id}{setting.preview_image_suffix}{setting.preview_image_ext}')
                            with open(description_img, 'wb') as f:
                                img_r.raw.decode_content = True
                                shutil.copyfileobj(img_r.raw, f)
                except Exception as e:
                    pass
    return 

def download_file(url, file_name):
    # Maximum number of retries
    max_retries = 5

    # Delay between retries (in seconds)
    retry_delay = 10

    while True:
        # Check if the file has already been partially downloaded
        if os.path.exists(file_name):
            # Get the size of the downloaded file
            downloaded_size = os.path.getsize(file_name)

            # Set the range of the request to start from the current size of the downloaded file
            headers = {"Range": f"bytes={downloaded_size}-"}
        else:
            downloaded_size = 0
            headers = {}

        headers["Authorization"] = f"Bearer {setting.civitai_api_key}"

        # Split filename from included path
        tokens = re.split(re.escape('\\'), file_name)
        file_name_display = tokens[-1]

        # Initialize the progress bar
        progress = tqdm(total=1000000000, unit="B", unit_scale=True,
                        desc=f"Downloading {file_name_display}", initial=downloaded_size, leave=False)

        # Open a local file to save the download
        with open(file_name, "ab") as f:
            while True:
                try:
                    # Send a GET request to the URL and save the response to the local file
                    response = requests.get(url, headers=headers, stream=True)

                    # Get the total size of the file
                    total_size = int(response.headers.get("Content-Length", 0))

                    # Update the total size of the progress bar if the `Content-Length` header is present
                    if total_size == 0:
                        total_size = downloaded_size
                    progress.total = total_size

                    # Write the response to the local file and update the progress bar
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:  # filter out keep-alive new chunks
                            f.write(chunk)
                            progress.update(len(chunk))

                    downloaded_size = os.path.getsize(file_name)
                    # Break out of the loop if the download is successful
                    break
                except ConnectionError as e:
                    # Decrement the number of retries
                    max_retries -= 1

                    # If there are no more retries, raise the exception
                    if max_retries == 0:
                        raise e

                    # Wait for the specified delay before retrying
                    time.sleep(retry_delay)

        # Close the progress bar
        progress.close()
        downloaded_size = os.path.getsize(file_name)
        # Check if the download was successful
        if downloaded_size >= total_size:            
            print(f"{file_name_display} successfully downloaded.")
            break
        else:
            print(f"Error: File download failed. Retrying... {file_name_display}")   

# 테스트중이다. download_file를 대체할것... 거의 같다.
def download_file_gr(url, file_name, progress_gr=None):
    # Maximum number of retries
    max_retries = 5

    # Delay between retries (in seconds)
    retry_delay = 10

    while True:
        # Check if the file has already been partially downloaded
        if os.path.exists(file_name):
            # Get the size of the downloaded file
            downloaded_size = os.path.getsize(file_name)

            # Set the range of the request to start from the current size of the downloaded file
            headers = {"Range": f"bytes={downloaded_size}-"}
        else:
            downloaded_size = 0
            headers = {}        
        
        # Split filename from included path
        tokens = re.split(re.escape('\\'), file_name)
        file_name_display = tokens[-1]
        
        # Open a local file to save the download
        with open(file_name, "ab") as f:
            while True:
                try:
                    # Send a GET request to the URL and save the response to the local file
                    response = requests.get(url, headers=headers, stream=True)

                    # Get the total size of the file
                    total_size = int(response.headers.get("Content-Length", 0))
                    
                    # Update the total size of the progress bar if the `Content-Length` header is present
                    if total_size == 0:
                        total_size = downloaded_size

                    # Initialize the progress bar
                    progress = tqdm(range(total_size), total=total_size, unit="B", unit_scale=True, desc=f"Downloading {file_name_display}", initial=downloaded_size, leave=False)
                    
                    # Write the response to the local file and update the progress bar
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:  # filter out keep-alive new chunks
                            f.write(chunk)
                            progress.update(len(chunk))                            

                    downloaded_size = os.path.getsize(file_name)
                    # Break out of the loop if the download is successful
                    
                    # Close the progress bar
                    progress.close()                    
                    break
                except ConnectionError as e:
                    # Decrement the number of retries
                    max_retries -= 1

                    # If there are no more retries, raise the exception
                    if max_retries == 0:
                        raise e

                    # Wait for the specified delay before retrying
                    time.sleep(retry_delay)

        downloaded_size = os.path.getsize(file_name)
        # Check if the download was successful
        if downloaded_size >= total_size:            
            print(f"{file_name_display} successfully downloaded.")
            break
        else:
            print(f"Error: File download failed. Retrying... {file_name_display}")               
