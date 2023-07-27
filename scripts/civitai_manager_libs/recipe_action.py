import os
import gradio as gr
import datetime
import modules
import uuid

from . import util
from . import setting
from . import recipe
from . import prompt
# from . import prompt_ui

from PIL import Image
    
def on_ui(recipe_input, civitai_tabs):   

    # data = '''Best quality, masterpiece, ultra high res, (photorealistic:1.4),girl, beautiful_face, detailed skin,upper body, <lora:caise2-000022:0.6>
    # Negative prompt: ng_deepnegative_v1_75t, badhandv4 (worst quality:2), (low quality:2), (normal quality:2), lowres, bad anatomy, bad hands, normal quality, ((monochrome)), ((grayscale)), ng_deepnegative_v1_75t, badhandv4 (worst quality:2), (low quality:2), (normal quality:2), lowres, bad anatomy, bad hands, normal quality, ((monochrome)), ((grayscale)),
    # Steps: 28, Sampler: DPM++ 2M Karras, CFG scale: 11, Seed: 2508416159, Size: 640x384, Model hash: 7af26c6c98, Model: 真人_xsmix_V04很好看, Denoising strength: 0.53, Hires upscale: 2, Hires steps: 20, Hires upscaler: 4x-UltraSharp, Dynamic thresholding enabled: True, Mimic scale: 7, Threshold percentile: 100'''

    # aaa = "D:\\AI\\stable-diffusion-webui\\outputs\\download-images\\【Macross Delta】Freyja Wion Charecter LoRA（芙蕾雅·薇恩人物模組）\\images\\59749-651966.png"
    
    with gr.Column(scale=setting.shortcut_browser_screen_split_ratio):
        with gr.Tabs():
            with gr.TabItem("Prompt Recipe List"):
                recipe_classification_list = gr.Dropdown(label="Prompt Recipe Classification", choices=[setting.PLACEHOLDER] + recipe.get_classifications(), value=setting.PLACEHOLDER, interactive=True, multiselect=False)
                recipe_list = gr.Dropdown(label="Prompt Recipe List", choices=[setting.NEWRECIPE] + recipe.get_list(), value=setting.NEWRECIPE, interactive=True, multiselect=None)
                recipe_drop_image = gr.Image(type="pil", label="Drop image").style(height='100%')                       

    with gr.Column(scale=(setting.shortcut_browser_screen_split_ratio_max-setting.shortcut_browser_screen_split_ratio)):       
        with gr.Accordion(label=setting.NEWRECIPE, open=True) as recipe_title_name: 
            with gr.Row():
                with gr.Column(scale=5):
                    recipe_name = gr.Textbox(label="Name", value="", interactive=True, lines=1, placeholder="Please enter the prompt recipe name.").style(container=True)
                    recipe_desc = gr.Textbox(label="Description", value="",interactive=True, lines=3, placeholder="Please enter the prompt recipe description.").style(container=True, show_copy_button=True)
                    recipe_prompt = gr.Textbox(label="Prompt", placeholder="Prompt", value="", lines=3 ,interactive=True).style(container=True, show_copy_button=True)
                    recipe_negative = gr.Textbox(label="Negative prompt", placeholder="Negative prompt", show_label=False, value="", lines=3 ,interactive=True).style(container=True, show_copy_button=True)
                    recipe_option = gr.Textbox(label="Parameter", placeholder="Parameter", value="", lines=3 ,interactive=True).style(container=True, show_copy_button=True)
                    # with gr.Accordion(label="Parameter", open=True):
                    #     prompt_ui.ui(recipe_option)
                    recipe_output = gr.Textbox(label="Generate Info", interactive=False, lines=6, placeholder="The prompt and parameters are combined and displayed here.").style(container=True, show_copy_button=True)
                    with gr.Row():
                        try:
                            send_to_buttons = modules.generation_parameters_copypaste.create_buttons(["txt2img","img2img", "inpaint", "extras"])
                        except:
                            pass                         
                    recipe_classification = gr.Dropdown(label="Prompt Recipe Classification", choices=[setting.PLACEHOLDER] + recipe.get_classifications(), value=setting.PLACEHOLDER, info="You can choose from a list or enter manually. If you enter a classification that didn't exist before, a new classification will be created." ,interactive=True, allow_custom_value=True)
                    with gr.Row():
                        recipe_create_btn = gr.Button(value="Create", variant="primary")
                        recipe_update_btn = gr.Button(value="Update", variant="primary", visible=False)
                        with gr.Accordion("Delete Prompt Recipe", open=False):
                            recipe_delete_btn = gr.Button(value="Delete", variant="primary")                        
                with gr.Column(scale=2):
                    gr.Markdown("###")
                    recipe_image = gr.Image(type="pil", interactive=True, label="Prompt recipe image").style(height='100%')
                    gr.Markdown("This image does not influence the prompt on the left. You can choose any image that matches the created prompt.")
                    # recipe_image_info = gr.Textbox(label="Ganerate Infomation", lines=6, visible=True)
                
    with gr.Row(visible=False):
        refresh_recipe = gr.Textbox()
        recipe_generate_data = gr.Textbox()
        
    try:
        modules.generation_parameters_copypaste.bind_buttons(send_to_buttons, recipe_image, recipe_output)
    except:
        pass
    
    recipe_prompt.blur(generate_prompt,[recipe_prompt,recipe_negative,recipe_option],recipe_output)
    recipe_negative.blur(generate_prompt,[recipe_prompt,recipe_negative,recipe_option],recipe_output)
    recipe_option.blur(generate_prompt,[recipe_prompt,recipe_negative,recipe_option],recipe_output)
    recipe_classification_list.change(
        fn=on_recipe_classification_list_change,
        inputs=recipe_classification_list,
        outputs=[
            recipe_list
        ]
    )

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
            recipe_generate_data,
            recipe_image,  
        ],
        show_progress=False
    )
    
    # shortcut information 에서 넘어올때는 새로운 레시피를 만든다.
    recipe_input.change(
        fn=on_recipe_input_change,
        inputs=[
            recipe_input
        ],
        outputs=[
            recipe_drop_image,
            recipe_image,
            recipe_generate_data,
            recipe_input,
            civitai_tabs,

            # 새 레시피 상태로 만든다.
            recipe_list,
            recipe_name,
            recipe_desc,
            recipe_classification,
            recipe_title_name,
            recipe_create_btn,
            recipe_update_btn                    
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
        inputs=[
            recipe_classification_list,
            recipe_list
        ],
        outputs=[
            recipe_classification_list,
            recipe_list,
            # recipe_name,
            # recipe_desc,
            # recipe_prompt,
            # recipe_negative,                        
            # recipe_option,
            # recipe_output,
            # recipe_classification,
            # recipe_title_name,
            # recipe_image,
            # recipe_create_btn,
            # recipe_update_btn
        ],
        show_progress=False
    )

    recipe_list.select(    
        fn=on_recipe_list_select,
        inputs=None,
        outputs=[
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
            recipe_update_btn            
        ],
        cancels=recipe_drop_image_upload
    )

    recipe_create_btn.click(
        fn=on_recipe_create_btn_click,
        inputs=[
            recipe_classification_list,
            recipe_name,
            recipe_desc,
            recipe_prompt,
            recipe_negative,
            recipe_option,
            recipe_classification,
            recipe_image
        ],
        outputs=[
            recipe_classification_list,
            recipe_list,
            recipe_classification,
            recipe_title_name,
            recipe_create_btn,
            recipe_update_btn              
        ]
    )
            
    recipe_update_btn.click(
        fn=on_recipe_update_btn_click,
        inputs=[
            recipe_classification_list,
            recipe_list,
            recipe_name,
            recipe_desc,
            recipe_prompt,
            recipe_negative,
            recipe_option,
            recipe_classification,
            recipe_image
        ],
        outputs=[
            recipe_classification_list,
            recipe_list,
            recipe_classification,
            recipe_title_name,          
        ]        
    )

    recipe_delete_btn.click(
        fn=on_recipe_delete_btn_click,
        inputs=[
            recipe_classification_list,
            recipe_list,
        ],
        outputs=[
            recipe_classification_list,
            recipe_list,
            recipe_classification,
            recipe_title_name,
            recipe_create_btn,
            recipe_update_btn
        ]        
    )
        
    return refresh_recipe

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

def on_recipe_input_change(recipe_input):
    if recipe_input:
        current_time = datetime.datetime.now()
        return recipe_input, recipe_input, current_time, None, gr.update(selected="Recipe"),\
            gr.update(value=setting.NEWRECIPE), gr.update(value=""), gr.update(value=""), \
            gr.update(choices=[setting.PLACEHOLDER] + recipe.get_classifications(), value=setting.PLACEHOLDER) ,gr.update(label=setting.NEWRECIPE),\
            gr.update(visible=True), gr.update(visible=False)            
    
    return gr.update(visible=True),gr.update(visible=True),gr.update(visible=False),gr.update(visible=False),gr.update(selected="Recipe"),\
        gr.update(visible=True), gr.update(value=""), gr.update(value=""), \
        gr.update(choices=[setting.PLACEHOLDER] + recipe.get_classifications(), value=setting.PLACEHOLDER), gr.update(label=setting.NEWRECIPE),\
        gr.update(visible=True), gr.update(visible=False)
    
def on_recipe_drop_image_upload(recipe_img):
    if recipe_img:
        current_time = datetime.datetime.now()
        return current_time, recipe_img
    return gr.update(visible=False),gr.update(visible=True)

def on_recipe_generate_data_change(recipe_img):  
    generate_data = None  
    if recipe_img:
        info1,generate_data,info3 = modules.extras.run_pnginfo(recipe_img)
        
    if generate_data:
        
        positivePrompt, negativePrompt, options, gen_string = analyze_prompt(generate_data)
            
        return gr.update(value=positivePrompt), gr.update(value=negativePrompt), gr.update(value=options), gr.update(value=gen_string)            
    return gr.update(value=""), gr.update(value=""), gr.update(value=""), gr.update(value="")
        
def on_recipe_classification_list_change(recipe_classification):
    if recipe_classification and recipe_classification != setting.PLACEHOLDER:
        return gr.update(choices=[setting.NEWRECIPE] + recipe.get_list(recipe_classification))
    return gr.update(choices=[setting.NEWRECIPE] + recipe.get_list())    

def on_refresh_recipe_change(selected_classification, select_name):    
    return gr.update(choices=[setting.PLACEHOLDER] + recipe.get_classifications()), gr.update(choices=[setting.NEWRECIPE] + recipe.get_list(selected_classification) if selected_classification != setting.PLACEHOLDER else recipe.get_list())
        
# def on_refresh_recipe_change(select_classification, select_name):    
#     if select_name != setting.NEWRECIPE:
        
#         description, Prompt, negativePrompt, options, gen_string, classification, imagefile = get_recipe_information(select_name)
#         if not os.path.isfile(imagefile):
#             imagefile = None
                                                    
#         return gr.update(choices=[setting.PLACEHOLDER] + recipe.get_classifications(), value=select_classification), gr.update(choices=[setting.NEWRECIPE] + recipe.get_list(select_classification) if select_classification != setting.PLACEHOLDER else recipe.get_list(), value=select_name),gr.update(value=select_name), gr.update(value=description), gr.update(value=Prompt), gr.update(value=negativePrompt), gr.update(value=options), gr.update(value=gen_string), gr.update(choices=[setting.PLACEHOLDER] + recipe.get_classifications(), value=classification) ,gr.update(label=select_name),imagefile,\
#             gr.update(visible=False), gr.update(visible=True)
#     return gr.update(choices=[setting.PLACEHOLDER] + recipe.get_classifications(), value=select_classification), gr.update(choices=[setting.NEWRECIPE] + recipe.get_list(select_classification) if select_classification != setting.PLACEHOLDER else recipe.get_list(), value=setting.NEWRECIPE), gr.update(value=""), gr.update(value=""), gr.update(value=""), gr.update(value=""), gr.update(value=""), gr.update(value=""), gr.update(choices=[setting.PLACEHOLDER] + recipe.get_classifications(), value=setting.PLACEHOLDER), gr.update(label=setting.NEWRECIPE),None,\
#         gr.update(visible=True), gr.update(visible=False)

def on_recipe_list_select(evt: gr.SelectData):
    if evt.value != setting.NEWRECIPE:
        select_name = evt.value
        
        description, Prompt, negativePrompt, options, gen_string, classification, imagefile = get_recipe_information(select_name)
        
        if imagefile:
            if not os.path.isfile(imagefile):
                imagefile = None
            
        return gr.update(value=select_name),gr.update(value=description), gr.update(value=Prompt), gr.update(value=negativePrompt), gr.update(value=options), gr.update(value=gen_string), gr.update(choices=[setting.PLACEHOLDER] + recipe.get_classifications(), value=classification), gr.update(label=select_name),imagefile,None,\
            gr.update(visible=False), gr.update(visible=True)
    return gr.update(value=""),gr.update(value=""), gr.update(value=""), gr.update(value=""), gr.update(value=""), gr.update(value=""), gr.update(choices=[setting.PLACEHOLDER] + recipe.get_classifications(), value=setting.PLACEHOLDER), gr.update(label=setting.NEWRECIPE), None, None,\
        gr.update(visible=True), gr.update(visible=False)

def on_recipe_create_btn_click(selected_classification, recipe_name, recipe_desc, recipe_prompt, recipe_negative, recipe_option, recipe_classification, recipe_image=None):    
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

            return gr.update(choices=[setting.PLACEHOLDER] + recipe.get_classifications()), gr.update(choices=[setting.NEWRECIPE] + recipe.get_list(selected_classification) if selected_classification != setting.PLACEHOLDER else recipe.get_list(), value=recipe_name),\
                gr.update(choices=[setting.PLACEHOLDER] + recipe.get_classifications(), value=s_classification), gr.update(label=recipe_name),\
                gr.update(visible=False),gr.update(visible=True)
    return gr.update(visible=True), gr.update(visible=True), \
        gr.update(choices=[setting.PLACEHOLDER] + recipe.get_classifications(), value=s_classification), gr.update(label=setting.NEWRECIPE),\
        gr.update(visible=True),gr.update(visible=False)

def on_recipe_update_btn_click(selected_classification, recipe_list, recipe_name ,recipe_desc, recipe_prompt, recipe_negative, recipe_option, recipe_classification, recipe_image=None):    
    
    chg_name = setting.NEWRECIPE
    s_classification = setting.PLACEHOLDER
    
    if recipe_list and recipe_list != setting.NEWRECIPE and recipe_name and recipe_name != setting.NEWRECIPE:
        
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
        
        if recipe.update_recipe(recipe_list, recipe_name, recipe_desc, pmt, recipe_classification):        
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

        if not recipe.is_classifications(selected_classification):
            selected_classification = setting.PLACEHOLDER
                                                            
    return gr.update(choices=[setting.PLACEHOLDER] + recipe.get_classifications(), value=selected_classification), gr.update(choices=[setting.NEWRECIPE] + recipe.get_list(selected_classification) if selected_classification != setting.PLACEHOLDER else recipe.get_list(), value=chg_name), \
        gr.update(choices=[setting.PLACEHOLDER] + recipe.get_classifications(), value=s_classification), gr.update(label=chg_name)

def on_recipe_delete_btn_click(selected_classification, select_name):
    if select_name and select_name.strip() != setting.NEWRECIPE:
        recipe.delete_recipe(select_name)
        
        if not recipe.is_classifications(selected_classification):
            selected_classification = setting.PLACEHOLDER
        
    return gr.update(choices=[setting.PLACEHOLDER] + recipe.get_classifications(), value=selected_classification), gr.update(choices=[setting.NEWRECIPE] + recipe.get_list(selected_classification) if selected_classification != setting.PLACEHOLDER else recipe.get_list(), value=setting.NEWRECIPE), \
        gr.update(choices=[setting.PLACEHOLDER] + recipe.get_classifications(), value=setting.PLACEHOLDER), gr.update(label=setting.NEWRECIPE),\
        gr.update(visible=True),gr.update(visible=False)
        
    
        
            
                