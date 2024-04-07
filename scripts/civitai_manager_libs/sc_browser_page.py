import gradio as gr
import math
import os
import datetime

from . import util
from . import setting
from . import model
from . import classification
from . import ishortcut

DOWNLOADED_MODEL = "Downloaded"
NOT_DOWNLOADED_MODEL = "Not Downloaded"
ALL_DOWNLOADED_MODEL = "All"

def on_ui(search_open=True,user_shortcut_browser_search_up=None,user_shortcut_column=None, user_shortcut_rows_per_page=None):
    shortcut_browser_search_up = setting.shortcut_browser_search_up
    shortcut_column = setting.shortcut_column
    shortcut_rows_per_page = setting.shortcut_rows_per_page
    
    if user_shortcut_browser_search_up:
        if user_shortcut_browser_search_up == "UP":
            shortcut_browser_search_up = True
        elif user_shortcut_browser_search_up == "DOWN":
            shortcut_browser_search_up = False
        
    if user_shortcut_column:
        shortcut_column = user_shortcut_column
        
    if user_shortcut_rows_per_page:
        shortcut_rows_per_page = user_shortcut_rows_per_page

    thumb_list , thumb_totals, thumb_max_page  = get_thumbnail_list(None,False,None,None,None,1,shortcut_column,shortcut_rows_per_page)
    
    show_downloaded_sc = gr.Dropdown(label='Filter Downloaded', multiselect=False, choices=[ALL_DOWNLOADED_MODEL,DOWNLOADED_MODEL,NOT_DOWNLOADED_MODEL], value=ALL_DOWNLOADED_MODEL, interactive=True)               
    
    # sc_list = list()
    # for i in range(0, shortcut_column):
    #     sc_list.append(gr.Button(value="tttt",scale=1))
        
    if shortcut_browser_search_up:
        with gr.Accordion("Search", open=search_open):        
            shortcut_type = gr.Dropdown(label='Filter Model Type', multiselect=True, choices=[k for k in setting.ui_typenames], interactive=True)
            sc_search = gr.Textbox(label="Search", value="", placeholder="Search name, #tags, @personal note ....",interactive=True, lines=1)
            sc_classification_list = gr.Dropdown(label='Classification',info="The selection options of classification are subject to the AND operation.", multiselect=True, choices=classification.get_list(), interactive=True)
            shortcut_basemodel = gr.Dropdown(label='Filter Model BaseModel', multiselect=True, choices=[k for k in setting.model_basemodels.keys()], interactive=True)
            reset_filter_btn = gr.Button(value="Reset Filter",variant="primary")
            
        sc_gallery_page = gr.Slider(minimum=1, maximum=thumb_max_page, value=1, step=1, label=f"Total {thumb_max_page} Pages", interactive=True, visible=True if shortcut_rows_per_page > 0 else False)                
        with gr.Row():
            sc_prevPage_btn = gr.Button(value="Prev",scale=1, visible=True if shortcut_rows_per_page > 0 else False)            
            sc_nextPage_btn = gr.Button(value="Next",scale=1, visible=True if shortcut_rows_per_page > 0 else False)
        
        sc_gallery = gr.Gallery(show_label=False, columns=shortcut_column, height="auto", object_fit=setting.gallery_thumbnail_image_style, allow_preview=False, value=thumb_list)
    else:
        sc_gallery_page = gr.Slider(minimum=1, maximum=thumb_max_page, value=1, step=1, label=f"Total {thumb_max_page} Pages", interactive=True, visible=True if shortcut_rows_per_page > 0 else False)                
        with gr.Row():
            sc_prevPage_btn = gr.Button(value="Prev",scale=1, visible=True if shortcut_rows_per_page > 0 else False)            
            sc_nextPage_btn = gr.Button(value="Next",scale=1, visible=True if shortcut_rows_per_page > 0 else False)
        
        sc_gallery = gr.Gallery(show_label=False, columns=shortcut_column, height="auto", object_fit=setting.gallery_thumbnail_image_style, allow_preview=False, value=thumb_list)
        
        with gr.Accordion("Search", open=search_open):        
            shortcut_type = gr.Dropdown(label='Filter Model Type', multiselect=True, choices=[k for k in setting.ui_typenames], interactive=True)
            sc_search = gr.Textbox(label="Search", value="", placeholder="Search name, #tags, @personal note ....",interactive=True, lines=1)
            sc_classification_list = gr.Dropdown(label='Classification',info="The selection options of classification are subject to the AND operation.", multiselect=True, choices=classification.get_list(), interactive=True)
            shortcut_basemodel = gr.Dropdown(label='Filter Model BaseModel', multiselect=True, choices=[k for k in setting.model_basemodels.keys()], interactive=True)
            reset_filter_btn = gr.Button(value="Reset Filter",variant="primary")
            
    with gr.Row(visible=False):
        refresh_sc_browser = gr.Textbox()
        refresh_sc_gallery = gr.Textbox()
        sc_gallery_result = gr.State(thumb_list)
        sc_shortcut_column = gr.State(shortcut_column)
        sc_shortcut_rows_per_page = gr.State(shortcut_rows_per_page)
    
    refresh_sc_gallery.change(lambda x:x, sc_gallery_result, sc_gallery, show_progress=False)

    sc_gallery_page.release(
        fn = on_sc_gallery_page,
        inputs = [            
            shortcut_type,
            sc_search,
            shortcut_basemodel,
            sc_classification_list,            
            show_downloaded_sc,
            sc_gallery_page,
            
            sc_shortcut_column,
            sc_shortcut_rows_per_page
        ],
        outputs=[
            sc_gallery,
            sc_gallery_result
        ],
        show_progress=False                    
    )
    
    refresh_sc_browser.change(
        fn=on_refresh_sc_list_change,
        inputs= [
            shortcut_type,
            sc_search,
            shortcut_basemodel,
            sc_classification_list,            
            show_downloaded_sc,
            sc_gallery_page,

            sc_shortcut_column,
            sc_shortcut_rows_per_page
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
            
            sc_shortcut_column,
            sc_shortcut_rows_per_page            
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
            
            sc_shortcut_column,
            sc_shortcut_rows_per_page            
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
            
            sc_shortcut_column,
            sc_shortcut_rows_per_page            
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
            
            sc_shortcut_column,
            sc_shortcut_rows_per_page            
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
            
            sc_shortcut_column,
            sc_shortcut_rows_per_page            
        ],
        outputs=[
            sc_gallery,
            sc_gallery_page,
            sc_gallery_result
        ]
    )

    reset_filter_btn.click(
        fn=on_reset_filter_btn_click,
        inputs=None,
        outputs=[
            shortcut_type,            
            sc_search,
            shortcut_basemodel,
            sc_classification_list,            
            show_downloaded_sc,
            sc_gallery_page,
            
            refresh_sc_browser
        ],
        show_progress=False                
    )

    sc_prevPage_btn.click(
        fn = on_sc_prevPage_btn_click,
        inputs = [            
            shortcut_type,
            sc_search,
            shortcut_basemodel,
            sc_classification_list,            
            show_downloaded_sc,
            sc_gallery_page,
            
            sc_shortcut_column,
            sc_shortcut_rows_per_page
        ],
        outputs=[
            sc_gallery,
            sc_gallery_page,
            sc_gallery_result
        ],
        show_progress=False                    
    )

    sc_nextPage_btn.click(
        fn = on_sc_nextPage_btn_click,
        inputs = [            
            shortcut_type,
            sc_search,
            shortcut_basemodel,
            sc_classification_list,            
            show_downloaded_sc,
            sc_gallery_page,
            
            sc_shortcut_column,
            sc_shortcut_rows_per_page
        ],
        outputs=[
            sc_gallery,
            sc_gallery_page,
            sc_gallery_result
        ],
        show_progress=False                    
    )            

    return sc_gallery, refresh_sc_browser, refresh_sc_gallery

