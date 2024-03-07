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
    global leftSpeed
    global rightSpeed
    global maxAccel
    logging.info("Thread for side %s: starting", side)

    try:
        if side == 0:
            Motor = DRV8825(dir_pin=13, step_pin=19, enable_pin=12, mode_pins=(16, 17, 20))
        else:
            Motor = DRV8825(dir_pin=24, step_pin=18, enable_pin=4, mode_pins=(21, 22, 27))
        logging.info("Motor side %s initialized", side)

        while True:
            try:
                if gamePadReady:
                    if side == 0:
                        newSpeed = gamepad.axis('LEFT-Y')
                        
                        if abs(newSpeed - leftSpeed) <= maxAccel:
                            leftSpeed = newSpeed
                        elif newSpeed > leftSpeed:
                            leftSpeed = leftSpeed + maxAccel
                        else:
                            leftSpeed = leftSpeed - maxAccel
                        
                        if leftSpeed < 0:
                            direction='forward'
                        elif leftSpeed > 0:
                            direction ='backward'

                        speedIndex = abs(math.floor(leftSpeed * 10))
                        #logging.info("Left: %s",leftSpeed)

                    else:
                        newSpeed = gamepad.axis('RIGHT-Y')
                        
                        if abs(newSpeed - rightSpeed) <= maxAccel:
                            rightSpeed = newSpeed
                        elif newSpeed > rightSpeed:
                            rightSpeed = rightSpeed + maxAccel
                        else:
                            rightSpeed = rightSpeed - maxAccel

                        if rightSpeed < 0:
                            direction='backward'
                        elif rightSpeed > 0:
                            direction ='forward'

                        speedIndex = abs(math.floor(rightSpeed * 10))
                        #logging.info("Right: %s",speedIndex)

                    if speedIndex < deadZone:
                        Motor.Stop()
                    else:
                        #logging.info("Rotating %s in direction %s with speed %s", side, direction, stepperDelayMapping[speed-1])
                        Motor.TurnStep(Dir=direction, steps=1, stepdelay = 1 / stepperDelayMapping[speedIndex-1])

                time.sleep(pollInterval)
            
            except IOError as e:
                logging.info("Gamepad disconnected")

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

    gamepadType = Gamepad.Xbox360
    stepperDelayMapping = [1024,1024,1280,1536,2048,2560,3584,5120,8192,8192]
    pollInterval = 1/8192
    deadZone = 3
    leftSpeed = 0.0
    rightSpeed = 0.0
    maxAccel = 0.002
    gamePadReady = False

    if Gamepad.available():
        gamepad = gamepadType()
        gamepad.startBackgroundUpdates()
        gamePadReady = True
    else:
        gamePadReady = False

    leftSideMotors = threading.Thread(target=threadedMovement, args=(0,), daemon=True)
    leftSideMotors.start()
    rightSideMotors = threading.Thread(target=threadedMovement, args=(1,), daemon=True)
    rightSideMotors.start()

    
    try:
        while True:
            try:
                if not Gamepad.available():
                    gamePadReady = False
                    logging.info("No gamepad connected")
                    while not Gamepad.available():
                        time.sleep(1.0) 
                    gamepad = gamepadType()
                    gamepad.startBackgroundUpdates()
                    gamePadReady = True
                    logging.info("Gamepad connected")

                time.sleep(1)
            
            except IOError:
                logging.info("Gamepad disconnected")

    except KeyboardInterrupt:
        pass

    finally:
         # Ensure the background thread is always terminated when we are done
         gamepad.disconnect()
