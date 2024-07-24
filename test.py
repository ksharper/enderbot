import RPi.GPIO as GPIO          
from time import sleep

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

RightFrontMotorBackward = GPIO.PWM(Driver2MotorBIn1,100)
RightFrontMotorForward = GPIO.PWM(Driver2MotorBIn2,100)
RightBackMotorForward = GPIO.PWM(Driver2MotorAIn1,100)
RightBackMotorBackward = GPIO.PWM(Driver2MotorAIn2,100)

LeftFrontMotorForward = GPIO.PWM(Driver1MotorBIn1,100)
LeftFrontMotorBackward = GPIO.PWM(Driver1MotorBIn2,100)
LeftBackMotorBackward = GPIO.PWM(Driver1MotorAIn1,100)
LeftBackMotorForward = GPIO.PWM(Driver1MotorAIn2,100)

# RightFrontMotorBackward.start(0)
# RightFrontMotorForward.start(50)

# sleep(2)

# RightFrontMotorBackward.start(0)
# RightFrontMotorForward.start(0)

# RightBackMotorBackward.start(0)
# RightBackMotorForward.start(50)

# sleep(2)

# RightBackMotorBackward.start(0)
# RightBackMotorForward.start(0)

# LeftFrontMotorBackward.start(0)
# LeftFrontMotorForward.start(50)

# sleep(2)

# LeftFrontMotorBackward.start(0)
# LeftFrontMotorForward.start(0)

# LeftBackMotorBackward.start(0)
# LeftBackMotorForward.start(50)

# sleep(2)

# LeftBackMotorBackward.start(0)
# LeftBackMotorForward.start(00)


RightFrontMotorBackward.start(0)
RightFrontMotorForward.start(50)
RightBackMotorBackward.start(0)
RightBackMotorForward.start(50)
LeftFrontMotorBackward.start(50)
LeftFrontMotorForward.start(0)
LeftBackMotorBackward.start(50)
LeftBackMotorForward.start(0)

sleep(2)

GPIO.cleanup()

