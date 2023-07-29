import gradio as gr
import math
import os
import datetime

from . import util
from . import setting
from . import recipe
from . import ishortcut

from PIL import Image

def on_ui():
    
    recipe_thumb_list, thumb_list , thumb_totals, thumb_max_page  = get_recipe_list(None,None,None,1)    
    reference_list, reference_totals, reference_max_page = get_recipe_reference_list(1)
        
    recipe_list = gr.Dropdown(label="Recipe List", choices=recipe_thumb_list, interactive=True, multiselect=None, visible=False)
    recipe_gallery_page = gr.Slider(minimum=1, maximum=thumb_max_page, value=1, step=1, label=f"Total {thumb_max_page} Pages", interactive=True, visible=True)
    recipe_gallery = gr.Gallery(value=thumb_list, show_label=False).style(grid=[setting.shortcut_column], height="full", object_fit=setting.gallery_thumbnail_image_style, preview=False)
    
    with gr.Accordion(label="Search Recipe", open=True):
        recipe_search = gr.Textbox(label="Search", value="", placeholder="Search name, #description ....",interactive=True, lines=1)
        recipe_classification_list = gr.Dropdown(label="Filter Recipe Classification", choices=[setting.PLACEHOLDER] + recipe.get_classifications(), value=setting.PLACEHOLDER, interactive=True, multiselect=False)        

    with gr.Accordion(label="Filter Reference Shortcut Items", open=False):      
        recipe_reference_select_gallery = gr.Gallery(elem_id="recipe_select_reference_gallery", label="Filter Reference Models").style(grid=[setting.shortcut_column], height="full", object_fit=setting.gallery_thumbnail_image_style, preview=False)
        recipe_reference_gallery_page = gr.Slider(minimum=1, maximum=reference_max_page, value=1, step=1, label=f"Total {reference_max_page} Pages", interactive=True, visible=True)      
        recipe_reference_gallery = gr.Gallery(value=reference_list, show_label=False).style(grid=[setting.shortcut_column], height="full", object_fit=setting.gallery_thumbnail_image_style, preview=False)

    with gr.Row(visible=False):
        # recipe_browser 갱신 트리거
        refresh_recipe_browser = gr.Textbox()

        # 강제 검색 트리거
        refresh_recipe_search = gr.Textbox()        
        
        # recipe_reference_gallery 갱신 트리거
        refresh_recipe_reference_select_gallery = gr.Textbox()

        # 현재 선택된 리퍼런스를 저장하는 곳
        recipe_reference_select = gr.State()
        
    # recipe_reference_select_shortcuts_gallery 에서 선택할때 작용
    recipe_reference_select_gallery.select(
        fn=on_recipe_reference_select_gallery_select,
        inputs=[
            recipe_reference_select
        ],
        outputs=[
            recipe_reference_select,
            recipe_reference_select_gallery,
            refresh_recipe_reference_select_gallery,            
        ],
        show_progress=False
    ) 
    
    # recipe_reference_select_gallery를 recipe_reference_select 값에서 갱신
    refresh_recipe_reference_select_gallery.change(
        fn=on_recipe_reference_select_gallery_loading,
        inputs=[
            recipe_reference_select,
        ],
        outputs=[
            recipe_reference_select_gallery,
            refresh_recipe_search
        ],
        show_progress=False
    )
    
    # recipe_reference_shortcuts_gallery를 선택할때 작용
    recipe_reference_gallery.select(
        fn=on_recipe_reference_gallery_select,
        inputs=[
            recipe_reference_select
        ],
        outputs=[
            recipe_reference_select,            
            refresh_recipe_reference_select_gallery,
        ],
        show_progress=False        
    )               

    recipe_reference_gallery_page.release(
        fn = on_recipe_reference_gallery_page,
        inputs = [            
            recipe_reference_gallery_page
        ],
        outputs=[
            recipe_reference_gallery,
            refresh_recipe_reference_select_gallery
        ]                    
    )
        
    #==============================
    
    recipe_gallery_page.release(
        fn = on_recipe_gallery_page,
        inputs = [          
            recipe_search,
            recipe_classification_list,
            recipe_reference_select,                    
            recipe_gallery_page
        ],
        outputs=[
            recipe_gallery
        ]                    
    )
        
    refresh_recipe_search.change(
        fn=on_recipe_list_search,
        inputs=[            
            recipe_search,
            recipe_classification_list,
            recipe_reference_select
        ],
        outputs=[
            recipe_list,
            recipe_gallery
        ]        
    )
        
    refresh_recipe_browser.change(
        fn=on_refresh_recipe_browser_change,
        inputs= [
            recipe_search,
            recipe_classification_list,            
            recipe_reference_select,
            recipe_gallery_page,
            
            recipe_reference_gallery_page
        ],
        outputs=[
            recipe_classification_list,
            recipe_list,
            recipe_gallery,
            recipe_gallery_page,
            
            recipe_reference_gallery,            
            recipe_reference_gallery_page
        ],
        show_progress=False
    )    
        
    recipe_search.submit(
        fn=on_recipe_list_search,
        inputs=[            
            recipe_search,
            recipe_classification_list,
            recipe_reference_select
        ],
        outputs=[
            recipe_list,
            recipe_gallery
        ]        
    )

    recipe_classification_list.change(
        fn=on_recipe_list_search,
        inputs=[
            recipe_search,
            recipe_classification_list,
            recipe_reference_select
        ],
        outputs=[
            recipe_list,
            recipe_gallery
        ]
    )
        
    return recipe_list, recipe_gallery, refresh_recipe_browser

