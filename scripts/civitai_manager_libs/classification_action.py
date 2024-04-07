import os
import math
import gradio as gr
import datetime

from . import util
from . import setting
from . import ishortcut
from . import classification
from . import classification_browser_page

def on_ui(shortcut_input):   
    with gr.Row(visible=False):
        selected_classification_name = gr.Textbox()
        classification_shortcuts = gr.State()
        # classification_shortcuts_page = gr.State()
        refresh_gallery = gr.Textbox()
        refresh_classification = gr.Textbox()
        
    with gr.Column(scale=setting.shortcut_browser_screen_split_ratio):        
        classification_new_btn = gr.Button(value="New Classification", variant="primary")
        with gr.Tabs():
            with gr.TabItem("Classification List"):                        
                classification_list = gr.Dropdown(label='Classification List', multiselect=None, choices=classification.get_list(), value="" ,interactive=True)
            with gr.TabItem("Additional Shortcut Models"):
                sc_gallery, refresh_sc_browser, refresh_sc_gallery = classification_browser_page.on_ui(classification_shortcuts,False)

    with gr.Column(scale=(setting.shortcut_browser_screen_split_ratio_max-setting.shortcut_browser_screen_split_ratio)):  
        with gr.Accordion(label=setting.PLACEHOLDER, open=True) as classification_title_name: 
            with gr.Row():
                with gr.Column():            
                # with gr.Column(scale=4):           
                    classification_name = gr.Textbox(label="Name", value="",interactive=True, lines=1)
                    with gr.Tabs() as classification_information_tabs:
                        with gr.TabItem("Classification Shortcuts", id="Classification_Shortcuts"):   
                            with gr.Row():
                                with gr.Column(scale=4):
                                    classification_gallery_page = gr.Slider(minimum=1, maximum=1, value=1, step=1, label=f"Total {1} Pages", interactive=True, visible=True if setting.classification_gallery_rows_per_page > 0 else False)
                                    with gr.Row():
                                        classification_prevPage_btn = gr.Button(value="Prev",scale=1)            
                                        classification_nextPage_btn = gr.Button(value="Next",scale=1)
                                                
                                    classification_shortcut_delete = gr.Checkbox(label="Delete from classification when selecting a thumbnail.", value=False)
                                    classification_gallery = gr.Gallery(elem_id="classification_gallery", show_label=False, columns=setting.classification_gallery_column, height="auto", object_fit=setting.gallery_thumbnail_image_style, preview=False, allow_preview=False)                                                
                                with gr.Accordion("#", open=True, visible=False) as shortcut_model_information:        
                                    shortcut_modelid = gr.Textbox(visible=False)
                                    shortcut_modeltype = gr.Textbox(label="Model Type", interactive=False, lines=1)
                                    shortcut_versions = gr.Dropdown(label="Model Version",interactive=True)
                                    shortcut_filenames = gr.Dropdown(label="Version filename", interactive=True)
                                    shortcut_triger = gr.Textbox(label="Triger", interactive=True, lines=1)
                                    goto_model_info_btn = gr.Button(value="Information", variant="primary") 
                                    delete_shortcut_model_btn = gr.Button(value="Delete", variant="primary")
                                    close_shortcut_model_information_btn = gr.Button(value="Close", variant="primary")
                                    
                            with gr.Row():
                                classification_clear_shortcut_btn = gr.Button(value="Clear")
                                classification_reload_shortcut_btn = gr.Button(value="Reload")
                        with gr.TabItem("Classification Info"):                                            
                            classification_info = gr.Textbox(label="Description", value="",interactive=True, lines=7)                                
                    with gr.Row():                        
                        classification_create_btn = gr.Button(value="Create", variant="primary")
                        classification_update_btn = gr.Button(value="Update", variant="primary", visible=False)
                
                        with gr.Accordion("Delete Classification", open=False): 
                            classification_delete_btn = gr.Button(value="Delete")

    classification_gallery_page.release(
        fn = on_classification_gallery_page,
        inputs = [          
            classification_gallery_page
        ],
        outputs=[
            refresh_gallery
        ]                    
    )
       
    classification_new_btn.click(    
        fn=on_classification_new_btn_click,
        inputs=None,
        outputs=[
            selected_classification_name,
            classification_name,
            classification_info,
            classification_shortcuts,            
            classification_gallery_page,
            shortcut_modelid,
            refresh_gallery,
            refresh_sc_browser,
            classification_title_name,
            classification_create_btn,
            classification_update_btn                                    
        ]          
    ) 
            
    refresh_classification.change(
        fn=on_refresh_classification_change,
        inputs=[
            selected_classification_name
        ],
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
            classification_gallery_page
        ],
        outputs=[
            classification_gallery,
            classification_gallery_page,
            refresh_sc_browser
        ],
        show_progress=False
    )

    sc_gallery.select(
        fn=on_sc_gallery_select,
        inputs=[
            classification_shortcuts,
            classification_gallery_page
        ],
        outputs=[
            classification_shortcuts,
            classification_gallery_page,
            refresh_gallery,            
            # sc_gallery,
            # refresh_sc_gallery,
            classification_information_tabs
        ],
        show_progress=False        
    )
    
    classification_gallery.select(
        fn=on_classification_gallery_select,
        inputs=[
            classification_shortcuts,
            classification_shortcut_delete
        ],
        outputs=[
            classification_shortcuts,
            refresh_gallery,
            classification_gallery, # 이거는 None으로 할 필요는 gallery를 미선택으로 만드는 방법을 몰라서 일단 이렇게 해보자 
            shortcut_modelid
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
            selected_classification_name,
            classification_list,            
            refresh_sc_browser,
            classification_title_name,
            classification_create_btn,
            classification_update_btn             
        ]        
    )
    
    classification_update_btn.click(
        fn=on_classification_update_btn_click,
        inputs=[
            selected_classification_name,
            classification_name,
            classification_info,
            classification_shortcuts
        ],
        outputs=[
            selected_classification_name,
            classification_list,            
            refresh_sc_browser,
            classification_title_name
        ]         
    )

    classification_delete_btn.click(
        fn=on_classification_delete_btn_click,
        inputs=[
            selected_classification_name
        ],
        outputs=[
            selected_classification_name,
            classification_list,            
            # classification_shortcuts,
            # refresh_gallery,
            refresh_sc_browser,
            classification_title_name,
            classification_create_btn,
            classification_update_btn
        ]         
    )

    classification_clear_shortcut_btn.click(
        fn=on_classification_clear_shortcut_btn_click,
        inputs=None,
        outputs=[
            classification_shortcuts,
            classification_gallery_page,
            shortcut_modelid,
            refresh_gallery
        ]         
    )    

    classification_reload_shortcut_btn.click(
        fn=on_classification_reload_shortcut_btn_click,
        inputs=[
            selected_classification_name
        ],
        outputs=[
            classification_shortcuts,
            classification_gallery_page,
            refresh_gallery
        ]
    )   
                        
    classification_list.select(    
        fn=on_classification_list_select,
        inputs=None,
        outputs=[
            selected_classification_name,
            classification_name,
            classification_info,
            classification_shortcuts,
            classification_gallery_page,
            shortcut_modelid,
            refresh_gallery,
            refresh_sc_browser,
            classification_title_name,
            classification_create_btn,
            classification_update_btn                        
        ]          
    )

    shortcut_modelid.change(
        fn=on_shortcut_modelid_change,
        inputs=[
            shortcut_modelid,
        ],
        outputs=[            
            shortcut_modeltype,
            shortcut_versions,                    
            shortcut_filenames,
            shortcut_triger,
            shortcut_model_information
        ],
        show_progress=False
    )
    
    shortcut_versions.select(
        fn=on_shortcut_versions_select,
        inputs=[
            shortcut_modelid,
        ],
        outputs=[
            shortcut_modeltype,
            shortcut_versions,                    
            shortcut_filenames,
            shortcut_triger,
            shortcut_model_information
        ],
        show_progress=False
    )

    goto_model_info_btn.click(lambda x:x,shortcut_modelid,shortcut_input)
    
    delete_shortcut_model_btn.click(
        fn=on_delete_shortcut_model_btn_click,
        inputs=[
            shortcut_modelid,
            classification_shortcuts,
        ],
        outputs=[
            classification_shortcuts,
            refresh_gallery,
            classification_gallery,
            shortcut_modelid
        ],
        show_progress=False
    ) 

    close_shortcut_model_information_btn.click(
        fn=on_close_shortcut_model_information_btn_click,
        inputs=[
            classification_shortcuts,
        ],
        outputs=[
            classification_shortcuts,
            refresh_gallery,
            classification_gallery,
            shortcut_modelid
        ],
        show_progress=False
    ) 

    classification_prevPage_btn.click(
        fn = on_classification_prevPage_btn_click,
        inputs = [          
            classification_gallery_page
        ],
        outputs=[
            refresh_gallery,
            classification_gallery_page
        ],
        show_progress=False                    
    )

    classification_nextPage_btn.click(
        fn = on_classification_nextPage_btn_click,
        inputs = [          
            classification_gallery_page
        ],
        outputs=[
            refresh_gallery,
            classification_gallery_page
        ],
        show_progress=False
    )
               
    return refresh_classification

