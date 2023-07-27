import gradio as gr
import math

from . import util
from . import setting
from . import model
from . import classification
from . import ishortcut

DOWNLOADED_MODEL = "Downloaded"
NOT_DOWNLOADED_MODEL = "Not Downloaded"
ALL_DOWNLOADED_MODEL = "All"

# def get_thumbnail_list(shortcut_types=None, downloaded_sc=ALL_DOWNLOADED_MODEL, search=None, shortcut_basemodels=None, sc_classifications=None, page = 0):
def get_thumbnail_list(shortcut_types=None, downloaded_sc=False, search=None, shortcut_basemodels=None, sc_classifications=None, page = 0):
    
    total = 0
    max_page = 1
    shortlist =  ishortcut.get_image_list(shortcut_types, search, shortcut_basemodels, sc_classifications)
    result = None
    
    if not shortlist:
        return None, total, max_page
        
    # if downloaded_sc == DOWNLOADED_MODEL:
    #     if model.Downloaded_Models:                
    #         downloaded_list = list()            
    #         for short in shortlist:
    #             sc_name = short[1]
    #             mid = setting.get_modelid_from_shortcutname(sc_name)
    #             if mid in model.Downloaded_Models.keys():
    #                 downloaded_list.append(short)
    #         shortlist = downloaded_list
    #     else:
    #         shortlist = None
    # elif downloaded_sc == NOT_DOWNLOADED_MODEL:
    #     if model.Downloaded_Models:                
    #         downloaded_list = list()            
    #         for short in shortlist:
    #             sc_name = short[1]
    #             mid = setting.get_modelid_from_shortcutname(sc_name)
    #             if mid not in model.Downloaded_Models.keys():
    #                 downloaded_list.append(short)
    #         shortlist = downloaded_list
    
    if downloaded_sc:
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

def on_refresh_sc_list_change(sc_types, sc_search, sc_basemodels, sc_classifications, show_downloaded_sc,sc_page):
    
    thumb_list , thumb_totals, thumb_max_page  = get_thumbnail_list(sc_types,show_downloaded_sc,sc_search,sc_basemodels,sc_classifications,sc_page)
    
    # 현재 페이지가 최대 페이지보다 크면 (최대 페이지를 현재 페이지로 넣고)다시한번 리스트를 구한다.
    if thumb_max_page < sc_page:
        sc_page = thumb_max_page
        thumb_list , thumb_totals, thumb_max_page  = get_thumbnail_list(sc_types,show_downloaded_sc,sc_search,sc_basemodels,sc_classifications,sc_page)
        
    return gr.update(value=thumb_list),gr.update(choices=classification.get_list()),gr.update(minimum=1, maximum=thumb_max_page, value=sc_page, step=1, label=f"Total {thumb_max_page} Pages"),thumb_list

def on_shortcut_gallery_refresh(sc_types, sc_search, sc_basemodels, sc_classifications, show_downloaded_sc):
    thumb_list , thumb_totals, thumb_max_page  = get_thumbnail_list(sc_types,show_downloaded_sc,sc_search,sc_basemodels,sc_classifications,1)
    return gr.update(value=thumb_list),gr.update(minimum=1, maximum=thumb_max_page, value=1, step=1, label=f"Total {thumb_max_page} Pages"),thumb_list

def on_sc_gallery_page(sc_types, sc_search, sc_basemodels, sc_classifications, show_downloaded_sc,sc_page):
    thumb_list , thumb_totals, thumb_max_page  = get_thumbnail_list(sc_types,show_downloaded_sc,sc_search,sc_basemodels,sc_classifications,sc_page)
    return gr.update(value=thumb_list),thumb_list

