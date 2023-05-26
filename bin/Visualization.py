import numpy as np
import matplotlib.pyplot as plt
import matplotlib


class Visualization:

    def __init__(self) -> None:
        plt.ion()
        matplotlib.use('QtAgg')
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(projection='3d')
        self.ax.axes.set_xlim3d(left=0, right=200) 
        self.ax.axes.set_ylim3d(bottom=0, top=200) 
        self.ax.axes.set_zlim3d(bottom=-5, top=5) 
        self.plot_points = [[],[],[]]
        self.line = self.ax.plot(self.plot_points[0], self.plot_points[1], self.plot_points[2])[0]
        plt.show()

    def addPoint(self, X,Y,Z):
        self.plot_points[0].append(X)
        self.plot_points[1].append(Y)
        self.plot_points[2].append(Z)
        #self.ax.plot(self.plot_points[0], self.plot_points[1], self.plot_points[2])
        #plt.draw()
        #plt.pause(0.1)

    def draw(self):
        #self.ax.cla()
        #self.ax.plot(self.plot_points[0], self.plot_points[1], self.plot_points[2])
        self.line.set_data(self.plot_points[0],self.plot_points[1])
        self.line.set_3d_properties(self.plot_points[2])
        self.fig.canvas.blit(self.ax.bbox)
        self.fig.canvas.flush_events()
        plt.pause(0.001)
        #plt.pause(999)
