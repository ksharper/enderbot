#!/usr/bin/env python
# coding: utf-8

import Gamepad
import time
import RPi.GPIO as GPIO
import time
import math
import threading
import logging
from DRV8825 import DRV8825

def threadedMovement(side):
    logging.info("Thread for side %s: starting", side)

    try:
        if side == 0:
            Motor = DRV8825(dir_pin=13, step_pin=19, enable_pin=12, mode_pins=(16, 17, 20))
        else:
            Motor = DRV8825(dir_pin=24, step_pin=18, enable_pin=4, mode_pins=(21, 22, 27))
        Motor.SetMicroStep('hardward' ,'1/32step')
        logging.info("Motor side %s initialized", side)

        while True:
            if side == 0:
                speed = gamepad.axis('LEFT-Y')

                if speed < 0:
                    direction='backward'
                    speed = math.floor(speed * -10)
                elif speed > 0:
                    direction ='forward'
                    speed = math.floor(speed * 10)
            else:
                speed = gamepad.axis('RIGHT-Y')

                if speed < 0:
                    direction='forward'
                    speed = math.floor(speed * -10)
                elif speed > 0:
                    direction ='backward'
                    speed = math.floor(speed * 10)

            if speed < deadZone:
                Motor.Stop()
            else:
                #logging.info("Rotating %s in direction %s with speed %s", side, direction, stepperDelayMapping[speed-1])
                Motor.TurnStep(Dir=direction, steps=1, stepdelay = 1 / stepperDelayMapping[speed-1])

            time.sleep(pollInterval)

    except:
        logging.info("Motor side %s failed to initialize", side)
        Motor.Stop()
        exit()

    finally:
        Motor.stop()
        logging.info("Thread for side %s: finishing", side)

       
if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    # Gamepad settings
    gamepadType = Gamepad.Xbox360
    pollInterval = 0.00001
    deadZone = 0.1
    stepperDelayMapping = [1000,1000,1000,10000,10000,100000,100000,1000000,1000000,10000000]
    deadZone = 2
    leftSpeed = 0.0
    leftSpeed = 0.0

    # Wait for a connection
    if not Gamepad.available():
        logging.info("No gamepad connected")
        while not Gamepad.available():
            time.sleep(1.0)
    gamepad = gamepadType()
    logging.info("Gamepad connected")

    # Start the background updating
    gamepad.startBackgroundUpdates()

    leftSideMotors = threading.Thread(target=threadedMovement, args=(0,), daemon=True)
    leftSideMotors.start()
    rightSideMotors = threading.Thread(target=threadedMovement, args=(1,), daemon=True)
    rightSideMotors.start()

    try:
        while True:
            time.sleep(pollInterval)

    except KeyboardInterrupt:
        pass

    finally:
         # Ensure the background thread is always terminated when we are done
         gamepad.disconnect()
