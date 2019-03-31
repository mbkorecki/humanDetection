import rospy
import time
from numpy import *
from sensor_msgs.msg import LaserScan
from clustering import Clustering
from featureExtraction import FeatureExtraction
from adaBoost import AdaBoost
import sys
sys.path.append("../fusion/")
from fusion import Fusion
sys.path.append("../camera/")
from cameraProcessing import Kinect

class Listener:
    def __init__(self):
        self.clusteringInstance = Clustering()
        self.featureExtractionInstance = FeatureExtraction()
        self.adaBoostInstance = AdaBoost()
        self.fusionInstance = Fusion()
        self.cameraInstance = Kinect()
        self.prevTime = 0
        self.topic = "/scan"

    def processData(self):
        laser_data = rospy.wait_for_message(self.topic, LaserScan)
        polarRange = laser_data.ranges
        starting_angle = laser_data.angle_min
        inc_angle = laser_data.angle_increment

        cartesian = []
        polar = []

        for idx in range(0, len(polarRange)):
            if (idx > (len(polarRange) / 3) and idx < 2 * (len(polarRange) / 3)):
                polarAngle = starting_angle + inc_angle * idx
                if not isnan(polarRange[idx]) and not isinf(polarRange[idx]):
                    cartesian.append([polarRange[idx] * sin(polarAngle), polarRange[idx] * cos(polarAngle)])
                    polar.append([polarRange[idx], polarAngle])

        clusters = self.clusteringInstance.generateClusters(polar)
        clustersFiltered = []
        for idx in range(0, len(clusters)):
            if (clusters[idx][2] > 2 and clusters[idx][2] < 12):
                clustersFiltered.append(clusters[idx])

        features = []
        for idx in range(0, len(clustersFiltered)):
            features.append(self.featureExtractionInstance.extractFeatures(clustersFiltered[idx], polar, cartesian))

        labels = []
        if (len(features) > 0):
            prediction = self.adaBoostInstance.performBoost(features, labels, "test")
            print "prediction:", prediction
            leftEdge = cartesian[len(cartesian) - 1][0]
            rightEdge = cartesian[0][0]
            # print "absdiff: ", abs(leftEdge - rightEdge)
            if abs(leftEdge - rightEdge) > 0.8:
                distance = 0
                leftLeg = 0
                rightLeg = 0
                for idx in range(0, len(prediction)):
                    if (rightLeg == 0 and prediction[idx] == 1):
                        distance = cartesian[clustersFiltered[idx][0]][1]
                        rightLeg = cartesian[clustersFiltered[idx][0]][0]
                    elif (prediction[idx] == 1):
                        leftLeg = cartesian[clustersFiltered[idx][0]][0]
                ROI = self.fusionInstance.regionOfInterest(distance, leftLeg, rightLeg, leftEdge, rightEdge)
                self.cameraInstance.processData(ROI)
        else:
            self.fusionInstance.regionOfInterest(0, 0, 0, 0, 0)


if __name__ == '__main__':
    rospy.init_node('laser_listener', anonymous = True)
    listener = Listener()
    while(True):
        listener.processData()
