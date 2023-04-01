import logging
from Command import Command
from MyUtils import MyUtils
from submodules.fanucpy_extended import Robot
from Visualization import Visualization
import math
import numpy as np


class CommandExecutor:

    dryRun: bool = True
    showVisualization: bool = False
    smoothArcs: bool = True
    curPos: list[float] = [0,0,0] 
    absolutePos = False
    zOffset = 0
    FSpeeds: int = 10
    orientation: list[float] = [0,0,0]

    
    def __init__(self, robot: Robot | None, visualization: bool = False) -> None:
        self.robot : Robot | None = robot
        self.showVisualization = visualization
        if self.robot == None:
            self.dryRun = True
        if self.showVisualization:
            self.visualization = Visualization()
        
 
    def _handleGCommand(self, command: Command):

        def assertNoAttribute(command: Command):
            assert(len(command.params) == 0)

        def calcNextPoint(command: Command) -> list[float]:
            X = command.params.get("X",self.curPos[0])
            Y = command.params.get("Y",self.curPos[1])
            Z = command.params.get("Z",self.curPos[2])
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
                speed: int = command.params["F"] // 60
                logging.info(f"Setting speed to {str(speed)} mm/s")
                self.FSpeeds = speed



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
                nextPoint = calcNextPoint(command)
                if self.showVisualization:
                    self.addToVisualization([nextPoint])
                if not self.dryRun:
                    self.robot.move(
                        "pose",
                        vals= nextPoint + self.orientation,
                        velocity=10,
                        acceleration=100,
                        cnt_val=0,
                        linear=False,
                    )

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
            case 6:
                logging.info("M6 - Tool change")
            case 8:
                logging.info("M8 - Turn on tool flood coolant")
            case 9:
                logging.info("M9 - Turn off coolant")
            case 30:
                logging.info("M30 - Program end")
            case other:
                logging.error(f"Unrecognize command!: {command.command_type} {str(command.command_no)}")
                pass

    def _handleSCommand(self, command: Command):
        if command.command_no < 0:
            logging.error(f"Unrecognize command!: {command.command_type} {str(command.command_no)}")
            return
        logging.info(f"S{str(command.command_no)} - Set speed to {str(command.command_no)}RPM")
        #TODO: control spindle

    def execute(self, command: Command):
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

