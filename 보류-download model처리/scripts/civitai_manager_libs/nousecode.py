
# 갤러리 방식으로 숏컬리스트 표시할때
# def on_sc_gallery_select(evt : gr.SelectData):
#     def_id = ""
#     if evt.value:
#         shortcut = evt.value 
#         sc_model_id = shortcut[0:shortcut.find(':')]      
#         sc_model_url = civitai.Url_ModelId() + sc_model_id  

#         model_id, model_name, model_type, model_url, def_id, def_name, def_image, vlist = civitai_action.get_selected_model_info_by_url(sc_model_url)     
        
#         if def_id:
#             return sc_model_url, gr.Dropdown.update(choices=vlist, value=def_name), gr.Textbox.update(value=def_id), gr.Textbox.update(value=sc_model_id)
#     return sc_model_url, gr.Dropdown.update(choices=[setting.NORESULT], value=setting.NORESULT), gr.Textbox.update(value=""), gr.Textbox.update(value=sc_model_id)  

# def on_civitai_internet_url_upload(files, sc_types, sc_owned_types):   
    
#     if files:
#         shortcut = None
#         for file in tqdm(files, desc=f"Civitai Shortcut"):                        
#             shortcut = util.load_InternetShortcut(file.name)            
#             model_id, model_name, model_type, model_url, def_id, def_name, def_image, vlist = internet_shortcut_upload(shortcut)
        
#     if not model_url:
#         return "",gr.Gallery.update(value=ishortcut.get_image_list(sc_types)),gr.Gallery.update(value=ishortcut.get_owned_image_list(sc_owned_types)),gr.Dropdown.update(choices=[setting.NORESULT], value=setting.NORESULT),gr.Textbox.update(value=""),gr.Textbox.update(value="")
    
#     if not def_id:
#         return model_url,gr.Gallery.update(value=ishortcut.get_image_list(sc_types)),gr.Gallery.update(value=ishortcut.get_owned_image_list(sc_owned_types)),gr.Dropdown.update(choices=[setting.NORESULT], value=setting.NORESULT),gr.Textbox.update(value=""),gr.Textbox.update(value="")
#     return model_url,gr.Gallery.update(value=ishortcut.get_image_list(sc_types)),gr.Gallery.update(value=ishortcut.get_owned_image_list(sc_owned_types)),gr.Dropdown.update(choices=vlist, value=def_name),gr.Textbox.update(value=def_id),gr.Textbox.update(value=model_id)

# def internet_shortcut_upload(url):
#     if url:  
#         #util.printD(url)
#         model_id, model_name, model_type, model_url, def_id, def_name, def_image, vlist = civitai_action.get_selected_model_info_by_url(url)
        
#         if model_id:
#             # util.printD(model_id)
#             ISC = ishortcut.load()                           
#             ISC = ishortcut.add(ISC, model_id, model_name, model_type, model_url, def_id, def_image)                        
#             ishortcut.save(ISC)
#     return model_id, model_name, model_type, model_url, def_id, def_name, def_image, vlist
  
# def get_version_description_by_version_id(version_id=None):
#     if not version_id:
#         return "",None,None
#     version_info = civitai.get_version_info_by_version_id(version_id)    
#     return get_version_description_by_version_info(version_info)        

# url에서 model info 정보를 반환한다
# def get_selected_model_info_by_url(url:str):
#     model_id = None
#     model_name = None
#     model_type = None
#     def_id = None
#     def_name = None
#     def_image = None
#     model_url = None
    
#     versions_list = []
#     if url:  
#         model_id = util.get_model_id_from_url(url) 
#         model_info = civitai.get_model_info(model_id)
#         if model_info:
#             model_id = model_info['id']
#             model_name = model_info['name']
#             model_type = model_info['type']
#             model_url = f"{civitai.Url_ModelId()}{model_id}"
            
#             if "modelVersions" in model_info.keys():            
#                 def_version = model_info["modelVersions"][0]
#                 def_id = def_version['id']
#                 def_name = def_version['name']
                
#                 if 'images' in def_version.keys():
#                     if len(def_version["images"]) > 0:
#                         img_dict = def_version["images"][0]
#                         def_image = img_dict["url"]
                                                                
#                 for version_info in model_info['modelVersions']:
#                     versions_list.append(version_info['name'])                        
        
#     return model_id, model_name, model_type, model_url, def_id, def_name, def_image ,[v for v in versions_list]  
  
  
  