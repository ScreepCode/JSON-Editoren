# -*- coding: utf-8 -*-

import json
import os
import sys
import time

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

TITLE = "JSON Editor"
GEOMETRIE = [300, 200, 400, 600]
GEOMETRIEADD = [300, 200, 700, 800]
GEOMETRIETABLE = [300, 200, 300, 500]

class JSONTool(object):
    def __init__(self):
       self.dateipfad = os.path.abspath(".")+ "/CMS.js"
    
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

        jsonData = json.loads(tmp)
        return jsonData

    def appendNewJSON(self, newJsonString):
        data = self.openJSON()

        dataStr = str(data)[:-1]
        dataStr += "," + newJsonString + "]"
        
        jsonData = json.loads(dataStr.replace("'", '"'))

        f = open(self.dateipfad, "w")
        out = '\nvar data = "[" + \n'
        for x in jsonData:
            y = str(x).replace("'", '"')
            out +=  "        '" + y + ",' + \n"
        out = out[:-6] + "' + \n"   
        out += '        "]"'
        f.write(out)

    def editJSON(self, index, editJsonString):
        jsonData = self.openJSON()

        jsonData[index] = editJsonString

        f = open(self.dateipfad, "w")
        out = '\nvar data = "[" + \n'
        for x in jsonData:
            y = str(x).replace("'", '"')
            out +=  "        '" + y + ",' + \n"
        out = out[:-6] + "' + \n"   
        out += '        "]"'
        f.write(out)

    def deleteJSON(self, index):
        jsonData = self.openJSON()
        tempJSON = []

        for x in range(len(jsonData)):
            if(x != index):
                tempJSON.append(str(jsonData[x]))

        f = open(self.dateipfad, "w")
        out = '\nvar data = "[" + \n'
        for x in tempJSON:
            y = str(x).replace("'", '"')
            out +=  "        '" + y + ",' + \n"
        out = out[:-6] + "' + \n"   
        out += '        "]"'
        f.write(out)

    def JSONWithPictureName(self, pictureName):

        pictureNameSplit = pictureName.split("_")

        title = ""
        year = ""
        format = ""
        technic = ""

        next = 0

        for x in range(len(pictureNameSplit)):
            if self.checkInt(pictureNameSplit[x]) == False:
                title += pictureNameSplit[x] + " "
            else:
                next = x
                break

        year = pictureNameSplit[next]
        next += 1
        formatArr = pictureNameSplit[next:(next+4)]
        format = " ".join(formatArr)
        next += 4
        technicArr = pictureNameSplit[next:]
        technic = " ".join(technicArr)

        data = []
        data.append(title[:-1])
        data.append(year)
        data.append(format)
        data.append(technic)

        return data
    
    def checkInt(self, data):
        try:
            x = int(data)
            return True
        except:
            return False

    def changeOrder(self, original, new):
        jsonData = self.openJSON()
        
        x = jsonData[original]
        jsonData.remove(x)
        jsonData.insert(new-1, x)

        f = open(self.dateipfad, "w")
        out = '\nvar data = "[" + \n'
        for x in jsonData:
            y = str(x).replace("'", '"')
            out +=  "        '" + y + ",' + \n"
        out = out[:-6] + "' + \n"   
        out += '        "]"'
        f.write(out)

    def changeDatei(self, id):
        if id == 1:
            self.dateipfad = os.path.abspath(".")+ "/Museum.js"
        elif id == 0:
            self.dateipfad = os.path.abspath(".")+ "/ImgDetails.js"

class JSONOpen(QWidget):
    def __init__(self, tool):
        super().__init__()
        self.tool = tool
        self.initUI()

    def initUI(self):
        self.setWindowTitle(TITLE)
        self.setGeometry(GEOMETRIE[0], GEOMETRIE[1], GEOMETRIE[2], GEOMETRIE[3])
        
        #Button
        self.button1 = QPushButton("Neues Album hinzufügen", self)
        self.button1.move(50, 50)
        self.button1.resize(300, 50)

        self.button2 = QPushButton("Bestehendes Album bearbeiten", self)
        self.button2.move(50, 150)
        self.button2.resize(300, 50)
        
        self.button3 = QPushButton("Reihenfolge der Alben ändern", self)
        self.button3.move(50, 250)
        self.button3.resize(300, 50)

