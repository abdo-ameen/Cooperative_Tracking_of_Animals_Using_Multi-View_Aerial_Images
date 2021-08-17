#!/usr/bin/env python3
from y_prediction_pkg.prediction import predict
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import rospy
import cv2
from detection_pkg_3.msg import bbox_coord_3

bridge = CvBridge()

def callback(data):
    frame_3 = bridge.imgmsg_to_cv2(data, 'bgr8')
    frame_3, xmin, ymin, xmax, ymax, idx = predict(frame_3)
    # msg_3 = bbox_coord()
    # msg_3.xmin = xmin
    # msg_3.ymin = ymin
    # msg_3.xmax = xmax
    # msg_3.ymax = ymax
    # msg_3.class_index = idx
    # pub.publish(msg_3)
    cv2.imshow('frame_3', frame_3)
    key = cv2.waitKey(1) & 0xFF
    now = rospy.get_time()

def main():
    rospy.init_node('detection_node_3', anonymous=False)
    # pub = rospy.Publisher("/drone_3/bbox_coord_3", msg_3, queue_size=10)
    sub = rospy.Subscriber("/airsim_node/drone_3/camera_3/Scene", Image, callback)
    rospy.spin()
    rospy.Rate(1)

if __name__ == '__main__':
    main()
