import RPi.GPIO as GPIO
from threading import Thread
import time

class Step_Motor:

    def __init__(self, pins=[4,17,27,22], delay=0.001):
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
        self.dir = 2
        self.delay = delay
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
            if self.dir == 0:
                self.clockwise(self.delay)
            elif self.dir == 1:
                self.clockwise(2 * self.delay)
            elif self.dir == 2:
                for i in range(4):
                    for pin in range(4):
                        GPIO.output(self.control_pins[pin], 0)
                    time.sleep(self.delay)   
            elif self.dir == 3:
                self.counter_clockwise(2 * self.delay)
            elif self.dir == 4:
                self.counter_clockwise(self.delay)
        GPIO.cleanup()
    
    def update(self, dir):
        self.dir = dir

    def stop(self):
        self.stopped = True
