import os
import json

from . import util
from . import setting


def create_classification(name, info):
    if name and len(name.strip()) > 0:
        add_CISC = create(None, name.strip(), info)
                      
        CISC = load()
        if CISC:
            CISC.update(add_CISC)
        else:
            CISC = add_CISC            
        save(CISC)
        
        if CISC:
            if name in CISC:
                return True
    return False
        
        
def update_classification(s_name, name, info):
    if not s_name:
        return

    if not name:
        return
    
    name = name.strip()
        
    CISC = load()
    CISC = update(CISC,s_name, name, info)
    save(CISC)
    
    if CISC:
        if name in CISC:
            return True
        
    return False

def delete_classification(s_name):
    if not s_name:
        return
        
    CISC = load()
    CISC = delete(CISC,s_name)
    save(CISC)
    

def get_classification_info(s_name):
    if not s_name:
        return None
    
    CISC = load()
    if s_name in CISC:
        return CISC[s_name]['info']
    
    return None


def get_list():
    
    CISC = load()                           
    
    tmp_cisc_name = []
    if CISC:   
        tmp_cisc_name = [k for k in CISC.keys()]
    
    return tmp_cisc_name
        
def get_shortcut_list(CISC:dict, classification):
    if not CISC:
        return None
    
    if not classification:
        return None   
    
    classification = classification.strip()
                    
    if classification not in CISC:
        return None
    
    return CISC[classification]['shortcuts']
    
def add_shortcut(CISC:dict, classification, modelid):
        
    if not CISC:
        CISC = dict()
        
    if not classification:
        return CISC   
        
    if not modelid:
        return CISC
    
    classification = classification.strip()
    
    if classification not in CISC:
        CISC = create(CISC,classification,None)
    
    if str(modelid) not in CISC[classification]['shortcuts']:
        CISC[classification]['shortcuts'].append(str(modelid))
            
    return CISC

def remove_shortcut(CISC:dict, classification, modelid):

    if not CISC:
        return CISC
    
    if not classification:
        return CISC   
        
    if not modelid:
        return CISC   
            
    if classification not in CISC:
        return CISC
    
    classification = classification.strip()
    
    if str(modelid) in CISC[classification]['shortcuts']:
        CISC[classification]['shortcuts'].remove(str(modelid))    
            
    return CISC

def clear_shortcut(CISC:dict, classification):

    if not CISC:
        return CISC
    
    if not classification:
        return CISC   
                   
    if classification not in CISC:
        return CISC
    
    classification = classification.strip()

    CISC[classification]['shortcuts'].clear()
            
    return CISC
    
def create(CISC:dict, classification, info=None)->dict:

    if not classification:
        return CISC   
        
    if not CISC:
        CISC = dict()
    
    classification = classification.strip()
    if len(classification) > 0:
        if classification not in CISC:
            CISC[classification] = {
                "info":info , 
                "shortcuts":[]
            }

    return CISC

def delete(CISC:dict, classification)->dict:
    if not classification:
        return CISC
    
    if not CISC:
        return CISC
           
    sc = CISC.pop(classification,None)
      
    return CISC

def update(CISC:dict, classification, name, info):

    if not CISC:
        return CISC
    
    if not classification:
        return CISC   
       
    if classification not in CISC:
        return CISC

    if not name:
        return CISC   
        
    name = name.strip()
    
    if classification == name:
        CISC[classification]['info'] = info
    else:
        if name not in CISC:
            sc = CISC.pop(classification,None)
            sc['info'] = info    
            CISC[name] = sc            
            
    return CISC

def save(CISC:dict):
    output = ""
    
    #write to file
    try:
        with open(setting.shortcut_classification, 'w') as f:
            json.dump(CISC, f, indent=4)
    except Exception as e:
        util.printD("Error when writing file:"+setting.shortcut_classification)
        return output

    output = "Civitai Internet Shortcut Classification saved to: " + setting.shortcut_classification
    #util.printD(output)

    return output

def load()->dict:
    if not os.path.isfile(setting.shortcut_classification):        
        save({})
        return
    
    json_data = None
    try:
        with open(setting.shortcut_classification, 'r') as f:
            json_data = json.load(f)
    except:
        return None            

    # check error
    if not json_data:
        return None

    # check for new key
    return json_data