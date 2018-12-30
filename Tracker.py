from pivideostream import PiVideoStream
from Step_Motor import Step_Motor
from PIL import Image
from keras.models import load_model
import numpy as np
import sys
import time
from const import *
    
#Load model
model = load_model("model.h5")
print("Model loaded")

# create a threaded video stream, allow the camera sensor to warmup
vs = PiVideoStream().start()
time.sleep(2.0)

motor = Step_Motor()

#test
try:
    frame = vs.read()
    img = Image.fromarray(frame)
    img.save("test.png")
except:
    print("Error : Video stream error")
    exit(0)
    
print("Tracker Started")
while True:
    # grab the frame from the threaded video stream 
    frame = vs.read()
    image = np.array([frame]) / 255.0
    
    # Model prediction
    pred = model.predict(image)
    pred = np.argmax(pred)
    
    # Motor drive
    motor.update(pred)
    
motor.stop()
vs.stop()
print("Stop")
