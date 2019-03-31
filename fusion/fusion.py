import numpy as np
from imtest import image_converter

class Fusion:
    def __init__(self):
        self.imtest = image_converter()
        self.ROIWidth = 0
        self.ROIHeight = 0
        self.ROICentre = 0
        self.topMargin = 0

    def regionOfInterest(self, distance, leftLeg, rightLeg, leftEdge, rightEdge):
        if not(distance == 0):
            objectHeight = 2
            frameHeight = 480
            sensorHeight = 0.4
            self.topMargin = min(pow(6, distance), 479)
            self.ROIHeight = min((objectHeight / distance) * 800, 479 - self.topMargin)
            self.ROIWidth = self.ROIHeight / 1.5
            bottomCentre = rightLeg + ((leftLeg - rightLeg) / 2)
            if (bottomCentre < 0):
                percentage = min((bottomCentre / rightEdge), 1)
            else:
                percentage = -min((bottomCentre / leftEdge), 1)
            self.ROICentre = 320 + 320 * percentage
            self.imtest.setValues(self.ROICentre - (self.ROIWidth / 2), self.topMargin, self.ROICentre + (self.ROIWidth / 2), self.topMargin + self.ROIHeight)
            return [int(self.ROIWidth), int(self.ROIHeight), int(self.ROICentre), int(self.topMargin)]
        else:
            self.imtest.setValues(0, 0, 0, 0)
            return [0, 0, 0, 0]
