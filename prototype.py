#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  5 17:52:56 2018

@author: mark
"""
import matplotlib.pyplot as plt
import numpy as np
import validity91

import usb.core
import usb.util
import usb.control

import usb

from array import array

import time

file = open('dump.txt', 'w')
#file = None

dev = usb.core.find(idVendor=0x138A, idProduct=0x0091)
if dev is None:
    raise ValueError('Device not found!')

dev.reset()

cfg = dev.get_active_configuration()
endpoints = cfg[(0, 0)]

for endpoint in endpoints:
    endpoint.clear_halt()

bulk_out = endpoints[0]  # Ednpoint 0x01, Direction OUT
bulk_in = endpoints[1]    # Endpoint 0x81. Direction IN

interrupt_in = endpoints[3] # Endpoint 0x83. Interrupt IN

# %%
"""
# is this needed?
assert(dev.ctrl_transfer(usb.util.CTRL_IN | usb.util.CTRL_TYPE_VENDOR |
                     usb.util.CTRL_RECIPIENT_DEVICE, 20, 0, 0, 2) ==
       validity91.success)
"""
time.sleep(0.05)
for i, message in enumerate(validity91.init_messages):
    response = message.send(bulk_out, bulk_in)
    message.print(response, file=file)
    try:
        message.check(response)
    except AssertionError:
        if file is not None:
            file.close()
        file = None
        raise

i = None

# %%
# You can keep running this section to get new fingerprints
response = validity91.acquisition_start_message.send(bulk_out, bulk_in)
validity91.acquisition_start_message.print(response, file=file)
try:
    validity91.acquisition_start_message.check(response)
except AssertionError:
    if file is not None:
        file.close()
    file = None
    raise


int_response1 = interrupt_in.read(8)
assert(int_response1 == validity91.interrupt_ready_response)
validity91.print_array(int_response1, 'Interrupt 1:', file=file)

print('Sensor ready, put your finger on')
int_response2 = interrupt_in.read(8, timeout=0)
validity91.print_array(int_response2, 'Interrupt 2:', file=file)

img = validity91.read_image(bulk_out, bulk_in)


for i, message in enumerate(validity91.stop_acquisition):
    response = message.send(bulk_out, bulk_in)
    message.print(response, file=file)
    try:
        message.check(response)
    except AssertionError:
        if file is not None:
            file.close()
        file = None
        raise

i = None

if file is not None:
    file.close()
    file = None

fig = plt.figure('Your fingerprint')
ax = fig.gca()
ax.imshow(img, vmin=0, vmax=255)
ax.set_title('Your fingerprint')
ax.set_xlabel('x (pixel)')
ax.set_ylabel('y (pixel)')

print('')  # matplotlib returns the handle to a text that gets annoying to see.
# fig.dpi = 200  # set to 200 for high dpi screens
