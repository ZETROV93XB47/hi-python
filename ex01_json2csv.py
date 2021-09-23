import PySimpleGUI as gui
import json
import pandas as pd
from collections import defaultdict

#Définition de la structure de l'interface graphique (Thème, boutons, menus, agencement des boutons, boîtes de texte etc)
###########################################################################################################
gui.theme('Dark')

menu_def = [
                            ['About', ['Who am i ? ', 'Software Version']]
                        ]

layout = [  
                    [gui.Menu(menu_def)],
                    [gui.Text('Please, pick JSON file : ')],
                    [gui.T("")], [gui.Text("Pick a file: "), gui.Input(key="-IN2-" ,change_submits=True), gui.FileBrowse(file_types=(("INI Files", "*.json"),), key="file_path")],
                    [gui.Multiline(size=(80,10),tooltip='Write your Text here', auto_size_text=True, write_only=True, autoscroll=True, key='textbox')],
                    [gui.Text("", key="txt")],
                    [gui.Button('Show File Content'), gui.Button('Convert and Save INI Version'), gui.Button('Convert and Save CSV Version')],
                ]
###########################################################################################################

#Création de la fenêtre
window = gui.Window('JSON Document Converter', layout, resizable=True, button_color="red", auto_size_text=True)

"""
{
    "bitbucket.org": {
        "serveraliveinterval": "45",
        "compression": "yes",
        "compressionlevel": "9",
        "forwardx11": "yes",
        "user": "hg"
    },
    "topsecret.server.com": {
        "serveraliveinterval": "45",
        "compression": "yes",
        "compressionlevel": "9",
        "forwardx11": "no",
        "port": "50022"
    }
}
#Mon fichier JSON de test

"""


def convertINItoDict(config):
    configDict = defaultdict(dict)
    for section in config.sections():
        for key, value in config.items(section):
            configDict[section][key] = value
    return configDict


def convertJSONToINI(jsonObject):
    try :
        string = ""
        for i in jsonObject:
            string+= "["+i+"]\n"
            for j in (jsonObject[i]):
                string+= j+"="+str(jsonObject[i][j])+"\n"
    except json.JSONDecodeError:
        print("Fichier JSON invalide")
        return False
    return string

def ReadFile(path): 
    try:
        if(len(path) == 0):
            gui.popup("Veuillez entrer un chemin de fichier valide ! ")
        else:
            with open(path,  'r', encoding='utf-8-sig') as f:
                contents = f.read()
                return contents
    except IOError:
        gui.popup("Une erreur est survenue lors de l'ouverture du fichier, veuillez réessayer")
        return False


def writeInFile(path, content):
    try:
        with open(path, 'w', encoding='utf-8-sig') as f:
            f.write(content)
            return True
    except IOError:
        print("Une erreur est survenue lors de l'écriture du fichier, veuillez réessayer")
        return False





#Boucle de gestion d'événements, cette boucle sert à gérer les intercations derrière les boutons de l'interface graphique 
while True:
    event, values = window.read()
    print(event)
    print(values)
    if event == gui.WIN_CLOSED or event == 'Exit': # if user closes window or clicks cancel
        break
    # print('You entered ', values[0])

    if(event == 'Show File Content'):
        window['textbox'].update(ReadFile(values['file_path']))

    elif(event == 'Convert and Save INI Version'):
        jsonTextContent = ReadFile(values['file_path'])
        if(jsonTextContent == None):
            gui.popup("Une erreur inatendue s'est produite !")
        else:
            jsonObject = json.loads(jsonTextContent)
            string = convertJSONToINI(jsonObject)
            window['textbox'].update(string)
            status = writeInFile(values['file_path']+".ini", string)
            if(status):
                gui.popup('Saving','Your file has been saved at this location : '+values['file_path']+".ini")

    elif(event == 'Convert and Save CSV Version'):
        jsonTextContent = ReadFile(values['file_path'])
        if(jsonTextContent == None):
            gui.popup("Une erreur inatendue s'est produite !")
        else:
            jsonObject = json.loads(jsonTextContent)
            df = pd.read_json (jsonTextContent, orient="values")
            df.to_csv (r""+values['file_path']+".csv")
            window['textbox'].update(ReadFile(values['file_path']+".csv"))
            gui.popup('Saving','Your file has been saved at this location : '+values['file_path']+".csv")

    elif(event == 'Who am i ? '):
        gui.popup('Author : ',"bégédu93XD")

    elif(event == 'Software Version'):
        gui.popup('Software Version : '," V 0.1")

window.close()