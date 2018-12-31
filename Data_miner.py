from Pi_Videostream import PiVideoStream
from Step_Motor import Step_Motor
import cv2
from const import *
import time
import os

# create a threaded video stream, allow the camera sensor to warmup
vs = PiVideoStream().start() # def: resolution=RESOLUTION, framerate=32, format="bgr"
time.sleep(2.0)

# init motor
motor = Step_Motor().start() # def: pins=[4,17,27,22], delay=0.001
command = 2

print("Miner Started")

while True:
    # grab the frame from the threaded video stream 
    frame = vs.read()
    # grab command
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('a') and command > 0:
        command -= 1
    elif key == ord('z'):
        command = 2
    elif key == ord('e') and command < 4:
        command += 1
    # save picture
    pic_name = os.path.join("ML/Datas/Mined", str(command) + "_" + str(time.time()) + ".png")
    cv2.imwrite(pic_name, frame)
    # print command
    cv2.putText(frame, str(command), (10, 10), \
        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    # Display the resulting frame
    cv2.imshow('frame', frame)
    # Motor drive
    motor.update(command)
    time.sleep(0.1)
motor.stop()
vs.stop()
cv2.destroyAllWindows()
print("Stop")