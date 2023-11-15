# Personal reasons make it difficult for further updates. Feel free to use the source without any restrictions. I sincerely apologize.

# This update is compatible with gradio version 3.41.2 or higher. It requires the latest update of A1111 to function correctly.

# Civitai Shortcut

Stable Diffusion Webui Extension for Civitai, to download civitai shortcut and models.

# Install

Stable Diffusion Webui's Extension tab, go to Install from url sub-tab. Copy this project's url into it, click install.

    git clone https://github.com/sunnyark/civitai-shortcut

# Usage instructions

![screenshot 2023-09-15 203613](https://github.com/sunnyark/civitai-shortcut/assets/40237431/fdac59c0-0ced-41fb-8faa-83029b3ffc3f)

* Upload : This function creates a shortcut that can be used by the extension when you enter the Civitai site's model URL. It only works when the site is functioning properly. You can either click and drag the URL from the address bar or drag and drop saved internet shortcuts. You can also select multiple internet shortcuts and drop them at once.
* Model Browsing : "This feature displays registered models in thumbnail format and, upon selection, shows detailed information about the model on the right side of the window.
* Scan New Version : This is a function that searches for the latest version of downloaded models on the Civitai site. It retrieves information from the site and only functions properly when the site is operational.

![register_model_direct](https://github.com/sunnyark/civitai-shortcut/assets/40237431/c6db4ced-9cec-4488-ac3f-9a17fadb42b8)

![register_model_shortcut](https://github.com/sunnyark/civitai-shortcut/assets/40237431/a18cc188-0d7a-4860-91fa-b9b2b27f4bdc)

* Prompt Recipe : The Prompt Recipe feature allows you to register and manage frequently used prompts.

![screenshot 2023-09-15 201815](https://github.com/sunnyark/civitai-shortcut/assets/40237431/d3d61c0a-c749-40ee-bc8c-69c35e9c6ba7)

![screenshot 2023-09-15 201833](https://github.com/sunnyark/civitai-shortcut/assets/40237431/773dc92f-3fd5-4509-94bb-99a9e50bec34)

![screenshot 2023-09-15 201853](https://github.com/sunnyark/civitai-shortcut/assets/40237431/ecf6e1a7-59f8-4eb5-a58f-5a7ff7824437)

* Assistance

1. Classification : Function for managing shortcuts by classification.

![screenshot 2023-09-15 201933](https://github.com/sunnyark/civitai-shortcut/assets/40237431/7881d3d8-d2a3-4502-b39c-fb40a17cf21c)

![screenshot 2023-09-15 201956](https://github.com/sunnyark/civitai-shortcut/assets/40237431/94b2b2a1-f148-42dc-b6a8-21c1381dc55f)

![screenshot 2023-09-15 202004](https://github.com/sunnyark/civitai-shortcut/assets/40237431/9003d94d-5a13-4613-9fa6-722b1e892874)

2. Scan and Update Models
   Scan Models - Scan and register shortcut for models without model information that are currently held.
   Update Shortcut - Move the shortcut update function from the Upload tab.
   Update the model information for the shortcut - Update the information of registered shortcuts with the latest information.
   Scan downloaded models for shortcut registration - Register new shortcuts for downloaded models that have been deleted or have missing model information.

![screenshot 2023-09-15 202018](https://github.com/sunnyark/civitai-shortcut/assets/40237431/7f200d24-a4ca-4e23-834a-71470590ee49)

* Setting tab - Set the number of columns in the image gallery.

![screenshot 2023-09-15 202037](https://github.com/sunnyark/civitai-shortcut/assets/40237431/67e2e7c5-0cd6-4917-a4c8-b9ffb45832f9)

# Features

You can save the model URL of the Civitai site for future reference and storage.
This allows you to download the model when needed and check if the model has been updated to the latest version.
The downloaded models are saved to the designated storage location.

# Notice

Four folders and five JSON files will be created, each serving the following roles.

* sc_recipes : Folder where Prompt Recipe images are saved.
* sc_gallery : Folder for caching images in the User Gallery.
* sc_thumb_images : Folder where thumbnails are saved.
* sc_infos : Folder where model information and images are saved upon registration.
* CivitaiShortCut.json : JSON file for recording and managing registered model URLs.
* CivitaiShortCutClassification.json: JSON file for managing classification categories.
* CivitaiShortCutSetting.json: JSON file for storing configuration settings.
* CivitaiShortCutRecipeCollection.json : JSON file for managing data related to Prompt Recipes.
* CivitaiShortCutBackupUrl.json : JSON file for backing up the URL during shortcut registration.

# Change Log

v 1.6.7

* Changed the names of each menu to correspond to their functions.

v 1.6.6

* In Prompt Recipe, the option 'Delete from references when selecting a thumbnail' has been deselected, and when clicking on a model within the references, it now displays brief information on the top instead of navigating to the model information.
* An added feature in Prompt Recipe allows the input of directives in the prompt based on the type of the selected reference model.
* In classification, the option 'Delete from classification when selecting a thumbnail' has been deselected, and when clicking on a model within the classification, it now displays brief information on the right instead of navigating to the model information.

v 1.6.5

* This update is compatible with gradio version 3.41.2 or higher.
* It requires the latest update of A1111 to function correctly.

v 1.6.4

* Save the available model data in sdui's LoRa metadata editor. (Note that it will only be saved if there is no existing data.)
* Change the names of some menus.
* Added a feature to Assistance->Scan and Update Models for generating missing LoRa metadata files (2023-08-19).

v 1,6.3

* The interface of the classification has been modified.
* Added shortcut browser feature to the classification, improving convenience.
* Modified shortcut information to include the respective shortcut as the default reference model when sending a prompt from the image to the recipe.

v 1.6.2

* Update the registration date of the shortcut
  (Perform Assistance->Update Shortcuts: Update the model information for the shortcut for existing data)
* Intuitively modify the settings of the gallery

v 1.6.1

* The interface of the reference shortcut model in the recipe has been modified.
* When generating thumbnails automatically, the model with the lowest NSFW level (most safe for work) will be selected.
* The NSFW filter will now operate across all ranges.
* In the classification, display the removed models among the shortcut models.

v 1.6.0

* Adding NSFW Filter function
* Revamping prompt recipe
* Adding a tab to register reference models in the prompt recipe
* Enhancing the search function for prompt recipes
* Added a setting in the shortcut browser to allow users to change the position of the search bar to their desired location, either above or below the thumbnail list.

v 1.5.8

* Add a 'Personal Note' section to the model information, and make it searchable using '@' in the search.

v 1.5.7

* The functionality to filter using the base model provided by Civitai has been added.
* I changed the classification categories to be selected from a dropdown list instead of searching in the search section. The selected classification categories will work as an 'AND' operation, meaning they will function as an intersection. This way, we can manage shortcuts that are classified under multiple categories in a more detailed manner

v 1.5.6

* Change the "user gallery paging" method to cursor-based paging as recommended by Civitai.

v 1.5.5

* When downloading a file, if there is no primary file in the download list, it will be modified to not generate version info and preview images. Only the corresponding file will be downloaded.
* The download file list will indicate whether it is a primary file.
* The sorting has been modified so that the shortcuts are sorted based on the 'name' field.

v 1.5.4

* The prompt recipe has been modified to update only the current state of the prompt content when dropping an image, without generating a new recipe.
* Add a feature to suggest available names for the model download folder: The names will be listed in the order of model name, author, and model tag.
* Correcting a typo
* When the shortcut is selected, the information will load only in the selected tab.
* Modify to search for the model information used in the User Gallery screen from the downloaded model information. Retrieve only image information in real-time from the user gallery images on the Civitai website. (I expect a reduction in ASGI application errors)

v 1.5.3

* Added the ability to change the file name of the model file to be downloaded.
* Change to allow selection only through checkboxes when choosing files.
* When clicking on the file name, an input field appears to allow changing the file name.
* Changed the behavior during file downloads to prevent the download of info and preview images when there is no download file available. This is done to avoid confusion with the ability to change the file name.
* Changed the search criteria for Scan Models.
* Modified the size of the thumbnail image to be smaller.
  Modified the thumbnail image to be changeable.
* Shortcut Browser screen ratio error fix

v 1.5.2

* Add description/modify the wording for folder creation during model download.
* Change the position of Prompt Recipe (Assistance -> Top level)
* Change the position of Scan and Update Models (Manage -> Assistance)

v 1.5.1

* Add the feature to change the preview image in the model information tab -> images: Change Preview Image button.
  The button will only appear if the model has been downloaded.
* For downloaded models, update the default folder name displayed to be the downloaded folder information.
  There may be inaccuracies if the model is downloaded in more than one location.
  In the Downloaded Model Information Tab, you can view the downloaded location and files.

v 1.5

* The information tab and the saved model information tab in the Civitai model have been merged. The Civitai model information, which used to fetch real-time information from the Civitai site, has been removed. Instead, the shortcut information registered during Stable Diffusion startup will be updated. You can enable or disable this feature in manage->setting->option.
* The Assistance tab has been added. Furthermore, the classification feature has been moved to the Assistance tab. Additionally, a new feature called Prompt Recipe has been added.
* The Prompt Recipe is a feature that allows you to register and manage frequently used prompts. You can register a prompt by directly writing it, uploading an image file, or using the 'Send to Recipe' button in the Image Information section of Model Information or User Gallery.
* In the Classification and Prompt Recipe sections, the 'Create' button now appears only when [New Classification] or [New Prompt Recipe] is selected, clearly distinguishing between the Create and Update states.
* The 'sc_saved' folder, which was used to backup the registration URLs for shortcuts, is no longer in use and can be deleted. Instead, the registration URLs are now stored in the CivitaiShortCutBackupUrl.json file in the format {url: name}. You can re-register the shortcuts by uploading this file in the Upload section.
  This file is automatically generated and updated when performing 'Update the model information for the shortcut' in Manage->Scan and Update Models or when the automatic update feature is enabled.
* A folder named 'sc_recipe' is created to store the images for the Prompt Recipe.
* Bug: There is an issue in the prompt recipe where the saved image loses the generated image information. It appears to be a problem with the Gradio Image component.
* A new option 'Disable Classification Gallery Preview Mode' has been added under 'Manage -> Settings -> Options'. This is an experimental feature and will be removed once it becomes an official functionality in Gradio

v 1.4a

* The interface design has been changed.
* More detailed information about the file to be downloaded is provided.
* A version information file and preview image will be generated even if a file is not selected for download.
  You can use the "Downloaded Model Information Tab" without actually downloading the file.
  Please note that even if you have not downloaded the file, it will be recognized as downloaded.
* The "open folder" function provided in the information tab may be inaccurate if the same file is downloaded multiple times from different locations.
  Please use the "Downloaded Model Information Tab" for accurate information.
* There is an error in the "Downloaded Model Information Tab" where downloading files with the same filename will be recognized as all downloaded.
* There have been some design and functionality changes to the Manage -> Classification section.
* The create, modify, delete, and update functions for classification have been integrated with the "Shortcut Item" section on the left.

  - The update function only updates the name and description of the classification.
  - Saving shortcut items registered to the classification should be done using "Save Classification Shortcuts".
* The "Screen Style" option has been added to Manage -> Setting.
  You can adjust the ratio between Shortcut Browser and Information Tab according to your monitor or work preference, and apply it.
  I recommend combining this feature with the Shortcut Browser and Information Images options to find a suitable combination.
* A new option has been added to set the download folder location for LyCORIS in "Download Folder for Extensions" settings.
  Previously, LoRA folder was used together, but now it has been added to allow appropriate modifications since LyCORIS extension can also be recognized in extra networks. (Thank you for letting me know.)
* A "Reload UI" button has been added. It reloads the SDUI.
  However, please note that it does not include a feature to save settings. Please use the "Save Setting" button next to it for that purpose. :)
* The internal format of the uploaded files in the Upload section has been slightly modified.
  The format of "url=civitai model url" has been modified to be recognized.
  e.g.)
  sample.txt:
  url=https://civitai.com/models/64863/cute-oil-impasto-chibi
  url=https://civitai.com/models/64850/koga-tomoe-from-bunny-girl-senpai
  url=https://civitai.com/models/64849/blackwhite
* Drag & drop feature in Upload does not work properly in Linux environment.
  I apologize for the inconvenience, but please use the textbox above for the time being.

v 1.4

* A new tab called "Downloaded Model Information" has been added to the Information tab.
  This tab allows you to view information about the currently downloaded files. A list of versions of the downloaded model is displayed, and selecting a version shows detailed information about the file in the bottom section. In the detailed display section, you can see the actual information about the downloaded file and access the downloaded folder. Please note that the information may be somewhat inaccurate due to reasons such as file duplication. In addition, you can view Civitai-provided information for that version in JSON format.

  All "Open Folder" functions only work when the folder exists.

  - The "Open Download Image Folder" function opens the folder containing the downloaded images.
  - The "Open Saved Information Folder" function opens the folder where the model's information files and images are downloaded when the shortcut is registered. If the folder is deleted, it can be restored using the "Update Model Information" function under "Civitai Shortcut -> Saved Model Information" or "Manage -> Scan and Update Models -> Update Shortcuts: Update the model information for the shortcut".
* You can set the display style of the Shortcut Browser on the left side. This can be done in "Manage->Setting->Shortcut Browser and Information Images: Shortcut Browser Thumbnail Count per Page". If you set it to 0, the entire list will be displayed as before.
* Additional feature description 1 (Update the model information for the shortcut):
  "Manage->Scan and Update Models->Update Shortcuts" is a function that updates the information of already registered shortcuts to the latest information. This applies to all registered shortcuts. Individual updates for shortcuts can be done in "Civitai Shortcut->Saved Model Information: Update Model Information".
* Additional feature description 2 (Scan new version model):
  The "Civitai Shortcut->Scan New Version: Scan new version model" function scans for new versions of downloaded model version files. It does not search for models that have not been downloaded.

v 1.3ss

* There have been changes to the rules and methods for downloading the model. You can now specify the folder to download to and set the user-defined classification item as the download item for the model.
* If you set the user-defined classification item as the download item, you cannot create subfolders. The folder for the user-defined classification item specified by the user will be created in the model type base folder (e.g. model/lora) and downloaded.
* If you select "Create Model Name Folder," a folder will be created based on the model name in the model type base folder (e.g. model/lora), and you can create a subfolder with the desired name according to the version.
* Downloaded model files can be freely moved to any desired folder. This extension only facilitates the convenience of downloading files and does not manage downloaded files. You can move them comfortably without any problems.
* Image downloads are downloaded by default to outputs/download-images, and can be set in setting->download for extension->Download Images Folder. Depending on the system, permission settings may be required.
* Since the user-defined classification item is used as the folder name, it is recommended to change difficult-to-use characters for folder creation. The "-" character will be replaced when creating the folder.
* The display type of thumbnail images can be changed. You can set it in setting->Shortcut Browser and Information Images->Gallery Thumbnail Image Style.
* When registering a shortcut, you can set the number of images to download. You can set it in setting->Shortcut Browser and Information Images->Maximum number of download images per version, and when set to 0, all images will be downloaded.

v 1.3c

* Add "Scan and Update Models" and "Settings" tabs to the Manage tab.
* Scan and Update Models tab
  Scan Models for Civitai - Scan and register shortcut for models without model information that are currently held.
  Update Shortcut - Move the shortcut update function from the Upload tab.
  Update the model information for the shortcut - Update the information of registered shortcuts with the latest information.
  Scan downloaded models for shortcut registration - Register new shortcuts for downloaded models that have been deleted or have missing model information.
* Setting tab
  Shortcut Browser and Information Images,User Gallery Images - Set the number of columns in the image gallery.
  Download Folder for Extensions - Can set the download path for specific extensions.
* The name of the model info file that records information about the model has been changed.
  As a result, even models with a normal model info file may be moved to a  new folder when scanning models for Civitai.
  To prevent this, uncheck the "Create a model folder corresponding to the model type" option.

v 1.3a

* A new feature has been added that allows you to manage and classify items.
  You can add, delete, and update classification items in the "manage" -> "classification" tab.
  To add a shortcut, select the desired classification item in the center top and click on the list on the left to register the desired shortcut. When you click, the registered shortcut appears in the center of the screen, and you can remove it by clicking on the registered shortcut.
  Click the "update" button to complete the registration.
  In the "civitai shortcut" -> "information" tab, a "model classification" item has been added on the right side, and you can perform registration and deletion of shortcuts for the model corresponding to the desired classification item.
  After modification, click the "update" button to complete the task.
* In the browsing "search" feature, you can check the items registered in the classification.
  When you select a classification item from the dropdown list, the selected item appears in the list and works in conjunction with the "filter model type" and "search" features.
  The "search" feature works by entering items such as tags, classification, and search keywords.
  The tags, classification, and search keywords are applied with "and" operation, and each item is applied with "or" operation. Each item is separated by ",".
  Although only one item can be selected from the classification dropdown list, you can enter multiple items by using the "@" prefix.

v 1.2a

* The Downloaded Model tab, which duplicated the functionality of the Saved Model Information tab, has been removed
* The application method for generating image information has been internally modified to include information from Civitai's 'information' field in addition to the image. As a result, there have been changes to the naming convention for saved images. Please update the images using 'Update Shortcut's Model Information' accordingly.

v 1.2

* A Civitai User Gallery tab has been added where users can view the information and images of the models in the gallery. If there are no images available for a particular model, the tab may appear empty. There may also be a delay in the data provided by the API.
* An "Update Downloaded Model Information" button has been added below the "Upload" button on the left-hand side. This button updates the internal information when users rename folders during Stable Diffusion operation.
* The option to download additional networks by selecting them from a list has been removed. This feature was deemed unnecessary as users can simply specify the desired folder in Settings -> Additional Networks. Personally, I use the "models/Lora" folder for this purpose.
* Users can now specify the folder name when downloading a model to an individual folder. The default format is "model name-version name", but users can input their preferred value. If a folder with the same version of the model already exists within the model's folder, that folder name will be displayed.
* Minor design changes have been made.
* Bug: There are several bugs, but when viewing the gallery images at full size, the image control and browsing controls overlap.

v 1.1c

* Measures have been taken to alleviate bottleneck issues during information loading.
* The search function now includes a #tag search feature.
  Search terms are separated by commas (,) and are connected with an "or" operation within the search terms and within the tags. There is an "and" operation between the search terms and tags.
* The shortcut storage table has been changed to add the #tag search function.
  Existing shortcuts require an "update shortcut model information" for tag searches.

v 1.1

* When registering a shortcut, model information and images are saved in a separate folder.
* This allows users to access model information from "Saved Model Information" Tab even if there is no connection to the Civitai site.
* "Thumbnail Update" button is removed and replaced with an "Update Shortcut's Model Information" button to keep the model information and images up to date.
* "Download images Only" button is removed from "Civitai Model Information" Tab that can be accessed live, and "Delete shortcut" button is moved to "Saved Model Information" Tab.
* "Delete shortcut" button removes the model information and images stored in sc_infos in one go.
* "Update Model Information" button is added to "Saved Model Information" Tab for individual updating of model information, in addition to "Update Shortcut's Model Information" that updates all model information.

# Screenshot

![screenshot 2023-09-15 203613](https://github.com/sunnyark/civitai-shortcut/assets/40237431/fdac59c0-0ced-41fb-8faa-83029b3ffc3f)
![screenshot 2023-09-15 202037](https://github.com/sunnyark/civitai-shortcut/assets/40237431/67e2e7c5-0cd6-4917-a4c8-b9ffb45832f9)
![screenshot 2023-09-15 202018](https://github.com/sunnyark/civitai-shortcut/assets/40237431/7f200d24-a4ca-4e23-834a-71470590ee49)
![screenshot 2023-09-15 202004](https://github.com/sunnyark/civitai-shortcut/assets/40237431/9003d94d-5a13-4613-9fa6-722b1e892874)
![screenshot 2023-09-15 201956](https://github.com/sunnyark/civitai-shortcut/assets/40237431/94b2b2a1-f148-42dc-b6a8-21c1381dc55f)
![screenshot 2023-09-15 201933](https://github.com/sunnyark/civitai-shortcut/assets/40237431/7881d3d8-d2a3-4502-b39c-fb40a17cf21c)
![screenshot 2023-09-15 201909](https://github.com/sunnyark/civitai-shortcut/assets/40237431/d3a300da-bccf-4452-ad59-11904c44f585)
![screenshot 2023-09-15 201853](https://github.com/sunnyark/civitai-shortcut/assets/40237431/ecf6e1a7-59f8-4eb5-a58f-5a7ff7824437)
![screenshot 2023-09-15 201845](https://github.com/sunnyark/civitai-shortcut/assets/40237431/c1726ab5-15b7-499f-9067-9755fba332c0)
![screenshot 2023-09-15 201833](https://github.com/sunnyark/civitai-shortcut/assets/40237431/773dc92f-3fd5-4509-94bb-99a9e50bec34)
![screenshot 2023-09-15 201815](https://github.com/sunnyark/civitai-shortcut/assets/40237431/d3d61c0a-c749-40ee-bc8c-69c35e9c6ba7)
![screenshot 2023-09-15 201738](https://github.com/sunnyark/civitai-shortcut/assets/40237431/b8673673-ea42-43ad-942f-15437fce6b26)
![screenshot 2023-09-15 201708](https://github.com/sunnyark/civitai-shortcut/assets/40237431/9f8f7ab3-245c-4878-b722-5cb7de2f1c9d)
![register_model_shortcut](https://github.com/sunnyark/civitai-shortcut/assets/40237431/a18cc188-0d7a-4860-91fa-b9b2b27f4bdc)
![register_model_direct](https://github.com/sunnyark/civitai-shortcut/assets/40237431/c6db4ced-9cec-4488-ac3f-9a17fadb42b8)
