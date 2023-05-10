import os
import json
import gradio as gr
import datetime
import modules

from . import util
from . import model
from . import civitai
from . import setting

def on_ui():
            
    with gr.Column(scale=1):
        downloaded_information = gr.DataFrame(
            headers=["", "version ID", "version Name","Location"],
            datatype=["str", "number", "str","str"], 
            col_count=(4,"fixed"),
        )
        pass        
                
    with gr.Row(visible=False): 
        selected_model_id = gr.Textbox()        
        refresh_information = gr.Textbox()
        
    selected_model_id.change(
        fn=on_load_model,
        inputs=[
            selected_model_id,
        ],
        outputs=None
    )
    
    refresh_information.change(
        fn=on_load_model,
        inputs=[
            selected_model_id,
        ],
        outputs=None
    )
    
    # refresh_btn.click(lambda :datetime.datetime.now(),None,refresh_information)
    
    return selected_model_id, refresh_information

def on_load_model(modelid=None):
    pass
        