class JSONAdd(QWidget):
    def __init__(self, tool):
        super().__init__()
        self.initUI()

        self.tool = tool
        self.trackList = []
        self.platformList = []
        # self.trackList = [["1._Unburdened_4.59", "Unburdened_4.59_A.mp3"],["2._Lighthearted_4.12", "Lighthearted_4.12_A.mp3"],["4._Under Water_3.17", "Under_Water_3.17_A.mp3"],["5._Maiocarina_2.48", "Maiocarina_2.48_A.mp3"],["6._Voyage_3.28", "Voyage_3.28_A.mp3"],["7._Mist in the Wood_4.17", "Mist_in_the_Wood_4.17_A.mp3"],["8._Prairie Whistler_2.50", "Prairie_Whistler_2.50_A.mp3"],["9._Hope_4.01", "Hope_4.01_A.mp3"],["10._Complete_Satisfaction_4.30", "Complete_Satisfaction_4.30_A.mp3"],["11._Serenity_3.04", "Serenity_3.04_A.mp3"],["12._Smooth_End_4.07", "Smooth_End_4.07_A.mp3"],["13._Easy_Listening_4.04", "Easy_Listening_4.04_A.mp3"],["14._Electric_Baroque_3.27", "Electric_Baroque_3.27_A.mp3"],["15._Holiday_Enjoyment_4:41", "Holiday_Enjoyment_4-41_A.mp3"]]
        # self.trackList = [["1._Spanish_Hopper_ I_7.28", "Spanish_Hopper_I_7.28_A.mp3"], ["2._Spanish_Hopper_II_4.37", "Spanish_Hopper_II_4.37_A.mp3"],["3._Spanish_Hopper_III_9.20", "Spanish_Hopper_III_9.20_A.mp3"], ["4._Spanish_Hopper_IV_7.58", "Spanish_Hopper_IV_7.58_A.mp3"], ["5._Spanish_Hopper_V_3.28", "Spanish_Hopper_V_3.28_A.mp3"], ["6._Spanish_Hopper_VI_2.39", "Spanish_Hopper_VI_2.39_A.mp3"], ["7._Spanish_Hopper_VII_3.25", "Spanish_Hopper_VII_3.25_A.mp3"], ["Spanish_Hopper_VIII_3.49", "Spanish_Hopper_VIII_3.49_A.mp3"], ["9._Spanish_Hopper_IX_7.08", "Spanish_Hopper_IX_7.08_A.mp3"], ["10._Nite_Nite_Little_Hopper_2.24", "Nite_Nite_Little_Hopper_2.24_A.mp3"], ["11._Childrens_Song_2.06", "Childrens_Song_2.06_A.mp3"], ["12._Little Anthem_2.30", "Little_Anthem_2.30_A.mp3"], ["13._Schmaltzy Western Song _2.49", "Schmaltzy_Western_Song_2.49_A.mp3"], ["14._Tender Melody_3.08", "Tender_Melody_3.08_A.mp3"]]
        # self.trackList = [["2. Michi`s_Song_II_2.01", "Michi`s_Song_II_2.01_A.mp3"], ["3. Michi`s_Song_III_4.29", "Michi`s_Song_III_4.29_A.mp3"], ["4. Michi`s_Song_IV_2.55", "Michi`s_Song_IV_2.55_A.mp3"], ["5. Michi`s_Song_V_6.51", "Michi`s_Song_V_6.51_A.mp3"], ["6. Michi`s_Song_VI_3.14", "Michi`s_Song_VI_3.14_A.mp3"], ["7. Michi`s_Song_VII_2.28", "Michi`s_Song_VII_2.28_A.mp3"], ["8. Michi`s_Song_VIII_3.19", "Michi`s_Song_VIII_3.19_A.mp3"], ["9. Michi`s_Song_IX_7.18", "Michi`s_Song_IX_7.18_A.mp3"], ["10. Michi`s_Song_X_4.47", "Michi`s_Song_X_4.47_A.mp3"], ["11. Michi`s_Song_XI_1.28", "Michi`s_Song_XI_1.28_A.mp3"], ["12. Michi`s_Song_XII_4.49", "Michi`s_Song_XII_4.49_A.mp3"]]
        # self.platformList = [["Spotify", "https://open.spotify.com/album/3sbBPRHvLiKkKZWiiRpYp2?si=z80F98_7SAmk7GR82uL8Cg"]]
        # self.platformList = [["Spotify", "https://open.spotify.com/album/5oCIMOmjnfDCj3mDvOy6xm?si=xRIKazEiTlGqYTNfc496gg"]]
        # self.platformList = [["Spotify", "https://open.spotify.com/album/4fgMAEP5iHc1A3tArxEM8t?si=U33VkckfRVmIbcvGNSgPTA"]]

    def initUI(self):
        self.setWindowTitle(TITLE)
        self.setGeometry(GEOMETRIEADD[0], GEOMETRIEADD[1], GEOMETRIEADD[2], GEOMETRIEADD[3])

        #Textfelder
        self.StilText = QLineEdit(self)
        self.StilText.move(200,50)
        self.StilText.resize(300, 40)

        self.NameText = QLineEdit(self)
        self.NameText.move(200,100)
        self.NameText.resize(300, 40)

        self.CoverText = QLineEdit(self)
        self.CoverText.move(320,150)
        self.CoverText.resize(180, 40)

        self.TextText = QLineEdit(self)
        self.TextText.move(200,200)
        self.TextText.resize(300, 40)

        self.TrackNameText = QLineEdit(self)
        self.TrackNameText.move(200,250)
        self.TrackNameText.resize(150, 40)

        self.TrackListView = QListWidget(self)
        self.TrackListView.move(200, 300)
        self.TrackListView.resize(300, 100)

        self.PlatformLinkText = QLineEdit(self)
        self.PlatformLinkText.move(200,450)
        self.PlatformLinkText.resize(300, 40)

        self.PlatformCombo = QComboBox(self)
        self.PlatformCombo.move(200, 500)
        self.PlatformCombo.resize(200, 40)
        self.PlatformCombo.addItems(["Apple Music", "Spotify", "Amazon Music", "Google Play", "YouTube Music", "Deezer", "7Digital", "Slacker", "Shazam", "Tidal", "Napster", "Rhapsody", "Yandex", "Pandora"])

        self.PlatformListView = QListWidget(self)
        self.PlatformListView.move(200, 550)
        self.PlatformListView.resize(300, 100)

        
        #Button
        self.selectCFile = QPushButton("Select", self)
        self.selectCFile.move(200, 150)
        self.selectCFile.resize(100, 30)
        self.selectCFile.clicked.connect(self.getCoverFile)

        self.selectTrack = QPushButton("Select", self)
        self.selectTrack.move(375, 250)
        self.selectTrack.resize(100, 30)
        self.selectTrack.clicked.connect(self.getTrackFile)

        self.setPlatform = QPushButton("Speichern", self)
        self.setPlatform.move(400, 500)
        self.setPlatform.resize(100, 30)
        self.setPlatform.clicked.connect(self.addPlatform)

        self.Bestätigen = QPushButton("Bestätigen", self)
        self.Bestätigen.move(50, 700)
        self.Bestätigen.resize(300, 50)
        self.Bestätigen.clicked.connect(self.on_button_clicked)

        self.homeButton = QPushButton("Home", self)
        self.homeButton.move(0, 0)
        self.homeButton.resize(60, 25)

        #Label
        self.StilLabel = QLabel("Stil:", self)
        self.StilLabel.move(150, 50)
        self.StilLabel.setFont(QFont("Arial", 18))

        self.NameLabel = QLabel("Albumname:", self)
        self.NameLabel.move(50, 100)
        self.NameLabel.setFont(QFont("Arial", 18))

        self.CFileLabel = QLabel("Coverfile:", self)
        self.CFileLabel.move(50, 150)
        self.CFileLabel.setFont(QFont("Arial", 18))

        self.TextLabel = QLabel("Text:", self)
        self.TextLabel.move(50, 200)
        self.TextLabel.setFont(QFont("Arial", 18))

        self.TrackLabel = QLabel("Track:", self)
        self.TrackLabel.move(50, 250)
        self.TrackLabel.setFont(QFont("Arial", 18))

        self.PlatformLabel = QLabel("Platformen:", self)
        self.PlatformLabel.move(50, 450)
        self.PlatformLabel.setFont(QFont("Arial", 18))


    def getCoverFile(self):
        fname = QFileDialog.getOpenFileName(self, 'Album Cover wählen', QStandardPaths.writableLocation(QStandardPaths.DesktopLocation) ,"Image files (*.jpg)")
        ifile = QFileInfo(str(fname[0]))
        
        self.CoverText.setText(ifile.fileName())

    def getTrackFile(self):
        if(self.TrackNameText.text() != ""):
            fname = QFileDialog.getOpenFileName(self, 'Track wählen', QStandardPaths.writableLocation(QStandardPaths.DesktopLocation) ,"Track files (*.mp3)")
            ifile = QFileInfo(str(fname[0]))
            if(ifile.fileName() != ""):
            # print(ifile.fileName()) #VERARBEITEN!
                self.TrackListView.addItem(self.TrackNameText.text())
                self.trackList.append([self.TrackNameText.text(), ifile.fileName()])
                
                self.TrackNameText.setText("")
        else:
            print("Erst Liedname auswählen")

    def addPlatform(self):
        if(self.PlatformLinkText.text() != ""):
            platform = self.PlatformCombo.currentText()
            link = self.PlatformLinkText.text()
            self.platformList.append([platform, link])
            
            self.PlatformListView.addItem(self.PlatformCombo.currentText())
            self.PlatformLinkText.setText("")
        else:
            print("Füge bitte noch einen Link hinzu")

    def on_button_clicked(self):
        if(self.StilText.text() == ""):
            print("Bitte einen Stil hinzufügen")
            return

        if(self.NameText.text() == ""):
            print("Bitte einen Namen hinzufügen")
            return

        if(self.TextText.text() == ""):
            print("Bitte einen Text hinzufügen")
            return

        if(self.CoverText.text() == ""):
            print("Bitte eine CoverDatei hinzufügen")
            return

        if(self.trackList == []):
            print("Bitte mind. einen Track hinzufügen")
            return

        jsonData = "{"
        jsonData += '"stile": "' + self.StilText.text() + '",'
        jsonData += '"albumname": "' + self.NameText.text() + '",'
        jsonData += '"coverfile": "' + self.CoverText.text() + '",'
        jsonData += '"text": "' + self.TextText.text() + '",'

        trackData = '"titles": ['
        for x in self.trackList:
            trackData += '{"title": "' + x[0] + '", "filename": "' + x[1] + '"},' 
        trackData = trackData[:-1] + ']'

        jsonData += trackData + ','

        platformData = '"links": ['
        for x in self.platformList:
            platformData += '{"platform": "' + x[0] + '", "link": "' + x[1] + '"},' 
        platformData = platformData[:-1] + ']'

        jsonData += platformData
        jsonData += "}"

        self.tool.appendNewJSON(jsonData)

        self.StilText.setText("")
        self.NameText.setText("")
        self.TextText.setText("")
        self.CoverText.setText("")
        self.trackList = []
        self.platformList = []
        self.TrackListView.clear()
        self.PlatformListView.clear()

        # if(self.textbox1.text() != "" and self.textbox2.text() != "" and self.textbox3.text() != "" and self.textbox4.text() != ""):
        #     jsonData2 = '{"title": "'+ self.textbox1.text() +'", "year": "'+ self.textbox2.text() +'", "format": "'+ self.textbox3.text() +'", "technic": "'+ self.textbox4.text() +'"}'
        #     self.tool.appendNewJSON(jsonData)
        #     self.textbox1.setText("")
        #     self.textbox2.setText("")
        #     self.textbox3.setText("")
        #     self.textbox4.setText("")
        #     self.label5.setText("JSON String erfolgreich erstellt und hinzugefügt")
        # else:
        #     self.label5.setText("Bitte fülle alle Felder aus")