def on_reset_filter_btn_click():
    current_time = datetime.datetime.now()
    return gr.update(value=[]), gr.update(value=None), gr.update(value=[]), gr.update(value=[]), gr.update(value=ALL_DOWNLOADED_MODEL),gr.update(value=1), current_time

def get_thumbnail_list(shortcut_types=None, downloaded_sc=False, search=None, shortcut_basemodels=None, sc_classifications=None, page = 0, columns=0, rows=0):
    
    total = 0
    max_page = 1
    shortcut_list =  ishortcut.get_image_list(shortcut_types, search, shortcut_basemodels, sc_classifications)
    shortlist = None
    result = None
    
    if not shortcut_list:
        return None, total, max_page
        
    if downloaded_sc == DOWNLOADED_MODEL:
        if model.Downloaded_Models:                
            downloaded_list = list()            
            for short in shortcut_list:
                mid = short['id']
                if str(mid) in model.Downloaded_Models.keys():
                    downloaded_list.append(short)
            shortcut_list = downloaded_list
        else:
            shortcut_list = None
    elif downloaded_sc == NOT_DOWNLOADED_MODEL:
        if model.Downloaded_Models:                
            downloaded_list = list()            
            for short in shortcut_list:
                mid = short['id']
                if str(mid) not in model.Downloaded_Models.keys():
                    downloaded_list.append(short)
            shortcut_list = downloaded_list
    
    # if downloaded_sc:
    #     if model.Downloaded_Models:                
    #         downloaded_list = list()            
    #         for short in shortcut_list:
    #             mid = short['id']
    #             if str(mid) in model.Downloaded_Models.keys():
    #                 downloaded_list.append(short)
    #         shortcut_list = downloaded_list
    #     else:
    #         shortcut_list = None
    
    if shortcut_list:        
        total = len(shortcut_list)

        # name 기준으로 정렬        
        shortcut_list = sorted(shortcut_list, key=lambda x: x["name"].lower().strip(), reverse=False)
        
        # 등록일 기준으로 정렬
        # strptime str을 datetime 형식으로 변환(스트링과 형식일치해야함)
        # strftime datetime 형식을 str로 변환(스트링과 형식이 일치할필요는 없다.)
        # shortcut_list = sorted(shortcut_list, key=lambda x: datetime.datetime.strptime(x["date"], '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d'), reverse=True)
        # shortcut_list = sorted(shortcut_list, key=lambda x: x["date"], reverse=True)        
        # shortcut_list = sorted(shortcut_list, key=lambda x: (x["date"], x['name']) , reverse=True)

        shortlist = shortcut_list
        
    if total > 0:
        # page 즉 페이징이 아닌 전체가 필요할때도 총페이지 수를 구할때도 있으므로..
        # page == 0 은 전체 리스트를 반환한다
        shortcut_count_per_page = columns * rows
        if shortcut_count_per_page > 0:
            max_page = math.ceil(total / shortcut_count_per_page)

        if page > max_page:
            page = max_page
            
        if page > 0 and shortcut_count_per_page > 0:
            item_start = shortcut_count_per_page * (page - 1)
            item_end = (shortcut_count_per_page * page)
            if total < item_end:
                item_end = total
            shortlist = shortcut_list[item_start:item_end]

    if shortlist:
        result = list()        
        # 썸네일이 있는지 판단해서 대체 이미지 작업
        for v in shortlist:
            if v:
                if ishortcut.is_sc_image(v['id']):
                    if 'nsfw' in v.keys() and bool(v['nsfw']) and setting.NSFW_filtering_enable:
                        result.append((setting.nsfw_disable_image,setting.set_shortcutname(v['name'],v['id'])))
                    else:
                        result.append((os.path.join(setting.shortcut_thumbnail_folder,f"{v['id']}{setting.preview_image_ext}"),setting.set_shortcutname(v['name'],v['id'])))
                else:
                    result.append((setting.no_card_preview_image,setting.set_shortcutname(v['name'],v['id'])))
                                    
    return result, total, max_page

