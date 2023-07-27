# Civitai Shortcut

Stable Diffusion Webui Extension for Civitai, to download civitai shortcut and models.

# Install

Stable Diffusion Webui의 Extension 탭에서 'URL에서 설치' 서브 탭으로 이동하세요. 해당 프로젝트의 URL을 복사하여 붙여넣고 '설치'를 클릭하세요.

    git clone https://github.com/sunnyark/civitai-shortcut
    URL : https://github.com/sunnyark/civitai-shortcut

# Usage instructions

![screenshot 2023-05-24 132752](https://github.com/sunnyark/civitai-shortcut/assets/40237431/17f28498-43a6-4be3-83cb-b7d8602e3b00)

* Upload : 이 기능은 Civitai 사이트의 모델 URL을 이용하여 확장 프로그램에서 사용할 수 있는 바로 가기를 생성합니다. 주소 창에서 URL을 클릭하고 드래그하거나 저장된 인터넷 바로 가기를 드래그앤드롭할 수 있습니다. 또한 여러 개의 인터넷 바로 가기를 선택하고 한 번에 드롭할 수도 있습니다.
* Browsing : 이 기능은 등록된 바로 가기를 섬네일 형식으로 표시하며, 선택 시 창의 오른쪽에 해당 바로 가기의 세부 정보를 표시합니다.
* Scan New Version : 이 기능은 Civitai 사이트에서 다운로드한 모델의 최신 버전을 검색하는 기능입니다. 사이트에서 정보를 가져오며, 사이트가 정상 작동할 때에만 정상적으로 작동합니다.
* Model Information 의 정보를 최신 상태로 유지하기 위해서는 주기적인 데이터 업데이트가 필요합니다.
  방법에는 model information 하면에서 Update Shortcut 기능을 이용해서 개별적으로 업데이트 하거나, manage->setting->option 의 자동 업데이트를 활성화 , Manage->Scan and Update Models->Update the model information for the shortcut 기능을 이용하는 방법이 있습니다.

![drag_drop_upload](https://github.com/sunnyark/civitai-shortcut/assets/40237431/e4f0bd60-0c81-45fe-aa60-652027579247)

![file_drop_upload](https://github.com/sunnyark/civitai-shortcut/assets/40237431/efdee43a-795e-4cb9-8c5e-322b5824bb8f)

![file_upload](https://github.com/sunnyark/civitai-shortcut/assets/40237431/dbcbc789-89a9-45fd-b8a9-388ba33c916f)

* Classification : Shortcut에서 사용하는 분류항목을 관리하는 기능입니다.

![classification_action](https://github.com/sunnyark/civitai-shortcut/assets/40237431/ec0ddb51-6b8b-485a-a560-9c174a962001)

* Prompt Recipe : Prompt recipe는 자주 사용하는 Prompt를 등록하고 관리 할수 있는 기능입니다.

![prompt_recipe_create01](https://github.com/sunnyark/civitai-shortcut/assets/40237431/7f8db7b5-f3d0-45bc-a8b9-181f3befe4ef)

![prompt_recipe_create02](https://github.com/sunnyark/civitai-shortcut/assets/40237431/9218f2bd-9bf9-47ee-b61f-80cc1816da1e)

![prompt_recipe_send_txt2image](https://github.com/sunnyark/civitai-shortcut/assets/40237431/abeb0af6-fe97-4cef-b4b5-92110237c6b2)

* Scan and Update Models
  Scan Models : 현재 보유 중인 모델 정보가 없는 모델에 대해 스캔하여 바로 가기를 등록하는 기능입니다.
  Update the model information for the shortcut : 등록된 바로 가기의 정보를 최신 정보로 업데이트합니다.
  Scan downloaded models for shortcut registration : 삭제되거나 모델 정보가 누락된 다운로드된 모델에 대해 새로운 바로 가기를 등록합니다.

![screenshot 2023-05-24 134729](https://github.com/sunnyark/civitai-shortcut/assets/40237431/812457f2-5ea1-460e-b023-c9b50c664227)

* Setting : 확장프로그램의 다양한 설정값을 관리합니다.

![screenshot 2023-05-24 134749](https://github.com/sunnyark/civitai-shortcut/assets/40237431/3758bee5-71ea-4fb1-a411-e55213f701d4)

# Features

Civitai 사이트의 모델 URL을 저장하여 나중에 참조하고 보관할 수 있습니다.

이를 통해 필요할 때 모델을 다운로드하고 모델이 최신 버전으로 업데이트되었는지 확인할 수 있습니다.
다운로드 된 모델은 지정된 저장 위치에 저장됩니다.

# Notice

4개의 폴더와 5개의 json 파일이 생성되며 각각의 역할은 다음과 같습니다.

* sc_recipes : Prompt Recipe이미지가 저장되는 폴더
* sc_gallery : 유저갤러리의 이미지 캐싱을 위한폴더
* sc_thumb_images : 등록된 url의 thumbnail이 저장되는 폴더
* sc_infos : 등록시 모델정보와 이미지가 저장되는 폴더
* CivitaiShortCut.json : 등록된 model url 을 기록 관리 하는  json 파일
* CivitaiShortCutClassification.json: 분류항목을 관리하는 파일
* CivitaiShortCutSetting.json: 설정값을 저장하는 파일
* CivitaiShortCutRecipeCollection.json : Prompt Recipe 의 데이터를 관리하는 파일
* CivitaiShortCutBackupUrl.json : Shortcut 등록시의 URL을 백업하는 파일

# Change Log
v 1.5.8
* 모델 인포메이션에 personal note 항목을 추가, 검색에서 "@" 를 이용해서 검색가능

v 1.5.7
* Civitai에서 제공하는 기본 모델을 사용하여 필터링하는 기능이 추가되었습니다.
* 분류 항목을 검색 섹션에서 검색하는 대신 드롭다운 목록에서 선택할 수 있도록 변경합니다. 선택된 분류 항목은 'AND' 연산으로 작동하여 교집합처럼 동작합니다. 이렇게 하면 다중 카테고리에 속하는 바로 가기들을 더 자세하게 관리할 수 있습니다.

v 1.5.6
* Civitai에서 권장하는 대로 "user gallery paging" 방법을 cursor paging 으로 변경합니다.

v 1.5.5

* 파일 다운로드시 다운로드 목록에 primary 파일이 없으면 version info 와 프리뷰 이미지를 생성하지 않도록 수정됨. 해당파일만 다운로드하게됨.
* 다운로드 파일 목록에 primary 여부 표시.
* shortcut이 name 을 기준으로 정렬 되도록 수정

v 1.5.4

* 프롬프트 레시피에서 이미지를 drop할때 새 레시피가 생성되지 않고 현재 상태의 프롬프트 내용만 갱신되도록 변경
* 모델 다운로드 폴더명에 사용가능한 이름을 제시기능 추가 : 모델명, 작성자, 모델 tag 순으로 나열됨
* 오탈자 수정
* shortcut을 선택할때 information이 선택한 탭에서만 로딩되도록 변경.
* User Gallery 화면에서 사용하는 모델정보는 다운로드한 모델 정보에서 검색하도록 수정합니다. Civitai 웹 사이트의 사용자 갤러리 이미지에서 이미지 정보만 실시간으로 검색합니다. (ASGI 애플리케이션 오류가 줄어들 것으로 기대합니다.)

v 1.5.3

* 파일명을 변경할수 있게 수정
* 파일 선택시 체크 박스를 통해서만 선택가능하게 변경
* 파일명을 클릭하면 파일명을 변경할 수 있는 입력란이 나타납니다.
* 파일 다운로드시 다운로드 파일이 없어도 인포와 프리뷰 이미지가 다운로드 되던 것을 못하게 변경
  파일명을 변경가능함에따라 혼동을 막기위함
* Scan Models 의 검색조건을 변경하여 다운로드 파일이 여러개인 경우도 처리 하도록 변경
* 썸네일의 이미지를 크기를 작게 수정
  썸네일의 이미지를 변경 가능하게 수정
* Shortcut Browser screen ratio 오류 수정

v 1.5.2

* model download시 생성되는 폴더생성에 대한 설명추가/문구 변경.
* Prompt Recipe 의 위치 변경 (Assistance -> Top level)
* Scan and Update Models 의 위치변경 (Manage -> Assictance)

v 1.5.1

* preview 이미지의 변경 기능 추가 model imformation tab -> images : change preview image 버튼
  모델을 다운로드한 경우에만 버튼이 나타납니다.
* 파일 다운로드시 create model folder 선택시 다운로드할 모델폴더명을 변경가능하게 변경.
  다운로드된 모델의 경우 기본 표기되는 폴더이름이 다운로드된 폴더정보를 기본 정보로 표기되도록 변경. 모델이 중복 다운로드된 경우 부정확할수 있음.
  Downloaded Model Information Tab에서 다운로드한 파일의 다운로드된 위치, 파일을 확인할수 있습니다.

v 1.5

* information tab의 civitai model information 과 saved model information tab이 통합되었습니다.
  civitai 싸이트의 실시간 정보를 가져오던 civitai model information이 제거된대신 stable diffusion 시작시 등록된 솟컷의 정보를 자동으로 업데이트 하는 기능이 추가되었습니다.
  manage->setting->option 에서 기능을 끄고 켤수 있습니다.
* Assistance tab이 추가되고 classification이 Assistance tab으로 이동 하였습니다.
* Assistance tab에 새로운 기능인 Prompt recipe 기능이 추가 되었습니다.
* Prompt recipe는 자주 사용하는 Prompt를 등록하고 관리 할수 있는 기능입니다.
  프롬프트의 등록은 직접 작성하거나 , 이미지 파일일을 업로드 또는 Model Information 또는 User Gallery 의 Image Information 의 send to recipe 버튼으로 등록 할수 있습니다.
* classification 과 prompt recipe에서 목록의 [New Classification] ,[New Prompt Recipe] 상태에서만 Create 버튼이 나타나도록 변경하여 Create 상태와 Update 상태를 명확히 하였습니다.
* bug : prompt recipe 에서 저장되는 이미지는 이미지 생성정보가 사라지는 버그가 있습니다. gradio Image 컴포넌트 문제인것 같습니다.
* 숏컷의 등록 URL을 백업하던 sc_saved 폴더가 더이상 사용되지 않습니다. (삭제 가능)
  대신 CivitaiShortCutBackupUrl.json 파일에 {url : 이름} 형태로 저장됩니다.
  Upload항목에 이 파일을 upload 하면 숏컷을 다시 등록 할 수 있습니다.
  이 파일은 Manage->Scan and Update Models ->Update Shorts -> "Update the model information for the shortcut" 을 수행하거나 자동 업데이트 기능을 켜놓으면 자동으로 생성, 업데이트 됩니다.
* prompt recipe 의 이미지를 저장하는 sc_recipe 폴더 생성됩니다.
* manage->setting->option 에 classification gallery preview mode disable 이 생겼습니다. 이는 실험적인것입니다.
  gradio 에 정식으로 기능이 생기면 제거될것입니다.

v 1.4a

* 인터페이스 디자인 인이 변경되었습니다.
* 다운 받을 파일에 대한 좀더 자세한 정보를 제공하도록 변경되었습니다.
* 파일을 선택하지 않고 다운로드 시에도 version information 파일과 preview 이미지를 생성 하도록 변경하였습니다.
* 실제 파일을 다운 로드 하지 않고도 Downloaded Model Information을 이용하실수 있습니다.
* 파일을 다운 받지 않았어도 다운 받은걸로 인식되므로 참고 부탁드립니다.
* 인포메이션탭에서 제공하는 open folder 기능은 여러곳에 중복 다운로드했을시 부정확할수 있습니다.
  정확한 내용을 알고 싶으시면 Downloaded Model Information tab 을 활용해주세요.
* Downloaded Model Information tab 에서 파일명이 동일한 파일을 다운 받을 경우 모두 다은받은걸로 인식되는 오류가 있습니다.
* Manage -> Classification 디자인 과 기능에 일부 변경이 있습니다.
* Classification 의 생성 수정 삭제 업데이트 기능이 좌측의 Shortcut Item 항목과 통합되었습니다.

  - Update 기능은 classification 의 이름과 설명의 Update만 합니다.
  - classification에 등록되는 shortcut Item 의 저장은 Save Classification Shortcuts 을 이용하셔야 합니다.
* Manage -> Setting 에 Screen Style 항목이 추가되었습니다.
  Shortcut Brower 와 Information Tab 간의 비율을 설정할수있습니다.
  자신의 모니터나 작업취향에 따라 적절한 비율을 선택하시고 적용할수 있습니다.
  Shortcut Browser and Information Images 항목과 적절히 조합하시길 추천드립니다.
* Download Folder for Extensions 에 LyCORIS의 다운로드 위치를 설정할수 있는 항목이 추가 되었습니다.
  기존에 는 LoRA 폴더를 같이 이용했지만 LyCORIS확장을 사용하시면 extra networks 에서도 인식되는것을 알게되어 적절히 수정 하실수 있게 추가 하였습니다.
  (알려주시어 감사합니다.)
* Reload UI 버튼이 추가 되었습니다. SDUI 를 리로드 시킵니다.
  단 setting을 저장하는 기능은 넣지 않았습니다. 저장은 옆의 Save Setting 버튼을 이용해주세요. :)
* Upload 항목에 업로드 되는 파일의 내부 형식을 조금 변경하였습니다.

  - url=civitai model url 의 구성을하면 인식되도록 수정하였습니다.
  - e.g.)
    sample.txt :
    url=https://civitai.com/models/64863/cute-oil-impasto-chibi
    url=https://civitai.com/models/64850/koga-tomoe-from-bunny-girl-senpai
    url=https://civitai.com/models/64849/blackwhite
* Upload 의 드래그 & 드롭이 리눅스 환경에서 제대로 작동 되지 않습니다.
  불편하시겠지만 당분간 윗쪽의 Textbox 를 활용해주세요.

v 1.4

* 인포메이션 탭에 Downloaded Model Information 탭이 추가 되었습니다.
  현재 다운로드한 파일의 정보를 확인 할 수 있는 탭입니다. 다운로드한 모델의 버전 리스트가 나타나며 선택시 하단에 세부 정보가 나타납니다. 세부표시 항목에서는 실제 다운 로드한 파일의 정보를 확인할수 있으며 다운로드된 폴더에 접근할수 있습니다. 파일 중복등의 사유로 다소 부정확할수 있습니다. 또한 해당버전의 Civitai 제공 정보를 json형태로 확인 하실수 있습니다.
  모든 Open Folder 기능은 해당 폴더가 존재 할때만 작동됩니다.

  - Open Download Image Folder : 다운로드한 이미지들이 포함되어 있는 폴더를 열어줍니다.
  - Open Saved Information Folder : Shortcut 등록시 모델의 정보파일과 이미지들이 다운로드 되는 폴더를 열어줍니다.
    삭제시 되었을시 Civitai Shortcut->Saved Model Inforamtion : Update Model Information 이나 Manage->Scan and Update Models->Update Shortcuts : Update the model information for the shortcut 으로 복구할 수 있습니다.
* 좌측의 shortcut browser의 표시 방식을 설정할 수 있습니다.
  Manage->Setting->Shortcut Browser and Information Images : Shortcut Browser Thumbnail Count per Page
  항목에서 설정할 수 있으며 0으로 설정시 기존의 방식처럼 전체 리스트가 출력됩니다.
* 추가 기능 설명 1 (Update the model information for the shortcut)
  Manage->Scan and Update Models->Update Shortcuts : Update the model information for the shortcut
  기능은 이미등록된 shortcut 의 정보를 최신 정보로 업데이트 하는 기능입니다. 이는 등록된 모든 숏컷을 대상으로 합니다.
  숏컷의 개별적인 업데이트는 Civitai Shortcut->Saved Model Inforamtion : Update Model Information 에서 할수 있습니다.
* 추가 기능 설명 2 (Scan new version model)
  Civitai Shortcut->Scan New Version : Scan new version model: 의 기능은 다운 로드된 모델 버전파일의 새로운 버전이 있는지 스캔하는 기능입니다. 다운로드하지 않은 모델은 검색하지 않습니다.

v 1.3ss

* 모델의 다운로드 규칙, 방법에 변경이 있습니다.
  다운로드시 폴더를 지정할수 있습니다. 사용자 분류 항목을 모델의 다운로드 항목으로 설정할수있습니다.
* 사용자가 등록한 분류 항목으로 설정하면 하위폴더는 작성할 수 없으며 사용자가 지정한 분류항목의 폴더가 model type base folder(e.g. model/lora) 에 만들어지고 다운로드 됩니다.
* "Create Model Name Folder" 선택하면 model type base folder(e.g. model/lora) 에 모델명을 베이스로 폴더가 만들어지며 버전에 따라 서브폴더를 원하는 이름으로 만들수 있습니다.
* 다운로드된 모델파일은 원하는 폴더로 자유롭게 이동하셔도 됩니다.
  본 확장프로그램은 파일의 다운로드의 편의를 돕기만할뿐 다운로드된 파일을 관리 하지는 않습니다.
  편하게 이동 하셔도 문제 없습니다.
* 이미지 다운로드는 기본으로 outputs/download-images 에 다운 로드되며 setting->download for extension->Download Images Folder 에서 설정할수 있습니다. 시스템에따라 접근권한의 설정이 필요할수 있습니다.
* 사용자 정의 분류항목이 폴더명으로 사용되어지므로 폴더생성에 사용하기 어려운 문자는 변경을 권장드립니다.
  폴더 생성시 "-" 문자로 대체됩니다.
* thumbnail 이미지의 display type 을 변경할수 있습니다. setting->Shortcut Browser and Information Images->Gallery Thumbnail Image Style 에서 설정할수 있습니다.
* 쇼컷 등록시 다운로드 되는 이미지의 수를 설정할수 있습니다. setting->Shortcut Browser and Information Images->Maximum number of download images per version 에서 절정하룻 있으며 0일때는 모두 다운로드 됩니다.

v 1.3c

* Manage tab 에 scan and update models 와 setting 탭추가
* Scan and Update Models tab
  Scan Models for Civitai - 보유하고 있는 모델중 모델 정보가 없는 파일을 스캔하고 숏컷으로 등록 함
  Update Shortcut - Upload tab 에 있던 shortcut update 기능을 옯겨옴
  Update the model information for the shortcut - 등록된 shortcut의 정보를 최신정보로 업데이트함
  Scan downloaded models for shortcut registration - 다운 로드 받았지만 삭제되었거나 모델 정보가 있는 모델의 shortcut을 새로이 등록해줌
* Setting tab
  Shortcut Browser and Information Images,User Gallery Images - 이미지 갤러리의 컬럼의 수를 설정함.
  Download Folder for Extensions - 특정 확장프로그램의 다운로드 경로를 설정함
* 모델의 정보를 기록하는 모델 인포 파일의 이름이 변경되었습니다.
  이에 따라 정상적인 model info 파일이 있는 모델도 "Scan Models for Civitai" 작업시 새로운 폴더로 이동되어질수 있습니다.
  "Create a model folder corresponding to the model type." 옵션을 해제 하시면 이동을 막을수 있습니다.

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

* Saved Model Information tab 과 중복되는 기능을 가진 Downloaded Model tab이 제거되었습니다.
* 이미지 생성정보 적용방식이 내부적으로 변경되었습니다.
  이미지외에 civitai 의 information 정보에서도 가져오도록 수정되었습니다.
  이에따라 내부적으로 이미지 저장명의 변경이 있었습니다. "Update Shortcut's Model Information" 으로 이미지 업데이트가 필요합니다.

v 1.2

* Civitai User Gallery 탭이 추가 되었습니다.
* 모델의 Gallery 의 정보를 확인 할수 있습니다. 해당모델 갤러리에 이미지가 없으면 아무것도 나타나지 않을수 있습니다.
  또한 api로 제공되는 데이터와 시간차가 있기도 하더군요.
  어떤 기능을 넣으면 좋을지 아이디어를 구하고 있습니다.
* 좌측에 Upload 하단에 "Update Downloaded Model Information" 버튼이 추가 되었습니다.
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

* information 로딩에 병목현상을 일부 완화
* Search 에 #tags 검색 기능 추가
  "," 구분되며 search keywords 끼리는 or, tags 끼리도 or , search keyword와 tags는 and 이 적용됩니다.
* Tags검색 기능 추가를 위해 shortcut 저장 테이블이 변경되었습니다.
  기존의 shortcut은 tag 검색을 위해 Update Shortcut's Model Information 이 필요합니다.

v 1.1

* Shortcut 등록 시 모델정보와 이미지가 별도의 폴더에 저장됩니다.
* 이를 통해 사용자는 Civitai 사이트에 연결되지 않은 경우에도Saved Model Information 탭에서 모델 정보에 액세스할 수 있습니다.
* 모델 정보와 이미지를 최신 상태로 유지하기 위해 "Thumbnail Update" 버튼이 제거되고 "Update Shortcut's Model Information" 버튼으로 대체됩니다.
* 섬네일 업데이트 버튼을 삭제하고 shortcut 의 모델 정보와 이미지를 최신 정보로 유지하기위한 Update Shortcut's Model Information 버튼을 추가
* 라이브로 접속 가능한 "Civitai Model Information" 탭에서 Download images Only 버튼이 제거되고, Delete shortcut 버튼이 Saved Model Information 탭으로 이동됩니다.
* Delete shortcut는 sc_infos에 저장된 모델 정보와 이미지를 한 번에 제거합니다.
  *전체 모델 정보를 업데이트하는 "Update Shortcut's Model Information" 버튼 외에 개별적으로 모델 정보를 업데이트할 수 있는 "Update Model Information" 버튼이 "Saved Model Information" 탭에 추가됩니다.

# Screenshot

![screenshot 2023-05-24 132752](https://github.com/sunnyark/civitai-shortcut/assets/40237431/17f28498-43a6-4be3-83cb-b7d8602e3b00)

![screenshot 2023-05-24 133740](https://github.com/sunnyark/civitai-shortcut/assets/40237431/14cba843-33f4-4100-80e9-ed17662a8fb9)

![screenshot 2023-05-24 134646](https://github.com/sunnyark/civitai-shortcut/assets/40237431/a38fe1d8-4f00-47e8-826a-3f8f8dee61f6)

![screenshot 2023-05-24 134708](https://github.com/sunnyark/civitai-shortcut/assets/40237431/52cc44c3-20cd-4177-b848-274374acaab6)

![screenshot 2023-05-24 134729](https://github.com/sunnyark/civitai-shortcut/assets/40237431/812457f2-5ea1-460e-b023-c9b50c664227)

![screenshot 2023-05-24 134749](https://github.com/sunnyark/civitai-shortcut/assets/40237431/3758bee5-71ea-4fb1-a411-e55213f701d4)

![drag_drop_upload](https://github.com/sunnyark/civitai-shortcut/assets/40237431/e4f0bd60-0c81-45fe-aa60-652027579247)

![file_drop_upload](https://github.com/sunnyark/civitai-shortcut/assets/40237431/efdee43a-795e-4cb9-8c5e-322b5824bb8f)

![file_upload](https://github.com/sunnyark/civitai-shortcut/assets/40237431/dbcbc789-89a9-45fd-b8a9-388ba33c916f)

![classification_action](https://github.com/sunnyark/civitai-shortcut/assets/40237431/ec0ddb51-6b8b-485a-a560-9c174a962001)

![prompt_recipe_create01](https://github.com/sunnyark/civitai-shortcut/assets/40237431/7f8db7b5-f3d0-45bc-a8b9-181f3befe4ef)

![prompt_recipe_create02](https://github.com/sunnyark/civitai-shortcut/assets/40237431/9218f2bd-9bf9-47ee-b61f-80cc1816da1e)

![prompt_recipe_send_txt2image](https://github.com/sunnyark/civitai-shortcut/assets/40237431/abeb0af6-fe97-4cef-b4b5-92110237c6b2)
