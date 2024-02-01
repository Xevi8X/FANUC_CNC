import logging
from Command import Command
from MyUtils import MyUtils
from submodules.fanucpy_extended import Robot
from Visualization import Visualization
import math
import numpy as np

import serial
import minimalmodbus
from time import sleep

class CommandExecutor:

    dryRun: bool = False
    showVisualization: bool = False
    smoothArcs: bool = True

    curPos: list[float] = [0,0,0] 
    absolutePos: bool = False
    zOffset: float = 0
    baseSpeed :float = 600.0
    FSpeeds: int = 100
    speed_factor: float = 8
    orientation: list[float] = [0,0,0]
    spindlespeed = 0

    client1 = minimalmodbus.Instrument('COM10', 1)  # port name, slave address (in decimal)
    client1.serial.baudrate = 9600  # baudrate
    client1.serial.bytesize = 8
    client1.serial.parity   = serial.PARITY_NONE
    client1.serial.stopbits = 1
    client1.serial.timeout  = 0.5      # seconds
    client1.address         = 1        # this is the slave address number
    client1.mode = minimalmodbus.MODE_RTU # rtu or ascii mode
    client1.clear_buffers_before_each_transaction = True

    
    def __init__(self, robot, visualization: bool = False) -> None:
        self.robot = robot
        self.showVisualization = visualization
        if self.robot == None:
            self.dryRun = True
        if self.showVisualization:
            self.visualization = Visualization()

    
    def setSpeedFactor(self,speed_factor: float):
        self.speed_factor = speed_factor
        self.FSpeeds = int(self.baseSpeed*self.speed_factor/60.0)
        if(self.FSpeeds < 1):
            self.FSpeeds = 1 #mm/sek - almost nothing
        logging.info(f"Setting output speed to {str(self.FSpeeds)} mm/sek")
        #add line to text box in GUI

    def setZOffset(self, zOffset : float):
        self.zOffset = zOffset
        logging.info(f"Setting z-offset to {str(self.zOffset)} mm")
        
 
    def _handleGCommand(self, command: Command):

        def assertNoAttribute(command: Command):
            assert(len(command.params) == 0)

        def calcNextPoint(command: Command) -> list[float]:
            X = command.params.get("X",self.curPos[0])
            Y = command.params.get("Y",self.curPos[1])
            if "Z" in command.params:
                Z = command.params["Z"]
                if self.absolutePos:
                    Z = Z + self.zOffset
            else:
                Z = self.curPos[2]
            if not self.absolutePos:
                X = self.curPos[0] + command.params.get("X",0)
                Y = self.curPos[1] + command.params.get("Y",0)
                Z = self.curPos[2] + command.params.get("Z",0)
            # Z -= self.zOffset
            self.curPos = [X,Y,Z]
            return self.curPos
        
        def calcArcs(command: Command, ccw: bool = False) -> list[list[float]]:
            points = []
            assert(not "Z" in command.params)
            assert(not "R" in command.params)
            endX = command.params.get("X",self.curPos[0])
            endY = command.params.get("Y",self.curPos[1])
            I = command.params.get("I",0)
            J = command.params.get("J",0)
            R = math.sqrt(I**2 + J**2)
            center = (self.curPos[0]+I,self.curPos[1]+J)
            startAngle = math.atan2(-J,-I)
            endAngle = math.atan2(endY - center[1], endX - center[0])
            if not ccw and endAngle > startAngle:
                endAngle -= 2*math.pi
            if ccw and endAngle < startAngle:
                endAngle += 2*math.pi
            steps = int(4.0*(startAngle-endAngle)/math.pi)
            if steps % 2 == 0:
                steps += 1
            if steps < 3:
                steps = 3
            angles = np.linspace(startAngle, endAngle, num = steps)
            for angle in angles[1:]:
                points.append([center[0] + R*math.cos(angle),center[1] + R*math.sin(angle),self.curPos[2]])
            # self.curPos[0] = endX
            # self.curPos[1] = endY
            # self.curPos[2] = command.params.get("Z",self.curPos[2])
            assert(len(points)>= 2 and len(points) % 2 == 0)
            return points
        
        def setSpeed(command: Command):
            if 'F' in command.params:
                speed = command.params["F"]
                logging.info(f"Setting base speed to {str(speed)} mm/min")
                self.baseSpeed = speed
                self.setSpeedFactor(self.speed_factor)

        match command.command_no:

            case 0:
                logging.info("G0 - Fast move (quasilinear)")
                setSpeed(command)
                nextPoint = calcNextPoint(command)
                if self.showVisualization:
                    self.addToVisualization([nextPoint])
                if not self.dryRun:
                    self.robot.move(
                        "pose",
                        vals= nextPoint + self.orientation,
                        velocity=self.FSpeeds,
                        acceleration=100,
                        cnt_val=0,
                        linear=True,
                    )

            case 1:
                logging.info("G1 - Linear move")
                setSpeed(command)
                nextPoint = calcNextPoint(command)
                if self.showVisualization:
                    self.addToVisualization([nextPoint])
                if not self.dryRun:
                    self.robot.move(
                        "pose",
                        vals= nextPoint + self.orientation,
                        velocity=self.FSpeeds,
                        acceleration=100,
                        cnt_val=0,
                        linear=True,
                    )

            case 2:
                logging.info("G2 - Circular move CW")
                setSpeed(command)
                arcPoints = calcArcs(command,False)
                if self.showVisualization:
                    if self.smoothArcs:
                        self.circleCW(command)
                    else:
                        self.addToVisualization(arcPoints)
                if not self.dryRun:
                    noOfArcs: int = len(arcPoints)//2
                    for i in range(noOfArcs):
                        self.robot.circ(
                            mid=arcPoints[2*i] + self.orientation,
                            end=arcPoints[2*i+1] + self.orientation,
                            velocity=self.FSpeeds,
                            acceleration=100,
                            cnt_val=0,
                        )
                self.curPos = arcPoints[-1]

            case 3:
                logging.info("G3 - Circular move CCW")
                setSpeed(command)
                arcPoints = calcArcs(command,True)
                if self.showVisualization:
                    if self.smoothArcs:
                        self.circleCCW(command)
                    else:
                        self.addToVisualization(arcPoints)
                if not self.dryRun:
                    noOfArcs: int = len(arcPoints)//2
                    for i in range(noOfArcs):
                        self.robot.circ(
                            mid=arcPoints[2*i] + self.orientation,
                            end=arcPoints[2*i+1] + self.orientation,
                            velocity=self.FSpeeds,
                            acceleration=100,
                            cnt_val=0,
                        )
                self.curPos = arcPoints[-1]

            case 17:
                logging.info("G17 - XY Plane Selection")
                pass

            case 21:
                logging.info("G21 - Metric units convention")
                pass

            case 28:
                logging.info("G28 - Go home")
                if not self.dryRun:
                    lpos = self.robot.get_lpos()
                    self.orientation = lpos[3:]
                    
                    logging.info(f"Setting orientation to {str(self.orientation[0])}, {str(self.orientation[1])}, {str(self.orientation[2])}")
                    print(f"Setting orientation to {str(self.orientation[0])}, {str(self.orientation[1])}, {str(self.orientation[2])}")
                nextPoint = calcNextPoint(command)
                nextPoint[2] += 5.0
                if self.showVisualization:
                    self.addToVisualization([nextPoint])
                if not self.dryRun:
                    pass
                    # self.robot.move(
                    #     "pose",
                    #     vals= nextPoint + self.orientation,
                    #     velocity=10,
                    #     acceleration=100,
                    #     cnt_val=0,
                    #     linear=False,
                    # )

            #TODO: What is G40-G42
            case 40:
                logging.warn("G40 - ")
                pass
            case 41:
                logging.warn("G41 - ")
                pass
            case 43:
                logging.info("G43 - Tool length compensation")
                pass

            case 54:
                logging.info("G54 - Active Coordinate System")
                assertNoAttribute(command)
                pass

            case 90:
                logging.info("G90 - Absolute positioning")
                self.absolutePos = True
                assertNoAttribute(command)

            case 91:
                logging.info("G91 - Incremental positioning")
                assertNoAttribute(command)
                self.absolutePos = False
                if self.robot != None:
                    self.curPos =  self.robot.get_lpos()[:3]
                else:
                    self.curPos = [0,0,0]

            case other:
                logging.error(f"Unrecognize command!: {command.command_type} {str(command.command_no)}")


    def _handleTCommand(self, command: Command):
        if command.command_no < 0:
            logging.error(f"Unrecognize command!: {command.command_type} {str(command.command_no)}")
            return
        logging.info(f"T{str(command.command_no)} - Load tool no.{str(command.command_no)}")
        #TODO: handle tool changing


    def _handleMCommand(self, command: Command):
        match command.command_no:
            case 3:
                logging.info("M3 - Start spindle")
                self.client1.write_register(5, 4930, number_of_decimals=0, functioncode=6) #zapis do rejestru wartosci powodujacej rozpoczecie pracy wrzeciona
                output_stats  = self.client1.read_register(20) #Odczyt pojedynczego rejestru 16bit zawierajacego RPM
                while(output_stats > 1.05*self.spindlespeed or output_stats < 0.95*self.spindlespeed):
                   print(self.spindlespeed)
                   output_stats  = self.client1.read_register(20) #Odczyt pojedynczego rejestru 16bit zawierajacego RPM
                   print("output stats decimal: {}".format(output_stats))
            case 6:
                logging.info("M6 - Tool change")
            case 8:
                logging.info("M8 - Turn on tool flood coolant")
            case 9:
                logging.info("M9 - Turn off coolant")
            case 30:
                logging.info("M30 - Program end")
                self.client1.write_register(5, 4929, number_of_decimals=0, functioncode=6) #zapis do rejestru wartosci powodujacej zakonczenieS pracy wrzeciona
                self.client1.close_port_after_each_call = True
            case other:
                logging.error(f"Unrecognize command!: {command.command_type} {str(command.command_no)}")
                pass

    def _handleSCommand(self, command: Command):
        if command.command_no < 0:
            logging.error(f"Unrecognize command!: {command.command_type} {str(command.command_no)}")
            return
        logging.info(f"S{str(command.command_no)} - Set speed to {str(command.command_no)}RPM")
        self.spindlespeed = command.command_no
        self.client1.write_register(4, 40000*command.command_no/12000, number_of_decimals=0, functioncode=6) #zapis do rejestru wartosci predkosci obrotowej
        self.client1.close_port_after_each_call = True

    def execute(self, command: Command):
        print("Execute called")
        match command.command_type:
            case 'G':
                self._handleGCommand(command)
            case 'T':
                self._handleTCommand(command)
            case 'M':
                self._handleMCommand(command)
            case 'S':
                self._handleSCommand(command)
            case other:
                logging.error(f"Unrecognize command!: {command.command_type} {str(command.command_no)}")

    ### VISUALIZATION

    def draw(self):
        self.visualization.draw()

    # def test(self):
    #     self.curPos = [50,50,0]
    #     command = Command()
    #     command.params = {}
    #     command.params["X"] = 75
    #     command.params["Y"] = 25
    #     command.params["I"] = 25
    #     command.params["J"] = 0
    #     self.circleCCW(command)
    #     self.draw()
    
    def circleCW(self, command: Command):
        assert(not "Z" in command.params)
        assert(not "R" in command.params)
        endX = command.params.get("X",self.curPos[0])
        endY = command.params.get("Y",self.curPos[1])
        I = command.params.get("I",0)
        J = command.params.get("J",0)
        R = math.sqrt(I**2 + J**2)
        center = (self.curPos[0]+I,self.curPos[1]+J)
        startAngle = math.atan2(-J,-I)
        endAngle = math.atan2(endY - center[1], endX - center[0])
        if endAngle > startAngle:
            endAngle -= 2*math.pi
        steps = np.linspace(startAngle, endAngle, num= int((startAngle-endAngle)*R/1))
        for angle in steps:
            point = (center[0] + R*math.cos(angle),center[1] + R*math.sin(angle))
            self.visualization.addPoint(point[0],point[1],self.curPos[2])
        self.curPos[0] = endX
        self.curPos[1] = endY
        self.curPos[2] = command.params.get("Z",self.curPos[2])
        self.draw()
    
    def circleCCW(self, command: Command):
        assert(not "Z" in command.params)
        assert(not "R" in command.params)
        endX = command.params.get("X",self.curPos[0])
        endY = command.params.get("Y",self.curPos[1])
        I = command.params.get("I",0)
        J = command.params.get("J",0)
        R = math.sqrt(I**2 + J**2)
        center = (self.curPos[0]+I,self.curPos[1]+J)
        startAngle = math.atan2(-J,-I)
        endAngle = math.atan2(endY - center[1], endX - center[0])
        if endAngle < startAngle:
            endAngle += 2*math.pi
        steps = np.linspace(startAngle, endAngle, num= int((endAngle-startAngle)*R/1))
        for angle in steps:
            point = (center[0] + R*math.cos(angle),center[1] + R*math.sin(angle))
            self.visualization.addPoint(point[0],point[1],self.curPos[2])
        self.curPos[0] = endX
        self.curPos[1] = endY 
        self.curPos[2] = command.params.get("Z",self.curPos[2])
        self.draw()
        
        
    def addToVisualization(self,points: list[list[float]]):
        for point in points:
            self.visualization.addPoint(point[0],point[1],point[2])
        self.draw()

