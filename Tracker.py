from pivideostream import PiVideoStream
from PIL import Image
from keras.models import load_model
import numpy as np
import sys
import time

#Load model
if len(sys.argv) > 1:
    model = load_model(sys.argv[1])
    print("Model loaded")
else:
    print("Error : No model specified")
    exit(0)

# create a threaded video stream, allow the camera sensor to warmup
vs = PiVideoStream().start()
time.sleep(2.0)

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
    
    #TODO Motor drive

vs.stop()
print("Stop")
