#!/usr/bin/env python3
from __future__ import print_function
import torch
from torch.autograd import Variable
import cv2
import time
from imutils.video import FPS, WebcamVideoStream, FileVideoStream

from y_data_pkg.data import BaseTransform, VOC_CLASSES as labelmap
from y_ssd_pkg.ssd import build_ssd
import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

weights = '/home/aabdulsalam/AirSim/ros/src/y_prediction_pkg/src/y_prediction_pkg/weights/ssd300_VOC_195000.pth'
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
FONT = cv2.FONT_HERSHEY_SIMPLEX

net = build_ssd('test', 300, 22)
net.load_state_dict(torch.load(weights, map_location=torch.device('cpu')))
transform = BaseTransform(net.size, (104 / 256.0, 117 / 256.0, 123 / 256.0))

xmin = int()
ymin = int()
xmax = int()
ymax = int()

def predict(frame):
    height, width = frame.shape[:2]
    x = torch.from_numpy(transform(frame)[0]).permute(2, 0, 1)
    x = Variable(x.unsqueeze(0))
    y = net(x)
    detections = y.data
    scale = torch.Tensor([width, height, width, height])

    for i in range(detections.size(1)):
        j = 0
        while detections[0, i, j, 0] >= 0.6:
            pt = (detections[0, i, j, 1:] * scale).cpu().numpy()
            global xmin, ymin, xmax, ymax
            xmin = int(pt[0])
            ymin = int(pt[1])
            xmax = int(pt[2])
            ymax = int(pt[3])
            cv2.rectangle(frame,
                          (int(pt[0]), int(pt[1])),
                          (int(pt[2]), int(pt[3])),
                          COLORS[i % 3], 2)
            cv2.putText(frame, labelmap[i - 1], (int(pt[0]), int(pt[1])),
                        FONT, 2, (255, 255, 255), 2, cv2.LINE_AA)
            j += 1
    return frame, xmin, ymin, xmax, ymax, i
