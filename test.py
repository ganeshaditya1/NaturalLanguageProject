import cv2
from threading import Timer
import const
from lampixapp import LampixApp
from cameraeventsource import SurfaceWatcher
from applicationmanager import ApplicationManager, RequiredFeature, HasMethods
from buttons import DelegateButton, Label


class TeaTimerApp(LampixApp):
    """
    The main application class
    """
    def __init__(self):
        # this is our custom detector component
        self.rp = RoundPotDetector(self)

    def activateApp(self):
        self.rp.activate()

    def deactivateApp(self):
        self.rp.deactivate()


class RoundPotDetector(SurfaceWatcher):
    """
    Detector looking for round pots over the whole surface under lampix
    """
    def __init__(self):
        SurfaceWatcher.__init__(self, "potdetector")
        # we need to watch for movement on the desk framework provides this component
        self.desk = RequiredFeature('deskwatcher')

    def onMovement(self, movement, baseDifference, frame, rawFrame, colorFrame, segFrame):
        for p in self._recognizeRoundPot(frame):
		print "One image detected"

    def _recognizeRoundPot(self, img):
        img = cv2.medianBlur(img, 5)
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
	
        return cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=0, maxRadius=0)





ApplicationManager().ProvideApp(TeaTimerApp())