def on_ui():
    
    thumb_list , thumb_totals, thumb_max_page  = get_thumbnail_list(None,False,None,None,None,1)   
    
    with gr.Accordion("Search", open=True):        
        shortcut_type = gr.Dropdown(label='Filter Model Type', multiselect=True, choices=[k for k in setting.ui_typenames], interactive=True)
        sc_search = gr.Textbox(label="Search", value="", placeholder="Search name, #tags, @personal note ....",interactive=True, lines=1)
        sc_classification_list = gr.Dropdown(label='Classification',info="The selection options of classification are subject to the AND operation.", multiselect=True, choices=classification.get_list(), interactive=True)
        shortcut_basemodel = gr.Dropdown(label='Filter Model BaseModel', multiselect=True, choices=[k for k in setting.model_basemodels], interactive=True)
        show_downloaded_sc = gr.Checkbox(label="Show downloaded model's shortcut only", value=False)
        # show_downloaded_sc = gr.Dropdown(label='Filter Downloaded Model View', multiselect=False, choices=[ALL_DOWNLOADED_MODEL,DOWNLOADED_MODEL,NOT_DOWNLOADED_MODEL], value=ALL_DOWNLOADED_MODEL, interactive=True)    
        
    sc_gallery_page = gr.Slider(minimum=1, maximum=thumb_max_page, value=1, step=1, label=f"Total {thumb_max_page} Pages", interactive=True, visible=True if setting.shortcut_count_per_page > 0 else False)
    # elem_id 를 안써줘야 옆의 인포와 연동이 안된다. 인포쪽에는 써줘야 할것....
    sc_gallery = gr.Gallery(show_label=False, value=thumb_list).style(grid=[setting.shortcut_column], height=["fit" if setting.shortcut_count_per_page != 0 else "auto"], object_fit=setting.gallery_thumbnail_image_style)    

    with gr.Row(visible=False):
        refresh_sc_browser = gr.Textbox()
        refresh_sc_gallery = gr.Textbox()
        sc_gallery_result = gr.State(thumb_list)
    
    refresh_sc_gallery.change(lambda x:x, sc_gallery_result, sc_gallery, show_progress=False)

    sc_gallery_page.release(
        fn = on_sc_gallery_page,
        inputs = [            
            shortcut_type,
            sc_search,
            shortcut_basemodel,
            sc_classification_list,            
            show_downloaded_sc,
            sc_gallery_page
        ],
        outputs=[
            sc_gallery,
            sc_gallery_result
        ]                    
    )
    
    refresh_sc_browser.change(
        fn=on_refresh_sc_list_change,
        inputs= [
            shortcut_type,
            sc_search,
            shortcut_basemodel,
            sc_classification_list,            
            show_downloaded_sc,
            sc_gallery_page
        ],
        outputs=[
            sc_gallery,
            sc_classification_list,
            sc_gallery_page,
            sc_gallery_result
        ],
        show_progress=False
    )
    
    shortcut_type.change(
        fn=on_shortcut_gallery_refresh,
        inputs=[
            shortcut_type,            
            sc_search,
            shortcut_basemodel,
            sc_classification_list,            
            show_downloaded_sc,    
        ],
        outputs=[
            sc_gallery,
            sc_gallery_page,
            sc_gallery_result
        ]
    ) 
        
    sc_search.submit(
        fn=on_shortcut_gallery_refresh,
        inputs=[            
            shortcut_type,
            sc_search,
            shortcut_basemodel,
            sc_classification_list,            
            show_downloaded_sc,    
        ],
        outputs=[
            sc_gallery,
            sc_gallery_page,
            sc_gallery_result
        ]        
    )

    shortcut_basemodel.change(
        fn=on_shortcut_gallery_refresh,
        inputs=[
            shortcut_type,            
            sc_search,
            shortcut_basemodel,
            sc_classification_list,            
            show_downloaded_sc,    
        ],
        outputs=[
            sc_gallery,
            sc_gallery_page,
            sc_gallery_result
        ]
    ) 
           
    show_downloaded_sc.change(
        fn=on_shortcut_gallery_refresh,
        inputs=[
            shortcut_type,
            sc_search,
            shortcut_basemodel,
            sc_classification_list,            
            show_downloaded_sc,
        ],
        outputs=[
            sc_gallery,
            sc_gallery_page,
            sc_gallery_result
        ]
    )    

    sc_classification_list.change(
        fn=on_shortcut_gallery_refresh,
        inputs=[
            shortcut_type,            
            sc_search,
            shortcut_basemodel,
            sc_classification_list,            
            show_downloaded_sc,    
        ],
        outputs=[
            sc_gallery,
            sc_gallery_page,
            sc_gallery_result
        ]
    )
    
    return sc_gallery, refresh_sc_browser, refresh_sc_gallery