class JSONEditTable(QWidget):
    def __init__(self, tool):
        super().__init__()
        self.initUI()

        self.tool = tool

    def initUI(self):
        self.setWindowTitle(TITLE)
        self.setGeometry(GEOMETRIETABLE[0], GEOMETRIETABLE[1], GEOMETRIETABLE[2], GEOMETRIETABLE[3])

        self.table = QTableWidget(self)
        self.table.resize(360, 400)
        self.table.move(0, 30)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Stil", "Albumname"])

        self.button = QPushButton("Ausgewählte Reihe ändern", self)
        self.button.move(20, 430)
        self.button.resize(260, 50)

        self.label = QLabel("", self)
        self.label.move(50, 550)
        self.label.setFont(QFont("Arial", 10))
        self.label.resize(300, 50)

        self.homeButton = QPushButton("Home", self)
        self.homeButton.move(0, 0)
        self.homeButton.resize(60, 25)

    def addTableRow(self):
        while (self.table.rowCount() > 0):
            self.table.removeRow(0)

        jsonData = self.tool.openJSON()

        for x in jsonData:
            row = self.table.rowCount()
            self.table.setRowCount(row+1)
            self.table.setItem(row, 0, QTableWidgetItem(str(x["stile"])))
            self.table.setItem(row, 1, QTableWidgetItem(str(x["albumname"])))
        self.table.resizeColumnsToContents()

