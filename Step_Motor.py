import RPi.GPIO as GPIO
import time

class Step_Motor:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        self.control_pins = [4,17,27,22]
        for pin in self.control_pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, 0)
        self.halfstep_seq = [
            [1,0,0,0],
            [1,1,0,0],
            [0,1,0,0],
            [0,1,1,0],
            [0,0,1,0],
            [0,0,1,1],
            [0,0,0,1],
            [1,0,0,1]
        ]
    
    def clockwise(self, step, delay):
        for i in range(step):
            for halfstep in self.halfstep_seq:
                for pin in range(4):
                    GPIO.output(self.control_pins[pin], halfstep[pin])
                time.sleep(delay)
                
    def counter_clockwise(self, step, delay):
        for i in range(step):
            for halfstep in reversed(self.halfstep_seq):
                for pin in range(4):
                    GPIO.output(self.control_pins[pin], halfstep[pin])
                time.sleep(delay)

    def stop(self):
        GPIO.cleanup()