def on_recipe_reference_gallery_page(page):    
    reference_list, reference_totals, reference_max_page = get_recipe_reference_list(page)
    return gr.update(value=reference_list), reference_list

def on_recipe_gallery_page(search, classification, shortcut, page = 0):        
    recipe_thumb_list, thumb_list , thumb_totals, thumb_max_page  = get_recipe_list(search, classification, shortcut,page)        
    return gr.update(value=thumb_list)

def get_recipe_reference_list(page = 0):

    total = 0
    max_page = 1        
    shortlist = None
    result = None
    
    reference_list =  recipe.get_reference_shortcuts()    
    
    if not reference_list:
        return None, total, max_page
            
    if reference_list:
        total = len(reference_list)
        shortlist = reference_list
        
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

            shortlist = reference_list[item_start:item_end]

    if shortlist:
        result = list()
        for shortcut in shortlist:
            v = ishortcut.get_shortcut_model(str(shortcut))
            if v:
                if ishortcut.is_sc_image(v['id']):
                    result.append((os.path.join(setting.shortcut_thumbnail_folder,f"{v['id']}{setting.preview_image_ext}"), setting.set_shortcutname(v['name'],v['id'])))
                else:
                    result.append((setting.no_card_preview_image,setting.set_shortcutname(v['name'],v['id'])))
                    
    return result, total, max_page                        

def get_recipe_list(search=None, classification=None, shortcut=None, page = 0):
    
    total = 0
    max_page = 1
    shortlist = None
    result = None
    txtlist = list()
    
    if classification == setting.PLACEHOLDER:
        classification = None
        
    recipe_list =  recipe.get_list(search, classification, shortcut)
                                    
    if not recipe_list:
        return txtlist, None, total, max_page
       
    if recipe_list:
        total = len(recipe_list)
        shortlist = recipe_list
        
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
            shortlist = recipe_list[item_start:item_end]
    
    if shortlist:
        result = list()
        txtlist = list()
        for shortcut in shortlist:            
            re = recipe.get_recipe(shortcut)            
            if re:
                if re["image"]:
                    dpimage = os.path.join(setting.shortcut_recipe_folder,f"{re['image']}")
                    
                    if os.path.isfile(dpimage):
                        result.append((dpimage,shortcut))
                    else:
                        result.append((setting.no_card_preview_image,shortcut))
                else:                    
                    result.append((setting.no_card_preview_image,shortcut))
                txtlist.append(shortcut)

    return txtlist, result, total, max_page

def on_recipe_list_search(search, classification, shortcut):
    thumb_list = None
    thumb_totals = 0
    thumb_max_page = 1
        
    recipe_thumb_list, thumb_list , thumb_totals, thumb_max_page  = get_recipe_list(search, classification, shortcut,1)        
        
    return gr.update(choices=recipe_thumb_list), gr.update(value=thumb_list)

def on_refresh_recipe_browser_change(search, classification, shortcut, sc_page, rs_page):
    thumb_list = None
    thumb_totals = 0
    thumb_max_page = 1
    
    recipe_thumb_list, thumb_list , thumb_totals, thumb_max_page  = get_recipe_list(search, classification, shortcut, sc_page)
    
    if not recipe.is_classifications(classification):        
        classification = setting.PLACEHOLDER
        
    reference_list, reference_totals, reference_max_page = get_recipe_reference_list(rs_page)
    return gr.update(choices=[setting.PLACEHOLDER] + recipe.get_classifications(), value=classification), gr.update(choices=recipe_thumb_list), gr.update(value=thumb_list), gr.update(minimum=1, maximum=thumb_max_page, value=sc_page, step=1, label=f"Total {thumb_max_page} Pages"), \
        reference_list, gr.update(minimum=1, maximum=reference_max_page, value=rs_page, step=1, label=f"Total {reference_max_page} Pages")

def on_recipe_reference_select_gallery_select(evt: gr.SelectData, shortcuts):
    if evt.value:               
        shortcut = evt.value 
        sc_model_id = setting.get_modelid_from_shortcutname(shortcut)
        current_time = datetime.datetime.now()
            
        if not shortcuts:
            shortcuts = list()
                
        if sc_model_id in shortcuts:
            shortcuts.remove(sc_model_id)
                    
        return shortcuts, None, current_time
    return shortcuts, None, None

def on_recipe_reference_select_gallery_loading(shortcuts):
    ISC = ishortcut.load()
    if not ISC:
        return None, gr.update(visible=False)
    
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

    current_time = datetime.datetime.now()
    
    return shotcutlist, current_time    

def on_recipe_reference_gallery_select(evt: gr.SelectData, shortcuts):
    clf = None
    current_time = datetime.datetime.now()
            
    if evt.value:
               
        shortcut = evt.value 
        sc_model_id = setting.get_modelid_from_shortcutname(shortcut)            
        
        if not shortcuts:
            shortcuts = list()
            
        if sc_model_id not in shortcuts:
            shortcuts.append(str(sc_model_id))

        return shortcuts, current_time
    return shortcuts, None

