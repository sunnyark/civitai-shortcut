import os
import json

from . import util
from . import setting

def get_classifications():    
    RecipeCollection = load()
    classifications = list()
    
    if not RecipeCollection:        
        return classifications
    
    for v in RecipeCollection.values():
        if v['classification']:
            classifications.append(v['classification'])
                
    classifications = list(set(classifications))
        
    return classifications

def is_classifications(classification):    
    RecipeCollection = load()

    if not RecipeCollection:        
        return False
    
    try:
        for v in RecipeCollection.values():
            if v['classification'] == classification:
                return True
    except:
        pass
                
    return False

def update_recipe_shortcuts(recipe, shortcuts:list):
    if not recipe:
        return
    
    RecipeCollection = load()
    RecipeCollection = update_shortcuts(RecipeCollection, recipe, shortcuts)    
    save(RecipeCollection)

    if RecipeCollection:
        if recipe in RecipeCollection:
            return True
        
    return False

def update_recipe_image(recipe, image):
    if not recipe:
        return
    
    RecipeCollection = load()
    RecipeCollection = update_image(RecipeCollection, recipe, image)    
    save(RecipeCollection)

    if RecipeCollection:
        if recipe in RecipeCollection:
            return True
        
    return False  

def delete_recipe(s_name):
    if not s_name:
        return
        
    RecipeCollection = load()
    RecipeCollection = delete(RecipeCollection,s_name)
    save(RecipeCollection)
        
def update_recipe(recipe, name, desc, prompt=None, classification=None):
    if not recipe:
        return

    if not name:
        return

    name = name.strip()
    
    RecipeCollection = load()
    RecipeCollection = update(RecipeCollection, recipe, name, desc, prompt, classification)
    
    save(RecipeCollection)

    if RecipeCollection:
        if name in RecipeCollection:
            return True
        
    return False    

def create_recipe(recipe, desc, prompt=None, classification=None):    
    if recipe and len(recipe.strip()) > 0:
        recipe = recipe.strip()
        RecipeCollection = load()                
        if not RecipeCollection:
            RecipeCollection = dict()
        else:
            if recipe in RecipeCollection:
                return False
                        
        RecipeCollection = create(RecipeCollection, recipe, desc, prompt, classification)
        
        save(RecipeCollection)
            
        if RecipeCollection:
            if recipe in RecipeCollection:
                return True
    return False

def get_recipe(s_name):
    if not s_name:
        return None
    
    RecipeCollection = load()
    if s_name in RecipeCollection:
        return RecipeCollection[s_name]
    
    return None

# def get_list():
    
#     RecipeCollection = load()                           
    
#     tmp_recipe_name = []
#     if RecipeCollection:   
#         tmp_recipe_name = [k for k in RecipeCollection.keys()]
    
#     return tmp_recipe_name

def get_list(key=None):    

    RecipeCollection = load()                           
            
    result = []
    if RecipeCollection:   
        for name, value in RecipeCollection.items():
            if key:
                if value['classification'] and key == value['classification']:
                    result.append(name)
            else:
                result.append(name)

    return result

#================= raw ===================================
def update_shortcuts(RecipeCollection:dict, recipe, shortcuts:list):

    if not RecipeCollection:
        return RecipeCollection
    
    if not recipe:
        return RecipeCollection   
       
    if recipe not in RecipeCollection:
        return RecipeCollection
    
    if not shortcuts:
        return RecipeCollection
        
    RecipeCollection[recipe]['shortcuts'] = shortcuts        
            
    return RecipeCollection

def update_image(RecipeCollection:dict, recipe, image):

    if not RecipeCollection:
        return RecipeCollection
    
    if not recipe:
        return RecipeCollection   
       
    if recipe not in RecipeCollection:
        return RecipeCollection
        
    try:        
        pre_image = RecipeCollection[recipe]['image']
        if image == pre_image:
            return RecipeCollection
        
        recipe_imgfile = os.path.join(setting.shortcut_recipe_folder,pre_image)  
        if os.path.isfile(recipe_imgfile):
            os.remove(recipe_imgfile)
    except:
        pass
    
    RecipeCollection[recipe]['image'] = image        
            
    return RecipeCollection

def update_classification(RecipeCollection:dict, recipe, classification):

    if not RecipeCollection:
        return RecipeCollection
    
    if not recipe:
        return RecipeCollection   
       
    if recipe not in RecipeCollection:
        return RecipeCollection
    
    if classification:
        classification = classification.strip()
        
    RecipeCollection[recipe]['classification'] = classification        
            
    return RecipeCollection

def update_prompt(RecipeCollection:dict, recipe, prompt):

    if not RecipeCollection:
        return RecipeCollection
    
    if not recipe:
        return RecipeCollection   
       
    if recipe not in RecipeCollection:
        return RecipeCollection
        
    RecipeCollection[recipe]['generate'] = prompt        
            
    return RecipeCollection

def delete(RecipeCollection:dict, recipe)->dict:
    if not recipe:
        return RecipeCollection
    
    if not RecipeCollection:
        return RecipeCollection
           
    rc = RecipeCollection.pop(recipe,None)

    try:        
        pre_image = rc['image']
        recipe_imgfile = os.path.join(setting.shortcut_recipe_folder,pre_image)  
        if os.path.isfile(recipe_imgfile):
            os.remove(recipe_imgfile)
    except:
        pass
          
    return RecipeCollection

def create(RecipeCollection:dict, recipe, desc, prompt=None, classification=None):
           
    if not recipe:
        return RecipeCollection   

    if not RecipeCollection:
        RecipeCollection = dict()
           
    recipe = recipe.strip()

    if classification:
        classification = classification.strip()
            
    if len(recipe) > 0:
        if recipe not in RecipeCollection:
            RecipeCollection[recipe] = {
                "description": desc,                 
                "generate": prompt,
                "classification": classification,
                "image": None,
                "shortcuts":[]
            } 
            
    return RecipeCollection

def update(RecipeCollection:dict, recipe, name, desc, prompt=None, classification=None):

    if not RecipeCollection:
        return RecipeCollection
    
    if not recipe:
        return RecipeCollection   
       
    if recipe not in RecipeCollection:
        return RecipeCollection

    if not name:
        return RecipeCollection   
        
    name = name.strip()

    if classification:
        classification = classification.strip()
            
    if recipe == name:
        RecipeCollection[recipe]['description'] = desc
        RecipeCollection[recipe]['generate'] = prompt        
        RecipeCollection[recipe]['classification'] = classification
    else:
        if name not in RecipeCollection:
            sc = RecipeCollection.pop(recipe,None)
            sc = {
                "description": desc,                 
                "generate": prompt,
                "classification": classification
                # "image": None
            }
            RecipeCollection[name] = sc
            
    return RecipeCollection

def save(RecipeCollection:dict):
    output = ""
    
    #write to file    
    try:
        with open(setting.shortcut_recipe, 'w') as f:
            json.dump(RecipeCollection, f, indent=4)
    except Exception as e:
        util.printD("Error when writing file:"+setting.shortcut_recipe)
        return output

    output = "Recipe saved to: " + setting.shortcut_recipe
    #util.printD(output)

    return output

def load()->dict:
    if not os.path.isfile(setting.shortcut_recipe):
        save({})
        return
    
    json_data = None
    try:
        with open(setting.shortcut_recipe, 'r') as f:
            json_data = json.load(f)
    except:
        return None            

    # check error
    if not json_data:
        return None

    # check for new key
    return json_data
#=========================================================================