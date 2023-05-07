# This Python file uses the following encoding: utf-8
import sys
import os
import datetime

from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtQuickControls2 import QQuickStyle
from PySide6.QtCore import QObject, Slot, Signal, QTimer, QUrl, Property

class mainWindow(QObject):
    def __init__(self):
        QObject.__init__(self)

        # QTimer - run timer
        self.timer = QTimer()
        self.timer.setInterval(100)
        #self.timer.timeout.connect(self.addressPort)
        self.timer.start(1000)
        

    # Signal set name
    setName = Signal(str)

    # Robot IP
    setIP = Signal(str)

    # Robot Port
    setPort= Signal(str)

    # Signal set Data
    printTime = Signal(str)

    # Signal visible
    isVisible = Signal(bool)

    # Open file to text edit
    readText = Signal(str)

    # Open file
    @Slot(str)
    def openFile(self, filePath):
        file = open(QUrl(filePath).toLocalFile(), encoding="utf-8")
        text = file.read()
        file.close()
        print(text)
        self.readText.emit(str(text))

    # Read text
    @Slot(str)
    def getTextField(self,text):
        self.textField = text

    # Write file
    @Slot(str)
    def writeFile(self, filePath):
        file = open(QUrl(filePath).toLocalFile(),"w")
        file.write(self.textField)
        file.close()
        print(self.textField)


    # Show/hide rectangle
    @Slot(bool)
    def showHideRectangle(self,isChecked):
        #print("Is rectangle visible ", isChecked)
        self.isVisible.emit(isChecked)

    # Set timer function
    def setTime(self):
        now = datetime.datetime.now()
        formatDate = now.strftime("%H:%M:%S")
        print(formatDate)
        self.printTime.emit(formatDate)

    # Function set name to label
    @Slot(str)
    def welcomeText(self, name):
       self.setName.emit("Welcome, " + name)

    # Set address IP of label
    @Slot(str)
    def addressIP(self, ip):
         self.setIP.emit("IP: " + ip)
         self.addressPort()
    
    def addressPort(self):
        port = str(676767)
        self.setPort.emit("Port: " + port)

    
if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    QQuickStyle.setStyle("Basic")
    engine = QQmlApplicationEngine()

    # Get Context
    main = mainWindow()
    engine.rootContext().setContextProperty("backend", main)

    # Load QML file
    engine.load(os.path.join(os.path.dirname(__file__), "qml/main.qml"))

    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec())
