import os
import gradio as gr
import datetime

from . import setting
from . import ishortcut
from . import classification
from . import util
from . import sc_browser

def on_ui(refresh_classification:gr.Textbox):
    with gr.Column(scale=1):
        with gr.Row(visible=False):
            classification_shortcuts = gr.State()
            refresh_gallery = gr.Textbox()
            refresh_sc_list = gr.Textbox()
            
        with gr.Row():
            with gr.Column():
                sc_gallery = sc_browser.on_ui(refresh_sc_list)
    with gr.Column(scale=5):  
        classification_list = gr.Dropdown(label='Classification List', multiselect=None, choices=[setting.PLACEHOLDER] + classification.get_list(), value=setting.PLACEHOLDER ,interactive=True)                          
        classification_gallery = gr.Gallery(elem_id="classification_gallery", show_label=False).style(grid=[setting.classification_gallery_column], height="auto", object_fit="scale-down")
        classification_name = gr.Textbox(label="Name", value="",interactive=True, lines=1)
        classification_info = gr.Textbox(label="Description", value="",interactive=True, lines=1)
        with gr.Row():
            classification_create_btn = gr.Button(value="Create", variant="primary")
            classification_update_btn = gr.Button(value="Update", variant="primary")
        with gr.Accordion("Delete Classification", open=False): 
            classification_delete_btn = gr.Button(value="Delete")    

    refresh_classification.change(
        fn=on_refresh_classification_change,
        inputs=None,
        outputs=[
            refresh_sc_list,
            classification_list,
        ]
    )
    
    refresh_gallery.change(
        fn=on_classification_gallery_loading,
        inputs=[
            classification_shortcuts,
        ],
        outputs=[
            classification_gallery
        ]    
    )

    sc_gallery.select(
        fn=on_sc_gallery_select,
        inputs=[
            classification_list,
            classification_shortcuts
        ],
        outputs=[
            classification_shortcuts,
            refresh_gallery
        ]        
    )
    
    classification_gallery.select(
        fn=on_classification_gallery_select,
        inputs=[
            classification_shortcuts
        ],
        outputs=[
            classification_shortcuts,
            refresh_gallery
        ]         
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
            refresh_sc_list
        ]        
    )
    
    classification_update_btn.click(
        fn=on_classification_update_btn_click,
        inputs=[
            classification_list,
            classification_name,
            classification_info,
            classification_shortcuts
        ],
        outputs=[
            classification_list,
            refresh_sc_list
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
            refresh_sc_list
        ]         
    )
        
    classification_list.select(    
        fn=on_classification_list_select,
        inputs=None,
        outputs=[
            classification_name,
            classification_info,
            classification_shortcuts,
            refresh_gallery
        ]          
    )

def on_refresh_classification_change():
    current_time = datetime.datetime.now()
    return current_time, gr.update(choices=[setting.PLACEHOLDER] + classification.get_list())

def on_sc_gallery_select(evt: gr.SelectData, Classification_name , shortcuts):
    
    clf = None
    
    if not Classification_name:
        return None, None
    
    if Classification_name == setting.PLACEHOLDER:
        return None, None
    
    if Classification_name != setting.PLACEHOLDER:
        clf = classification.get_classification(Classification_name)
        if not clf:
            return None, None
            
    if evt.value:
               
            shortcut = evt.value 
            sc_model_id = setting.get_modelid_from_shortcutname(shortcut)
            
            current_time = datetime.datetime.now()
            
            if not shortcuts:
                shortcuts = list()
                
            if sc_model_id not in shortcuts:
                shortcuts.append(sc_model_id)

            return shortcuts, current_time    
    return shortcuts, None

