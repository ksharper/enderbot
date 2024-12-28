#!/usr/bin/env python
# coding: utf-8

import pygame
import pygame.camera
from pygame.locals import *
import time
import RPi.GPIO as GPIO
import math
import logging
import cv2

format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO,
                    datefmt="%H:%M:%S")

Driver1Sleep = 12
Driver1MotorAIn1 = 17
Driver1MotorAIn2 = 27
Driver1MotorBIn1 = 22
Driver1MotorBIn2 = 23
Driver2Sleep = 13
Driver2MotorAIn1 = 24
Driver2MotorAIn2 = 25
Driver2MotorBIn1 = 26
Driver2MotorBIn2 = 16

pwm_freq = 100

GPIO.setmode(GPIO.BCM)
GPIO.setup(Driver1Sleep,GPIO.OUT)
GPIO.setup(Driver2Sleep,GPIO.OUT)
GPIO.setup(Driver1MotorAIn1,GPIO.OUT)
GPIO.setup(Driver1MotorAIn2,GPIO.OUT)
GPIO.setup(Driver1MotorBIn1,GPIO.OUT)
GPIO.setup(Driver1MotorBIn2,GPIO.OUT)
GPIO.setup(Driver2MotorAIn1,GPIO.OUT)
GPIO.setup(Driver2MotorAIn2,GPIO.OUT)
GPIO.setup(Driver2MotorBIn1,GPIO.OUT)
GPIO.setup(Driver2MotorBIn2,GPIO.OUT)

GPIO.output(Driver1Sleep,GPIO.HIGH)
GPIO.output(Driver2Sleep,GPIO.HIGH)

RightFrontMotorBackward = GPIO.PWM(Driver2MotorBIn1,pwm_freq)
RightFrontMotorForward = GPIO.PWM(Driver2MotorBIn2,pwm_freq)
RightBackMotorForward = GPIO.PWM(Driver1MotorAIn1,pwm_freq)
RightBackMotorBackward = GPIO.PWM(Driver1MotorAIn2,pwm_freq)

LeftFrontMotorForward = GPIO.PWM(Driver1MotorBIn1,pwm_freq)
LeftFrontMotorBackward = GPIO.PWM(Driver1MotorBIn2,pwm_freq)
LeftBackMotorBackward = GPIO.PWM(Driver2MotorAIn1,pwm_freq)
LeftBackMotorForward = GPIO.PWM(Driver2MotorAIn2,pwm_freq)

joysticks = []
deadZone = 20
interval = 60


pygame.init()
pygame.joystick.init()

clock = pygame.time.Clock()


clock = pygame.time.Clock()

run = True

try: 
    while run:
        clock.tick(interval)

        for event in pygame.event.get():
            if event.type == pygame.JOYDEVICEADDED:
                joy = pygame.joystick.Joystick(event.device_index)
                joysticks.append(joy)
                print("Joystick found")
            
            if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                cam.stop()
                run = False
            
        for joystick in joysticks:
            if joystick.get_button(7):
                run = False

            leftSpeed = round(-joystick.get_axis(1) * 100)
            rightSpeed= round(-joystick.get_axis(4) * 100)

            if leftSpeed > deadZone:
                LeftFrontMotorForward.start(abs(leftSpeed))
                LeftFrontMotorBackward.start(0)
                LeftBackMotorForward.start(abs(leftSpeed))
                LeftBackMotorBackward.start(0)
            elif leftSpeed < -deadZone:
                LeftFrontMotorForward.start(0)
                LeftFrontMotorBackward.start(abs(leftSpeed))
                LeftBackMotorForward.start(0)
                LeftBackMotorBackward.start(abs(leftSpeed))
            else:
                LeftFrontMotorForward.stop()
                LeftFrontMotorBackward.stop()
                LeftBackMotorForward.stop()
                LeftBackMotorBackward.stop()

            if rightSpeed > deadZone:
                RightFrontMotorForward.start(abs(rightSpeed))
                RightFrontMotorBackward.start(0)
                RightBackMotorForward.start(abs(rightSpeed))
                RightBackMotorBackward.start(0)
            elif rightSpeed < -deadZone:
                RightFrontMotorForward.start(0)
                RightFrontMotorBackward.start(abs(rightSpeed))
                RightBackMotorForward.start(0)
                RightBackMotorBackward.start(abs(rightSpeed))
            else:
                RightFrontMotorForward.stop()
                RightFrontMotorBackward.stop()
                RightBackMotorForward.stop()
                RightBackMotorBackward.stop()
            

finally:
    pygame.quit()
    GPIO.cleanup()
