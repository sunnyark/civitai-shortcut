# Civitai Shortcut

Stable Diffusion Webui Extension for Civitai, to download civitai shortcut and models.

# Install

Stable Diffusion Webui's Extension tab, go to Install from url sub-tab. Copy this project's url into it, click install.

    git clone https://github.com/sunnyark/civitai-shortcut


Stable Diffusion Webui의 Extension 탭에서 'URL에서 설치' 서브 탭으로 이동하세요. 해당 프로젝트의 URL을 복사하여 붙여넣고 '설치'를 클릭하세요.

    git clone https://github.com/sunnyark/civitai-shortcut

# Usage instructions
![screenshot 2023-04-16 182259](https://user-images.githubusercontent.com/40237431/232289602-0b0cab3d-e90c-49c1-95cc-decf3cbe40bf.png)

1. The information in the Civitai model information tab is obtained in real-time from the Civitai website.
   Download : downloads the model for the selected version. You can choose to create specific folders for each version. The downloaded model will be automatically saved in the appropriate location, and a preview image and info will be generated together with it.

![screenshot 2023-04-16 182316](https://user-images.githubusercontent.com/40237431/232289625-48abfaab-8eb4-4af0-a58e-1a9716751302.png)
2. The information in the Saved model information tab are composed of the information saved on the Civitai website when creating the shortcut.
Update Model Information : updates the information of an individual shortcut to the latest information. This function only works when the site is functioning normally.
Delete Shortcut : deletes the information of a registered shortcut.

![screenshot 2023-04-16 182333](https://user-images.githubusercontent.com/40237431/232289652-89ec3225-1849-44f8-8387-6216b576574e.png)
3. The information in the Downloaded tab of the Civitai model information is obtained from the downloaded folder when the model is downloaded.
Goto civitai shortcut tab : switches to #1 screen to view new information.
Open Download Folder : opens the file explorer to the folder where the model was downloaded.

For #1, since the information is obtained in real-time from the website, it can only be accessed when the site is operational.
For #2 and #3, the information is displayed based on the saved information, so it can be accessed even when the site is not operational.

![screenshot 2023-04-16 182342](https://user-images.githubusercontent.com/40237431/232289694-e9f75198-75b4-492a-8f60-6fc453137f5c.png)
![browsertobrowser](https://user-images.githubusercontent.com/40237431/233503898-53fd19d2-13bf-4b05-801e-265472bac1b5.gif)
![filetobrowser](https://user-images.githubusercontent.com/40237431/233503915-0ebc4c6e-2218-4722-a83e-7d83d5580571.gif)
![multifilestobrowser](https://user-images.githubusercontent.com/40237431/233578034-d8920f29-a66e-4939-b6c1-cb760d809c13.gif)

* Upload : This function creates a shortcut that can be used by the extension when you enter the Civitai site's model URL. It only works when the site is functioning properly. You can either click and drag the URL from the address bar or drag and drop saved internet shortcuts. You can also select multiple internet shortcuts and drop them at once.
* Update Shortcut's Model Information : This function updates the information of the shortcut you have received by referencing the site.
* Scan Downloaded Models to Shortcut : This function searches for downloaded models and registers shortcuts for them, in case you have accidentally deleted the shortcut or downloaded the models to a different location. Only models with version info files are registered. You can use Civitai Helper's Scan function to generate version info for models that don't have it. Note that only models available on the Civitai site can be registered with this function. This function only works when the site is functioning properly.

![screenshot 2023-04-16 182349](https://user-images.githubusercontent.com/40237431/232289696-54479aec-4013-42f3-9ae8-9c1f203095f2.png)

* Browsing : This function displays the registered shortcuts in thumbnail format, and when selected, displays their details on the right-hand side of the window. This function works independently of the Civitai site.

![screenshot 2023-04-16 182354](https://user-images.githubusercontent.com/40237431/232289699-c8b87b7a-85f7-436a-91e0-0c10620599c3.png)

* Scan New Version : This is a function that searches for the latest version of downloaded models on the Civitai site. It retrieves information from the site and only functions properly when the site is operational.

# Features

You can save the model URL of the Civitai site for future reference and storage.
This allows you to download the model when needed and check if the model has been updated to the latest version.
The downloaded models are saved to the designated storage location.

Civitai 사이트의 모델 URL을 저장하여 나중에 참조하고 보관할 수 있습니다.
이를 통해 필요할 때 모델을 다운로드하고 모델이 최신 버전으로 업데이트되었는지 확인할 수 있습니다.
다운로드 된 모델은 지정된 저장 위치에 저장됩니다.

# Notice

When using Civitai Shortcut, four items will be created:

* sc_saves: a folder where registered model URLs are backed up and stored.
* sc_thumb_images: a folder where thumbnails of registered URLs are stored.
* sc_infos: a folder where model info and images are saved when registering a shortcut.
* CivitaiShortCut.json: a JSON file that records and manages registered model URLs.

세개의 폴더와 하나의 json 파일이 생성되며 각각의 역할은 다음과 같습니다.

* sc_saves : 등록된 model url이 백업되는 폴더, 등록된 모든 url이 저장되는 폴더
* sc_thumb_images : 등록된 url의 thumbnail이 저장되는 폴더
* sc_infos : 등록시 모델정보와 이미지가 저장되는 폴더
* CivitaiShortCut.json : 등록된 model url 을 기록 관리 하는  json 파일

# Change Log

v 1.2
* A Civitai User Gallery tab has been added where users can view the information and images of the models in the gallery. If there are no images available for a particular model, the tab may appear empty. There may also be a delay in the data provided by the API.

* An "Update Downloaded Model Information" button has been added below the "Upload" button on the left-hand side. This button updates the internal information when users rename folders during Stable Diffusion operation.

* The option to download additional networks by selecting them from a list has been removed. This feature was deemed unnecessary as users can simply specify the desired folder in Settings -> Additional Networks. Personally, I use the "models/Lora" folder for this purpose.

* Users can now specify the folder name when downloading a model to an individual folder. The default format is "model name-version name", but users can input their preferred value. If a folder with the same version of the model already exists within the model's folder, that folder name will be displayed.

* Minor design changes have been made.

* Bug: There are several bugs, but when viewing the gallery images at full size, the image control and browsing controls overlap. 


* Civitai User Gallery 탭이 추가 되었습니다. 
모델의 Gallery 의 정보를 확인 할수 있습니다. 해당모델 갤러리에 이미지가 없으면 아무것도 나타나지 않을수 있습니다.
또한 api로 제공되는 데이터와 시간차가 있기도 하더군요.
어떤 기능을 넣으면 좋을지 아이디어를 구하고 있습니다. 

* 좌측에 Uplaod 하단에 "Update Downloaded Model Information" 버튼이 추가 되었습니다.
Stable Diffusion 작동중에 임의로 폴더명을 바꾸거나 했을때 내부 정보를 갱신 시켜줍니다.

* 다운로드 부분에 더이상 Additional networks 로 선택해서 다운 로드 하는 항목을 제거 하였습니다.
효용성도 떨어지고 Settings->Additional Networks 원하시는 폴더를 지정하면 되기때문에 필요없다 생각했습니다.
저는 models\Lora 입력하여 같이 사용중에 있습니다.

* 모델을 개별폴더에 다운 받을 때 폴더명을 직접 지정할수 있습니다. 
기존 적으로는 "모델명-버전명" 형시으로 보여지며 원하는 값으로 입력해주시면 됩니다. 
공백으로 하면 "모델명-버전명"으로 만들어 집니다. 
제시되는 폴더명은 다르게 나타날수도 있는데, 
같은 버전의 모델을 다운 받은 폴더가 해당 모델 폴더 하위에 있으면 그 이름이 나타납니다.

* 그 외에 소소하게 디자인 이 변경되었습니다.

* 버그 :많은 버그가 있지만 ; , 갤러리의 이미지를 full size로 볼때 information 쪽과 Browsing 쪽의 이미지와 제어가 섞입니다.

v 1.1c

* Measures have been taken to alleviate bottleneck issues during information loading.
* The search function now includes a #tag search feature.
  Search terms are separated by commas (,) and are connected with an "or" operation within the search terms and within the tags. There is an "and" operation between the search terms and tags.
* The shortcut storage table has been changed to add the #tag search function.
  Existing shortcuts require an "update shortcut model information" for tag searches.
* information 로딩에 병목현상을 일부 완화
* Search 에 #tags 검색 기능 추가
  "," 구분되며 search keywords 끼리는 or, tags 끼리도 or , search keyword와 tags는 and 이 적용됩니다.
* Tags검색 기능 추가를 위해 shortcut 저장 테이블이 변경되었습니다.
  기존의 shortcut은 tag 검색을 위해 Update Shortcut's Model Information 이 필요합니다.

v 1.1

* When registering a shortcut, model information and images are saved in a separate folder.
* This allows users to access model information from "Saved Model Information" Tab even if there is no connection to the Civitai site.
* "Thumbnail Update" button is removed and replaced with an "Update Shortcut's Model Information" button to keep the model information and images up to date.
* "Download images Only" button is removed from "Civitai Model Information" Tab that can be accessed live, and "Delete shortcut" button is moved to "Saved Model Information" Tab.
* "Delete shortcut" button removes the model information and images stored in sc_infos in one go.
* "Update Model Information" button is added to "Saved Model Information" Tab for individual updating of model information, in addition to "Update Shortcut's Model Information" that updates all model information.
* Shortcut 등록 시 모델정보와 이미지가 별도의 폴더에 저장됩니다.
* 이를 통해 사용자는 Civitai 사이트에 연결되지 않은 경우에도Saved Model Information 탭에서 모델 정보에 액세스할 수 있습니다.
* 모델 정보와 이미지를 최신 상태로 유지하기 위해 "Thumbnail Update" 버튼이 제거되고 "Update Shortcut's Model Information" 버튼으로 대체됩니다.
* 섬네일 업데이트 버튼을 삭제하고 shortcut 의 모델 정보와 이미지를 최신 정보로 유지하기위한 Update Shortcut's Model Information 버튼을 추가
* 라이브로 접속 가능한 "Civitai Model Information" 탭에서 Download images Only 버튼이 제거되고, Delete shortcut 버튼이 Saved Model Information 탭으로 이동됩니다.
* Delete shortcut는 sc_infos에 저장된 모델 정보와 이미지를 한 번에 제거합니다.
  *전체 모델 정보를 업데이트하는 "Update Shortcut's Model Information" 버튼 외에 개별적으로 모델 정보를 업데이트할 수 있는 "Update Model Information" 버튼이 "Saved Model Information" 탭에 추가됩니다.

# Screenshot
![browsertobrowser](https://user-images.githubusercontent.com/40237431/233503936-cdf04502-04ee-41f3-8bd0-20349bc09f4a.gif)

![filetobrowser](https://user-images.githubusercontent.com/40237431/233503941-1e3ede4e-07e8-4b6e-9708-ab42a9cab566.gif)

![screenshot 2023-04-13 200422](https://user-images.githubusercontent.com/40237431/231810541-c91471e5-e7ae-4d3c-a825-2bfed6746b73.png)

![screenshot 2023-04-13 200432](https://user-images.githubusercontent.com/40237431/231810585-63f6bffd-defa-4582-a7da-750dae29f589.png)

![screenshot 2023-04-12 101437-1](https://user-images.githubusercontent.com/40237431/231810628-c962429a-5b0b-46a9-9cb4-fe52a9e4d998.png)

![screenshot 2023-04-12 152645-1](https://user-images.githubusercontent.com/40237431/231810678-19876694-d023-4f62-960d-9ce774cccf67.png)