def on_classification_gallery_loading(shortcuts):
    ISC = ishortcut.load()
    if not ISC:
        return None
    
    shotcutlist = list()
    
    if shortcuts:
        result_list = list()
        for mid in shortcuts:
            mid = str(mid)
            if mid in ISC:
                result_list.append(ISC[mid])
                
        for v in result_list:
            if v:
                if ishortcut.is_sc_image(v['id']):
                    shotcutlist.append((os.path.join(setting.shortcut_thumbnail_folder,f"{v['id']}{setting.preview_image_ext}"),setting.set_shortcutname(v['name'],v['id'])))
                else:
                    shotcutlist.append((setting.no_card_preview_image,setting.set_shortcutname(v['name'],v['id'])))

    return shotcutlist          

def on_classification_gallery_select(evt: gr.SelectData, shortcuts):
              
    if evt.value:               
            shortcut = evt.value 
            sc_model_id = setting.get_modelid_from_shortcutname(shortcut)
            current_time = datetime.datetime.now()
            
            if not shortcuts:
                shortcuts = list()
                
            if sc_model_id in shortcuts:
                shortcuts.remove(sc_model_id)

            return shortcuts, current_time    
    return shortcuts, None

def on_refresh_sc_list_change(sc_types,sc_search,show_only_downloaded_sc):
    return gr.update(value=sc_browser.get_thumbnail_list(sc_types,show_only_downloaded_sc,sc_search)),gr.update(choices=[setting.PLACEHOLDER] + classification.get_list())

def on_sc_search_submit(sc_types, sc_search):
    return gr.update(value=sc_browser.get_thumbnail_list(sc_types,False,sc_search))

def on_shortcut_type_change(sc_types, sc_search):
    return gr.update(value=sc_browser.get_thumbnail_list(sc_types,False,sc_search))

def on_classification_create_btn_click(new_name,new_info,classification_shortcuts):
    current_time = datetime.datetime.now()
    if classification.create_classification(new_name,new_info):                
        return gr.update(choices=[setting.PLACEHOLDER] + classification.get_list(), value=new_name), None, current_time, current_time
    return gr.update(choices=[setting.PLACEHOLDER] + classification.get_list()), classification_shortcuts, current_time, current_time

def on_classification_update_btn_click(select_name, new_name, new_info, new_shortcuts):
    chg_name = setting.PLACEHOLDER
    
    if select_name and select_name != setting.PLACEHOLDER:
        if classification.update_classification(select_name,new_name,new_info,new_shortcuts):
            chg_name = new_name
    
    current_time = datetime.datetime.now()        
    return gr.update(choices=[setting.PLACEHOLDER] + classification.get_list(), value=chg_name),current_time

def on_classification_delete_btn_click(select_name):
    if select_name and select_name != setting.PLACEHOLDER:
        classification.delete_classification(select_name)
        
    current_time = datetime.datetime.now()    
    return gr.update(choices=[setting.PLACEHOLDER] + classification.get_list(), value=setting.PLACEHOLDER), None, current_time, current_time
        
def on_classification_list_select(evt: gr.SelectData):
    if evt.value != setting.PLACEHOLDER:
        select_name = evt.value
        info = classification.get_classification_info(select_name)
        shortcuts = classification.get_classification_shortcuts(select_name)
        
        current_time = datetime.datetime.now()
        
        return gr.update(value=select_name),gr.update(value=info), shortcuts, current_time
    return gr.update(value=""), gr.update(value=""), None, None

def on_sc_classification_list_select(evt: gr.SelectData,sc_types, sc_search):
    keys, tags, clfs = util.get_search_keyword(sc_search)
    sc_search = ""    
    new_search = list()

    if keys:                
        new_search.extend(keys)

    if tags:                
        new_tags = [f"#{tag}" for tag in tags]
        new_search.extend(new_tags)
    
    if evt.value != setting.PLACEHOLDER:
        select_name = evt.value
        
        if select_name and len(select_name.strip()) > 0:       
            new_search.append(f"@{select_name.strip()}")
        
    if new_search:
        sc_search = ", ".join(new_search)
        
    return gr.update(value=sc_search),gr.update(value=sc_browser.get_thumbnail_list(sc_types,False,sc_search))
                   