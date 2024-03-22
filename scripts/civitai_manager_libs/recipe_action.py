import os
import gradio as gr
import datetime
import uuid
import re

import modules
import modules.infotext_utils as parameters_copypaste

from . import util
from . import setting
from . import recipe
from . import prompt
# from . import prompt_ui
from . import sc_browser_page
from . import ishortcut
from . import recipe_browser_page

from PIL import Image
                
def on_ui(recipe_input, shortcut_input, civitai_tabs):   

    # data = '''Best quality, masterpiece, ultra high res, (photorealistic:1.4),girl, beautiful_face, detailed skin,upper body, <lora:caise2-000022:0.6>
    # Negative prompt: ng_deepnegative_v1_75t, badhandv4 (worst quality:2), (low quality:2), (normal quality:2), lowres, bad anatomy, bad hands, normal quality, ((monochrome)), ((grayscale)), ng_deepnegative_v1_75t, badhandv4 (worst quality:2), (low quality:2), (normal quality:2), lowres, bad anatomy, bad hands, normal quality, ((monochrome)), ((grayscale)),
    # Steps: 28, Sampler: DPM++ 2M Karras, CFG scale: 11, Seed: 2508416159, Size: 640x384, Model hash: 7af26c6c98, Model: 真人_xsmix_V04很好看, Denoising strength: 0.53, Hires upscale: 2, Hires steps: 20, Hires upscaler: 4x-UltraSharp, Dynamic thresholding enabled: True, Mimic scale: 7, Threshold percentile: 100'''

    # aaa = "D:\\AI\\stable-diffusion-webui\\outputs\\download-images\\【Macross Delta】Freyja Wion Charecter LoRA（芙蕾雅·薇恩人物模組）\\images\\59749-651966.png"
    
    with gr.Column(scale=setting.shortcut_browser_screen_split_ratio):
        with gr.Tabs():
            with gr.TabItem("Prompt Recipe List"):
                recipe_new_btn = gr.Button(value="New Recipe", variant="primary")
                recipe_gallery, refresh_recipe_browser = recipe_browser_page.on_ui()
            with gr.TabItem("Generate Prompt From Image"):
                recipe_drop_image = gr.Image(type="pil", label="Drop image", height='100%')

    with gr.Column(scale=(setting.shortcut_browser_screen_split_ratio_max-setting.shortcut_browser_screen_split_ratio)):       
        with gr.Accordion(label=setting.NEWRECIPE, open=True) as recipe_title_name: 
            with gr.Row():
                with gr.Column(scale=4):
                    with gr.Tabs() as recipe_prompt_tabs:
                        with gr.TabItem("Prompt", id="Prompt"):                    
                            recipe_name = gr.Textbox(label="Name", value="", interactive=True, lines=1, placeholder="Please enter the prompt recipe name.", container=True)
                            recipe_desc = gr.Textbox(label="Description", value="",interactive=True, lines=3, placeholder="Please enter the prompt recipe description.", container=True, show_copy_button=True)
                            recipe_prompt = gr.Textbox(label="Prompt", placeholder="Prompt", value="", lines=3 ,interactive=True, container=True, show_copy_button=True)
                            recipe_negative = gr.Textbox(label="Negative prompt", placeholder="Negative prompt", show_label=False, value="", lines=3 ,interactive=True ,container=True, show_copy_button=True)
                            recipe_option = gr.Textbox(label="Parameter", placeholder="Parameter", value="", lines=3 ,interactive=True, container=True, show_copy_button=True)
                            # with gr.Accordion(label="Parameter", open=True):
                            #     prompt_ui.ui(recipe_option)
                            # recipe_output = gr.Textbox(label="Generate Info", interactive=False, lines=6, placeholder="The prompt and parameters are combined and displayed here.", container=True, show_copy_button=True)
                            with gr.Row():
                                try:
                                    send_to_buttons = parameters_copypaste.create_buttons(["txt2img","img2img", "inpaint", "extras"])
                                except:
                                    pass                         
                            recipe_classification = gr.Dropdown(label="Prompt Recipe Classification", choices=[setting.PLACEHOLDER] + recipe.get_classifications(), value=setting.PLACEHOLDER, info="You can choose from a list or enter manually. If you enter a classification that didn't exist before, a new classification will be created." ,interactive=True, allow_custom_value=True)
                        with gr.TabItem("Additional Shortcut Models for Reference"):                    
                            reference_sc_gallery, refresh_reference_sc_browser, refresh_reference_sc_gallery = sc_browser_page.on_ui(False,"DOWN",setting.prompt_reference_shortcut_column,setting.prompt_reference_shortcut_rows_per_page)
                    with gr.Row():
                        recipe_create_btn = gr.Button(value="Create", variant="primary")
                        recipe_update_btn = gr.Button(value="Update", variant="primary", visible=False)
                        with gr.Accordion("Delete Prompt Recipe", open=False):
                            recipe_delete_btn = gr.Button(value="Delete", variant="primary")                        

                with gr.Column(scale=2):                    
                    gr.Markdown("###")
                    with gr.Tabs() as recipe_reference_tabs:
                        with gr.TabItem("Reference Image", id="reference_image"):
                            recipe_image = gr.Image(type="pil", interactive=True, label="Prompt recipe image", height='100%')
                            gr.Markdown("This image does not influence the prompt on the left. You can choose any image that matches the created prompt.")
                            # recipe_image_info = gr.Textbox(label="Ganerate Infomation", lines=6, visible=True)
                        with gr.TabItem("Reference Models", id="reference_model"):
                            reference_delete = gr.Checkbox(label="Delete from references when selecting a thumbnail.", value=False)

                            with gr.Accordion("#", open=True, visible=False) as reference_model_information:        
                                reference_modelid = gr.Textbox(visible=False)
                                reference_modeltype = gr.Textbox(visible=False)
                                reference_disp_modeltype = gr.Textbox(label="Model Type", interactive=False, lines=1)
                                reference_versions = gr.Dropdown(label="Model Version",interactive=True)
                                reference_filenames = gr.Dropdown(label="Version filename", interactive=True)
                                reference_weight_slider = gr.Slider(minimum=0, maximum=2, value=0.7, step=0.1, label="Preferred weight", interactive=True, visible=True)
                                reference_triger = gr.Textbox(label="Triger", interactive=True, lines=1)
                                insert_prompt_btn = gr.Button(value="Add\\Remove from Prompt", variant="primary")        
                                with gr.Row():
                                    goto_model_info_btn = gr.Button(value="Information", variant="primary") 
                                    delete_reference_model_btn = gr.Button(value="Delete", variant="primary")
                                close_reference_model_information_btn = gr.Button(value="Close", variant="primary")
                                
                            reference_gallery = gr.Gallery(show_label=False, columns=3, height='auto', object_fit=setting.gallery_thumbnail_image_style, preview=False, allow_preview=False)
                            # with gr.Accordion("Add Reference Shortcut Items", open=False):
                            #     reference_sc_gallery, refresh_reference_sc_browser, refresh_reference_sc_gallery = sc_browser_page.on_ui()
                        with gr.TabItem("Generate Information", id="generation_info"):
                            recipe_output = gr.Textbox(label="Generate Information", interactive=False, lines=20, placeholder="The prompt and parameters are combined and displayed here.", container=True, show_copy_button=True)
                
    with gr.Row(visible=False):
        selected_recipe_name = gr.Textbox()
        
        refresh_recipe = gr.Textbox()
        recipe_generate_data = gr.Textbox()        
        
        reference_shortcuts = gr.State()
        refresh_reference_gallery = gr.Textbox()
    try:
        parameters_copypaste.bind_buttons(send_to_buttons, recipe_image, recipe_output)
    except:
        pass

    recipe_prompt_tabs.select(on_recipe_prompt_tabs_select,None,[recipe_reference_tabs])
                    
    # reference shortcuts
    reference_gallery.select(
        fn=on_reference_gallery_select,
        inputs=[
            reference_shortcuts,
            reference_delete
        ],
        outputs=[
            reference_shortcuts,
            refresh_reference_gallery,
            reference_gallery, # 이거는 None으로 할 필요는 gallery를 미선택으로 만드는 방법을 몰라서 일단 이렇게 해보자
            reference_modelid
            # shortcut_input
        ],
        show_progress=False
    )   
    
    refresh_reference_gallery.change(
        fn=on_reference_gallery_loading,
        inputs=[
            reference_shortcuts,
        ],
        outputs=[
            reference_gallery
        ],
        show_progress=False
    )
        
    reference_sc_gallery.select(
        fn=on_reference_sc_gallery_select,
        inputs=[
            reference_shortcuts
        ],
        outputs=[
            reference_shortcuts,            
            refresh_reference_gallery,
        ],
        show_progress=False        
    )        
    # reference shortcuts
    
    recipe_prompt.blur(generate_prompt,[recipe_prompt,recipe_negative,recipe_option],recipe_output)
    recipe_negative.blur(generate_prompt,[recipe_prompt,recipe_negative,recipe_option],recipe_output)
    recipe_option.blur(generate_prompt,[recipe_prompt,recipe_negative,recipe_option],recipe_output)
    
    # 이렇게 합시다.
    # send to reciepe -> recipe_input : input drop image, reciep image, call recipe_generate_data(drop image) -> recipe_generate_data: img info 생성 ,분석, 갱신
    # drop image -> recipe_drop_image.upload(drop image) : reciep image, call recipe_generate_data(drop image) -> recipe_generate_data: img info 생성 ,분석, 갱신
    # drop image.upload 만쓰이고 change는 안쓰임
    
    # 이미지를 드롭할때는 현재 레시피 상태에서 정보만 갱신한다.
    recipe_drop_image_upload = recipe_drop_image.upload(
        fn=on_recipe_drop_image_upload,
        inputs=[
            recipe_drop_image
        ],
        outputs=[
            recipe_image,  
            recipe_generate_data,            
        ],
        show_progress=False
    )
    
    # shortcut information 에서 넘어올때는 새로운 레시피를 만든다.
    recipe_input.change(
        fn=on_recipe_input_change,
        inputs=[
            recipe_input,
            reference_shortcuts
        ],
        outputs=[
            selected_recipe_name,
            
            recipe_drop_image,
            recipe_image,
            recipe_generate_data,
            recipe_input,
            civitai_tabs,
            recipe_prompt_tabs,
            recipe_reference_tabs,
            

            # 새 레시피 상태로 만든다.
            recipe_name,
            recipe_desc,
            recipe_classification,
            recipe_title_name,
            recipe_create_btn,
            recipe_update_btn,
            reference_shortcuts,
            reference_modelid,
            reference_gallery,            
            refresh_reference_gallery            
        ],
        cancels=recipe_drop_image_upload
    )  

    recipe_generate_data.change(
        fn=on_recipe_generate_data_change,
        inputs=[
            recipe_drop_image
        ],
        outputs=[
            recipe_prompt,
            recipe_negative,                        
            recipe_option,
            recipe_output,
        ]
    ) 
              
    refresh_recipe.change(
        fn=on_refresh_recipe_change,
        inputs=None,
        outputs=[
            refresh_reference_sc_browser,
            refresh_recipe_browser,
            refresh_reference_gallery
        ],
        show_progress=False
    )

    recipe_gallery.select(
        fn=on_recipe_gallery_select,
        inputs=None,
        outputs=[
            selected_recipe_name,
            recipe_name,
            recipe_desc,
            recipe_prompt,
            recipe_negative,
            recipe_option,            
            recipe_output,
            recipe_classification,
            recipe_title_name,
            recipe_image,
            recipe_drop_image,
            recipe_create_btn,
            recipe_update_btn,
            reference_shortcuts,   
            reference_modelid,
            reference_gallery,            
            refresh_reference_gallery                             
        ],
        cancels=recipe_drop_image_upload
    )  
    
    recipe_new_btn.click(
        fn=on_recipe_new_btn_click,
        inputs=None,
        outputs=[
            selected_recipe_name,
            recipe_name,
            recipe_desc,
            recipe_prompt,
            recipe_negative,
            recipe_option,            
            recipe_output,
            recipe_classification,
            recipe_title_name,
            recipe_image,
            recipe_drop_image,
            recipe_create_btn,
            recipe_update_btn,
            reference_shortcuts,
            reference_modelid,
            refresh_reference_gallery          
        ]
    )
        
    recipe_create_btn.click(
        fn=on_recipe_create_btn_click,
        inputs=[
            recipe_name,
            recipe_desc,
            recipe_prompt,
            recipe_negative,
            recipe_option,
            recipe_classification,
            recipe_image,
            reference_shortcuts
        ],
        outputs=[
            selected_recipe_name,            
            recipe_classification,
            recipe_title_name,
            recipe_create_btn,
            recipe_update_btn,
            refresh_recipe_browser            
        ]
    )
            
    recipe_update_btn.click(
        fn=on_recipe_update_btn_click,
        inputs=[
            selected_recipe_name,
            recipe_name,
            recipe_desc,
            recipe_prompt,
            recipe_negative,
            recipe_option,
            recipe_classification,
            recipe_image,
            reference_shortcuts
        ],
        outputs=[
            selected_recipe_name,
            recipe_classification,
            recipe_title_name,
            refresh_recipe_browser                      
        ]        
    )

    recipe_delete_btn.click(
        fn=on_recipe_delete_btn_click,
        inputs=[
            selected_recipe_name            
        ],
        outputs=[            
            selected_recipe_name,
            recipe_classification,
            recipe_title_name,
            recipe_create_btn,
            recipe_update_btn,
            refresh_recipe_browser            
        ]        
    )

    reference_modelid.change(
        fn=on_reference_modelid_change,
        inputs=[
            reference_modelid,
        ],
        outputs=[            
            reference_modeltype,
            reference_disp_modeltype,
            reference_versions,                    
            reference_filenames,
            reference_triger,
            reference_weight_slider,
            insert_prompt_btn,
            reference_model_information
        ],
        show_progress=False
    )
    
    reference_versions.select(
        fn=on_reference_versions_select,
        inputs=[
            reference_modelid,
        ],
        outputs=[
            reference_modeltype,
            reference_disp_modeltype,
            reference_versions,                    
            reference_filenames,
            reference_triger,
            reference_weight_slider,
            insert_prompt_btn,
            reference_model_information
        ],
        show_progress=False
    )

    goto_model_info_btn.click(lambda x:x,reference_modelid,shortcut_input)
    
    delete_reference_model_btn.click(
        fn=on_delete_reference_model_btn_click,
        inputs=[
            reference_modelid,
            reference_shortcuts,
        ],
        outputs=[
            reference_shortcuts,
            refresh_reference_gallery,
            reference_gallery,
            reference_modelid
        ],
        show_progress=False
    )  

    insert_prompt_btn.click(
        fn=on_insert_prompt_btn_click,
        inputs=[
            reference_modeltype,
            recipe_prompt,
            recipe_negative,
            recipe_option,
            reference_filenames,            
            reference_weight_slider,
            reference_triger
        ],
        outputs=[
            recipe_prompt,
            recipe_output
        ]        
    )
    
    # close_reference_model_information_btn.click(lambda :gr.update(visible=False),None,reference_model_information)

    close_reference_model_information_btn.click(
        fn=on_close_reference_model_information_btn_click,
        inputs=[
            reference_shortcuts,
        ],
        outputs=[
            reference_shortcuts,
            refresh_reference_gallery,
            reference_gallery,
            reference_modelid
        ],
        show_progress=False
    )  

    return refresh_recipe

