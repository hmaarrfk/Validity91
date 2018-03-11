#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  5 17:52:56 2018

@author: mark
"""
import matplotlib.pyplot as plt
import validity91
import logging
logging.basicConfig(
    filename='dump.txt',
    format='%(levelname)s: %(filename)s - %(funcName)s \n%(message)s',
    level=logging.DEBUG, filemode='w')

f_sensor = validity91.vfs7552()


f_sensor.initiate_capture()
print("Put your finger on.")
f_sensor.wait_finger_on()
img = f_sensor.capture_image()
print("Take your finger off.")
f_sensor.wait_finger_off()
f_sensor.disable_sensor()

skip_optional = False

fig = plt.figure('Your fingerprint')
ax = fig.gca()
ax.imshow(img, vmin=0, vmax=255)
ax.set_title('Your fingerprint')
ax.set_xlabel('x (pixel)')
ax.set_ylabel('y (pixel)')

print('')  # matplotlib returns the handle to a text that gets annoying to see.
# fig.dpi = 200  # set to 200 for high dpi screens
plt.show()
