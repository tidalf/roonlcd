#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2017-2020 Richard Hull and contributors
# See LICENSE.rst for details.
# PYTHON_ARGCOMPLETE_OK

"""
Displays an animated gif.
"""

from pathlib import Path
from demo_opts import get_device
from PIL import Image, ImageSequence, ImageDraw
from luma.core.sprite_system import framerate_regulator
import roonapi
import time
import requests
import datetime
from hotspot.common import title_text, right_text, tiny_font

appinfo = {
        "extension_id": "roon_oled_info",
        "display_name": "Python library oled info for Roon",
        "display_version": "1.0.0",
        "publisher": "tidalf",
        "email": "tidalf@ematome.com"
    }
  
def title_text(draw, y, width, text):
    x = (width - draw.textsize(text)[0]) / 2
    draw.text((x, y), text=text, fill="yellow")

def main():
    size = [min(*device.size)] * 2
    host = "192.168.33.30" # set host if it picks the wrong one.
    token = open('mytokenfile').read()
    old_image_url = ''
    roonapid = roonapi.RoonApi(appinfo, token, host=host)
    # save the token for next time
    with open('mytokenfile', 'w') as f:
      f.write(roonapid.token)# save the token for next time
    # image_composition = ImageComposition(device)
    last_zone = ''
    background = Image.new("RGB", device.size, "black")
    image = None
    margin = 4 # :p
    current = 0
    length = 0
    playing = ''
    playing2 = ''
    zone = False

    while True:

        found_zone = False
        for zone in roonapid.zones:
            if 'state' in roonapid.zones[zone]:
                state = roonapid.zones[zone]['state']
            if state == "playing" and 'seek_position' in roonapid.zones[zone]:
                found_zone = zone
                last_zone = zone

        if not found_zone:
          time.sleep(1)
          # device.display(background)

        if not found_zone:
           if last_zone:
              found_zone=last_zone
           else:
              found_Zone=next(iter(roonapid.zones.values()))
              
        if found_zone:
          zone_id = found_zone['zone_id'] if isinstance(found_zone,dict) else found_zone
          zone = roonapid.zones[zone_id]

        if 'state' in zone:
            state = zone['state']
            
            if "now_playing" in zone:
                now = zone['now_playing']
                playing = now['two_line']['line1']
                playing2 = now['two_line']['line2']
                
                if "image_key" in now: 
                  image_url = roonapid.get_image(now['image_key']).replace('=500','=64',1)
                  if image_url != old_image_url:
                      image = Image.open(requests.get(image_url, stream=True).raw)
                      old_image_url = image_url
                  background = Image.new("RGB", device.size, "black")
                  background.paste(image.resize(size, resample=Image.LANCZOS), (192,0))

                if "length" in now:
                  length = now['length']
                if state == "playing" and 'seek_position' in zone:
                  current = zone['seek_position']
                elif "seek_position" in now:
                  current = now['seek_position']
            else:
              image = Image.new("RGB", device.size, "black")
            
        draw = ImageDraw.Draw(background)
        if 'state' in zone:
          title_text(draw, margin, 256, "%s - %s" % (zone['display_name'], state) )

        if current:
          draw.text( (margin, 50), text="%s / %s" % (str(datetime.timedelta(seconds=current)), str(datetime.timedelta(seconds=length)) ) )
          
        draw.text( (margin, 20), text=playing, font=tiny_font)
        draw.text( (margin, 35), text=playing2, font=tiny_font)

        device.display(background)
        time.sleep(1)

if __name__ == "__main__":
    try:
        device = get_device()
        main()
    except KeyboardInterrupt:
        pass
