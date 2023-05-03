import os
import datetime
import gradio as gr
import modules.scripts as scripts

from modules import shared
from modules import script_callbacks

from scripts.civitai_manager_libs import model
from scripts.civitai_manager_libs import setting
from scripts.civitai_manager_libs import classification_action
from scripts.civitai_manager_libs import civitai_shortcut_action
from scripts.civitai_manager_libs import setting_action
from scripts.civitai_manager_libs import util

def on_civitai_tabs_select(evt: gr.SelectData):
    if evt.index == 0:
        current_time = datetime.datetime.now() 
        return current_time,gr.update(visible=False)
    elif evt.index == 1:
        current_time = datetime.datetime.now() 
        return gr.update(visible=False),current_time
            
    return gr.update(visible=False),gr.update(visible=False)

def on_civitai_manage_tabs_select(evt: gr.SelectData):
    if evt.index == 0:
        current_time = datetime.datetime.now() 
        return current_time

    return gr.update(visible=True)

# def readmarkdown():

#     path = os.path.join(setting.extension_base,"README.md")
#     markdown_text = None

#     try:    
#         with open(path, 'r',encoding='UTF-8') as f:
#             markdown_text = f.read()                
#     except Exception as e:    
#         util.printD(e)        
#         return
            
#     return markdown_text
                   
def civitai_shortcut_ui():    
    with gr.Tabs(elem_id="civitai_shortcut_tabs_container") as civitai_tabs:
        with gr.TabItem("Civitai Shortcut" , id="Shortcut"):
            with gr.Row(visible=False):
          
                # SC 리스트틑 갱신하게 된다.
                refresh_shortcut = gr.Textbox()              
                refresh_classification = gr.Textbox()
                
            with gr.Row():
                civitai_shortcut_action.on_ui(refresh_shortcut)
     
        with gr.TabItem("Manage" , id="Manage"):
            with gr.Tabs() as civitai_manage_tabs:        
                with gr.TabItem("Classification"):
                    with gr.Row():
                        classification_action.on_ui(refresh_classification)
                with gr.TabItem("Scan and Update Models"):
                    with gr.Row():
                        setting_action.on_scan_ui()
                with gr.TabItem("Setting"):
                    with gr.Row():
                        setting_action.on_setting_ui()
                # with gr.TabItem("ReadMe"):
                #     with gr.Row():  
                #         gr.Markdown(value=readmarkdown())
    # civitai tab start
    civitai_tabs.select(
        fn=on_civitai_tabs_select,
        inputs=None,
        outputs=[refresh_shortcut,refresh_classification]
    )
    
    civitai_manage_tabs.select(
        fn=on_civitai_manage_tabs_select,
        inputs=None,
        outputs=[refresh_classification]        
    )
    
def init_civitai_shortcut():
    setting.init()
    model.update_downloaded_model()
               
# init
init_civitai_shortcut()

def on_ui_tabs():
    # with gr.Blocks(analytics_enabled=False) as civitai_shortcut:
    with gr.Blocks() as civitai_shortcut:
        civitai_shortcut_ui()
        
    return (civitai_shortcut, "Civitai Shortcut", "civitai_shortcut"),


script_callbacks.on_ui_tabs(on_ui_tabs)
