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

from time import sleep
from shairportmetadatareader import AirplayPipeListener #, AirplayPipeListener

artist=''
track=''
def on_track_info(lis, info):
    """
    Print the current track information.
    :param lis: listener instance
    :param info: track information
    """
    artist=info['songartist']
    track=info['itemname']

listener = AirplayPipeListener() # You can use AirplayPipeListener or AirplayMQTTListener
listener.bind(track_info=on_track_info) # receive callbacks for metadata changes
listener.start_listening() # read the data asynchronously from the udp server
# print(json.dumps(roonapid.outputs))

# receive state updates in your callback
# roonapid.register_state_callback(state_callback)


# time.sleep(100)

def render(draw, width, height):
    # dac_zone='160155895af4376afe74c12da20fdadfc027'
    title_text(draw, margin, width, "On Airplay" % interface )
    draw.text( (margin, 20), text=artist, font=tiny_font)
    draw.text( (margin, 35), text=track, font=tiny_font)
    # right_text(draw, 35, width, margin, text="%d / %d" % (current, length)) 
