import cv2
from PIL import Image
import sys
import os
import time

if len(sys.argv) > 1:
    for video_file in sys.argv[1:]:
        cap = cv2.VideoCapture(video_file)
        while(cap.isOpened()):
            # Capture frame-by-frame
            ret, frame = cap.read()
            if ret == True:
                rgb = cv2.cvtColor(cv2.resize(frame, (160, 96)), cv2.COLOR_BGR2RGB)
                img = Image.fromarray(rgb)
                img.save(os.path.join("raw/" + str(time.time()) + ".png"))
            else:
                cap.release()
else:
    print("Error : no file")
    exit(0)


