from Pi_Videostream import PiVideoStream
from Step_Motor import Step_Motor
import cv2
from const import *
import time

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
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    elif cv2.waitKey(1) & 0xFF == ord('a') and command > 0:
        command -= 1
    elif cv2.waitKey(1) & 0xFF == ord('z'):
        command = 2
    elif cv2.waitKey(1) & 0xFF == ord('e') and command < 4:
        command += 1
    # print command
    cv2.putText(frame, str(command), (10, 10), \
        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    # Display the resulting frame
    cv2.imshow('frame', frame)
    # Motor drive
    motor.update(command)

motor.stop()
vs.stop()
cv2.destroyAllWindows()
print("Stop")