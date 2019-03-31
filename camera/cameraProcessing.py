import numpy
import rospy
import cv2
from PIL import Image as PILImage
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from hogFeatures import HOG
from svm import SVM

class Kinect:
    def __init__(self):
        self.image_topic = '/camera/rgb/image_raw'
        self.bridge = CvBridge()
        self.hogInstance = HOG()
        self.svmInstance = SVM()

    def processData(self, ROI):
        image_data = rospy.wait_for_message(self.image_topic, Image)
        self.cv_image = self.bridge.imgmsg_to_cv2(image_data, "bgr8")
        pil_image = PILImage.fromarray(self.cv_image)
        if (ROI[0] > 0):
            features = self.hogInstance.extractFeatures(pil_image, ROI)
            if len(features) == 1:
                self.svmInstance.classify(features)

if __name__ == '__main__':
    rospy.init_node('kinect', anonymous = True)
    k = Kinect()
    try:
        while True:
            k.processData()

    except KeyboardInterrupt:
        print("Shutting Down")
        cv2.destroyAllWindows()
