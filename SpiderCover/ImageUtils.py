#!/usr/bin/env python
# -*- coding: utf-8 -*-

import colorsys
from PIL import Image

def get_dominant_color(image):

    image = image.convert('RGBA')
    image.thumbnail((200, 200))

    max_score = None
    dominant_color = None

    for count, (r, g, b, a) in image.getcolors(image.size[0] * image.size[1]):
        # 跳过纯黑色
        if a == 0:
            continue
        
        saturation = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)[1]
        y = min(abs(r * 2104 + g * 4130 + b * 802 + 4096 + 131072) >> 13, 235)
        y = (y - 16.0) / (235 - 16)
         
        # 忽略高亮色
        if y > 0.9:
            continue

        score = (saturation + 0.1) * count
         
        if score > max_score:
            max_score = score
            dominant_color = (r, g, b)
     
    return dominant_color


def hex2rgb(hexcolor):
    rgb = [(hexcolor >> 16) & 0xff, (hexcolor >> 8) & 0xff, hexcolor & 0xff]
    return rgb


def rgb2hex(rgbcolor):
    r, g, b = rgbcolor
    return (r << 16) + (g << 8) + b


def get_image_info(filepath):
    img = Image.open(filepath)

    color = rgb2hex(get_dominant_color(img))
    strs = str("%x"%(color))
    while len(strs) < 6:
        strs = '0' + strs
    strs = '#' + strs

    return (strs, img.size[0], img.size[1])