def on_classification_nextPage_btn_click(page):
    page = page + 1    
    current_time = datetime.datetime.now()
    return current_time, page

def on_classification_prevPage_btn_click(page):    
    page = page - 1
    if page < 1:
        page = 1      
    current_time = datetime.datetime.now()
    return current_time, page

def load_model_information(modelid=None, ver_index=None):
    if modelid:        
        model_info,version_info,versionid,version_name,model_type,model_basemodels,versions_list, dhtml, triger, files = ishortcut.get_model_information(modelid,None,ver_index)
        if model_info:
            flist = list()
            for file in files:            
                flist.append(file['name'])
                
            file_name = ''
            if len(flist) > 0:
                file_name = flist[0]
                            
            title_name = f"# {model_info['name']} : {version_name}"
                        
            return gr.update(value=setting.get_ui_typename(model_type)), gr.update(choices=versions_list,value=version_name), gr.update(choices=flist,value=file_name), gr.update(value=triger), gr.update(label=title_name,visible=True)
    return None, None, None, gr.update(value=None), gr.update(label="#",visible=False)

def on_shortcut_modelid_change(modelid=None):    
    return load_model_information(modelid, None)

def on_shortcut_versions_select(evt: gr.SelectData, modelid:str):
    return load_model_information(modelid, evt.index)    

