import gradio as gr

from . import util
from . import setting
from . import ishortcut_action
from . import classification

def on_refresh_sc_list_change(sc_types,sc_search,show_only_downloaded_sc):
    return gr.update(value=ishortcut_action.get_thumbnail_list(sc_types,show_only_downloaded_sc,sc_search)),gr.update(choices=[setting.PLACEHOLDER] + classification.get_list())

def on_shortcut_gallery_refresh(sc_types, sc_search, show_only_downloaded_sc):
    return gr.update(value=ishortcut_action.get_thumbnail_list(sc_types,show_only_downloaded_sc,sc_search))

def on_sc_classification_list_select(evt: gr.SelectData,sc_types, sc_search, show_only_downloaded_sc):
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
        
    return gr.update(value=sc_search),gr.update(value=ishortcut_action.get_thumbnail_list(sc_types,show_only_downloaded_sc,sc_search))

def on_ui(refresh_sc_list: gr.Textbox):

    with gr.Accordion("Search", open=True):
        shortcut_type = gr.Dropdown(label='Filter Model type', multiselect=True, choices=[k for k in setting.ui_model_types], interactive=True)
        sc_search = gr.Textbox(label="Search", value="", placeholder="Search name, #tags, @classification, ....",interactive=True, lines=1)
        sc_classification_list = gr.Dropdown(label='Classification', multiselect=None, value=setting.PLACEHOLDER, choices=[setting.PLACEHOLDER] + classification.get_list(), interactive=True)
        show_only_downloaded_sc = gr.Checkbox(label="Show downloaded model's shortcut only", value=False)
    sc_gallery = gr.Gallery(label="SC Gallery", elem_id="sc_gallery", show_label=False, value=ishortcut_action.get_thumbnail_list()).style(grid=[setting.shortcut_colunm], height="auto")    
       
    refresh_sc_list.change(
        fn=on_refresh_sc_list_change,
        inputs= [
            shortcut_type,
            sc_search,
            show_only_downloaded_sc,
        ],
        outputs=[
            sc_gallery,
            sc_classification_list
        ]
    )
    
    shortcut_type.change(
        fn=on_shortcut_gallery_refresh,
        inputs=[
            shortcut_type,            
            sc_search,
            show_only_downloaded_sc,            
        ],
        outputs=[
            sc_gallery,
        ]
    ) 
        
    sc_search.submit(
        fn=on_shortcut_gallery_refresh,
        inputs=[            
            shortcut_type,
            sc_search,
            show_only_downloaded_sc,                        
        ],
        outputs=[
            sc_gallery
        ]        
    )
       
    show_only_downloaded_sc.change(
        fn=on_shortcut_gallery_refresh,
        inputs=[
            shortcut_type,
            sc_search,
            show_only_downloaded_sc,
        ],
        outputs=[
            sc_gallery,
        ]
    )    
    
    sc_classification_list.select(
        fn=on_sc_classification_list_select,
        inputs=[
            shortcut_type,
            sc_search,
            show_only_downloaded_sc,
        ],
        outputs=[
            sc_search,
            sc_gallery
        ]        
    )
    
    return sc_gallery