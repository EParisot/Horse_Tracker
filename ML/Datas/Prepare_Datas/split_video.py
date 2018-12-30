import cv2
from PIL import Image
import sys
import os
import time

rev = False
if len(sys.argv) > 1:
    for arg in sys.argv:
        if arg == "--r":
            rev = True
        else:
            cap = cv2.VideoCapture(arg)
            while(cap.isOpened()):
                # Capture frame-by-frame
                ret, frame = cap.read()
                if ret == True:
                    rgb = cv2.cvtColor(cv2.resize(frame, (160, 96)), cv2.COLOR_BGR2RGB)
                    img = Image.fromarray(rgb)
                    if rev:
                        img = img.transpose(Image.FLIP_LEFT_RIGHT)
                    img.save(os.path.join("raw/" + str(time.time()) + ".png"))
                    time.sleep(0.1)
                else:
                    cap.release()
else:
    print("Error : no file")
    exit(0)