def load_model_information(modelid=None, ver_index=None):
    if modelid:
        model_info,version_info,versionid,version_name,model_type,model_basemodels,versions_list, dhtml, triger, files = ishortcut.get_model_information(modelid,None,ver_index)
        if model_info:                        
            insert_btn_visible=False
            weight_visible=False
            triger_visible=False
            if model_type == 'LORA' or  model_type == 'LoCon' or model_type == 'Hypernetwork':
                insert_btn_visible=True
                weight_visible=True
                triger_visible=True
            elif model_type == 'TextualInversion':
                insert_btn_visible=True
                
            flist = list()
            for file in files:            
                flist.append(file['name'])
                
            file_name = ''
            if len(flist) > 0:
                file_name = flist[0]
                            
            title_name = f"# {model_info['name']} : {version_name}"
            
            return gr.update(value=model_type),gr.update(value=setting.get_ui_typename(model_type)), gr.update(choices=versions_list,value=version_name), gr.update(choices=flist,value=file_name), gr.update(value=triger,visible=triger_visible), \
                gr.update(visible=weight_visible), gr.update(visible=insert_btn_visible), gr.update(label=title_name,visible=True)
    return None, None, None, None, gr.update(value=None,visible=True),\
        gr.update(visible=True), gr.update(visible=True), gr.update(label="#",visible=False)
        
