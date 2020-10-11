#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014-18 Richard Hull and contributors
# See LICENSE.rst for details.
# PYTHON_ARGCOMPLETE_OK

"""
Showcase viewport and hotspot functionality.

Loosely based on poster_demo by @bjerrep
https://github.com/bjerrep/ssd1306/blob/master/examples/poster_demo.py

Needs psutil (+ dependencies) installed::
  $ sudo apt-get install python-dev
  $ sudo pip install psutil
"""

import psutil
import roonapi

from demo_opts import get_device
from luma.core.virtual import viewport, snapshot

from hotspot import memory, uptime, cpu_load, clock, network, disk, music # , shairplay
import time
import random
import os.path
from demo_opts import get_device
from luma.core.virtual import viewport
from PIL import Image

appinfo = {
        "extension_id": "roon_oled_info",
        "display_name": "Python library oled info for Roon",
        "display_version": "1.0.0",
        "publisher": "tidalf",
        "email": "tidalf@ematome.com"
    }




def scroll_down(virtual, pos):
    x, y = pos
    if virtual.height > device.height:
        while y < virtual.height - device.height:
            virtual.set_position((x, y))
            y += 1
        y -= 1
    return (x, y)


def scroll_right(virtual, pos):
    x, y = pos
    if virtual.width > device.width:
        while x < virtual.width - device.width:
            virtual.set_position((x, y))
            x += 1
        x -= 1
    return (x, y)


def scroll_up(virtual, pos):
    x, y = pos
    while y >= 0:
        virtual.set_position((x, y))
        y -= 1
    y = 0
    return (x, y)


def scroll_left(virtual, pos):
    x, y = pos
    while x >= 0:
        virtual.set_position((x, y))
        x -= 1
    x = 0
    return (x, y)


def images():
  images = [
      "pixelart1.png"
      "pixelart2.png",
      "pixelart3.jpg",
      "pixelart4.jpg",
      "pixelart5.jpg"
  ]

  img_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
  'images', random.choice(images)))
  pixel_art = Image.open(img_path).convert(device.mode)
  w, h = pixel_art.size
  
  virtual = viewport(device, width=w, height=h)
  
  virtual.display(pixel_art)
  
  time.sleep(2)
  
  pos = (0, 0)
  pos = scroll_down(virtual, pos)
  time.sleep(2)
  pos = scroll_right(virtual, pos)
  time.sleep(2)
  pos = scroll_up(virtual, pos)
  time.sleep(2)
  pos = scroll_left(virtual, pos)
  time.sleep(2)



def position(max):
    forwards = range(0, max)
    backwards = range(max, 0, -1)
    while True:
        for x in forwards:
            yield x
        for x in backwards:
            yield x


def pause_every(interval, generator):
    try:
        while True:
            x = next(generator)
            if x % interval == 0:
                for _ in range(20):
                    yield x
            else:
                yield x
    except StopIteration:
        pass


def intersect(a, b):
    return list(set(a) & set(b))


def first(iterable, default=None):
    if iterable:
        for item in iterable:
            return item
    return default


def main():
    if device.rotate in (0, 2):
        # Horizontal
        widget_width = device.width // 2
        widget_height = device.height
    else:
        # Vertical
        widget_width = device.width
        widget_height = device.height // 2


    token = open('/opt/roonlcd/mytokenfile').read()
    roonapid = roonapi.RoonApi(appinfo, token)
    # save the token for next time
    with open('/opt/roonlcd/mytokenfile', 'w') as f:
      f.write(roonapid.token)# save the token for next time

    # Either function or subclass
    #  cpuload = hotspot(widget_width, widget_height, cpu_load.render)
    #  cpuload = cpu_load.CPU_Load(widget_width, widget_height, interval=1.0)
    # utime = snapshot(widget_width, widget_height, uptime.render, interval=1.0)
    # mem = snapshot(widget_width, widget_height, memory.render, interval=2.0)
    # dsk = snapshot(widget_width, widget_height, disk.render, interval=2.0)
    zoneid=0
    widgets=[]
    for zone in roonapid.zones:
        widgets.append(snapshot(widget_width, widget_height, music.get_data(roonapid, zone), interval=1.0))
        
    # shair = snapshot(widget_width, widget_height, shairplay.render, interval=2.0)
    # cpuload = snapshot(widget_width, widget_height, cpu_load.render, interval=0.5)
    # clk = snapshot(widget_width, widget_height, clock.render, interval=1.0)

    # network_ifs = psutil.net_if_stats().keys()
    # wlan = first(intersect(network_ifs, ["wlan0", "wl0"]), "wlan0")
    # eth = first(intersect(network_ifs, ["eth0", "en0"]), "eth0")
    # lo = first(intersect(network_ifs, ["lo", "lo0"]), "lo")

    # net_wlan = snapshot(widget_width, widget_height, network.stats(wlan), interval=2.0)
    # net_eth = snapshot(widget_width, widget_height, network.stats(eth), interval=2.0)
    # net_lo = snapshot(widget_width, widget_height, network.stats(lo), interval=2.0)

    # widgets = [cpuload, msc, net_eth, msc, mem, msc, dsk, msc]

    if device.rotate in (0, 2):
        virtual = viewport(device, width=widget_width * len(widgets), height=widget_height)
        for i, widget in enumerate(widgets):
            virtual.add_hotspot(widget, (i * widget_width, 0))

        for x in pause_every(widget_width, position(widget_width * (len(widgets) - 2))):
            virtual.set_position((x, 0))

    else:
        virtual = viewport(device, width=widget_width, height=widget_height * len(widgets))
        for i, widget in enumerate(widgets):
            virtual.add_hotspot(widget, (0, i * widget_height))

        for y in pause_every(widget_height, position(widget_height * (len(widgets) - 2))):
            virtual.set_position((0, y))


if __name__ == "__main__":
    try:
        device = get_device()
        # images()
        1smain()
    except KeyboardInterrupt:
        pass
