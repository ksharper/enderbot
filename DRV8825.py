import RPi.GPIO as GPIO
import time

MotorDir = [
    'forward',
    'backward',
]

ControlMode = [
    'hardward',
    'softward',
]

class DRV8825():
    def __init__(self, dir_pin, step_pin, enable_pin, mode_pins):
        self.dir_pin = dir_pin
        self.step_pin = step_pin        
        self.enable_pin = enable_pin
        self.mode_pins = mode_pins
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.dir_pin, GPIO.OUT)
        GPIO.setup(self.step_pin, GPIO.OUT)
        GPIO.setup(self.enable_pin, GPIO.OUT)
        GPIO.setup(self.mode_pins, GPIO.OUT)
        
    def digital_write(self, pin, value):
        GPIO.output(pin, value)
        
    def Stop(self):
        self.digital_write(self.enable_pin, 0)
    
    def SetMicroStep(self, mode, stepformat):
        microstep = {'fullstep': (0, 0, 0),
                     'halfstep': (1, 0, 0),
                     '1/4step': (0, 1, 0),
                     '1/8step': (1, 1, 0),
                     '1/16step': (0, 0, 1),
                     '1/32step': (1, 0, 1)}

        if (mode == ControlMode[1]):
            self.digital_write(self.mode_pins, microstep[stepformat])
        
    def TurnStep(self, Dir, steps, stepdelay=0.005):
        if (Dir == MotorDir[0]):
            self.digital_write(self.enable_pin, 1)
            self.digital_write(self.dir_pin, 0)
        elif (Dir == MotorDir[1]):
            self.digital_write(self.enable_pin, 1)
            self.digital_write(self.dir_pin, 1)
        else:
            self.digital_write(self.enable_pin, 0)
            return

        if (steps == 0):
            return
            
        for i in range(steps):
            self.digital_write(self.step_pin, True)
            time.sleep(stepdelay)
            self.digital_write(self.step_pin, False)
            time.sleep(stepdelay)
