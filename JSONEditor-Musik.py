# -*- coding: utf-8 -*-

import json
import os
import sys
import time
import logging

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import *
from PyQt5.QtWidgets import *

class JSONTool():
    def __init__(self):
        self.dateipfad = os.path.abspath(".")+ "/CMS.js"
    
    def openJSON(self):
        # Datei öffnen
        f = open(self.dateipfad, "r", encoding="utf-8")
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

        newJsonString = newJsonString.replace("'", "´")

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

        editJsonString = editJsonString.replace("'", "´")
        jsonData[index] = editJsonString

        f = open(self.dateipfad, "w", encoding="utf-8")
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

class JSONEditor():
    def __init__(self):
        self.mainApp = QApplication(sys.argv)
        self.mainGui = loadUi("Musik.ui")
        self.mainGui.stackedWidget.setCurrentIndex(0)
        self.mainGui.show()
        self.mainGui.albumstilBox.addItems(["", "E-Musik", "U-Musik", "C-Musik"])
        self.mainGui.comboBox.addItems(["Not Released", "Apple Music", "Spotify", "Amazon Music", "Google Play", "YouTube Music", "Deezer", "7Digital", "Slacker", "Shazam", "Tidal", "Napster", "Rhapsody", "Yandex", "Pandora"])

        self.tool = JSONTool()
        self.MODE = ""
        self.trackList = []
        self.platformList = []
        self.aktNumber = None
        self.selectedTitleRow = None
        self.selectedPlatformRow = None
        self.directory = QStandardPaths.writableLocation(QStandardPaths.DesktopLocation)

        self.connectButtons()
        
        sys.exit(self.mainApp.exec_())

    def connectButtons(self):
        #HomeButton
        self.mainGui.homeButton.clicked.connect(lambda: self.changePage("open"))

        #OpenButton
        self.mainGui.openAddGui.clicked.connect(lambda: self.changePage("add"))
        self.mainGui.openEditGui.clicked.connect(lambda: self.changePage("editTab"))
        self.mainGui.openChangeOrderGui.clicked.connect(lambda: self.changePage("changeOrder"))

        #AddButton
        self.mainGui.coverButton.clicked.connect(lambda: self.addManager("cover"))
        self.mainGui.trackButton.clicked.connect(lambda: self.addManager("track"))
        self.mainGui.platformButton.clicked.connect(lambda: self.addManager("platform"))
        self.mainGui.saveButton.clicked.connect(lambda: self.addManager("final"))
        self.mainGui.trackDeleteButton.clicked.connect(lambda: self.addManager("removeTitle"))
        self.mainGui.platformDeleteButton.clicked.connect(lambda: self.addManager("removePlatform"))

        #Table
        self.mainGui.selectRowButton.clicked.connect(lambda: self.tableManager())

        #Listen
        # self.mainGui.trackListView.clicked.connect(lambda: self.getTrackFile())
        self.mainGui.trackListView.clicked.connect(lambda: self.selectTitle())
        self.mainGui.platformListView.clicked.connect(lambda: self.selectPlatform())
        self.mainGui.platformListView.clicked.connect(lambda: self.getPlatformLink())

    def changePage(self, page):
        if(page == "open"):
            self.mainGui.infoLabel.setText("")
            self.mainGui.caption.setText("Auswahlseite")
            self.mainGui.stackedWidget.setCurrentIndex(0) 
        elif(page == "add"):
            self.mainGui.infoLabel.setText("")
            self.MODE = "create"
            self.mainGui.caption.setText("Neues Album hinzufügen")
            self.mainGui.stackedWidget.setCurrentIndex(1)
            self.clearText()
        elif(page == "editTab"):
            self.mainGui.infoLabel.setText("")
            self.MODE = "edit"
            self.mainGui.caption.setText("Album zum bearbeiten auswählen")
            self.mainGui.stackedWidget.setCurrentIndex(2)
            self.fillTableRows()
            self.mainGui.selectRowButton.setText("Ausgewählte Reihe \n bearbeiten")
        elif(page == "edit"):
            self.mainGui.infoLabel.setText("")
            self.MODE = "edit"
            self.mainGui.caption.setText("Album bearbeiten")
            self.mainGui.stackedWidget.setCurrentIndex(1)
            self.mainGui.trackDeleteButton.setHidden(False)
        elif(page == "changeOrder"):
            self.mainGui.infoLabel.setText("")
            self.MODE = "changeOrder"
            self.mainGui.caption.setText("Alben Reihenfolge ändern")
            self.mainGui.stackedWidget.setCurrentIndex(2)
            self.fillTableRows()
            self.mainGui.lineText.setHidden(False)
            self.mainGui.selectRowButton.setText("Ausgewählte Reihe \n verschieben")

    def addManager(self, action):
        if(action == "cover"):
            self.getCoverFile()
        elif(action == "track"):
            self.addTrack()
        elif(action == "platform"):
            self.addPlatform()
        elif(action == "final"):
            self.final()
        elif(action == "removeTitle"):
            self.removeTitle()
        elif(action == "removePlatform"):
            self.removePlatform()

    def tableManager(self):
        if(self.MODE == "edit"):
            self.callEditRow()
        elif(self.MODE == "changeOrder"):
            self.changeOrder()

    def selectTitle(self):
        try:
            self.selectedTitleRow = self.mainGui.trackListView.currentRow()
        except Exception as Argument:
            self.error("selectTitle", Argument)

    def removeTitle(self):
        try:
            if self.selectedTitleRow != None:
                self.trackList.remove(self.trackList[self.selectedTitleRow])
                self.selectedTitleRow = None
                self.clearText()
                self.fillText(self.aktNumber)
        except Exception as Argument:
            self.error("removeTitle", Argument)

    def getCoverFile(self):
        try:
            fname = QFileDialog.getOpenFileName(caption='Album Cover wählen', directory=self.directory , filter="Image files (*.jpg)")
            ifile = QFileInfo(str(fname[0]))
            if(ifile.fileName() != ""):
                self.directory = ifile.path()
                self.mainGui.coverfileText.setText(ifile.fileName())
        except Exception as Argument:
            self.error("getCoverFile", Argument)

    def addTrack(self):
        try:
            fname = QFileDialog.getOpenFileName(caption='Track wählen', directory=self.directory , filter="Track files (*.mp3)")
            ifile = QFileInfo(str(fname[0]))
            if(ifile.fileName() != ""):
                self.directory = ifile.path()
                self.mainGui.trackListView.addItem(ifile.fileName())
                # self.trackList.append([ifile.fileName(), ifile.fileName()])
                self.trackList.append([ifile.fileName()])
        except Exception as Argument:
            self.error("addTrack", Argument)

    def addPlatform(self):
        try:
            if(self.getPlatformIndex(self.mainGui.comboBox.currentText()) != None):
                if(self.mainGui.platformlinkText.text() != ""):
                    self.platformList[self.getPlatformIndex(self.mainGui.comboBox.currentText())][1] = self.mainGui.platformlinkText.text()
                    self.mainGui.platformlinkText.setText("")
                else:
                    print("Füge bitte noch einen Link hinzu")

            elif(self.mainGui.platformlinkText.text() != ""):
                platform = self.mainGui.comboBox.currentText()
                link = self.mainGui.platformlinkText.text()
                self.platformList.append([platform, link])
                
                self.mainGui.platformListView.addItem(self.mainGui.comboBox.currentText())
                self.mainGui.platformlinkText.setText("")
            else:
                print("Füge bitte noch einen Link hinzu")
        except Exception as Argument:
            self.error("addPlatform", Argument)

    def selectPlatform(self):
        try:
            self.selectedPlatformRow = self.mainGui.platformListView.currentRow()
        except Exception as Argument:
            self.error("selectPlatform", Argument)

    def removePlatform(self):
        try:
            if self.selectedPlatformRow != None:
                self.platformList.remove(self.platformList[self.selectedPlatformRow])
                self.selectedPlatformRow = None
                self.clearText()
                self.fillText(self.aktNumber)
        except Exception as Argument:
            self.error("removePlatform", Argument)

    def final(self):
        # try:
            if(self.mainGui.albumstilBox.currentText() == ""):
                print("Bitte einen Stil hinzufügen")
                return

            if(self.mainGui.albumnameText.text() == ""):
                print("Bitte einen Namen hinzufügen")
                return

            if(self.mainGui.coverfileText.text() == ""):
                print("Bitte eine CoverDatei hinzufügen")
                return

            if(self.mainGui.promoText.text() == ""):
                print("Bitte einen Text hinzufügen")
                return

            if(self.trackList == []):
                print("Bitte mind. einen Track hinzufügen")
                return
                
            jsonData = "{"
            jsonData += '"stile": "' + self.mainGui.albumstilBox.currentText() + '",'
            jsonData += '"albumname": "' + self.mainGui.albumnameText.text() + '",'
            jsonData += '"coverfile": "' + self.mainGui.coverfileText.text() + '",'
            jsonData += '"text": "' + self.mainGui.promoText.text() + '",'

            trackData = '"titles": ['
            for x in self.trackList:
                # trackData += '{"title": "' + x[0] + '", "filename": "' + x[1] + '"},'
                trackData += '{"title": "' + x[0] + '"},' 
            trackData = trackData[:-1] + ']'

            jsonData += trackData + ','

            platformData = '"links": ['
            for x in self.platformList:
                platformData += '{"platform": "' + x[0] + '", "link": "' + x[1] + '"},' 
            platformData = platformData[:-1] + ']'

            jsonData += platformData
            jsonData += "}"


            if(self.MODE == "create"):
                self.tool.appendNewJSON(jsonData)
            elif(self.MODE == "edit"):
                self.tool.editJSON(self.number, jsonData)

            self.mainGui.albumstilBox.setCurrentIndex(0)
            self.mainGui.albumnameText.setText("")
            self.mainGui.promoText.setText("")
            self.mainGui.coverfileText.setText("")
            self.trackList = []
            self.platformList = []
            self.mainGui.trackListView.clear()
            self.mainGui.platformListView.clear()

            self.mainGui.infoLabel.setText("Erfolgreich gespeichert")
        # except Exception as Argument:
        #     self.error("final", Argument)

    def fillText(self, number):
        try:
            self.number = number
            jsonData = self.tool.openJSON()
            self.mainGui.albumstilBox.setCurrentIndex(self.mainGui.albumstilBox.findText(jsonData[number]["stile"]))
            self.mainGui.albumnameText.setText(jsonData[number]["albumname"])
            self.mainGui.promoText.setText(jsonData[number]["text"])
            self.mainGui.coverfileText.setText(jsonData[number]["coverfile"])

            if(self.trackList == []):
                for x in jsonData[number]["titles"]:
                    # self.trackList.append([x["title"], x["filename"]])
                    self.trackList.append([x["title"]])
            if(self.platformList == []):
                for x in jsonData[number]["links"]:
                    self.platformList.append([x["platform"], x["link"]])

            for x in self.trackList:
                self.mainGui.trackListView.addItem(x[0])

            for x in self.platformList:
                self.mainGui.platformListView.addItem(x[0])
        except Exception as Argument:
            self.error("fillText", Argument)

    def clearText(self):
        try:
            self.mainGui.albumstilBox.itemText(0)
            self.mainGui.albumnameText.setText("")
            self.mainGui.promoText.setText("")
            self.mainGui.coverfileText.setText("")
            # self.mainGui.tracknameText.setText("")
            # self.mainGui.trackFileText.setText("")
            self.mainGui.platformlinkText.setText("")

            self.mainGui.trackListView.clear()
            self.mainGui.platformListView.clear()
        except Exception as Argument:
            self.error("clearText", Argument)

    def getPlatformLink(self):
        try: 
            self.mainGui.platformlinkText.setText(self.platformList[self.getPlatformIndex(self.mainGui.platformListView.currentIndex().data())][1])
            self.mainGui.comboBox.setCurrentText(self.mainGui.platformListView.currentIndex().data())
        except Exception as Argument:
            self.error("getPlatformLink", Argument)

    def getPlatformIndex(self, platform):
        try:
            for x in range(len(self.platformList)):
                if(self.platformList[x][0] == platform):
                    return x
            return None
        except Exception as Argument:
            self.error("getPlatformIndex", Argument)
    
    def fillTableRows(self):
        try:
            while (self.mainGui.tableWidget.rowCount() > 0):
                self.mainGui.tableWidget.removeRow(0)

            jsonData = self.tool.openJSON()

            for x in jsonData:
                row = self.mainGui.tableWidget.rowCount()
                self.mainGui.tableWidget.setRowCount(row+1)
                self.mainGui.tableWidget.setItem(row, 0, QTableWidgetItem(str(x["stile"])))
                self.mainGui.tableWidget.setItem(row, 1, QTableWidgetItem(str(x["albumname"])))
            self.mainGui.tableWidget.resizeColumnsToContents()
        except Exception as Argument:
            self.error("fillTableRows", Argument)

    def changeOrder(self):
        try:
            indexes = self.mainGui.tableWidget.selectionModel().selectedRows()
            if len(indexes) > 0:
                for index in sorted(indexes):
                    #print('Row %d is selected' % index.row())
                    original = (int("%d" % index.row()))
            new = int(self.mainGui.lineText.text())
            self.tool.changeOrder(original, new)
            self.fillTableRows()
            self.mainGui.infoLabel.setText("Reihen ändern")
        except Exception as Argument:
            if(str(Argument) == "invalid literal for int() with base 10: ''"):
                self.hinweis("Es muss eine Stelle angegeben werden, \nwohin verschoben werden soll")
            elif(str(Argument) == "local variable 'original' referenced before assignment"):
                self.hinweis("Es muss ein Eintrag ausgewählt sein, \nder Verschoben werden soll")
            else:
                self.error("changeOrder", Argument)

    def callEditRow(self):
        try:
            indexes = self.mainGui.tableWidget.selectionModel().selectedRows()
            if len(indexes) > 0:
                for index in sorted(indexes):
                    #print('Row %d is selected' % index.row())
                    self.clearText()
                    self.trackList = []
                    self.platformList = []
                    self.aktNumber = int("%d" % index.row())
                    self.fillText(self.aktNumber)

                self.changePage("edit")
                
            else:
                editTableGui.label.setText("Bitte wähle ein Reihe aus")
        except Exception as Argument:
            self.error("callEditRow", Argument)

    def hinweis(self, hinweis):
        msg = QMessageBox()
        msg.setWindowTitle("Ein bekanntes Problem ist aufgetreten")
        msg.setText(hinweis)
        msg.setIcon(QMessageBox.Information)
        x = msg.exec_()

    def error(self, stelle, Argument):
        print(stelle, Argument)

        f = open("errorlog.txt", "a")
        f.write(stelle + ":" + str(Argument) + "\n\n")
        f.close()

        msg = QMessageBox()
        msg.setWindowTitle("Ein Fehler ist aufgetreten")
        msg.setText("Es ist ein unbekannter Fehler aufgetreten. \nDer Fehler wurde der Textdatei hinzugefügt.")
        msg.setIcon(QMessageBox.Critical)
        x = msg.exec_()

JE = JSONEditor()