def on_reference_modelid_change(modelid=None):    
    return load_model_information(modelid, None)

def on_reference_versions_select(evt: gr.SelectData, modelid:str):
    return load_model_information(modelid, evt.index)    

def on_delete_reference_model_btn_click(sc_model_id:str, shortcuts):
    if sc_model_id:                       
        current_time = datetime.datetime.now()
            
        if not shortcuts:
            shortcuts = list()
        
        if sc_model_id in shortcuts:
            shortcuts.remove(sc_model_id)                
            return shortcuts, current_time, None, None
        
    return shortcuts, gr.update(visible=False), gr.update(visible=True), gr.update(visible=False)

def on_close_reference_model_information_btn_click(shortcuts):
    current_time = datetime.datetime.now()    
    return shortcuts, current_time, None, None

def add_string(text, mtype, filename, weight, triger=None):
    pattern = f"<{mtype}:{filename}:{weight}>"
    if triger:
        pattern = pattern + ' ' + triger
        
    return text.strip() + ' ' + pattern

def remove_strings(text, mtype, filename, triger=None):
    # Use regular expression to find and remove all <lora:filename:number> strings
    pattern = f"<{mtype}:{re.escape(filename)}:.*?>"
    if triger:
        pattern = pattern + ' ' + triger    
    text = re.sub(pattern,'', text)
    return text

