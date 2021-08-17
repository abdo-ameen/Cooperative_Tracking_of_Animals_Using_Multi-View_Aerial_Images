#!/usr/bin/env python3
import airsim
import rospy
from geometry_msgs.msg import Point32

HOST = '172.30.16.1'
client = airsim.MultirotorClient(ip=HOST)
client.confirmConnection()
client.enableApiControl(True, "drone_1")
client.enableApiControl(True, "drone_2")
client.enableApiControl(True, "drone_3")
client.armDisarm(True, "drone_1")
client.armDisarm(True, "drone_2")
client.armDisarm(True, "drone_3")
f1 = client.takeoffAsync(vehicle_name="drone_1")
f2 = client.takeoffAsync(vehicle_name="drone_2")
f3 = client.takeoffAsync(vehicle_name="drone_3")
f1.join()
f2.join()
f3.join()


def controller1(msg_1):
    x_coord_1 = msg_1.x
    y_coord_1 = msg_1.y
    z_coord_1 = msg_1.z

    rospy.loginfo(x_coord_1, y_coord_1, z_coord_1)
    f1 = client.moveToPositionAsync(x_coord_1 - 5, y_coord_1 + 5, -5, 5, vehicle_name="drone_1")
    # f2 = client.moveToPositionAsync(x_coord_1 + 5, y_coord_1 + 5, -5, 5, vehicle_name="drone_2")
    # f3 = client.moveToPositionAsync(x_coord_1, y_coord_1 - 5, -5, 5, vehicle_name="drone_3")
    f1.join()
    # f2.join()
    # f3.join()

def controller2(msg_2):
    x_coord_2 = msg_2.x
    y_coord_2 = msg_2.y
    z_coord_2 = msg_2.z

    rospy.loginfo(x_coord_2, y_coord_2, z_coord_2)
    f2 = client.moveToPositionAsync(x_coord_2 + 5, y_coord_2 + 5, -5, 5, vehicle_name="drone_2")
    f2.join()

def controller3(msg_3):
    x_coord_3 = msg_3.x
    y_coord_3 = msg_3.y
    z_coord_3 = msg_3.z

    rospy.loginfo(x_coord_3, y_coord_3, z_coord_3)
    f3 = client.moveToPositionAsync(x_coord_3, y_coord_3 - 5, -5, 5, vehicle_name="drone_3")
    f3.join()

if __name__ == '__main__':
    rospy.init_node('control_node', anonymous=True)
    rospy.Subscriber("data_tracker_1", Point32, controller1)
    rospy.Subscriber("data_tracker_2", Point32, controller2)
    rospy.Subscriber("data_tracker_3", Point32, controller3)
    rospy.spin()
