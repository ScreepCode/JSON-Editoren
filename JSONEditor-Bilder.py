# -*- coding: utf-8 -*-

import json
import os
import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

GEOMETRIE = [300, 200, 400, 600]
GEOMETRIETABLE = [300, 200, 700, 600]

class JSONTool(object):
    def __init__(self):
       self.dateipfad = os.path.abspath(".")+ "/ImgDetails.js"
       #self.dateipfad = os.path.abspath(".")+ "/json.js"
       #self.dateipfad = "Users/detlefhommel/Desktop/WebSeites/json/ImgDetails.js"
    
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
        self.title = "JSON Parser"
        self.tool = tool
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(GEOMETRIE[0], GEOMETRIE[1], GEOMETRIE[2], GEOMETRIE[3])

        #Combobox
        self.cb = QComboBox(self)
        self.cb.addItems(["ImgDetails", "Museum"])
        self.cb.move(50, 50)
        self.cb.resize(300, 20)
        self.cb.currentIndexChanged.connect(self.tool.changeDatei)
        
        #Button
        self.button1 = QPushButton("Neuen JSON String hinzufügen", self)
        self.button1.move(50, 100)
        self.button1.resize(300, 50)

        self.button2 = QPushButton("Bestehenden JSON String bearbeiten", self)
        self.button2.move(50, 200)
        self.button2.resize(300, 50)
        
        self.button3 = QPushButton("Bestehenden JSON String entfernen", self)
        self.button3.move(50, 300)
        self.button3.resize(300, 50)

        self.button4 = QPushButton("Neuen JSON String mit Bildtitel hinzufügen", self)
        self.button4.move(50, 400)
        self.button4.resize(300, 50)

        self.button5 = QPushButton("Reihenfolge der Bilder ändern", self)
        self.button5.move(50, 500)
        self.button5.resize(300, 50)

class JSONAdd(QWidget):
    def __init__(self, tool):
        super().__init__()
        self.title = "JSON Parser"
        self.initUI()

        self.tool = tool

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(GEOMETRIE[0], GEOMETRIE[1], GEOMETRIE[2], GEOMETRIE[3])

        #Textfelder
        self.textbox1 = QLineEdit(self)
        self.textbox1.move(50,100)
        self.textbox1.resize(300, 50)

        self.textbox2 = QLineEdit(self)
        self.textbox2.move(50,200)
        self.textbox2.resize(300, 50)

        self.textbox3 = QLineEdit(self)
        self.textbox3.move(50,300)
        self.textbox3.resize(300, 50)

        self.textbox4 = QLineEdit(self)
        self.textbox4.move(50,400)
        self.textbox4.resize(300, 50)

        #Button
        self.button = QPushButton("Bestätigen", self)
        self.button.move(50, 500)
        self.button.resize(300, 50)
        self.button.clicked.connect(self.on_button_clicked)

        #Label
        self.label1 = QLabel("Title", self)
        self.label1.move(50, 75)
        self.label1.setFont(QFont("Arial", 18))

        self.label2 = QLabel("Year", self)
        self.label2.move(50, 175)
        self.label2.setFont(QFont("Arial", 18))

        self.label3 = QLabel("Format", self)
        self.label3.move(50, 275)
        self.label3.setFont(QFont("Arial", 18))

        self.label4 = QLabel("Technic", self)
        self.label4.move(50, 375)
        self.label4.setFont(QFont("Arial", 18))

        self.label5 = QLabel("", self)
        self.label5.move(50, 550)
        self.label5.setFont(QFont("Arial", 10))
        self.label5.resize(300, 50)

        self.homeButton = QPushButton("Home", self)
        self.homeButton.move(0, 0)
        self.homeButton.resize(60, 25)

    def on_button_clicked(self):
        if(self.textbox1.text() != "" and self.textbox2.text() != "" and self.textbox3.text() != "" and self.textbox4.text() != ""):
            jsonData = '{"title": "'+ self.textbox1.text() +'", "year": "'+ self.textbox2.text() +'", "format": "'+ self.textbox3.text() +'", "technic": "'+ self.textbox4.text() +'"}'
            self.tool.appendNewJSON(jsonData)
            self.textbox1.setText("")
            self.textbox2.setText("")
            self.textbox3.setText("")
            self.textbox4.setText("")
            self.label5.setText("JSON String erfolgreich erstellt und hinzugefügt")
        else:
            self.label5.setText("Bitte fülle alle Felder aus")

