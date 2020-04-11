# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 15:26:35 2020

@author: Kiryonn
"""


def rgb_to_hex(rgb):
    hexe = [str(hex(rgb[i]))[2:] if rgb[i]>15 else "0" + str(hex(rgb[i]))[2:] for i in range(3)]
    return "%s%s%s" % (hexe[0], hexe[1], hexe[2])

def hex_to_rgb(h):
    return (int(h[i:i+2], 16) for i in (0, 2, 4))

def infosBase(name):
    infos = {}
    infos["name"] = name
    infos["map"] = (0, 0)
    infos["life"] = 300
    infos["maxLife"] = 300
    return infos

def save(infos, file):
    for line in infos:
        file.write(str(infos[line]) + "\n")