def is_string(text,mtype, filename, triger=None):
    pattern = f"<{mtype}:{re.escape(filename)}:.*?>"
    if triger:
        pattern = pattern + ' ' + triger    
    return re.search(pattern,text)

def on_insert_prompt_btn_click(model_type, recipe_prompt, recipe_negative, recipe_option, filename, weight, triger):

    if model_type == 'LORA' or  model_type == 'LoCon':
        mtype = 'lora'
    elif model_type == 'Hypernetwork':
        mtype = 'hypernet'
    elif model_type == 'TextualInversion':
        mtype = 'ti'
    
    if filename:
        filename , ext = os.path.splitext(filename)
        
    if mtype == 'lora' or mtype == 'hypernet':                    
        if is_string(recipe_prompt, mtype, filename, triger):
            recipe_prompt = remove_strings(recipe_prompt, mtype, filename, triger)
        else:
            recipe_prompt = remove_strings(recipe_prompt, mtype, filename)
            recipe_prompt = add_string(recipe_prompt, mtype, filename, weight, triger)
    elif mtype == 'ti':
        if filename in recipe_prompt:
            recipe_prompt = recipe_prompt.replace(filename,'')
        else:
            recipe_prompt = recipe_prompt.replace(filename,'')
            recipe_prompt = recipe_prompt + ' ' + filename

    return gr.update(value=recipe_prompt), gr.update(value=generate_prompt(recipe_prompt, recipe_negative, recipe_option))