def on_refresh_sc_list_change(sc_types, sc_search, sc_basemodels, sc_classifications, show_downloaded_sc, sc_page, columns, rows):
    
    thumb_list , thumb_totals, thumb_max_page  = get_thumbnail_list(sc_types,show_downloaded_sc,sc_search,sc_basemodels,sc_classifications,sc_page, columns, rows)
    
    # 현재 페이지가 최대 페이지보다 크면 (최대 페이지를 현재 페이지로 넣고)다시한번 리스트를 구한다.
    if thumb_max_page < sc_page:
        sc_page = thumb_max_page
        thumb_list , thumb_totals, thumb_max_page  = get_thumbnail_list(sc_types,show_downloaded_sc,sc_search,sc_basemodels,sc_classifications,sc_page, columns, rows)
        
    return gr.update(value=thumb_list),gr.update(choices=classification.get_list()),gr.update(minimum=1, maximum=thumb_max_page, value=sc_page, step=1, label=f"Total {thumb_max_page} Pages"),thumb_list

def on_shortcut_gallery_refresh(sc_types, sc_search, sc_basemodels, sc_classifications, show_downloaded_sc, columns, rows):
    thumb_list , thumb_totals, thumb_max_page  = get_thumbnail_list(sc_types,show_downloaded_sc,sc_search,sc_basemodels,sc_classifications,1, columns, rows)
    return gr.update(value=thumb_list),gr.update(minimum=1, maximum=thumb_max_page, value=1, step=1, label=f"Total {thumb_max_page} Pages"),thumb_list

def on_sc_gallery_page(sc_types, sc_search, sc_basemodels, sc_classifications, show_downloaded_sc, sc_page, columns, rows):
    thumb_list , thumb_totals, thumb_max_page  = get_thumbnail_list(sc_types,show_downloaded_sc,sc_search,sc_basemodels,sc_classifications,sc_page, columns, rows)
    return gr.update(value=thumb_list),thumb_list

def on_sc_nextPage_btn_click(sc_types, sc_search, sc_basemodels, sc_classifications, show_downloaded_sc, sc_page, columns, rows):
    sc_page = sc_page + 1
    thumb_list , thumb_totals, thumb_max_page  = get_thumbnail_list(sc_types,show_downloaded_sc,sc_search,sc_basemodels,sc_classifications,sc_page, columns, rows)
    
    if sc_page > thumb_max_page:
        sc_page = thumb_max_page
        
    return gr.update(value=thumb_list),sc_page,thumb_list

def on_sc_prevPage_btn_click(sc_types, sc_search, sc_basemodels, sc_classifications, show_downloaded_sc, sc_page, columns, rows):
    sc_page = sc_page - 1
    if sc_page < 1:
        sc_page = 1    
    thumb_list , thumb_totals, thumb_max_page  = get_thumbnail_list(sc_types,show_downloaded_sc,sc_search,sc_basemodels,sc_classifications,sc_page, columns, rows)
    return gr.update(value=thumb_list),sc_page,thumb_list