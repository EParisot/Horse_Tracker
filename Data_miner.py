from Pi_Videostream import PiVideoStream
from Step_Motor import Step_Motor
import cv2
from const import *
import time
import os
from inputs import get_gamepad

# create a threaded video stream, allow the camera sensor to warmup
resolution = (400, 300)
vs = PiVideoStream(resolution=resolution).start() # def: resolution=RESOLUTION, framerate=32, format="bgr"
time.sleep(1.0)

# init motor
zero = 5
motor = Step_Motor(zero=zero, delay=0.005).start() # def: pins=[4,17,27,22], delay=0.001, zero=3
x_val = zero

rec = False

print("Miner Started")

while True:
    # grab the frame from the threaded video stream 
    frame = vs.read()
    # grab x_val
    events = get_gamepad()
    for event in events:
        if event.code == "ABS_X":
            x_val = int(((event.state + 32768) / 65535) * (2 * zero) + 1) 
        elif event.code == "BTN_SOUTH":
            if rec == False:
                rec = True
            else:
                rec = False
    # save picture
    if rec == True:
        pic_name = os.path.join("ML/Datas/Mined", str(x_val) + "_" + str(time.time()) + ".png")
        img = frame
        if frame.size != RESOLUTION:
            img = cv2.resize(frame, RESOLUTION)
        cv2.imwrite(pic_name, img)
    print(x_val)
    # horizontal line
    cv2.line(frame, (0, CROP), (RESOLUTION[0], CROP), (255, 255, 255))
    # vertical lines
    cv2.line(frame, (int((1/4)*resolution[0]), 0), (int((1/4)*resolution[0]), resolution[1]), (255, 255, 255))
    cv2.line(frame, (int((3/4)*resolution[0]), 0), (int((3/4)*resolution[0]), resolution[1]), (255, 255, 255))
    cv2.putText(frame, str(x_val), (10, resolution[1] - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    # Display the resulting frame
    cv2.imshow('frame', frame)
    # Motor drive
    motor.update(x_val)
    time.sleep(0.1)
motor.stop()
vs.stop()
cv2.destroyAllWindows()
print("Stop")