class JSONEditTable(QWidget):
    def __init__(self, tool):
        super().__init__()
        self.title = "JSON Parser"
        self.initUI()

        self.tool = tool

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(GEOMETRIETABLE[0], GEOMETRIETABLE[1], GEOMETRIETABLE[2], GEOMETRIETABLE[3])

        self.table = QTableWidget(self)
        self.table.resize(700, 500)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Title", "Year", "Format", "Technic"])

        self.button = QPushButton("Ausgewählte Reihe ändern", self)
        self.button.move(50, 500)
        self.button.resize(300, 50)

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
            self.table.setItem(row, 0, QTableWidgetItem(str(x["title"])))
            self.table.setItem(row, 1, QTableWidgetItem(str(x["year"])))
            self.table.setItem(row, 2, QTableWidgetItem(str(x["format"])))
            self.table.setItem(row, 3, QTableWidgetItem(str(x["technic"])))
        self.table.resizeColumnsToContents()

class JSONEditString(QWidget):
    def __init__(self, tool):
        super().__init__()
        self.title = "JSON Parser"
        self.initUI()

        self.tool = tool

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(GEOMETRIE[0], GEOMETRIE[1], GEOMETRIE[2], GEOMETRIE[3])

        #Textfelder
        self.textbox1 = QLineEdit(self)
        self.textbox1.move(50,100)
        self.textbox1.resize(300, 50)

        self.textbox2 = QLineEdit(self)
        self.textbox2.move(50,200)
        self.textbox2.resize(300, 50)

        self.textbox3 = QLineEdit(self)
        self.textbox3.move(50,300)
        self.textbox3.resize(300, 50)

        self.textbox4 = QLineEdit(self)
        self.textbox4.move(50,400)
        self.textbox4.resize(300, 50)

        #Button
        self.button = QPushButton("Bestätigen", self)
        self.button.move(50, 500)
        self.button.resize(300, 50)

        #Label
        self.label1 = QLabel("Title", self)
        self.label1.move(50, 75)
        self.label1.setFont(QFont("Arial", 18))

        self.label2 = QLabel("Year", self)
        self.label2.move(50, 175)
        self.label2.setFont(QFont("Arial", 18))

        self.label3 = QLabel("Format", self)
        self.label3.move(50, 275)
        self.label3.setFont(QFont("Arial", 18))

        self.label4 = QLabel("Technic", self)
        self.label4.move(50, 375)
        self.label4.setFont(QFont("Arial", 18))

        self.label5 = QLabel("", self)
        self.label5.move(50, 550)
        self.label5.setFont(QFont("Arial", 10))
        self.label5.resize(300, 50)

        self.homeButton = QPushButton("Home", self)
        self.homeButton.move(0, 0)
        self.homeButton.resize(60, 25)

    def loadString(self, number):
        self.number = number
        jsonData = self.tool.openJSON()
        self.textbox1.setText(jsonData[number]["title"])
        self.textbox2.setText(jsonData[number]["year"])
        self.textbox3.setText(jsonData[number]["format"])
        self.textbox4.setText(jsonData[number]["technic"])

    def buttonFunction(self):
        if(self.textbox1.text() != "" and self.textbox2.text() != "" and self.textbox3.text() != "" and self.textbox4.text() != ""):
            editJsonData = '{"title": "'+ self.textbox1.text() +'", "year": "'+ self.textbox2.text() +'", "format": "'+ self.textbox3.text() +'", "technic": "'+ self.textbox4.text() +'"}'
            self.tool.editJSON(self.number, editJsonData)
            self.textbox1.setText("")
            self.textbox2.setText("")
            self.textbox3.setText("")
            self.textbox4.setText("")

            self.label5.setText("JSON String erfolgreich geändert")
            return True
        else:
            self.label5.setText("Es darf kein Textfeld leer sein")
            return False

