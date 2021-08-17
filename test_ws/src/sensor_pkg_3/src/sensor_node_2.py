#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Point32
from numpy.random import randn
import numpy as np

class Position_Sensor(object):
    def __init__(self, pos, vel, noise_std):
        self.vel = vel
        self.noise_std = noise_std
        self.pos = [pos[0], pos[1], pos[2]]
        
    def read(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.pos[2] += self.vel[2]
        
        return [self.pos[0] + randn() * self.noise_std,
                self.pos[1] + randn() * self.noise_std,
                self.pos[2] + randn() * self.noise_std]

def talker():
    pub = rospy.Publisher('data_sensor_2', Point32, queue_size=10)
    rospy.init_node('sensor_node_2', anonymous=True)
    rate = rospy.Rate(0.5)
    sensor = Position_Sensor((0, 0, 0), (0.5, 0.5, 0.5), noise_std=3)
    while not rospy.is_shutdown():
        
        sensor_data = sensor.read()
        msg = Point32()
        msg.x = sensor_data[0]
        msg.y = sensor_data[1]
        msg.z = sensor_data[2]

        rospy.loginfo(msg)
        pub.publish(msg)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
