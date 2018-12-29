from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

resolution = (800, 600)
camera = PiCamera()
camera.resolution = resolution
camera.framerate = 32
rawCapture = PiRGBArray(camera, size = resolution)

time.sleep(0.1)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image = frame.array
    cv2.imshow("", image)
    key = cv2.waitKey(1) & 0xFF
    rawCapture.truncate(0)
    if key == ord("q"):
        break

