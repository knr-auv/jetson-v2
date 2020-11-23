import cameraStream.stream as cs
import controlThread.controlThread as ct
import autonomy.Detectors as Detectors

class AutonomyThread:
    """
    This class should be responsible for creating and managing autonomy and vision system
    """
    def __init__(self, controlThread = ct.ControlThread(), cameraStream= cs.cameraStream()):
        self.cameraStream = cameraStream
        self.controlThread = controlThread
        #self.detector = Detector.Detector()
        
    def StartAutonomy(self):
        pass

    def StartDetections(self, callback):
        pass