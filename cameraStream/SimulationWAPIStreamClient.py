import communicationThreads.Simulation.simulationClient as sc
import threading, time
import cv2
import numpy as np
import math
from cameraStream.stream import cameraStream
import variable

class SimulationWAPIStreamClient(cameraStream):
    """Stream client which use simulation web API"""
    v_fov = 60
    h_fov = 60
    max_d = 20
    min_d = 0.4
    to_m = (max_d-min_d)/255
    __fi_x = (math.pi-h_fov)/2
    __fi_y = 2*math.pi - v_fov/2
    def __init__(self):
        threading.Thread.__init__(self)
        self.frame = None
        self.client = sc.SimulationClient()

    def run(self):
        while self.active:
            self.receive_frame()
            #around 50 fps
            time.sleep(0.01)

    def getFrame(self):
        return self.frame

    def receive_frame(self):
        val = self.client.get_stream_frame()
        if(val != None):
            self.frame = val

    def setFov(self, h_fov, v_fov):
        self.h_fov = h_fov
        self.v_fov = v_fov
        self.__fi_x = (math.pi-h_fov)/2
        self.__fi_y = 2*math.pi - v_fov/2

    def setMaxMinDeptDist(self, max, min):
        self.max_d = max
        self.min_d = min
        self.to_m = (max_d-min_d)/255
    def getDepthMap(self):
        return self.client.get_depth_map() #jpg bytes

    def getPointCloud(self):
        d_map = self.client.get_depth_map() #jpg bytes
        nparray = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(nparray,cv2.IMREAD_GRAYSCALE)
        rows,cols = img.shape
        res = np.zeros((cols,rows,3))
        for i in range(cols): #poziom
            for j in range(rows):#pion
                c_x = i
                c_y = j
                di =  img[j,i]/255
                di = 1-di
                di = di*to_m
                a_x = self.__fi_x + c_x*h_fov/cols
                x = -di/math.tan(a_x)
                a_y = self.__fi_y +c_y*v_fov/rows
                z = -di*math.tan(a_y)
                y = di
                res[i, j, 0]=x
                res[i, j, 1]=y
                res[i, j, 2]=z
        return res