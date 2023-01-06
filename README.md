# Gerar Doc. Teste

## :pushpin: Objetctives
Generate Word documents with pre-set formatting by simply passing the change number offered by Service-Now

## :hammer: Tecnologies
![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff&style=for-the-badge)
![Flask](https://img.shields.io/badge/Flask-000?logo=flask&logoColor=fff&style=for-the-badge)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?logo=html5&logoColor=fff&style=for-the-badge)
![Bootstrap](https://img.shields.io/badge/Bootstrap-7952B3?logo=bootstrap&logoColor=fff&style=for-the-badge)
![Word](https://img.shields.io/badge/Microsoft%20Word-2B579A?logo=microsoftword&logoColor=fff&style=for-the-badge)

## How it Works
This program will use the Word file "DocPadrao.docx" as a base, replacing the texts **TITLE**, **AUTHOR** and **DATA** by the name of the change typed by the user, the full name of the Windows and the current day the button was pressed respectively.

If by chance the typed number does not match the pattern **CHG[0-9]{7}**, which means that the pattern must contain the letters CHG followed by a sequence of 7 numbers between 0 and 9, it will send the user to an error screen.

https://user-images.githubusercontent.com/74682858/211036601-f15b3e88-34a6-46b3-a569-e8de231dec77.mp4

### Result
![word document generated](https://user-images.githubusercontent.com/74682858/211037126-e31efaaf-3095-42af-aeff-f3557f705826.png)