def on_recipe_prompt_tabs_select(evt: gr.SelectData):
    if evt.index == 1:      
        return gr.update(selected="reference_model")
    return gr.update(selected=None)

def analyze_prompt(generate_data):    
    positivePrompt = None
    negativePrompt = None
    options = None
    gen_string = None
        
    if generate_data:
        generate = None
        try:
            generate = prompt.parse_data(generate_data)
        except:
            pass
        
        if generate:
            if "options" in generate:
                options = [f"{k}:{v}" for k, v in generate['options'].items()]
                if options:
                    options = ", ".join(options)
        
            if 'prompt' in generate:
                positivePrompt = generate['prompt']

            if 'negativePrompt' in generate:
                negativePrompt = generate['negativePrompt']
            
        gen_string = generate_prompt(positivePrompt,negativePrompt,options)
        
    return positivePrompt, negativePrompt, options, gen_string
        
def generate_prompt(prompt, negativePrompt, Options):
    meta_string = None
    if prompt and len(prompt.strip()) > 0:
        meta_string = f"""{prompt.strip()}""" + "\n"
        
    if negativePrompt and len(negativePrompt.strip()) > 0:
        if meta_string:
            meta_string = meta_string + f"""Negative prompt:{negativePrompt.strip()}""" + "\n"    
        else:
            meta_string = f"""Negative prompt:{negativePrompt.strip()}""" + "\n"    

    if Options and len(Options.strip()) > 0:
        if meta_string:
            meta_string = meta_string + Options.strip()
        else:
            meta_string = Options.strip()
        
    return meta_string

