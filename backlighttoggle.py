#!/GitHub/Raspberry/KivyHomeScreen
#
#   backlight-toggle.py
#     
#   RPi 7" Touchscreen Display
#          Toggles backlight on/off when called

from subprocess import call
import time

def set_backlight(command):
    file = open('/sys/devices/platform/rpi_backlight/backlight/rpi_backlight/bl_power','r+')
   
    if command == 'off': bl_set = 1
    if command == 'on': bl_set = 0

    bl_update = str(bl_set)
    file.seek(0)
    file.write(bl_update)
    file.close