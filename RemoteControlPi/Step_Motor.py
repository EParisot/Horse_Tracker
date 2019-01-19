import RPi.GPIO as GPIO
from threading import Thread
import time
import math

class Step_Motor:

    def __init__(self, pins=[4,17,27,22], delay=0.001, zero=3):
        GPIO.setmode(GPIO.BCM)
        self.control_pins = pins
        for pin in self.control_pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, 0)
        self.halfstep_seq = [
            [1,0,0,1],
            [1,0,0,0],
            [1,1,0,0],
            [0,1,0,0],
            [0,1,1,0],
            [0,0,1,0],
            [0,0,1,1],
            [0,0,0,1]
        ]
        self.dir = zero
        self.delay = delay
        self.zero = zero
        self.stopped = False

    def clockwise(self, delay):
        for halfstep in self.halfstep_seq:
            for pin in range(4):
                GPIO.output(self.control_pins[pin], halfstep[pin])
            time.sleep(delay)
                
    def counter_clockwise(self, delay):
        for halfstep in reversed(self.halfstep_seq):
            for pin in range(4):
                GPIO.output(self.control_pins[pin], halfstep[pin])
            time.sleep(delay)

    def start(self):
        Thread(target=self.run, args=()).start()
        return self
    
    def run(self):
        while self.stopped == False:
            if self.dir >= 0 and self.dir <= 2 * self.zero:
                if self.dir == self.zero:
                    for i in range(4):
                        for pin in range(4):
                            GPIO.output(self.control_pins[pin], 0)
                        time.sleep(self.delay) 
                elif self.dir < self.zero:
                    self.counter_clockwise(self.delay * ((self.dir + 1) ** 2))
                elif self.dir > self.zero:
                    self.clockwise(self.delay * ((self.zero - (self.dir - self.zero - 1)) ** 2))
            else:
                print("Bad-Value")
        GPIO.cleanup()
    
    def update(self, dir):
        self.dir = dir

    def stop(self):
        self.stopped = True
