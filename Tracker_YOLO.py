from Pi_Videostream import PiVideoStream
from Step_Motor import Step_Motor
from const import *

from keras.models import load_model
import numpy as np
import time
import sys

###############################################
    
# Load model
model = load_model("model_YOLO.h5")
print("Model loaded, input_shape = ", model.layers[0].input_shape)
w = int(model.layers[-2].output_shape[-1])
h = int(model.layers[-1].output_shape[-1])
print("outputs = ", str(w), " " + str(h))

# create a threaded video stream, allow the camera sensor to warmup
vs = PiVideoStream().start() # def: resolution=RESOLUTION, framerate=32, format="bgr"
time.sleep(2.0)

# init motor
zero = int(w / 2)
motor = Step_Motor().start() # def: pins=[4,17,27,22], delay=0.001, zero=3

print("Tracker Started")
try:
    while True:
        # grab the frame from the threaded video stream 
        frame = vs.read()
        image = np.array([frame]) / 255.0
        image = image[:, CROP:]
        
        # Model prediction
        pred = model.predict(image)
        x_pred = np.argmax(pred[1])

        # Motor drive
        motor.update(x_pred)
except KeyboardInterrupt:
    print("Stop")
except:
    print("Unexpected error:", sys.exc_info())
    
motor.stop()
vs.stop()