def on_delete_shortcut_model_btn_click(sc_model_id:str, shortcuts):
    if sc_model_id:                       
        current_time = datetime.datetime.now()
            
        if not shortcuts:
            shortcuts = list()
        
        if sc_model_id in shortcuts:
            shortcuts.remove(sc_model_id)                
            return shortcuts, current_time, None, None
        
    return shortcuts, gr.update(visible=False), gr.update(visible=True), gr.update(visible=False)

def on_close_shortcut_model_information_btn_click(shortcuts):
    current_time = datetime.datetime.now()    
    return shortcuts, current_time, None, None
        
def get_shortcut_by_modelid(ISC, modelid):
    if ISC and modelid:
        try:           
            return ISC[str(modelid)]
        except:
            pass
    return None

def on_classification_gallery_page(page = 0):        
    current_time = datetime.datetime.now()
    return current_time

# shortcuts_list 에서 페이지 부분만 잘라서 리턴한다.
def paging_classification_shortcuts_list(shortcuts_list, page = 0):

    total = 0
    max_page = 1        
    shortlist = None
    result = None
    
    # shortcuts_list =  classification.get_classification_shortcuts(select_name) 
    
    if not shortcuts_list:
        return None, total, max_page
            
    if shortcuts_list:
        total = len(shortcuts_list)
        shortlist = shortcuts_list
        
    if total > 0:
        # page 즉 페이징이 아닌 전체가 필요할때도 총페이지 수를 구할때도 있으므로..
        # page == 0 은 전체 리스트를 반환한다
        shortcut_count_per_page = setting.classification_gallery_column * setting.classification_gallery_rows_per_page
        
        if shortcut_count_per_page > 0:
            max_page = math.ceil(total / shortcut_count_per_page)

        if page > max_page:
            page = max_page
            
        if page > 0 and shortcut_count_per_page > 0:
            item_start = shortcut_count_per_page * (page - 1)
            item_end = (shortcut_count_per_page * page)
            if total < item_end:
                item_end = total

            shortlist = shortcuts_list[item_start:item_end]

    result = shortlist

    return result, total, max_page, page

