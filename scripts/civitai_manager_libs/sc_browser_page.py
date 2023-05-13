import gradio as gr
import math

from . import util
from . import setting
from . import model
from . import classification
from . import ishortcut


def get_thumbnail_list(shortcut_types=None, only_downloaded=False, search=None, page = 0):
    
    total = 0
    max_page = 1
    shortlist =  ishortcut.get_image_list(shortcut_types, search)
    result = None
    
    if not shortlist:
        return None, total, max_page
    
    if only_downloaded:
        if model.Downloaded_Models:                
            downloaded_list = list()            
            for short in shortlist:
                sc_name = short[1]
                mid = setting.get_modelid_from_shortcutname(sc_name)
                if mid in model.Downloaded_Models.keys():
                    downloaded_list.append(short)
            shortlist = downloaded_list
        else:
            shortlist = None
            
    if shortlist:
        total = len(shortlist)
        result = shortlist
        
    if total > 0:
        # page 즉 페이징이 아닌 전체가 필요할때도 총페이지 수를 구할때도 있으므로..
        # page == 0 은 전체 리스트를 반환한다
        if setting.shortcut_count_per_page > 0:
            max_page = math.ceil(total / setting.shortcut_count_per_page)

        if page > 0 and setting.shortcut_count_per_page > 0:
            item_start = setting.shortcut_count_per_page * (page - 1)
            item_end = (setting.shortcut_count_per_page * page)
            if total < item_end:
                item_end = total
            result = shortlist[item_start:item_end]
                    
    return result, total, max_page

def on_refresh_sc_list_change(sc_types,sc_search,show_only_downloaded_sc,sc_page):
    
    thumb_list , thumb_totals, thumb_max_page  = get_thumbnail_list(sc_types,show_only_downloaded_sc,sc_search,sc_page)
    
    # 현재 페이지가 최대 페이지보다 크면 (최대 페이지를 현재 페이지로 넣고)다시한번 리스트를 구한다.
    if thumb_max_page < sc_page:
        sc_page = thumb_max_page
        thumb_list , thumb_totals, thumb_max_page  = get_thumbnail_list(sc_types,show_only_downloaded_sc,sc_search, sc_page)
        
    return gr.update(value=thumb_list),gr.update(choices=[setting.PLACEHOLDER] + classification.get_list()),gr.update(minimum=1, maximum=thumb_max_page, value=sc_page, step=1, label=f"Total {thumb_max_page} Pages")

def on_shortcut_gallery_refresh(sc_types, sc_search, show_only_downloaded_sc):
    thumb_list , thumb_totals, thumb_max_page  = get_thumbnail_list(sc_types,show_only_downloaded_sc,sc_search,1)
    return gr.update(value=thumb_list),gr.update(minimum=1, maximum=thumb_max_page, value=1, step=1, label=f"Total {thumb_max_page} Pages")

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
            
    thumb_list , thumb_totals, thumb_max_page  = get_thumbnail_list(sc_types,show_only_downloaded_sc,search,1)
    return gr.update(value=search),gr.update(value=thumb_list),gr.update(minimum=1, maximum=thumb_max_page, value=1, step=1, label=f"Total {thumb_max_page} Pages")

def on_sc_gallery_page(sc_types,sc_search,show_only_downloaded_sc,sc_page):
    thumb_list , thumb_totals, thumb_max_page  = get_thumbnail_list(sc_types,show_only_downloaded_sc,sc_search,sc_page)
    return gr.update(value=thumb_list)

def on_ui():
    
    thumb_list , thumb_totals, thumb_max_page  = get_thumbnail_list(None,False,None,1)   
    
    with gr.Accordion("Search", open=True):
        shortcut_type = gr.Dropdown(label='Filter Model type', multiselect=True, choices=[k for k in setting.ui_typenames], interactive=True)
        sc_search = gr.Textbox(label="Search", value="", placeholder="Search name, #tags, @classification, ....",interactive=True, lines=1)
        sc_classification_list = gr.Dropdown(label='Classification', multiselect=None, value=setting.PLACEHOLDER, choices=[setting.PLACEHOLDER] + classification.get_list(), interactive=True)
        show_only_downloaded_sc = gr.Checkbox(label="Show downloaded model's shortcut only", value=False)
    sc_gallery_page = gr.Slider(minimum=1, maximum=thumb_max_page, value=1, step=1, label=f"Total {thumb_max_page} Pages", interactive=True, visible=True if setting.shortcut_count_per_page > 0 else False)
    sc_gallery = gr.Gallery(show_label=False, value=thumb_list).style(grid=[setting.shortcut_column], height=["fit" if setting.shortcut_count_per_page != 0 else "auto"], object_fit=setting.gallery_thumbnail_image_style)    

    with gr.Row(visible=False):
        refresh_sc_list = gr.Textbox()
    
    sc_gallery_page.release(
        fn = on_sc_gallery_page,
        inputs = [            
            shortcut_type,
            sc_search,
            show_only_downloaded_sc,
            sc_gallery_page
        ],
        outputs=[
            sc_gallery
        ]                    
    )
    
    refresh_sc_list.change(
        fn=on_refresh_sc_list_change,
        inputs= [
            shortcut_type,
            sc_search,
            show_only_downloaded_sc,
            sc_gallery_page
        ],
        outputs=[
            sc_gallery,
            sc_classification_list,
            sc_gallery_page
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
            sc_gallery_page
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
            sc_gallery,
            sc_gallery_page
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
            sc_gallery_page
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
            sc_gallery,
            sc_gallery_page
        ]        
    )
    
    return sc_gallery, refresh_sc_list