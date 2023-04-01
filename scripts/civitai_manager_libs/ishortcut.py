import os
import json
from . import util
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
 
def get_list(shortcut_types=None)->str:
    
    ISC = load()                           
    if not ISC:
        return
    if "IShortCut" not in ISC.keys():
        return    
    
    tmp_types = []
    if shortcut_types:
        for sc_type in shortcut_types:
            try:
                tmp_types.append(setting.content_types_dict[sc_type])
            except:
                pass
            
    shotcutlist = []
    for k, v in ISC["IShortCut"].items():
        # util.printD(ISC["IShortCut"][k])
        if v:
            if tmp_types:
                if v['type'] in tmp_types:
                    shotcutlist.append(f"{v['id']}:{v['name']}")
            else:                                
                shotcutlist.append(f"{v['id']}:{v['name']}")                
                    
    return [v for v in shotcutlist]


def get_image_list(shortcut_types=None)->str:
    
    ISC = load()                           
    if not ISC:
        return
    if "IShortCut" not in ISC.keys():
        return    
    
    tmp_types = []
    if shortcut_types:
        for sc_type in shortcut_types:
            try:
                tmp_types.append(setting.content_types_dict[sc_type])
            except:
                pass
            
    shotcutlist = []
    for k, v in ISC["IShortCut"].items():
        # util.printD(ISC["IShortCut"][k])
        if v:
            if tmp_types:
                if v['type'] in tmp_types:
                    shotcutlist.append((v['imageurl'],f"{v['id']}:{v['name']}"))
            else:                                
                shotcutlist.append((v['imageurl'],f"{v['id']}:{v['name']}"))
                    
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