def on_classification_new_btn_click():
    current_time = datetime.datetime.now()
    return gr.update(value=""), gr.update(value=""), gr.update(value=""), None, gr.update(value=1, minimum=1, maximum=1, step=1, label=f"Total {1} Pages"), None, \
        current_time, current_time, gr.update(label=setting.NEWCLASSIFICATION),gr.update(visible=True), gr.update(visible=False)

def on_classification_reload_shortcut_btn_click(select_name):

    if select_name:
        shortcuts = classification.get_classification_shortcuts(select_name)
        
        current_time = datetime.datetime.now()
        
        return shortcuts, gr.update(value=1), current_time
    return None, gr.update(value=1, minimum=1, maximum=1, step=1, label=f"Total {1} Pages"), gr.update(visible=False)

def on_refresh_classification_change(select_name):
    current_time = datetime.datetime.now()
    if select_name:
        info = classification.get_classification_info(select_name)
        
        return gr.update(value=select_name), gr.update(value=info), current_time, gr.update(label=select_name), current_time, gr.update(choices=classification.get_list())
    return gr.update(value=""), gr.update(value=""), current_time, gr.update(label=setting.NEWCLASSIFICATION), gr.update(visible=True), gr.update(choices=classification.get_list())

def on_sc_gallery_select(evt: gr.SelectData, shortcuts, page):
    current_time = datetime.datetime.now()
    
    if evt.value:
               
        shortcut = evt.value 
        sc_model_id = setting.get_modelid_from_shortcutname(shortcut)            
        
        if not shortcuts:
            shortcuts = list()
            
        if sc_model_id not in shortcuts:
            shortcuts.append(sc_model_id)
        
        total = len(shortcuts)
        shortcut_count_per_page = setting.classification_gallery_column * setting.classification_gallery_rows_per_page
        if shortcut_count_per_page > 0:
            page = math.ceil(total / shortcut_count_per_page)

        return shortcuts, gr.update(value=page, maximum=page), current_time, gr.update(selected="Classification_Shortcuts")
    return shortcuts, gr.update(value=page), None, gr.update(selected="Classification_Shortcuts")

