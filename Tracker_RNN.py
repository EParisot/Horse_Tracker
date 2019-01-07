from Pi_Videostream import PiVideoStream
from Step_Motor import Step_Motor
from const import *

from keras.models import load_model
import numpy as np
import time

###############################################
    
# Load model
model = load_model("model.h5")
print("Model loaded, input_shape = ", model.layers[0].input_shape[1:])
win_size = model.layers[0].input_shape[1:][0]

# create a threaded video stream, allow the camera sensor to warmup
vs = PiVideoStream().start() # def: resolution=RESOLUTION, framerate=32, format="bgr"
time.sleep(2.0)

# init motor
motor = Step_Motor().start() # def: pins=[4,17,27,22], delay=0.001, zero=3

print("Tracker Started")
try:
    i = 0
    steps = []
    while True:
        # grab the frame from the threaded video stream 
        frame = vs.read()
        image = np.array([frame]) / 255.0

        if i % win_size == 0: 
            # Model prediction
            pred = model.predict(np.asarray(steps))
            pred = np.argmax(pred)
            i = 0
            steps = []
        else:
            steps.append(image)
            
        # Motor drive
        motor.update(pred)
        i += 1
except:
    motor.stop()
    vs.stop()
    print("Stop")
