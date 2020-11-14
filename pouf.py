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
from PIL import Image, ImageSequence, ImageDraw, ImageFont
# from luma.core.sprite_system import framerate_regulator
import roonapi
import time
import requests
import datetime
import os.path

appinfo = {
    "extension_id": "roon_oled_info",
    "display_name": "Python library oled info for Roon",
    "display_version": "1.0.0",
    "publisher": "tidalf",
    "email": "tidalf@ematome.com",
}

tiny_font = ImageFont.truetype(os.path.abspath(os.path.join(
    os.path.dirname(__file__), "fonts", "FreePixel.ttf")), 10)

def right_text(draw, y, width, margin, text):
    x = width - margin - draw.textsize(text, font=tiny_font)[0]
    draw.text((x, y), text=text, font=tiny_font, fill="white")

def title_text(draw, y, width, text):
    x = (width - draw.textsize(text)[0]) / 2
    draw.text((x, y), text=text, fill="yellow")

def get_playing(roonapid):
    found_zone = False
    for zone in roonapid.zones:
        if "state" in roonapid.zones[zone]:
            state = roonapid.zones[zone]["state"]
        if state == "playing" and "seek_position" in roonapid.zones[zone]:
            found_zone = zone
            last_zone = zone
    return found_zone

def get_api():
    token_file = ".roon_token"
    host = "192.168.33.30"  # set host if it picks the wrong one.
    token = open(token_file).read()
    roonapid = roonapi.RoonApi(appinfo, token, host=host)
    # save the token for next time
    with open(token_file, "w") as f:
        f.write(roonapid.token)  # save the token for next time
    return roonapid

def main():
    image = None

    margin = 4  # :p
    current = 0
    length = 0
    playing = ""
    playing2 = ""
    old_image_url = ""
    last_zone = ""
    roonapid = get_api()
    zone = ""
    icon_size = 64

    background = Image.new("RGB", device.size, "black")
    while True:
        found_zone = get_playing(roonapid)

        if found_zone:
            zone_id = (
                found_zone["zone_id"] if isinstance(found_zone, dict) else found_zone
            )
            zone = roonapid.zones[zone_id]

        if not "state" in zone:
            image = Image.new("RGB", device.size, "black")
        elif "now_playing" in zone:
            track = zone["now_playing"]

            if "image_key" in track:
                image_url = roonapid.get_image(track["image_key"]).replace(
                    "=500", "=%s" % device.height, 1
                )
                if image_url != old_image_url:
                    image = Image.open(requests.get(image_url, stream=True).raw)
                    old_image_url = image_url
                size = [min(*device.size)] * 2
                background = Image.new("RGB", device.size, "black")
                background.paste(
                    image.resize(size, resample=Image.LANCZOS),
                    (device.width - device.height, 0),
                )

            if "length" in track:
                length = track["length"]

            if zone["state"] == "playing" and "seek_position" in zone:
                current = zone["seek_position"]
            elif "seek_position" in track:
                current = track["seek_position"]
            
            playing = track["two_line"]["line1"]
            playing2 = track["two_line"]["line2"]

        # we draw after the cover rendering
        draw = ImageDraw.Draw(background)
        if "state" in zone:
            title_text(
                draw, margin, device.width, "%s - %s" % (zone["display_name"], zone['state'])
            )
        if 'now_playing' in zone:
            draw.text((margin, 20), text=playing, font=tiny_font)
            draw.text((margin, 35), text=playing2, font=tiny_font)

        if current: 
            w, h = device.width, device.height
            rect_right_offset = 94
            rect_top_offset = 50
            draw.text(
                (margin, 50),
                font=tiny_font,
                text="%s / %s"
                % (
                    str(datetime.timedelta(seconds=current)),
                    str(datetime.timedelta(seconds=length)),
                ),
            )

            # progressbar
            draw.rectangle(
                [
                    (rect_right_offset, rect_top_offset),          # x,y topright
                    (w - (icon_size + margin), h - (margin + 2)),  # x,y bottom left
                ]
            )
            progress_pct = (current * 100 / length) / 100
            rectangle_width = w - (icon_size + margin) - rect_right_offset 
            progress_width = rect_right_offset + ((rectangle_width) * (progress_pct))
            draw.rectangle(
                [
                    (rect_right_offset, rect_top_offset),
                    (progress_width, h - (margin + 2)),
                ],
                fill="#ffffff",
            )

        device.display(background)
        time.sleep(1)


if __name__ == "__main__":
    try:
        device = get_device()
        main()
    except KeyboardInterrupt:
        pass