class JSONEditString(QWidget):
    def __init__(self, tool):
        super().__init__()
        self.initUI()

        self.tool = tool
        self.trackList = []
        self.platformList = []

    def initUI(self):
        self.setWindowTitle(TITLE)
        self.setGeometry(GEOMETRIEADD[0], GEOMETRIEADD[1], GEOMETRIEADD[2], GEOMETRIEADD[3])

        #Textfelder
        self.StilText = QLineEdit(self)
        self.StilText.move(200,50)
        self.StilText.resize(300, 40)

        self.NameText = QLineEdit(self)
        self.NameText.move(200,100)
        self.NameText.resize(300, 40)

        self.CoverText = QLineEdit(self)
        self.CoverText.move(320,150)
        self.CoverText.resize(180, 40)

        self.TextText = QLineEdit(self)
        self.TextText.move(200,200)
        self.TextText.resize(300, 40)

        self.TrackNameText = QLineEdit(self)
        self.TrackNameText.move(200,250)
        self.TrackNameText.resize(150, 40)

        self.TrackFileText = QLineEdit(self)
        self.TrackFileText.move(370,270)
        self.TrackFileText.resize(130, 20)

        self.TrackListView = QListWidget(self)
        self.TrackListView.move(200, 300)
        self.TrackListView.resize(300, 100)
        self.TrackListView.clicked.connect(self.getTrackFile)

        self.PlatformLinkText = QLineEdit(self)
        self.PlatformLinkText.move(200,450)
        self.PlatformLinkText.resize(300, 40)

        self.PlatformCombo = QComboBox(self)
        self.PlatformCombo.move(200, 500)
        self.PlatformCombo.resize(200, 40)
        self.PlatformCombo.addItems(["Apple Music", "Spotify", "Amazon Music", "Google Play", "YouTube Music", "Deezer", "7Digital", "Slacker", "Shazam", "Tidal", "Napster", "Rhapsody", "Yandex", "Pandora"])

        self.PlatformListView = QListWidget(self)
        self.PlatformListView.move(200, 550)
        self.PlatformListView.resize(300, 100)
        self.PlatformListView.clicked.connect(self.getPlatformLink)

        
        #Button
        self.selectCFile = QPushButton("Select", self)
        self.selectCFile.move(200, 150)
        self.selectCFile.resize(100, 30)
        self.selectCFile.clicked.connect(self.getCoverFile)

        self.selectTrack = QPushButton("Select", self)
        self.selectTrack.move(370, 250)
        self.selectTrack.resize(130, 20)
        self.selectTrack.clicked.connect(self.addTrack)

        self.setPlatform = QPushButton("Speichern", self)
        self.setPlatform.move(400, 500)
        self.setPlatform.resize(100, 30)
        self.setPlatform.clicked.connect(self.addPlatform)

        self.Bestätigen = QPushButton("Bestätigen", self)
        self.Bestätigen.move(50, 700)
        self.Bestätigen.resize(300, 50)
        self.Bestätigen.clicked.connect(self.on_button_clicked)

        self.homeButton = QPushButton("Home", self)
        self.homeButton.move(0, 0)
        self.homeButton.resize(60, 25)

        #Label
        self.StilLabel = QLabel("Stil:", self)
        self.StilLabel.move(150, 50)
        self.StilLabel.setFont(QFont("Arial", 18))

        self.NameLabel = QLabel("Albumname:", self)
        self.NameLabel.move(50, 100)
        self.NameLabel.setFont(QFont("Arial", 18))

        self.CFileLabel = QLabel("Coverfile:", self)
        self.CFileLabel.move(50, 150)
        self.CFileLabel.setFont(QFont("Arial", 18))

        self.TextLabel = QLabel("Text:", self)
        self.TextLabel.move(50, 200)
        self.TextLabel.setFont(QFont("Arial", 18))

        self.TrackLabel = QLabel("Track:", self)
        self.TrackLabel.move(50, 250)
        self.TrackLabel.setFont(QFont("Arial", 18))

        self.PlatformLabel = QLabel("Platformen:", self)
        self.PlatformLabel.move(50, 450)
        self.PlatformLabel.setFont(QFont("Arial", 18))

    def loadString(self, number):
        self.number = number
        jsonData = self.tool.openJSON()
        self.StilText.setText(jsonData[number]["stile"])
        self.NameText.setText(jsonData[number]["albumname"])
        self.TextText.setText(jsonData[number]["text"])
        self.CoverText.setText(jsonData[number]["coverfile"])
        for x in jsonData[number]["titles"]:
            self.trackList.append([x["title"], x["filename"]])
        for x in jsonData[number]["links"]:
            self.platformList.append([x["platform"], x["link"]])

        for x in self.trackList:
            self.TrackListView.addItem(x[0])

        for x in self.platformList:
            self.PlatformListView.addItem(x[0])

    def getCoverFile(self):
        fname = QFileDialog.getOpenFileName(self, 'Album Cover wählen', QStandardPaths.writableLocation(QStandardPaths.DesktopLocation) ,"Image files (*.jpg)")
        ifile = QFileInfo(str(fname[0]))
        
        self.CoverText.setText(ifile.fileName())

    # def getTrackFile(self):
    #     if(self.TrackNameText.text() != ""):
    #         fname = QFileDialog.getOpenFileName(self, 'Track wählen', QStandardPaths.writableLocation(QStandardPaths.DesktopLocation) ,"Track files (*.mp3)")
    #         ifile = QFileInfo(str(fname[0]))
    #         if(ifile.fileName() != ""):
    #         # print(ifile.fileName()) #VERARBEITEN!
    #             self.TrackListView.addItem(self.TrackNameText.text())
    #             self.trackList.append([self.TrackNameText.text(), ifile.fileName()])
                
    #             self.TrackNameText.setText("")
    #     else:
    #         print("Erst Liedname auswählen")

    def addTrack(self):
        if(self.getTrackIndex(self.TrackNameText.text()) != None):
            self.trackList[self.getTrackIndex(self.TrackNameText.text())][1] = self.TrackFileText.text()
            self.TrackFileText.setText("")
            self.TrackNameText.setText("")
        else:
            if(self.TrackNameText.text() != ""):
                fname = QFileDialog.getOpenFileName(self, 'Track wählen', QStandardPaths.writableLocation(QStandardPaths.DesktopLocation) ,"Track files (*.mp3)")
                ifile = QFileInfo(str(fname[0]))
                if(ifile.fileName() != ""):
                # print(ifile.fileName()) #VERARBEITEN!
                    self.TrackListView.addItem(self.TrackNameText.text())
                    self.trackList.append([self.TrackNameText.text(), ifile.fileName()])
                    
                    self.TrackNameText.setText("")
            else:
                print("Erst Liedname auswählen")

    def getTrackFile(self):
        self.TrackNameText.setText(self.trackList[self.getTrackIndex(self.TrackListView.currentIndex().data())][0])
        self.TrackFileText.setText(self.trackList[self.getTrackIndex(self.TrackListView.currentIndex().data())][1])

    def getTrackIndex(self, track):
        for x in range(len(self.trackList)):
            if(self.trackList[x][0] == track):
                return x
        return None

    def addPlatform(self):
        if(self.getPlatformIndex(self.PlatformCombo.currentText()) != None):
            if(self.PlatformLinkText.text() != ""):
                self.platformList[self.getPlatformIndex(self.PlatformCombo.currentText())][1] = self.PlatformLinkText.text()
                self.PlatformLinkText.setText("")
            else:
                print("Füge bitte noch einen Link hinzu")

        elif(self.PlatformLinkText.text() != ""):
            platform = self.PlatformCombo.currentText()
            link = self.PlatformLinkText.text()
            self.platformList.append([platform, link])
            
            self.PlatformListView.addItem(self.PlatformCombo.currentText())
            self.PlatformLinkText.setText("")
        else:
            print("Füge bitte noch einen Link hinzu")

    def getPlatformLink(self):
        self.PlatformLinkText.setText(self.platformList[self.getPlatformIndex(self.PlatformListView.currentIndex().data())][1])
        self.PlatformCombo.setCurrentText(self.PlatformListView.currentIndex().data())


    def getPlatformIndex(self, platform):
        for x in range(len(self.platformList)):
            if(self.platformList[x][0] == platform):
                return x
        return None

    def on_button_clicked(self):
        if(self.StilText.text() == ""):
            print("Bitte einen Stil hinzufügen")
            return

        if(self.NameText.text() == ""):
            print("Bitte einen Namen hinzufügen")
            return

        if(self.TextText.text() == ""):
            print("Bitte einen Text hinzufügen")
            return

        if(self.CoverText.text() == ""):
            print("Bitte eine CoverDatei hinzufügen")
            return

        if(self.trackList == []):
            print("Bitte mind. einen Track hinzufügen")
            return

        jsonData = "{"
        jsonData += '"stile": "' + self.StilText.text() + '",'
        jsonData += '"albumname": "' + self.NameText.text() + '",'
        jsonData += '"coverfile": "' + self.CoverText.text() + '",'
        jsonData += '"text": "' + self.TextText.text() + '",'

        trackData = '"titles": ['
        for x in self.trackList:
            trackData += '{"title": "' + x[0] + '", "filename": "' + x[1] + '"},' 
        trackData = trackData[:-1] + ']'

        jsonData += trackData + ','

        platformData = '"links": ['
        for x in self.platformList:
            platformData += '{"platform": "' + x[0] + '", "link": "' + x[1] + '"},' 
        platformData = platformData[:-1] + ']'

        jsonData += platformData
        jsonData += "}"

        self.tool.editJSON(self.number, jsonData)

        self.StilText.setText("")
        self.NameText.setText("")
        self.TextText.setText("")
        self.CoverText.setText("")
        self.trackList = []
        self.platformList = []
        self.TrackListView.clear()
        self.PlatformListView.clear()

