from Pi_Videostream import PiVideoStream
import numpy as np
import cv2
import time

# create a threaded video stream, allow the camera sensor to warmup
vs = PiVideoStream().start() # def: resolution=RESOLUTION, framerate=32, format="bgr"
time.sleep(2.0)

while True:
    # grab the frame from the threaded video stream 
    frame = vs.read()
    # Display the resulting frame
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()