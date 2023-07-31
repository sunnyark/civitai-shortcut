import os
import gradio as gr
import datetime

from . import util
from . import setting
from . import ishortcut
from . import classification
from . import sc_browser_page

def on_ui():   
    with gr.Column(scale=setting.shortcut_browser_screen_split_ratio):
        classification_list = gr.Dropdown(label='Classification List', multiselect=None, choices=[setting.NEWCLASSIFICATION] + classification.get_list(), value=setting.NEWCLASSIFICATION ,interactive=True)
        with gr.Tabs():
            with gr.TabItem("Classification Info"):                
                classification_name = gr.Textbox(label="Name", value="",interactive=True, lines=1)
                classification_info = gr.Textbox(label="Description", value="",interactive=True, lines=3)
                classification_create_btn = gr.Button(value="Create", variant="primary")
                classification_update_btn = gr.Button(value="Update", variant="primary", visible=False)
           
                with gr.Accordion("Delete Classification", open=False): 
                    classification_delete_btn = gr.Button(value="Delete")    

            with gr.TabItem("Shortcut Items"):
                    sc_gallery, refresh_sc_browser, refresh_sc_gallery = sc_browser_page.on_ui()

    with gr.Column(scale=(setting.shortcut_browser_screen_split_ratio_max-setting.shortcut_browser_screen_split_ratio)):  
        with gr.Accordion(label=setting.PLACEHOLDER, open=True) as classification_title_name: 
            classification_save_shortcut_btn = gr.Button(value="Save Classification Shortcuts", variant="primary")
            with gr.Row():
                classification_clear_shortcut_btn = gr.Button(value="Clear")
                classification_reload_shortcut_btn = gr.Button(value="Reload")
            classification_gallery = gr.Gallery(elem_id="classification_gallery", show_label=False).style(grid=[setting.classification_gallery_column], height="auto", object_fit=setting.gallery_thumbnail_image_style, preview=False)
    
    with gr.Row(visible=False):
        classification_shortcuts = gr.State()
        refresh_gallery = gr.Textbox()
        refresh_classification = gr.Textbox()
                           
    refresh_classification.change(
        fn=on_refresh_classification_change,
        inputs=classification_list,
        outputs=[
            classification_name,
            classification_info,
            refresh_sc_browser,
            classification_title_name,
            refresh_gallery,
            classification_list
        ],
        show_progress=False
    )
    
    refresh_gallery.change(
        fn=on_classification_gallery_loading,
        inputs=[
            classification_shortcuts,
        ],
        outputs=[
            classification_gallery
        ],
        show_progress=False
    )

    sc_gallery.select(
        fn=on_sc_gallery_select,
        inputs=[
            classification_list,
            classification_shortcuts
        ],
        outputs=[
            classification_shortcuts,            
            refresh_gallery,
            sc_gallery,
            refresh_sc_gallery
        ],
        show_progress=False        
    )
    
    classification_gallery.select(
        fn=on_classification_gallery_select,
        inputs=[
            classification_shortcuts
        ],
        outputs=[
            classification_shortcuts,
            refresh_gallery,
            classification_gallery,
        ],
        show_progress=False
    )

    classification_create_btn.click(
        fn=on_classification_create_btn_click,
        inputs=[
            classification_name,
            classification_info,
            classification_shortcuts,
        ],
        outputs=[
            classification_list,
            classification_shortcuts,
            refresh_gallery,            
            refresh_sc_browser,
            classification_title_name,
            classification_create_btn,
            classification_update_btn             
        ]        
    )
    
    classification_update_btn.click(
        fn=on_classification_update_btn_click,
        inputs=[
            classification_list,
            classification_name,
            classification_info,
        ],
        outputs=[
            classification_list,
            refresh_sc_browser,
            classification_title_name
        ]         
    )

    classification_delete_btn.click(
        fn=on_classification_delete_btn_click,
        inputs=[
            classification_list,
        ],
        outputs=[
            classification_list,
            classification_shortcuts,
            refresh_gallery,
            refresh_sc_browser,
            classification_title_name,
            classification_create_btn,
            classification_update_btn
        ]         
    )
    
    classification_save_shortcut_btn.click(
        fn=on_classification_save_shortcut_btn_click,
        inputs=[
            classification_list,
            classification_shortcuts
        ],
        outputs=[
            refresh_gallery
        ]         
    )

    classification_clear_shortcut_btn.click(
        fn=on_classification_clear_shortcut_btn_click,
        inputs=[],
        outputs=[
            classification_shortcuts,            
            refresh_gallery
        ]         
    )    

    classification_reload_shortcut_btn.click(
        fn=on_classification_reload_shortcut_btn_click,
        inputs=classification_list,
        outputs=[
            classification_shortcuts,
            refresh_gallery
        ]
    )   
                        
    classification_list.select(    
        fn=on_classification_list_select,
        inputs=None,
        outputs=[
            classification_name,
            classification_info,
            classification_shortcuts,
            refresh_gallery,
            classification_title_name,
            classification_create_btn,
            classification_update_btn                        
        ]          
    )

    return refresh_classification