class JSONDelete(QWidget):
    def __init__(self, tool):
        super().__init__()
        self.title = "JSON Parser"
        self.initUI()

        self.tool = tool

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(GEOMETRIETABLE[0], GEOMETRIETABLE[1], GEOMETRIETABLE[2], GEOMETRIETABLE[3])

        self.table = QTableWidget(self)
        self.table.resize(700, 500)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Title", "Year", "Format", "Technic"])

        self.button = QPushButton("Reihe Auswählen", self)
        self.button.move(50, 500)
        self.button.resize(300, 50)
        self.button.clicked.connect(self.pick_row)

        self.button2 = QPushButton("Reihe löschen", self)
        self.button2.move(360, 500)
        self.button2.resize(300, 50)
        self.button2.clicked.connect(self.call_delete)
        self.button2.setEnabled(False)

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
            self.table.setItem(row, 0, QTableWidgetItem(str(x["title"])))
            self.table.setItem(row, 1, QTableWidgetItem(str(x["year"])))
            self.table.setItem(row, 2, QTableWidgetItem(str(x["format"])))
            self.table.setItem(row, 3, QTableWidgetItem(str(x["technic"])))
        self.table.resizeColumnsToContents()

    def pick_row(self):
        indexes = self.table.selectionModel().selectedRows()
        if len(indexes) > 0:
            for index in sorted(indexes):
                #print('Row %d is selected' % index.row())
                self.selectedRow = (int("%d" % index.row()))
                self.button2.setText("Reihe " + str(self.selectedRow+1) + " löschen")
                self.button2.setEnabled(True)

    def call_delete(self):
        self.tool.deleteJSON(self.selectedRow)
        self.button2.setEnabled(False)
        self.button2.setText("Reihe löschen")
        self.addTableRow()

class JSONAddWT(QWidget):
    def __init__(self, tool):
        super().__init__()
        self.title = "JSON Parser"
        self.initUI()

        self.tool = tool

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(100, 100, 400, 600)

        #Textfelder
        self.textbox1 = QLineEdit(self)
        self.textbox1.move(50,325)
        self.textbox1.resize(300, 20)

        self.textbox2 = QLineEdit(self)
        self.textbox2.move(50,375)
        self.textbox2.resize(300, 20)

        self.textbox3 = QLineEdit(self)
        self.textbox3.move(50,425)
        self.textbox3.resize(300, 20)

        self.textbox4 = QLineEdit(self)
        self.textbox4.move(50,475)
        self.textbox4.resize(300, 20)

        self.textbox5 = QLineEdit(self)
        self.textbox5.move(50, 130)
        self.textbox5.resize(300, 50)

        #Button
        self.button = QPushButton("Bestätigen", self)
        self.button.move(50, 500)
        self.button.resize(300, 30)
        self.button.clicked.connect(self.on_button_clicked)
        self.button.setEnabled(False)

        self.button2 = QPushButton("Laden", self)
        self.button2.move(50, 200)
        self.button2.resize(300, 50)
        self.button2.clicked.connect(self.on_load)

        #Label
        self.label1 = QLabel("Title", self)
        self.label1.move(50, 300)
        self.label1.setFont(QFont("Arial", 14))

        self.label2 = QLabel("Year", self)
        self.label2.move(50, 350)
        self.label2.setFont(QFont("Arial", 14))

        self.label3 = QLabel("Format", self)
        self.label3.move(50, 400)
        self.label3.setFont(QFont("Arial", 14))

        self.label4 = QLabel("Technic", self)
        self.label4.move(50, 450)
        self.label4.setFont(QFont("Arial", 14))

        self.label5 = QLabel("", self)
        self.label5.move(50, 550)
        self.label5.setFont(QFont("Arial", 10))
        self.label5.resize(300, 50)

        self.label6 = QLabel("Bildname:", self)
        self.label6.move(50, 100)
        self.label6.setFont(QFont("Arial", 18))


        self.homeButton = QPushButton("Home", self)
        self.homeButton.move(0, 0)
        self.homeButton.resize(60, 25)

    def on_load(self):

        data = self.tool.JSONWithPictureName(self.textbox5.text())

        self.textbox1.setText(data[0])
        self.textbox2.setText(data[1])
        self.textbox3.setText(data[2])
        self.textbox4.setText(data[3])

        self.button.setEnabled(True)

    def on_button_clicked(self):
        if(self.textbox1.text() != "" and self.textbox2.text() != "" and self.textbox3.text() != "" and self.textbox4.text() != ""):
            jsonData = '{"title": "'+ self.textbox1.text() +'", "year": "'+ self.textbox2.text() +'", "format": "'+ self.textbox3.text() +'", "technic": "'+ self.textbox4.text() +'"}'
            self.tool.appendNewJSON(jsonData)
            self.textbox1.setText("")
            self.textbox2.setText("")
            self.textbox3.setText("")
            self.textbox4.setText("")
            self.textbox5.setText("")
            self.label5.setText("JSON String erfolgreich erstellt und hinzugefügt")
        else:
            self.label5.setText("Bitte fülle alle Felder aus")

