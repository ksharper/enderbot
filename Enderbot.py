#!/usr/bin/env python
# coding: utf-8

# Load the gamepad and time libraries
import Gamepad
import time

# Gamepad settings
gamepadType = Gamepad.Xbox360

# Wait for a connection
if not Gamepad.available():
    print('Please connect your gamepad...')
    while not Gamepad.available():
        time.sleep(1.0)
gamepad = gamepadType()
print('Gamepad connected')

# Handle joystick updates one at a time
while gamepad.isConnected():
    # Wait for the next event
    eventType, control, value = gamepad.getNextEvent()

    if eventType == 'AXIS' and control == 'LEFT-Y':
        print(f'Left: {value}')
