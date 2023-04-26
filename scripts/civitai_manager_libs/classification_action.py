import os
import gradio as gr

from . import setting
from . import ishortcut_action
from . import classification

        
# def on_civitai_manage_tabs_select(evt: gr.SelectData, sc_types,sc_search,show_only_downloaded_sc,  classification_list):
#    if evt.index == 0:
#         if classification_list:
#             return gr.update(choices=[setting.PLACEHOLDER] + classification.get_list(), value=classification_list)
#         else:
#             return gr.update(choices=[setting.PLACEHOLDER] + classification.get_list(), value=setting.PLACEHOLDER)
        
#     return gr.update(visible=True)

def on_ui():
    with gr.Column(scale=1):     
        with gr.Row():
            with gr.Column():
                Classification_list = gr.Dropdown(label='Classification List', multiselect=None, choices=[setting.PLACEHOLDER] + classification.get_list(), interactive=True)
                Classification_name = gr.Textbox(label="Name", value="",interactive=True, lines=1)
                Classification_info = gr.Textbox(label="Description", value="",interactive=True, lines=1)

                Classification_create_btn = gr.Button(value="Create", variant="primary")
                Classification_update_btn = gr.Button(value="Update", variant="primary")
                Classification_delete_btn = gr.Button(value="Delete", variant="primary")
    with gr.Column(scale=4):  
        with gr.Row():
            with gr.Column(scale=2):  
                gr.Markdown(value="###", visible=True)
                classification_gallery = gr.Gallery(label="Classification Gallery", elem_id="classification_gallery", show_label=False, value="").style(grid=[setting.gallery_column], height="auto")
            with gr.Column(scale=1):
                classification_shortcut_type = gr.Dropdown(label='Filter Model type', multiselect=True, choices=[k for k in setting.ui_model_types], interactive=True)
                classification_sc_search = gr.Textbox(label="Search", value="", placeholder="Search name, #tags ....",interactive=True, lines=1)
                classification_sc_gallery = gr.Gallery(label="Classification Gallery2", elem_id="classification_gallery2", show_label=False, value=ishortcut_action.get_thumbnail_list()).style(grid=[setting.shortcut_colunm], height="auto")
                
    ###### Manage Tab ######       
    Classification_create_btn.click(
        fn=on_Classification_create_btn_click,
        inputs=[
            Classification_name,
            Classification_info
        ],
        outputs=[
            Classification_list
        ]        
    )
    
    Classification_update_btn.click(
        fn=on_Classification_update_btn_click,
        inputs=[
            Classification_list,
            Classification_name,
            Classification_info
        ],
        outputs=[
            Classification_list
        ]         
    )

    Classification_delete_btn.click(
        fn=on_Classification_delete_btn_click,
        inputs=[
            Classification_list,
        ],
        outputs=[
            Classification_list
        ]         
    )
        
    Classification_list.select(    
        fn=on_Classification_list_select,
        inputs=None,
        outputs=[
            Classification_name,
            Classification_info
        ]          
    )
    

def on_Classification_create_btn_click(new_name,new_info):
    
    classification.create_classification(new_name,new_info)
    
    return gr.update(choices=[setting.PLACEHOLDER] + classification.get_list())

def on_Classification_update_btn_click(select_name, new_name, new_info):
    
    chg_name = setting.PLACEHOLDER
    if classification.update_classification(select_name,new_name,new_info):
        chg_name = new_name
        
    return gr.update(choices=[setting.PLACEHOLDER] + classification.get_list(), value=chg_name)

def on_Classification_delete_btn_click(select_name):
    
    classification.delete_classification(select_name)
    
    return gr.update(choices=[setting.PLACEHOLDER] + classification.get_list(), value=setting.PLACEHOLDER)
        
def on_Classification_list_select(evt: gr.SelectData):
    if evt.value != setting.PLACEHOLDER:
        select_name = evt.value
        info = classification.get_classification_info(select_name)
        return gr.update(value=select_name),gr.update(value=info)
    return gr.update(value=""), gr.update(value="")

               