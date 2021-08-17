## Cooperative Tracking of Animals Using Multi View Aerial Images

This repository hosts the code used in the master thesis titled **'Cooperative Tracking of Animals Using Multi-View Aerial Images'** by **Abdulrahman Abdulsalam**.

The `ssd.pytorch` folder contains the code used to train a Single Shot Detector (implemented in PyTorch) as an animal detector. The SSD code was cloned from [amdegroot/ssd.pytorch](https://github.com/amdegroot/ssd.pytorch), debugged, updated, and adjusted according to the need. Due to the large size, the resulted weights were uploaded to a separate [link](https://drive.google.com/drive/folders/1bS8U3M0u12KoRpOE-qK-X8qpyl00IA27?usp=sharing)

The `test_ws` folder contains the ROS workspace we created to conduct the flight test in a simulation environment. The workspace was built with help from the example code available on the ROS documentation [website](http://wiki.ros.org/). The workspace contains the code that implements the four modules, detection, tracking, sensors and control.

The code used to implement the UKF tracker was cloned from the e-book [rlabbe/Kalman-and-Bayesian-Filters-in-Python](https://github.com/rlabbe/Kalman-and-Bayesian-Filters-in-Python) and adjusted to suite our application. It is embedded in `test_ws/src/tracking_pkg_3`.
