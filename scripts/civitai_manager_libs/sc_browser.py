import gradio as gr

from . import util
from . import setting
from . import model
from . import classification
from . import ishortcut


def get_thumbnail_list(shortcut_types=None, only_downloaded=False, search=None):
    
    shortlist =  ishortcut.get_image_list(shortcut_types, search)
    if not shortlist:
        return None
    
    if only_downloaded:
        if model.Downloaded_Models:                
            downloaded_list = list()            
            for short in shortlist:
                sc_name = short[1]
                mid = setting.get_modelid_from_shortcutname(sc_name)
                if mid in model.Downloaded_Models.keys():
                    downloaded_list.append(short)
            return downloaded_list
    else:
        return shortlist
    
    
    return None

def on_refresh_sc_list_change(sc_types,sc_search,show_only_downloaded_sc):
    return gr.update(value=get_thumbnail_list(sc_types,show_only_downloaded_sc,sc_search)),gr.update(choices=[setting.PLACEHOLDER] + classification.get_list())

def on_shortcut_gallery_refresh(sc_types, sc_search, show_only_downloaded_sc):
    return gr.update(value=get_thumbnail_list(sc_types,show_only_downloaded_sc,sc_search))

def on_sc_classification_list_select(evt: gr.SelectData,sc_types, sc_search, show_only_downloaded_sc):
    keys, tags, clfs = util.get_search_keyword(sc_search)
    search = ""    
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
        search = ", ".join(new_search)
        
    return gr.update(value=search),gr.update(value=get_thumbnail_list(sc_types,show_only_downloaded_sc,search))

def on_ui():
    with gr.Accordion("Search", open=True):
        shortcut_type = gr.Dropdown(label='Filter Model type', multiselect=True, choices=[k for k in setting.ui_typenames], interactive=True)
        sc_search = gr.Textbox(label="Search", value="", placeholder="Search name, #tags, @classification, ....",interactive=True, lines=1)
        sc_classification_list = gr.Dropdown(label='Classification', multiselect=None, value=setting.PLACEHOLDER, choices=[setting.PLACEHOLDER] + classification.get_list(), interactive=True)
        show_only_downloaded_sc = gr.Checkbox(label="Show downloaded model's shortcut only", value=False)
    sc_gallery = gr.Gallery(show_label=False,value=get_thumbnail_list()).style(grid=[setting.shortcut_column], height=["full" if setting.shortcut_count_per_page != 0 else "auto"], object_fit=setting.gallery_thumbnail_image_style)    
    # for v in get_thumbnail_list():
    #     util.printD(v)
    # im = gr.Image(visible=False)
    # gr.Examples(examples=[v for v in get_thumbnail_list()],inputs=im)
    with gr.Row(visible=False):
        refresh_sc_list = gr.Textbox()
        # pass
    
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
    
    return sc_gallery, refresh_sc_list