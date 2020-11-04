#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014-18 Richard Hull and contributors
# See LICENSE.rst for details.

# from datetime import datetime
import psutil
from hotspot.common import title_text, right_text, tiny_font

import roonapi
import time
import datetime

def state_callback(event, changed_items):
    print("%s: %s" %(event, changed_items))

appinfo = {
        "extension_id": "roon_oled_info",
        "display_name": "Python library oled info for Roon",
        "display_version": "1.0.0",
        "publisher": "tidalf",
        "email": "tidalf@ematome.com"
    }
  

def get_playing(roonapid):
  idx = 0
  found = 0
  for zone in roonapid.zones:
    if 'state' in roonapid.zones[zone]:
      state = roonapid.zones[zone]['state']
      if state == "playing" and 'seek_position' in roonapid.zones[zone]:
         found = idx
         return found
    idx = idx + 1
  return -1

def get_data(roonapid, dac_zone): 

  def render(draw, width, height):
      margin = 3
      playing = ''
      playing2 = ''
      current = 0
      length = 0
      if 'state' in roonapid.zones[dac_zone]:
          state = roonapid.zones[dac_zone]['state']
          title_text(draw, margin, width, "%s - %s" % (roonapid.zones[dac_zone]['display_name'], state) )
          if "now_playing" in roonapid.zones[dac_zone]:
            playing=roonapid.zones[dac_zone]['now_playing']['two_line']['line1']
            playing2=roonapid.zones[dac_zone]['now_playing']['two_line']['line2']
            if "image_key" in roonapid.zones[dac_zone]['now_playing']: 
              image=roonapid.get_image(roonapid.zones[dac_zone]['now_playing']['image_key'])
            if "length" in roonapid.zones[dac_zone]['now_playing']:
              length=roonapid.zones[dac_zone]['now_playing']['length']
            if state == "playing" and 'seek_position' in roonapid.zones[dac_zone]:
              current=roonapid.zones[dac_zone]['seek_position']
            elif "seek_position" in roonapid.zones[dac_zone]['now_playing']:
              current=roonapid.zones[dac_zone]['now_playing']['seek_position']
            if current:
              draw.text( (margin, 50), text="%s / %s" % (str(datetime.timedelta(seconds=current)), str(datetime.timedelta(seconds=length)) ) )
          
          draw.text( (margin, 20), text=playing, font=tiny_font)
          draw.text( (margin, 35), text=playing2, font=tiny_font)
  return render
