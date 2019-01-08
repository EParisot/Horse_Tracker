from Pi_Videostream import PiVideoStream
from Step_Motor import Step_Motor
from const import *

from keras.models import load_model
import numpy as np
import time
import sys

###############################################
    
# Load model
model = load_model("model_RNN.h5")
input_shape = model.layers[0].input_shape
print("Model loaded, input_shape = ", input_shape)
win_size = input_shape[1]

# create a threaded video stream, allow the camera sensor to warmup
vs = PiVideoStream().start() # def: resolution=RESOLUTION, framerate=32, format="bgr"
time.sleep(2.0)

# init motor
zero = int(model.layers[-1].output_shape[-1]/2)
print("zero = ", zero)
motor = Step_Motor(zero=zero).start() # def: pins=[4,17,27,22], delay=0.001, zero=3

print("Tracker Started")
try:
    steps = []
    while True:
        # grab the frame from the threaded video stream 
        frame = vs.read()
        image = np.array([frame]) / 255.0
        image = image[:, CROP:]
        pred = None
        if np.array(steps).shape[0] == win_size:
            steps_np = np.array(steps)
            steps_np = np.reshape(steps_np, (1, win_size, RESOLUTION[1] - CROP, RESOLUTION[0], 3))
            # Model prediction
            pred = model.predict(steps_np) ## Problem HERE
            pred = np.argmax(pred)
            # Motor drive
            motor.update(pred)
            steps.pop(0)
        steps.append(image)

except KeyboardInterrupt:
    print("Stop")
except:
    print("Unexpected error:", sys.exc_info())
    
motor.stop()
vs.stop()
