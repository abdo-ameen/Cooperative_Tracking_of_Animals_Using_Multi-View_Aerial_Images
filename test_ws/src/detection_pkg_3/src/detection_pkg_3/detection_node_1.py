#!/usr/bin/env python3
from y_prediction_pkg.prediction import predict
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import rospy
import cv2
from detection_pkg_2.msg import bbox_coord_2

bridge = CvBridge()

def callback(data):
    frame_1 = bridge.imgmsg_to_cv2(data, 'bgr8')
    frame_1, xmin, ymin, xmax, ymax, idx = predict(frame_1)
    # msg_1 = bbox_coord()
    # msg_1.xmin = xmin
    # msg_1.ymin = ymin
    # msg_1.xmax = xmax
    # msg_1.ymax = ymax
    # msg_1.class_index = idx
    # pub.publish(msg_1)
    cv2.imshow('frame_1', frame_1)
    key = cv2.waitKey(1) & 0xFF
    now = rospy.get_time()

def main():
    rospy.init_node('detection_node_1', anonymous=False)
    # pub = rospy.Publisher("/drone_1/bbox_coord_1", msg_1, queue_size=10)
    sub = rospy.Subscriber("/airsim_node/drone_1/camera_1/Scene", Image, callback)
    rospy.spin()
    rospy.Rate(1)

if __name__ == '__main__':
    main()