class JSONChangeOrder(QWidget):
    def __init__(self, tool):
        super().__init__()
        self.initUI()

        self.tool = tool

    def initUI(self):
        self.setWindowTitle(TITLE)
        self.setGeometry(GEOMETRIETABLE[0], GEOMETRIETABLE[1], GEOMETRIETABLE[2], GEOMETRIETABLE[3])

        self.table = QTableWidget(self)
        self.table.resize(360, 400)
        self.table.move(0, 30)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Stil", "Albumname"])

        self.button = QPushButton("Ausgewählte Reihe ändern", self)
        self.button.move(10, 430)
        self.button.resize(200, 50)

        self.lineEdit = QLineEdit(self)
        self.lineEdit.move(220, 430)
        self.lineEdit.resize(50, 50)
        self.lineEdit.setValidator(QIntValidator())

        self.label = QLabel("", self)
        self.label.move(50, 550)
        self.label.setFont(QFont("Arial", 10))
        self.label.resize(300, 50)

        self.homeButton = QPushButton("Home", self)
        self.homeButton.move(0, 0)
        self.homeButton.resize(60, 25)

    def addTableRow(self):
        while (self.table.rowCount() > 0):
            self.table.removeRow(0)

        jsonData = self.tool.openJSON()

        for x in jsonData:
            row = self.table.rowCount()
            self.table.setRowCount(row+1)
            self.table.setItem(row, 0, QTableWidgetItem(str(x["stile"])))
            self.table.setItem(row, 1, QTableWidgetItem(str(x["albumname"])))
        self.table.resizeColumnsToContents()


