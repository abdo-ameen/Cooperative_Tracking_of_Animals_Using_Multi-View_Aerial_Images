#!/usr/bin/env python3
import rospy
import sys, time
import numpy as np
from scipy.linalg import block_diag
from geometry_msgs.msg import Point32
from filterpy.common import Q_discrete_white_noise
from filterpy.kalman import UnscentedKalmanFilter
from filterpy.kalman import MerweScaledSigmaPoints

def fx(x, dt):   
    F = np.array([[1, dt, 0,  0, 0,  0],
                  [0,  1, 0,  0, 0,  0],
                  [0,  0, 1, dt, 0,  0],
                  [0,  0, 0,  1, 0,  0],
                  [0,  0, 0,  0, 1, dt],
                  [0,  0, 0,  0, 0, 1]])
    return F @ x

def hx(x):
    return x[[0, 2, 4]]

sigmas = MerweScaledSigmaPoints(n=6, alpha=0.1, beta=2, kappa=1)
UKF = UnscentedKalmanFilter(dim_x=6, dim_z=3, dt=1, hx=hx, fx=fx, points=sigmas)

dt = 1
R_std = 2
Q_std = 2.5
P_std = 5
q = Q_discrete_white_noise(dim=3, dt=dt, var=Q_std**2)

UKF.Q = block_diag(q, q)
UKF.R = np.eye(3) * R_std**2
UKF.P = np.eye(6) * P_std**2
UKF.x = np.array([0, 0, 0, 0, 0, 0]).T

zs, xs = [], []

class Pos_Vel_Tracker:

    def __init__(self):
        self.publisher  = rospy.Publisher("/data_tracker_3", 
            Point32, queue_size = 10)
        self.subscriber = rospy.Subscriber("/data_sensor_3", 
            Point32, self.callback,  queue_size = 10)

    def callback(self, msg_in):
        a = msg_in.x
        b = msg_in.y
        c = msg_in.z
        z = [a, b ,c]
        # z = np.array([a, b, c])
        # print(z.shape)
        # print(z.size)
        print('incoming measurements:')
        print(z)

        UKF.predict()
        UKF.update(z)

        xs.append(UKF.x)
        zs.append(z)

        msg_out = Point32()
        msg_out.x = UKF.x[0]
        msg_out.y = UKF.x[2]
        msg_out.z = UKF.x[4]
        print('message sent:')
        print(msg_out)
        self.publisher.publish(msg_out)
        return xs, zs

def main(args):
    PVT = Pos_Vel_Tracker()
    rospy.init_node("tracker_node_3", anonymous=True)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down ROS")

if __name__ == '__main__':
    main(sys.argv)