def get_recipe_information(select_name):
    
    generate = None
    options = None
    classification = None
    gen_string = None
    Prompt = None
    negativePrompt = None
    description = None
    imagefile = None
    
    if select_name:
        rc = recipe.get_recipe(select_name)
            
        if "generate" in rc:
            generate = rc['generate']
            if "options" in generate:
                options = [f"{k}:{v}" for k, v in generate['options'].items()]
                if options:
                    options = ", ".join(options)
            
            if "prompt" in generate:
                Prompt = generate['prompt']
                
            if "negativePrompt" in generate:
                negativePrompt = generate['negativePrompt']
                                
            gen_string = generate_prompt(Prompt, negativePrompt, options)

        if "image" in rc:
            if rc['image']:
                imagefile = os.path.join(setting.shortcut_recipe_folder,rc['image'])  
            
        if "description" in rc:
            description = rc['description'] 
            
        if "classification" in rc:
            classification = rc['classification']
            if not classification or len(classification.strip()) == 0:
                classification = setting.PLACEHOLDER      
                                                        
    return description, Prompt, negativePrompt, options, gen_string, classification, imagefile

def on_recipe_input_change(recipe_input, shortcuts):    
    current_time = datetime.datetime.now()
    if recipe_input:        
        shortcuts = None
        recipe_image = None
        # recipe_input의 넘어오는 데이터 형식을 [shortcut_id:파일네임] 으로 하면 
        # reference_shortcuts 에 shortcut id를 넣어줄수 있다.
        try:
            shortcutid, recipe_image = setting.get_imagefn_and_shortcutid_from_recipe_image(recipe_input)
            if shortcutid:
                shortcuts = list()
                shortcuts.append(shortcutid)            
        except:
            pass
        
        return gr.update(value=""), recipe_image, recipe_image, current_time, None, \
            gr.update(selected="Recipe"),gr.update(selected="Prompt"),gr.update(selected="reference_image"),\
            gr.update(value=""), gr.update(value=""), \
            gr.update(choices=[setting.PLACEHOLDER] + recipe.get_classifications(), value=setting.PLACEHOLDER) ,gr.update(label=setting.NEWRECIPE),\
            gr.update(visible=True), gr.update(visible=False),\
            shortcuts, None, None, current_time            
    
    return gr.update(visible=False),gr.update(visible=True),gr.update(visible=True),gr.update(visible=False),gr.update(visible=False),\
        gr.update(selected="Recipe"),gr.update(selected="Prompt"),gr.update(selected="reference_image"),\
        gr.update(value=""), gr.update(value=""), \
        gr.update(choices=[setting.PLACEHOLDER] + recipe.get_classifications(), value=setting.PLACEHOLDER), gr.update(label=setting.NEWRECIPE),\
        gr.update(visible=True), gr.update(visible=False),\
        shortcuts,None, None, gr.update(visible=False)
            
