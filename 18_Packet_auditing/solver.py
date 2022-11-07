#!/usr/bin/python3

import os
from PIL import Image

dir = "/tmp/packet_auditing"
# Brenda's delivery = bg_color orange = (242, 121, 48)
target_bg_color = (242, 121, 48)
# ready for pickup = package_color green = (0, 133, 71)
target_package_color = (0, 133, 71)


def parse_image(path):
    img = Image.open(path)
    pix = img.load()
    bg_color = pix[0, 0]
    package_color = pix[120, 120]
    if bg_color == target_bg_color and package_color == target_package_color:
        print(path, bg_color, package_color)


for root, dirs, files in os.walk(dir):
    for file in files:
        parse_image(os.path.join(root, file))
