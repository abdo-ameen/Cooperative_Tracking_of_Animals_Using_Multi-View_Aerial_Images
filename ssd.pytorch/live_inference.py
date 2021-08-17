from __future__ import print_function
import torch
from torch.autograd import Variable
import cv2
import time
from imutils.video import FPS, WebcamVideoStream, FileVideoStream
from data import BaseTransform, VOC_CLASSES as labelmap
from ssd import build_ssd
import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

weights = 'weights\ssd300_VOC_195000.pth'
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
FONT = cv2.FONT_HERSHEY_SIMPLEX
net = build_ssd('test', 300, 22)
net.load_state_dict(torch.load(weights, map_location=torch.device('cpu')))
transform = BaseTransform(net.size, (104 / 256.0, 117 / 256.0, 123 / 256.0))
global stream
# stream = WebcamVideoStream(src=0).start()
stream = FileVideoStream('videos/zebra_dazzle_1_007.mp4').start()
time.sleep(1.0)

def predict(frame):
    height, width = frame.shape[:2]
    x = torch.from_numpy(transform(frame)[0]).permute(2, 0, 1)
    x = Variable(x.unsqueeze(0))
    y = net(x)
    detections = y.data  # shape: [1, 21, 200, 5]
    scale = torch.Tensor([width, height, width, height])

    # i = class index >> which class is detected, person, horse, car etc.
    # j = detection index! >> will give 1 if detection happens!
    # for each class in the class list [21 VOC classes!]!
    for i in range(detections.size(1)):
        j = 0
        while detections[0, i, j, 0] >= 0.6:
            pt = (detections[0, i, j, 1:] * scale).cpu().numpy()
            cv2.rectangle(frame,
                          (int(pt[0]), int(pt[1])),
                          (int(pt[2]), int(pt[3])),
                          COLORS[i % 3], 2)
            cv2.putText(frame, labelmap[i - 1], (int(pt[0]), int(pt[1])),
                        FONT, 2, (255, 255, 255), 2, cv2.LINE_AA)
            j += 1
    return frame

def cv2_demo(net, transform):
    count = 1
    while True:
        frame = stream.read()
        frame = predict(frame)
        fps.update()

        key = cv2.waitKey(1) & 0xFF
        if key == ord('p'):
            while True:
                key2 = cv2.waitKey(1) or 0xff
                cv2.imshow('frame', frame)
                if key2 == ord('p'):
                    break

        if key == ord('s'):
            cv2.imwrite("zebra_1_%d.jpg" % count, frame)

        cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('frame', 700, 700)
        cv2.imshow('frame', frame)
        count += 1
        if key == 27:
            break

if __name__ == '__main__':
    fps = FPS().start()
    cv2_demo(net.eval(), transform)
    fps.stop()
    print("Elapsed Time: {:.2f}".format(fps.elapsed()))
    print("Approx. FPS: {:.2f}".format(fps.fps()))
    cv2.destroyAllWindows()
    stream.stop()
