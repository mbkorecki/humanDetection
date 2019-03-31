from __future__ import print_function

import sys
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

class image_converter:
    def __init__(self):
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("/camera/rgb/image_raw",Image,self.callback)
        self.x1 = 0
        self.y1 = 0
        self.x2 = 0
        self.y2 = 0

    def setValues(self, x1, y1, x2, y2):
        self.x1 = int(x1)
        self.y1 = int(y1)
        self.x2 = int(x2)
        self.y2 = int(y2)

    def callback(self,data):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)

        cv2.rectangle(cv_image, (self.x1, self.y1), (self.x2, self.y2), (0,255,0), 1)
        cv2.imshow("Image window", cv_image)
        cv2.waitKey(3)


    def main(args):
        ic = image_converter()
        rospy.init_node('image_converter', anonymous=True)
        try:
            rospy.spin()
        except KeyboardInterrupt:
            print("Shutting down")
        cv2.destroyAllWindows()

    if __name__ == '__main__':
        main(sys.argv)
