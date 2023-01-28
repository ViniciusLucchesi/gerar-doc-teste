# Gerar Doc. Teste

## :hammer: Tecnologies
![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff&style=for-the-badge)
![Flask](https://img.shields.io/badge/Flask-000?logo=flask&logoColor=fff&style=for-the-badge)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?logo=html5&logoColor=fff&style=for-the-badge)
![Bootstrap](https://img.shields.io/badge/Bootstrap-7952B3?logo=bootstrap&logoColor=fff&style=for-the-badge)
![Word](https://img.shields.io/badge/Microsoft%20Word-2B579A?logo=microsoftword&logoColor=fff&style=for-the-badge)


## :pushpin: Objetctives
Generate Word documents with pre-set formatting by simply passing the change number offered by Service-Now

![GerarDocTeste](https://user-images.githubusercontent.com/74682858/213464931-13dbf571-1531-4adf-ba06-b8571e1d7e7b.png?#vitrinedev)

In the GIF below you can see the application in operation
![generating the document](https://user-images.githubusercontent.com/74682858/213471754-033149ba-746a-4f92-a6ec-b727ddab13de.gif)

## Resources
- Generation of word documents _(with predefined standards)_
- Error handling _(document will not be generated until it meets the standards)_
- Allows you to add new standard word documents
- Allows you to change the save location of generated documents
- Keeps a History of the documents that were generated and their respective versions


## Download and run the project
1. Download the "GerarDocTeste.zip" folder to your computer
2. Extract your files to any location
3. Copy the executable path contained in the extracted folder
4. Create a shortcut passing the copied path
5. Double click on the shortcut
6. Click "Run Anyway" to run the project (only on first run)

![Download and run the project](https://user-images.githubusercontent.com/74682858/213461596-cefb7069-1680-42d2-b0f0-5d8780c10562.gif)


## How the templates should be
They must contain the words "TITLE", "AUTHOR", "DATE", regardless of the order in which they appear or the formatting they have, as they will be replaced as follows:
- TITLE will be the change number
- AUTHOR will be the full name or username of the current Windows user
- DATE will be the date of the day you are running this application

![DocTemplates](https://user-images.githubusercontent.com/74682858/213464469-b2b9c2a4-d2ad-4e25-9d37-a234344c5b67.png)


## What happens if I don't use the Service-Now default?
If the pattern that the field is expecting is not met, a pop-up will be returned on the screen indicating that the pattern must be used so that the document can be generated. As shown below

![non-standard](https://user-images.githubusercontent.com/74682858/213468403-cfdb1c2e-fa69-402a-b223-bc64c92a7685.gif)