def on_recipe_drop_image_upload(recipe_img):
    if recipe_img:
        current_time = datetime.datetime.now()
        return recipe_img, current_time
    return gr.update(visible=True),gr.update(visible=False)

def on_recipe_generate_data_change(recipe_img):  
    generate_data = None  
    if recipe_img:
        info1,generate_data,info3 = modules.extras.run_pnginfo(recipe_img)
        
    if generate_data:
        
        positivePrompt, negativePrompt, options, gen_string = analyze_prompt(generate_data)
            
        return gr.update(value=positivePrompt), gr.update(value=negativePrompt), gr.update(value=options), gr.update(value=gen_string)            
    return gr.update(value=""), gr.update(value=""), gr.update(value=""), gr.update(value="")
        
def on_refresh_recipe_change():    
    current_time = datetime.datetime.now()
    return current_time, current_time, current_time

def on_recipe_gallery_select(evt: gr.SelectData):
    current_time = datetime.datetime.now()
    select_name = evt.value
    
    description, Prompt, negativePrompt, options, gen_string, classification, imagefile = get_recipe_information(select_name)
    
    if imagefile:
        if not os.path.isfile(imagefile):
            imagefile = None
    
    shortcuts = recipe.get_recipe_shortcuts(select_name)                 
    
    return gr.update(value=select_name),gr.update(value=select_name),gr.update(value=description), gr.update(value=Prompt), gr.update(value=negativePrompt), gr.update(value=options), gr.update(value=gen_string), gr.update(choices=[setting.PLACEHOLDER] + recipe.get_classifications(), value=classification), gr.update(label=select_name),imagefile,None,\
        gr.update(visible=False), gr.update(visible=True),\
        shortcuts, None, None, current_time
                
def on_recipe_new_btn_click():
    current_time = datetime.datetime.now()
    return gr.update(value=""),gr.update(value=""),gr.update(value=""), gr.update(value=""), gr.update(value=""), gr.update(value=""), gr.update(value=""), gr.update(choices=[setting.PLACEHOLDER] + recipe.get_classifications(), value=setting.PLACEHOLDER), gr.update(label=setting.NEWRECIPE), None, None,\
        gr.update(visible=True), gr.update(visible=False),\
        None, None, current_time
        
def on_recipe_create_btn_click(recipe_name, recipe_desc, recipe_prompt, recipe_negative, recipe_option, recipe_classification, recipe_image=None, recipe_shortcuts=None):  
    current_time = datetime.datetime.now()  
    s_classification = setting.PLACEHOLDER
    if recipe_name and len(recipe_name.strip()) > 0 and recipe_name != setting.NEWRECIPE:
        pmt = dict()
        pmt['prompt'] = recipe_prompt
        pmt['negativePrompt'] = recipe_negative
        
        options = prompt.parse_option_data(recipe_option)
        if options:
            pmt['options'] = options
        
        if recipe_classification:
            if recipe_classification == setting.PLACEHOLDER:
                recipe_classification = ""  
                recipe_classification = recipe_classification.strip()              
            else:
                recipe_classification = recipe_classification.strip()
                s_classification = recipe_classification
            
        if recipe.create_recipe(recipe_name, recipe_desc, pmt, recipe_classification):  
            if recipe_image:          
                if not os.path.exists(setting.shortcut_recipe_folder):
                    os.makedirs(setting.shortcut_recipe_folder)
                unique_filename = f"{str(uuid.uuid4())}{setting.preview_image_ext}"
                recipe_imgfile = os.path.join(setting.shortcut_recipe_folder,unique_filename)                      
                recipe_image.save(recipe_imgfile)
                recipe.update_recipe_image(recipe_name,unique_filename)
                recipe.update_recipe_shortcuts(recipe_name, recipe_shortcuts)
                
            return gr.update(value=recipe_name),\
                gr.update(choices=[setting.PLACEHOLDER] + recipe.get_classifications(), value=s_classification), gr.update(label=recipe_name),\
                gr.update(visible=False),gr.update(visible=True),\
                current_time
    return gr.update(value=""),\
        gr.update(choices=[setting.PLACEHOLDER] + recipe.get_classifications(), value=s_classification), gr.update(label=setting.NEWRECIPE),\
        gr.update(visible=True),gr.update(visible=False),\
        gr.update(visible=False)

