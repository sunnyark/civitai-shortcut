import os
import json
import shutil
import requests
import gradio as gr

from . import util
from . import setting
from . import civitai


def create(CISC:dict, classification, info=None)->dict:

    if not classification:
        return CISC   
        
    if not CISC:
        CISC = dict()
    
    if classification not in CISC:
        CISC[classification] = {
            "info":info , 
            "shortcuts":[]
        }

    return CISC

def delete(CISC:dict, classification)->dict:
    if not classification:
        return 
    
    if not CISC:
        return 
           
    cisc = CISC.pop(classification,None)
      
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