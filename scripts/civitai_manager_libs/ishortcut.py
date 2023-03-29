import os
import json
import requests
from . import util
from . import civitai
from . import setting


# cis_list = {
#     "IShortCut":[{
#         model_id : 
#         {
#             "id" : model_id,
#             "type" : model_type,
#             "name": name,
#             "url": url,        
#             "image" : "default version image",
#         }
#     }],       
# }

# test1
# ISC={}
# ISC["IShortCut"] = cis_list    
# load_list = ISC["IShortCut"]
# util.printD(load_list['1'])
# util.printD(load_list['2'])
# util.printD(load_list['3'])    
# util.printD(ISC["IShortCut"]['1'])
# util.printD(ISC["IShortCut"]['2'])
# util.printD(ISC["IShortCut"]['3'])    
# ISC["IShortCut"].pop('2')    
# save(ISC)

#test2 
# ISC={}
# ISC["IShortCut"]= {}
# ISC["IShortCut"]['1']={"id": "1" ,"name" : "aa","url":"http://aaaa.com" }
# ISC["IShortCut"]['2']={"id": "2" ,"name" : "bb","url":"http://bbbb.com" }
# ISC["IShortCut"]['3']={"id": "3" ,"name" : "cc","url":"http://cccc.com" }
# save(ISC)
# util.printD(ISC["IShortCut"]['1'])
# util.printD(ISC["IShortCut"]['2'])
# util.printD(ISC["IShortCut"]['3'])    
# ISC["IShortCut"].pop('2')    
# save(ISC)    
 
def get_list()->str:
    
    ISC = load()                           
    if not ISC:
        return
    if "IShortCut" not in ISC.keys():
        return    
    
    shotcutlist = []
    for k, v in ISC["IShortCut"].items():
        # util.printD(ISC["IShortCut"][k])
        if v:
            shotcutlist.append(f"{v['id']}:{v['name']}")
                    
    return [v for v in shotcutlist]


def add(ISC:dict, model_id ,model_name, model_type, model_url, version_id, image_url)->dict:
    
    if not ISC:
        ISC = {}
        
    if "IShortCut" not in ISC.keys():
        ISC["IShortCut"] = {}
        
    cis = {
            "id" : model_id,
            "type" : model_type,
            "name": model_name,
            "url": model_url,
            "versionid":version_id,
            "imageurl" : image_url
    }
    
    ISC["IShortCut"][model_id] = cis
    return ISC

def delete(ISC:dict, model_id)->dict:
    
    if not ISC:
        return 
        
    if "IShortCut" not in ISC.keys():
        return   
    ISC["IShortCut"].pop(model_id,None)
    return ISC

def save(cis_data):
    #print("Saving Civitai Internet Shortcut to: " + setting.civitai_shortcut)

    json_data = json.dumps(cis_data, indent=4)

    output = ""

    #write to file
    try:
        with open(setting.civitai_shortcut, 'w') as f:
            f.write(json_data)
    except Exception as e:
        util.printD("Error when writing file:"+setting.civitai_shortcut)
        return output

    output = "Civitai Internet Shortcut saved to: " + setting.civitai_shortcut
    #util.printD(output)

    return output

def load()->dict:
    #util.printD("Load Civitai Internet Shortcut from: " + setting.civitai_shortcut)

    if not os.path.isfile(setting.civitai_shortcut):
        util.printD("No Civitai Internet Shortcut file, use blank")
        return

    json_data = None
    with open(setting.civitai_shortcut, 'r') as f:
        json_data = json.load(f)

    # check error
    if not json_data:
        util.printD("load Civitai Internet Shortcut file failed")
        return

    # check for new key
    return json_data


# data = {
#     "model":{
#         "max_size_preview": True,
#         "skip_nsfw_preview": False
#     },
#     "general":{
#         "open_url_with_js": True,
#         "always_display": False,
#         "show_btn_on_thumb": True,
#         "proxy": "",
#     },
#     "tool":{
#     }
# }



# # save setting
# # return output msg for log
# def save():
#     print("Saving setting to: " + path)

#     json_data = json.dumps(data, indent=4)

#     output = ""

#     #write to file
#     try:
#         with open(path, 'w') as f:
#             f.write(json_data)
#     except Exception as e:
#         util.printD("Error when writing file:"+path)
#         output = str(e)
#         util.printD(str(e))
#         return output

#     output = "Setting saved to: " + path
#     util.printD(output)

#     return output


# # load setting to global data
# def load():
#     # load data into globel data
#     global data

#     util.printD("Load setting from: " + path)

#     if not os.path.isfile(path):
#         util.printD("No setting file, use default")
#         return

#     json_data = None
#     with open(path, 'r') as f:
#         json_data = json.load(f)

#     # check error
#     if not json_data:
#         util.printD("load setting file failed")
#         return

#     data = json_data

#     # check for new key
#     if "always_display" not in data["general"].keys():
#         data["general"]["always_display"] = False

#     if "show_btn_on_thumb" not in data["general"].keys():
#         data["general"]["show_btn_on_thumb"] = True

#     if "proxy" not in data["general"].keys():
#         data["general"]["proxy"] = ""


#     return

# # save setting from parameter
# def save_from_input(max_size_preview, skip_nsfw_preview, open_url_with_js, always_display, show_btn_on_thumb, proxy):
#     global data
#     data = {
#         "model":{
#             "max_size_preview": max_size_preview,
#             "skip_nsfw_preview": skip_nsfw_preview
#         },
#         "general":{
#             "open_url_with_js": open_url_with_js,
#             "always_display": always_display,
#             "show_btn_on_thumb": show_btn_on_thumb,
#             "proxy": proxy,
#         },
#         "tool":{
#         }
#     }

#     output = save()

#     if not output:
#         output = ""

#     return output