def on_classification_gallery_loading(shortcuts, page=0):
    totals = 0
    max_page = 1    
    cur_page = 1
    ISC = ishortcut.load()
    if not ISC:
        return None, gr.update(minimum=1),gr.update(visible=False)
        
    result_list = None
    
    if shortcuts:
        
        # 현재 표시될 페이지 양만 잘라준다.
        shortcuts, totals, max_page, cur_page  = paging_classification_shortcuts_list(shortcuts, page)
        
        result_list = list()
        for mid in shortcuts:            
            if str(mid) in ISC.keys():
                v = ISC[str(mid)]
                if ishortcut.is_sc_image(v['id']):
                    if 'nsfw' in v.keys() and bool(v['nsfw']) and setting.NSFW_filtering_enable:
                        result_list.append((setting.nsfw_disable_image,setting.set_shortcutname(v['name'],v['id'])))
                    else:                    
                        result_list.append((os.path.join(setting.shortcut_thumbnail_folder,f"{v['id']}{setting.preview_image_ext}"),setting.set_shortcutname(v['name'],v['id'])))
                else:
                    result_list.append((setting.no_card_preview_image,setting.set_shortcutname(v['name'],v['id'])))
            else:
                result_list.append((setting.no_card_preview_image,setting.set_shortcutname("delete",mid)))                
                
    current_time = datetime.datetime.now()          
    return gr.update(value=result_list), gr.update(minimum=1, value=cur_page, maximum=max_page, step=1, label=f"Total {max_page} Pages"), current_time

def on_classification_gallery_select(evt: gr.SelectData, shortcuts, delete_opt=True):
    if evt.value:               
        shortcut = evt.value 
        sc_model_id = setting.get_modelid_from_shortcutname(shortcut)
        current_time = datetime.datetime.now()
        
        if not shortcuts:
            shortcuts = list()
                
        if delete_opt and sc_model_id in shortcuts:
            shortcuts.remove(sc_model_id)                
            return shortcuts, current_time, None, None
        
        return shortcuts, gr.update(visible=False), gr.update(visible=True), sc_model_id
        
    return shortcuts, gr.update(visible=False), gr.update(visible=True), None   

def on_classification_clear_shortcut_btn_click():
    current_time = datetime.datetime.now()        
    return None, gr.update(value=1, minimum=1, maximum=1, step=1, label=f"Total {1} Pages"), None, current_time

def on_classification_create_btn_click(new_name,new_info,classification_shortcuts):
    current_time = datetime.datetime.now()
    if classification.create_classification(new_name,new_info):     
        classification.update_classification_shortcut(new_name, classification_shortcuts)           
        return gr.update(value=new_name),\
            gr.update(choices=classification.get_list(), value=new_name), current_time, gr.update(label=new_name),\
            gr.update(visible=False), gr.update(visible=True)
    return gr.update(value=""),\
        gr.update(choices=classification.get_list()), current_time, gr.update(visible=True),\
        gr.update(visible=True), gr.update(visible=False)

def on_classification_update_btn_click(select_name, new_name, new_info, classification_shortcuts):
    chg_name = setting.NEWCLASSIFICATION
    
    if select_name:
        # classification.update_classification_shortcut(select_name,new_shortcuts)
        if classification.update_classification(select_name,new_name,new_info):
            classification.update_classification_shortcut(new_name, classification_shortcuts)   
            chg_name = new_name            
        
    current_time = datetime.datetime.now()        
    return gr.update(value=chg_name), gr.update(choices=classification.get_list(), value=chg_name),current_time, gr.update(label=chg_name)

def on_classification_delete_btn_click(select_name):
    if select_name:
        classification.delete_classification(select_name)
        
    current_time = datetime.datetime.now()    
    return gr.update(value=""), gr.update(choices=classification.get_list(), value=""), current_time,gr.update(label=setting.NEWCLASSIFICATION), gr.update(visible=True), gr.update(visible=False)

def on_classification_list_select(evt: gr.SelectData):
    select_name = evt.value
    info = classification.get_classification_info(select_name)
    shortcuts = classification.get_classification_shortcuts(select_name)
    
    current_time = datetime.datetime.now()
    
    return gr.update(value=select_name), gr.update(value=select_name), gr.update(value=info), shortcuts, gr.update(value=1, minimum=1, maximum=1, step=1, label=f"Total {1} Pages"), None, current_time, current_time, gr.update(label=select_name),\
        gr.update(visible=False),gr.update(visible=True)
