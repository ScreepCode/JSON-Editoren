import json
import os

class JSONTool():
    def __init__(self):
        self.dateipfad = os.path.abspath(".")+ "/CMS.js"
        self.openJSON()

    def openJSON(self):
        # Datei öffnen
        f = open(self.dateipfad, "r")
        rawJS = f.read()
        f.close()
        
        # Bisheriges Einlesen
        linesJS = rawJS.split("+")
        tmp = "["

        tmp += rawJS.replace("+", "")
        tmp = tmp.replace("'", "")
        tmp = tmp.replace('var data = "["', "")
        tmp = tmp.replace("\n", "")
        tmp = tmp.replace("        ", "")
        tmp = tmp.replace('"]"', "")

        tmp += "]"
        # print(tmp)

        jsonData = json.loads(tmp)
        print(json.dumps(jsonData, indent=4))

JT = JSONTool()