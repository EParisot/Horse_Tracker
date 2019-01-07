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
print("Model loaded, input_shape = ", model.layers[0].input_shape[1:])
win_size = model.layers[0].input_shape[1:][0]

# create a threaded video stream, allow the camera sensor to warmup
vs = PiVideoStream().start() # def: resolution=RESOLUTION, framerate=32, format="bgr"
time.sleep(2.0)

# init motor
zero = int(model.layers[-1].output_shape[-1]/2)
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
        if len(steps) == win_size:
            # Model prediction
            steps = np.array(steps)
            pred = model.predict(steps) ## Problem HERE
            pred = np.argmax(pred)
            steps = []
        steps.append(image)
        
        # Motor drive
        if pred != None:
            motor.update(pred)
        

except KeyboardInterrupt:
    print("Stop")
except:
    print("Unexpected error:", sys.exc_info())
    
motor.stop()
vs.stop()
print("Stop")