def on_recipe_update_btn_click(select_name, recipe_name ,recipe_desc, recipe_prompt, recipe_negative, recipe_option, recipe_classification, recipe_image=None, recipe_shortcuts=None):    
    
    chg_name = setting.NEWRECIPE
    s_classification = setting.PLACEHOLDER
    
    if select_name and select_name != setting.NEWRECIPE and recipe_name and recipe_name != setting.NEWRECIPE:
        
        pmt = dict()
        pmt['prompt'] = recipe_prompt
        pmt['negativePrompt'] = recipe_negative
        
        options = prompt.parse_option_data(recipe_option)
        if options:
            pmt['options'] = options
        
        if recipe_classification:
            if recipe_classification == setting.PLACEHOLDER:
                recipe_classification = ""
                recipe_classification = recipe_classification.strip()                
            else:
                recipe_classification = recipe_classification.strip()
                s_classification = recipe_classification
        
        if recipe.update_recipe(select_name, recipe_name, recipe_desc, pmt, recipe_classification):        
            chg_name = recipe_name     
            if recipe_image:
                if not os.path.exists(setting.shortcut_recipe_folder):
                    os.makedirs(setting.shortcut_recipe_folder)
                unique_filename = f"{str(uuid.uuid4())}{setting.preview_image_ext}"
                recipe_imgfile = os.path.join(setting.shortcut_recipe_folder,unique_filename)                      
                recipe_image.save(recipe_imgfile)
                recipe.update_recipe_image(recipe_name,unique_filename)
            else:
                recipe.update_recipe_image(recipe_name,None)

            recipe.update_recipe_shortcuts(recipe_name, recipe_shortcuts)
                   
    current_time = datetime.datetime.now()                                   
    return gr.update(value=chg_name), gr.update(choices=[setting.PLACEHOLDER] + recipe.get_classifications(), value=s_classification), gr.update(label=chg_name), current_time

def on_recipe_delete_btn_click(select_name):
    if select_name:
        recipe.delete_recipe(select_name)
           
    current_time = datetime.datetime.now()                                   
    return gr.update(value=""),\
        gr.update(choices=[setting.PLACEHOLDER] + recipe.get_classifications(), value=setting.PLACEHOLDER), gr.update(label=setting.NEWRECIPE),\
        gr.update(visible=True),gr.update(visible=False),\
        current_time
           
# reference shortcuts
def on_reference_gallery_loading(shortcuts):
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
                    if 'nsfw' in v.keys() and bool(v['nsfw']) and setting.NSFW_filtering_enable:
                        result_list.append((setting.nsfw_disable_image,setting.set_shortcutname(v['name'],v['id'])))
                    else:                    
                        result_list.append((os.path.join(setting.shortcut_thumbnail_folder,f"{v['id']}{setting.preview_image_ext}"),setting.set_shortcutname(v['name'],v['id'])))
                else:
                    result_list.append((setting.no_card_preview_image,setting.set_shortcutname(v['name'],v['id'])))
            else:
                result_list.append((setting.no_card_preview_image,setting.set_shortcutname("delete",mid)))                
                
    return gr.update(value=result_list)

def on_reference_sc_gallery_select(evt: gr.SelectData, shortcuts):
    current_time = datetime.datetime.now()
            
    if evt.value:               
        shortcut = evt.value 
        sc_model_id = setting.get_modelid_from_shortcutname(shortcut)            
        
        if not shortcuts:
            shortcuts = list()
            
        if sc_model_id not in shortcuts:
            shortcuts.append(sc_model_id)

        return shortcuts, current_time
    return shortcuts, gr.update(visible=False)

def on_reference_gallery_select(evt: gr.SelectData, shortcuts, delete_opt=True):
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