if __name__ == "__main__":
    App = QApplication(sys.argv)

    JTool = JSONTool()
    openGui = JSONOpen(JTool)
    addGui = JSONAdd(JTool)
    editTableGui = JSONEditTable(JTool)
    editStringGui = JSONEditString(JTool)
    changeGui = JSONChangeOrder(JTool)

    def on_click_add():
        addGui.show()
        openGui.hide()

    def on_click_edit():
        editTableGui.show()
        editTableGui.addTableRow()
        openGui.hide()

    def on_click_change():
        changeGui.show()
        changeGui.addTableRow()
        openGui.hide()

    def on_click_editRow():
        indexes = editTableGui.table.selectionModel().selectedRows()
        if len(indexes) > 0:
            for index in sorted(indexes):
                #print('Row %d is selected' % index.row())
                editStringGui.loadString(int("%d" % index.row()))

            editStringGui.show()
            editTableGui.hide()
            editTableGui.label.setText("")
            
        else:
            editTableGui.label.setText("Bitte wähle ein Reihe aus")
    
    def on_click_changeOrder():
        indexes = changeGui.table.selectionModel().selectedRows()
        if len(indexes) > 0:
            for index in sorted(indexes):
                #print('Row %d is selected' % index.row())
                original = (int("%d" % index.row()))
        new = int(changeGui.lineEdit.text())
        changeGui.tool.changeOrder(original, new)
        changeGui.addTableRow()

    def on_click_home():
        openGui.show()
        try:
            editTableGui.hide()
        except:
            pass
        try:
            editStringGui.hide()
        except:
            pass
        try:
            addGui.hide()
        except:
            pass
        try:
            changeGui.hide()
        except:
            pass

    openGui.button1.clicked.connect(on_click_add)
    openGui.button2.clicked.connect(on_click_edit)
    openGui.button3.clicked.connect(on_click_change)
    
    changeGui.button.clicked.connect(on_click_changeOrder)
    editTableGui.button.clicked.connect(on_click_editRow)

    addGui.homeButton.clicked.connect(on_click_home)
    editTableGui.homeButton.clicked.connect(on_click_home)
    editStringGui.homeButton.clicked.connect(on_click_home)
    changeGui.homeButton.clicked.connect(on_click_home)

    openGui.show()
    # addGui.show()
    sys.exit(App.exec_())