# This Python file uses the following encoding: utf-8
import sys
import os
import datetime
import time

from PySide6.QtGui import QGuiApplication, QIcon
from PySide6.QtWidgets import QLabel, QWidget
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtQuickControls2 import QQuickStyle
from PySide6.QtCore import QObject, Slot, Signal, QTimer, QUrl, Property

import logging
from CommandProcessor import CommandProcessor
from CommandExecutor import CommandExecutor
from submodules.fanucpy_extended import Robot
from time import sleep
import matplotlib.pyplot as plt

import threading



class mainWindow(QObject):
    def __init__(self):
        QObject.__init__(self)

        # QTimer - run timer
        self.timer = QTimer()
        self.timer.setInterval(100)
        #self.timer.timeout.connect(self.addressPort)
        self.timer.start(1000)

        self.run : bool = False

        self.robot = None
        self.processor = None
        self.executor = None

    def exit(self):
        print("Exiting")
        self.pause()
        if self.robot:
            self.robot.disconnect()
        

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
        path = QUrl(filePath).toLocalFile()
        self.processor = CommandProcessor(path)
        self.executor = CommandExecutor(self.robot,False)
        print(path)
        #self.readText.emit(str(text))
        #self.start()
        widget = QLabel()
        widget.setText("TEST")
        self.setVisualizationWidget()



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
    def addressIP(self, ip : str):
        elems = ip.split(":")
        address = elems[0]
        port = int(elems[1])

        self.robot = robot = Robot(
        robot_model="Fanuc",
        host=address,
        port=port,
        )
        robot.connect()

        self.setIP.emit("IP: " + address)
        self.addressPort(port)

    
    def addressPort(self, port):
        self.setPort.emit("Port: " + str(port))

    ##TODO link to GUI
    def setSpeed(self,speed):
        if self.executor:
            self.executor.setSpeedFactor(speed/100.0)

    ##TODO link to GUI
    def setZ(self,z_offset):
        if self.executor:
            self.executor.setZOffset(z_offset/10.0)

    ##TODO link to GUI
    def pause(self):
        self.run = False
        if self.loop.is_alive():
            self.loop.join()

    ##TODO link to GUI
    def start(self):
        if self.run == False:
            self.run = True
            self.loop = threading.Thread(target=self.loopJob)
            self.loop.start()
        pass

    ##TODO link to GUI
    def oneStep(self):
        if not self.run:
            self.executeOneLine()

    def executeOneLine(self) -> bool:
        if self.processor and self.executor:
            no,commands = self.processor.nextCommand()
            if no >= 0:
                for command in commands:
                    self.addLogLine(str(command))
                    self.setAccualLineNo(no)
                    self.executor.execute(command)
                return False
            else:
                self.addLogLine("EOF")
                self.setAccualLineNo(-1)
                return True

    ##TODO link to GUI
    def addLogLine(self, text: str):
        print(text)
        pass
    
    ##TODO link to GUI
    def setAccualLineNo(self, no: int):
        pass     

    def loopJob(self):
        while self.run:
            if self.executeOneLine():
                break
        print("Waiting to join!")

    def setVisualizationWidget(widget : QWidget):
        pass


    
if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    app.setWindowIcon(QIcon('bin/qml/images/svg_images/robot_icon_white.svg'))
    QQuickStyle.setStyle("Basic")
    engine = QQmlApplicationEngine()

    # Get Context
    main = mainWindow()
    engine.rootContext().setContextProperty("backend", main)

    # Load QML file
    engine.load(os.path.join(os.path.dirname(__file__), "qml/main.qml"))

    if not engine.rootObjects():
        sys.exit(-1)
    res = app.exec()
    main.exit()
    sys.exit(res)
