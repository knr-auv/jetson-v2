import time, math
import autonomy.Detectors.Helpers as h
import autonomy.Detectors.DetectorBaseClass as base
from communicationThreads.Simulation.simulationClient import SimulationClient
class Simulation_noGPU_detector(base.DetectorBaseClass):
    cameraStream = None
    def __init__(self, cameraStream, controlThread):
        super().__init__()
        #control thread is used for obtaining position and attitude data
        self.controlThread = controlThread
        self.cameraStream = cameraStream
        self.client = SimulationClient()
        if(cameraStream==None):
            return None

    def DetectorTask(self):
        time.sleep(1)
        detection = self.get_detection()
        detection = detection["detected"]
        for i in detection:
            if(i['visibleInFrame']):
                o = self.handle_detection(i)
                self.check_if_seen(o)
                self.LastDetections.append(o)

        #########only for testing ###########
        if(len(self.LastDetections)>=5):
            self.LastDetections.pop(0)

        ####################################
        fps = 1
        self.InvokeCallback(fps,*self.prepareCb())
        
    def handle_detection(self, detection):
        """
        dictionary keys (not sure about min,max... probably min = [min_x,min_y]) you can just print this dictionary and check...:
        visibleInFrame;
        min, max ->vec2
        fill
        className
        distance;
        colorPercentVisible;
        """
        x,y,z = [self.controlThread.getPosition()[0],self.controlThread.getPosition()[1],self.controlThread.getPosition()[2]]
        name = detection["className"]
        dist = detection["distance"]
        min =detection["min"]
        minx= min['x']
        miny= min['y']
        max = detection["max"]
        maxx = max["x"]
        maxy = max["y"]
        center_width = (minx+maxx)/2
        center_height = (miny+maxy)/2
        obj = base.Object()
        obj.type = name
        obj.accuracy = 1
        
        a,b,c = [self.controlThread.getAttitude()[0],self.controlThread.getAttitude()[1],self.controlThread.getAttitude()[2]]
        obj.x , obj.y, obj.z = h.object_position(107,60,dist,center_width,center_height,[x,y,z], [a,b,c])

        #more smart stuff
        return obj

    def check_if_seen(self, o):
        pos = [o.x,o.y,o.z]
        ap = True
        l = h.vec_length(pos)
        if len(self.ObjectsList)!=0:
            ap = False
            for i in self.ObjectsList:
                pos = [i.x,i.y,i.z]
                li = h.vec_length(pos)
                if abs(l-li)>2:
                    self.ObjectsList.append(o)
                    ap = True
                else:
                    ap = False
        if ap:
            self.ObjectsList.append(o)
        #sprawdź, czy widziany
        #jeśli tak to może popraw pozycje już wcześniej znalezionego obiektu
        #cokolwiek
        return False
    
    def prepareCb(self):
        a = list()
        b = list()
        for i in self.ObjectsList:
            a.append(i.toDictionary())
        for i in self.LastDetections:
            b.append(i.toDictionary())
        return a,b

    def get_detection(self):
        #camera stream is based on simulation web api.
        return self.client.get_detection()

