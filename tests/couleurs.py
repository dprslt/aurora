#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
from PIL import Image
import time,math

data = np.zeros((64,64,3), dtype=np.uint8)

step = 0

period = 1440 / (2*math.pi)

alpha = 7
bravo = 13
charlie = period / alpha / bravo

print alpha,",",bravo,",",charlie

while True:

    r = ((math.sin(math.radians(step/alpha)) + 1) / 2) * 255
    b = ((math.sin(math.radians(step/bravo)) + 1) / 2) * 255
    g = ((math.sin(math.radians(step/charlie)) + 1) / 2) * 255



    print step, " : ",(r,g,b)

    data[:,:,0] = int(r)
    data[:,:,1] = int(g)
    data[:,:,2] = int(b)

    img = Image.fromarray(data,'RGB')
    img.save('render.png')

    step = (step + 1) % 1440

    time.sleep(0.02)