def on_classification_reload_shortcut_btn_click(select_name):

    if select_name != setting.PLACEHOLDER:
        shortcuts = classification.get_classification_shortcuts(select_name)
        
        current_time = datetime.datetime.now()
        
        return shortcuts, current_time
    return None, gr.update(visible=False)

def on_refresh_classification_change(select_name):
    current_time = datetime.datetime.now()
    if select_name != setting.NEWCLASSIFICATION:
        info = classification.get_classification_info(select_name)
        
        return gr.update(value=select_name), gr.update(value=info), current_time, gr.update(label=select_name), current_time, gr.update(choices=[setting.NEWCLASSIFICATION] + classification.get_list())
    return gr.update(value=""), gr.update(value=""), current_time, gr.update(label=setting.NEWCLASSIFICATION), gr.update(visible=True), gr.update(choices=[setting.NEWCLASSIFICATION] + classification.get_list())

def on_sc_gallery_select(evt: gr.SelectData, Classification_name , shortcuts):
    sc_reload = setting.classification_preview_mode_disable
    clf = None
    current_time = datetime.datetime.now()
    
    if not Classification_name:
        return None, None, None if sc_reload else gr.update(show_label=False), current_time if sc_reload else gr.update(visible=False)
    
    if Classification_name == setting.NEWCLASSIFICATION:
        return None, None, None if sc_reload else gr.update(show_label=False), current_time if sc_reload else gr.update(visible=False)
    
    if Classification_name != setting.NEWCLASSIFICATION:
        clf = classification.get_classification(Classification_name)
        if not clf:
            return None, None, None if sc_reload else gr.update(show_label=False), current_time if sc_reload else gr.update(visible=False)
            
    if evt.value:
               
        shortcut = evt.value 
        sc_model_id = setting.get_modelid_from_shortcutname(shortcut)            
        
        if not shortcuts:
            shortcuts = list()
            
        if sc_model_id not in shortcuts:
            shortcuts.append(sc_model_id)

        return shortcuts, current_time, None if sc_reload else gr.update(show_label=False), current_time if sc_reload else gr.update(visible=False)
    return shortcuts, None, None if sc_reload else gr.update(show_label=False), current_time if sc_reload else gr.update(visible=False)

