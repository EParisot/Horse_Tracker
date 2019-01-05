from Pi_Videostream import PiVideoStream
from Step_Motor import Step_Motor
import cv2
from const import *
import time
import sys
import os

# create a threaded video stream, allow the camera sensor to warmup
vs = PiVideoStream().start() # def: resolution=RESOLUTION, framerate=32, format="bgr"
time.sleep(2.0)

# init motor
zero = 4
motor = Step_Motor(zero=zero).start() # def: pins=[4,17,27,22], delay=0.001, zero=2
command = zero

print("Miner Started")

while True:
    # grab the frame from the threaded video stream 
    frame = vs.read()
    # print command
    cv2.line(frame, (int((1/4)*RESOLUTION[0]), 0), (int((1/4)*RESOLUTION[0]), RESOLUTION[1]), (255, 255, 255))
    cv2.line(frame, (int((3/4)*RESOLUTION[0]), 0), (int((3/4)*RESOLUTION[0]), RESOLUTION[1]), (255, 255, 255))
    cv2.putText(frame, str(command), (10, 20), \
        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    # Display the resulting frame
    cv2.imshow('frame', frame)
    # grab command
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('a') and command > 0:
        if command - 1 != zero:
            command -= 1
        else:
            command -= 2
    elif key == ord('z'):
        command = zero
    elif key == ord('e') and command < (2 * zero):
        if command + 1 != zero:
            command += 1
        else:
            command += 2
    # save picture
    if len(sys.argv) > 1 and sys.argv[1] == "--r":
        pic_name = os.path.join("ML/Datas/Mined", str(command) + "_" + str(time.time()) + ".png")
        if frame.size != RESOLUTION:
            frame = cv2.resize(frame, RESOLUTION)
        cv2.imwrite(pic_name, frame)
    # Motor drive
    motor.update(command)
    time.sleep(0.1)
motor.stop()
vs.stop()
cv2.destroyAllWindows()
print("Stop")