class JSONChangeOrder(QWidget):
    def __init__(self, tool):
        super().__init__()
        self.title = "JSON Parser"
        self.initUI()

        self.tool = tool

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(GEOMETRIETABLE[0], GEOMETRIETABLE[1], GEOMETRIETABLE[2], GEOMETRIETABLE[3])

        self.table = QTableWidget(self)
        self.table.resize(700, 500)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Title", "Year", "Format", "Technic"])

        self.button = QPushButton("Ausgewählte Reihe verschieben", self)
        self.button.move(50, 500)
        self.button.resize(300, 50)

        self.lineEdit = QLineEdit(self)
        self.lineEdit.move(350, 500)
        self.lineEdit.resize(50, 50)
        self.lineEdit.setValidator(QIntValidator())

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
            self.table.setItem(row, 0, QTableWidgetItem(str(x["title"])))
            self.table.setItem(row, 1, QTableWidgetItem(str(x["year"])))
            self.table.setItem(row, 2, QTableWidgetItem(str(x["format"])))
            self.table.setItem(row, 3, QTableWidgetItem(str(x["technic"])))
        self.table.resizeColumnsToContents()

if __name__ == "__main__":
    App = QApplication(sys.argv)

    testTool = JSONTool()

    openGui = JSONOpen(testTool)
    addGui = JSONAdd(testTool)
    delGui = JSONDelete(testTool)
    addwTGui = JSONAddWT(testTool)
    editTableGui = JSONEditTable(testTool)
    editStringGui = JSONEditString(testTool)
    changeGui = JSONChangeOrder(testTool)

    def on_click_add():
        addGui.show()
        openGui.hide()

    def on_click_edit():
        editTableGui.show()
        editTableGui.addTableRow()
        openGui.hide()

    def on_click_del():
        delGui.show()
        delGui.addTableRow()
        openGui.hide()

    def on_click_edit_wT():
        addwTGui.show()
        openGui.hide()

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
            delGui.hide()
        except:
            pass
        try:
            addwTGui.hide()
        except:
            pass
        try:
            changeGui.hide()
        except:
            pass

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
    
    def on_click_editString():
        if(editStringGui.buttonFunction()):
            editStringGui.button.setEnabled(False)
            timer = QTimer()
            timer.singleShot(2000, afterTimerTask)

    def on_click_change():
        changeGui.show()
        changeGui.addTableRow()
        openGui.hide()

    def afterTimerTask():
        editTableGui.show()
        editTableGui.addTableRow()
        editStringGui.hide()
        editStringGui.label5.setText("")
        editStringGui.button.setEnabled(True)
    
    def on_click_changeOrder():
        indexes = changeGui.table.selectionModel().selectedRows()
        if len(indexes) > 0:
            for index in sorted(indexes):
                #print('Row %d is selected' % index.row())
                original = (int("%d" % index.row()))
        new = int(changeGui.lineEdit.text())
        changeGui.tool.changeOrder(original, new)
        changeGui.addTableRow()

    openGui.button1.clicked.connect(on_click_add)
    openGui.button2.clicked.connect(on_click_edit)
    openGui.button3.clicked.connect(on_click_del)
    openGui.button4.clicked.connect(on_click_edit_wT)
    openGui.button5.clicked.connect(on_click_change)
    editTableGui.button.clicked.connect(on_click_editRow)
    editStringGui.button.clicked.connect(on_click_editString)
    changeGui.button.clicked.connect(on_click_changeOrder)

    editTableGui.homeButton.clicked.connect(on_click_home)
    editStringGui.homeButton.clicked.connect(on_click_home)
    addGui.homeButton.clicked.connect(on_click_home)
    delGui.homeButton.clicked.connect(on_click_home)
    addwTGui.homeButton.clicked.connect(on_click_home)
    changeGui.homeButton.clicked.connect(on_click_home)



    openGui.show()
    #editTableGui.show()
    sys.exit(App.exec_())