def on_classification_gallery_loading(shortcuts):
    ISC = ishortcut.load()
    if not ISC:
        return None
        
    result_list = None
    
    if shortcuts:
        result_list = list()
        for mid in shortcuts:            
            if str(mid) in ISC.keys():
                v = ISC[str(mid)]
                if ishortcut.is_sc_image(v['id']):
                    if bool(v['nsfw']) and setting.NSFW_filtering_enable:
                        result_list.append((setting.nsfw_disable_image,setting.set_shortcutname(v['name'],v['id'])))
                    else:                    
                        result_list.append((os.path.join(setting.shortcut_thumbnail_folder,f"{v['id']}{setting.preview_image_ext}"),setting.set_shortcutname(v['name'],v['id'])))
                else:
                    result_list.append((setting.no_card_preview_image,setting.set_shortcutname(v['name'],v['id'])))
            else:
                result_list.append((setting.no_card_preview_image,setting.set_shortcutname("delete",mid)))                
                
    return gr.update(value=result_list)

def on_classification_gallery_select(evt: gr.SelectData, shortcuts):
    classification_reload = setting.classification_preview_mode_disable
    if evt.value:               
            shortcut = evt.value 
            sc_model_id = setting.get_modelid_from_shortcutname(shortcut)
            current_time = datetime.datetime.now()
            
            if not shortcuts:
                shortcuts = list()
                
            if sc_model_id in shortcuts:
                shortcuts.remove(sc_model_id)

            return shortcuts, current_time , None if classification_reload else gr.update(show_label=False)
    return shortcuts, None, None if classification_reload else gr.update(show_label=False)

def on_classification_save_shortcut_btn_click(select_name, new_shortcuts):   
    if select_name and select_name != setting.NEWCLASSIFICATION:
        classification.update_classification_shortcut(select_name,new_shortcuts)
        
    current_time = datetime.datetime.now()        
    return current_time

def on_classification_clear_shortcut_btn_click():
    current_time = datetime.datetime.now()        
    return None, current_time

def on_classification_create_btn_click(new_name,new_info,classification_shortcuts):
    current_time = datetime.datetime.now()
    if classification.create_classification(new_name,new_info):                
        return gr.update(choices=[setting.NEWCLASSIFICATION] + classification.get_list(), value=new_name), None, current_time, current_time,gr.update(label=new_name),\
            gr.update(visible=False), gr.update(visible=True)
    return gr.update(choices=[setting.NEWCLASSIFICATION] + classification.get_list()), classification_shortcuts, current_time, current_time,gr.update(visible=True),\
        gr.update(visible=True), gr.update(visible=False)

def on_classification_update_btn_click(select_name, new_name, new_info):
    chg_name = setting.NEWCLASSIFICATION
    
    if select_name and select_name != setting.NEWCLASSIFICATION:
        # classification.update_classification_shortcut(select_name,new_shortcuts)
        if classification.update_classification(select_name,new_name,new_info):
            chg_name = new_name            
        
    current_time = datetime.datetime.now()        
    return gr.update(choices=[setting.NEWCLASSIFICATION] + classification.get_list(), value=chg_name),current_time, gr.update(label=chg_name)

def on_classification_delete_btn_click(select_name):
    if select_name and select_name != setting.NEWCLASSIFICATION:
        classification.delete_classification(select_name)
        
    current_time = datetime.datetime.now()    
    return gr.update(choices=[setting.NEWCLASSIFICATION] + classification.get_list(), value=setting.NEWCLASSIFICATION), None, current_time, current_time,gr.update(label=setting.NEWCLASSIFICATION),\
        gr.update(visible=True), gr.update(visible=False)
        
def on_classification_list_select(evt: gr.SelectData):
    if evt.value != setting.NEWCLASSIFICATION:
        select_name = evt.value
        info = classification.get_classification_info(select_name)
        shortcuts = classification.get_classification_shortcuts(select_name)
        
        current_time = datetime.datetime.now()
        
        return gr.update(value=select_name), gr.update(value=info), shortcuts, current_time, gr.update(label=select_name),\
            gr.update(visible=False),gr.update(visible=True)
    return gr.update(value=""), gr.update(value=""), None, None, gr.update(label=setting.NEWCLASSIFICATION),\
        gr.update(visible=True), gr.update(visible=False)
