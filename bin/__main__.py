# This Python file uses the following encoding: utf-8
import sys
import os
import datetime

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
#import matplotlib.pyplot as plt

from threading import Thread



class mainWindow(QObject):

    def __init__(self):
        QObject.__init__(self)
        # QTimer - run timer
        # self.timer = QTimer()
        # self.timer.setInterval(100)
        # self.timer.timeout.connect(self.addressPort)
        # self.timer.start(1000)

        self.run : bool = False

        self.robot = None
        self.processor = None
        self.executor = None

    def exit(self):
        print("Exiting")
        self.working = False
        self.pause()
        if self.robot:
            self.robot.disconnect()

    # Signal set name
    setName = Signal(str)

    # Robot IP
    setIP = Signal(str)

    # Robot Port
    setPort = Signal(str)

    # Spindle Speed
    setZ = Signal(int)

    # Signal timer
    printTime = Signal(str)

    # Signal set line number
    lineNo = Signal(str)

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
        # print(path)
        self.start()

    # Read text
    @Slot(str)
    def getTextField(self,text):
        self.textField = text

    # Show/hide rectangle
    @Slot(bool)
    def showHideRectangle(self, isChecked):
        #print("Is rectangle visible", isChecked)
        self.isVisible.emit(isChecked)

    # Set timer function
    def setTime(self):
        while self.run:
            now = datetime.datetime.now()
            formatDate = now.strftime("%H:%M:%S")
            # print(formatDate)
            self.printTime.emit(formatDate)
            sleep(2)

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

    # Setting spindle speed
    @Slot(int)
    def setSpeed(self, speed):
        print("Spindle speed: " + str(speed/100.0))
        if self.executor:
            self.executor.setSpeedFactor(speed/100.0)

    # Setting Z offset
    @Slot(int)
    def setZ(self, z_offset):
        print("Z offset: " + str(z_offset/100.0))
        if self.executor:
            self.executor.setZOffset(z_offset/100.0)

    # Pausing program
    @Slot()
    def pause(self):
        self.run = False
        print("Pause")
        if self.loop.is_alive():
            self.loop.join()

    @Slot()
    def start(self):
        print("Start")
              
        if self.run == False:
            print("Running")
            self.run = True
            self.loop = Thread(target=self.loopJob)
            self.timer_thread = Thread(target=self.setTime).start()
            self.loop.start()

    @Slot()
    def oneStep(self):
        if not self.run:
            print("Executing One Line")
            self.executeOneLine()

    def executeOneLine(self) -> bool:
        if self.processor and self.executor:
            no,commands = self.processor.nextCommand()
            if no >= 0:
                for command in commands:
                    self.addLogLine(str(command))
                    self.setActualLineNo(no)
                    self.executor.execute(command)
                return False
            else:
                self.addLogLine("EOF")
                self.setActualLineNo(-1)
                self.run = False
                return True

    ##TODO link to GUI
    def addLogLine(self, text: str):
        print(text)
        pass
    
    def setActualLineNo(self, no: int):
        
        if self.run:
            no += 10
        else:
            no = -1
        self.lineNo.emit("Actual Line #:" + str(no))
        

    def loopJob(self):
        while self.run:
            if self.executeOneLine():
                break
        print("Waiting to join!")

    # def setVisualizationWidget(widget : QWidget):
    #     pass


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
