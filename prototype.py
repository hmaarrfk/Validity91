
import validity91
from array import array
import numpy as np

import usb.core
import usb.util
import usb.control

import usb


dev = usb.core.find(idVendor=0x138A, idProduct=0x0091)
if dev is None:
    raise ValueError('Device not found!')

dev.reset()


cfg = dev.get_active_configuration()
endpoints = cfg[(0, 0)]

for endpoint in endpoints:
    endpoint.clear_halt()


# I forget what this does
assert(dev.ctrl_transfer(usb.util.CTRL_IN | usb.util.CTRL_TYPE_VENDOR |
                         usb.util.CTRL_RECIPIENT_DEVICE, 20, 0, 0, 2) ==
       array('B', [0, 0]))



bulk_out = endpoints[0]  # Ednpoint 0x01, Direction OUT
bulk_in = endpoints[1]    # Endpoint 0x81. Direction IN
bulk_in2 = endpoints[2]    # Endpoint 0x82. Direction IN

interrupt_in = endpoints[3] # Endpoint 0x83. Interrupt IN


bulk_out.write(validity91.message1)
response1 = bulk_in.read(64)
assert(response1 == validity91.response1)

bulk_out.write(validity91.message2)
response2 = bulk_in.read(68)
# not the same
#assert(response2 == validity91.response2)

bulk_out.write(validity91.message3)
response3 = bulk_in.read(64)
assert(response3 == validity91.response3)

bulk_out.write(validity91.message4)
response4 = bulk_in.read(64)
assert(response4 == validity91.response4)

bulk_out.write(validity91.message5)
response5 = bulk_in.read(64)
assert(response5 == validity91.response5)

bulk_out.write(validity91.message6)
response6 = bulk_in.read(64)
assert(response6 == validity91.response6)

bulk_out.write(validity91.message7)
response7 = bulk_in.read(64)
assert(response7 == validity91.response7)

bulk_out.write(validity91.message8)
response8 = bulk_in.read(4096)
assert(len(response8) == 1962)  # this seems to be consistent
# assert(response8 == validity91.response8)


# %%
int_response1 = interrupt_in.read(8)
assert(int_response1 == array('B', [0, 0, 0, 0, 0]))
# Should return 0 (It is ready to take inputs??)
# %%
# By setting the timeout to 0, it will notify you that a finger has been put down
print("Waiting for you to put your finger")
r = interrupt_in.read(8,timeout=0)
print(r)
print("You may now remove your finger!")
# %%

img = None
for i in range(100):
    bulk_out.write(validity91.message_is_image_ready)
    res = bulk_in.read(64)
    # res == 0s seems to indicate that data is ready
    # res == 1, 0, 0, 0, 0 seems to indicate that data isn't ready

    if res[0] == 0:
        print("Data ready")

        bulk_out.write(validity91.message_read_image_part)

        # You can read the data in small chunks
        img1 = bulk_in.read(4096)

        # 6 first bytes are descriptive
        # They contain the length of the remaining array
        frame_size = img1[3]*256 + img1[2]
        if frame_size > len(img1) - 6:
            img1 = img1 + bulk_in.read(4096)

        # or you can read them all in 1 shot if you know exactly how
        # many bytes are coming in
        bulk_out.write(validity91.message_read_image_part)
        img2 = bulk_in.read(4806)

        bulk_out.write(validity91.message_read_image_part)
        img3 = bulk_in.read(4806)

        # put the 3 arrays together
        img = np.array(img1[6:] + img2[6:] + img3[6:])
        # remove the blanking lines (maybe these mean something important)
        img = img.reshape(-1, 120)[:, 8:]
        break
    elif res[0] == 1:
        print("Data not ready")
    else:
        print(res)



import matplotlib.pyplot as plt
# plot it if you wish
plt.imshow(img, vmin=0, vmax=255)
#plt.colorbar()

# %%

bulk_out.write(validity91.repeated_message1)
repeated_response1 = bulk_in.read(64)
assert(repeated_response1 == validity91.repeated_response1)


bulk_out.write(validity91.repeated_message2)
repeated_response2 = bulk_in.read(64)
assert(repeated_response2 == validity91.repeated_response2)
# %%
# Is this necessary
# The wireshark capture showed that it sent out a bulk_in2 read.
# but this only throws me an error
# res = bulk_in2.read(1024)
# print(res)

# %%

response8 = None
bulk_out.write(validity91.message8)
response8 = bulk_in.read(4096)
# assert(response8 == validity91.response8)
