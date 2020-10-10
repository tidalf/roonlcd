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
    

# get all outputs (as dict)
# print(json.dumps(roonapid.outputs))

# receive state updates in your callback
# roonapid.register_state_callback(state_callback)


# time.sleep(100)

token = open('/opt/roonlcd/mytokenfile').read()
roonapid = roonapi.RoonApi(appinfo, token)
# save the token for next time
with open('/opt/roonlcd/mytokenfile', 'w') as f:
    f.write(roonapid.token)# save the token for next time

def render(draw, width, height):
    # dac_zone='160155895af4376afe74c12da20fdadfc027'
    dac_zone=0
    margin = 3
    try: 
      for zone in roonapid.zones:
          if roonapid.zones[zone]['display_name'] == "evo":
              dac_zone=zone
  
              playing=roonapid.zones[dac_zone]['now_playing']['two_line']['line1']
              playing2=roonapid.zones[dac_zone]['now_playing']['two_line']['line2']
              current=roonapid.zones[dac_zone]['seek_position']
              length=roonapid.zones[dac_zone]['now_playing']['length']
     
              title_text(draw, margin, width, "Playing")
              draw.text( (margin, 20), text=playing, font=tiny_font)
              draw.text( (margin, 35), text=playing2, font=tiny_font)
              right_text(draw, 50, width, margin, text="%s / %s" % (str(datetime.timedelta(seconds=current)), str(datetime.timedelta(seconds=length)) ) )
    except: 
      title_text(draw, margin, width, "Not playing")

    # right_text(draw, 35, width, margin, text="%d / %d" % (current, length)) 
