#!/usr/bin/env python3
from y_prediction_pkg.prediction import predict
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import rospy
import cv2
from detection_pkg_2.msg import bbox_coord_2

bridge = CvBridge()

def callback(data):
    frame_2 = bridge.imgmsg_to_cv2(data, 'bgr8')
    frame_2, xmin, ymin, xmax, ymax, idx = predict(frame_2)
    # msg_2 = bbox_coord()
    # msg_2.xmin = xmin
    # msg_2.ymin = ymin
    # msg_2.xmax = xmax
    # msg_2.ymax = ymax
    # msg_2.class_index = idx
    # pub.publish(msg_2)
    cv2.imshow('frame_2', frame_2)
    key = cv2.waitKey(1) & 0xFF
    now = rospy.get_time()

def main():
    rospy.init_node('detection_node_2', anonymous=False)
    # pub = rospy.Publisher("/drone_2/bbox_coord_2", msg_2, queue_size=10)
    sub = rospy.Subscriber("/airsim_node/drone_2/camera_2/Scene", Image, callback)
    rospy.spin()
    rospy.Rate(1)

if __name__ == '__main__':
    main()
