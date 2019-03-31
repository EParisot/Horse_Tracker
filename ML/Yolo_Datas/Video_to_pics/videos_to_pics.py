import os, sys, time
import cv2
sys.path.insert(1, os.path.join(sys.path[0], '../../../'))
from const import *

video_file = None

if len(sys.argv) > 1:
    for i, arg in enumerate(sys.argv):
        if arg == "--v" and len(sys.argv) > i:
            video_file = sys.argv[i + 1]

if video_file:
    cap = cv2.VideoCapture(video_file)
    i = 0
    while(cap.isOpened()):
        ret, frame = cap.read()
        if i == 7:
            resized = cv2.resize(frame,RESOLUTION)
            img_name = "out/" +  str(time.time()) + ".png"
            cv2.imwrite(img_name,resized)
        i += 1
        if i == 8:
            i = 0
    cap.release()
    cv2.destroyAllWindows()
else:
    print("No video file provided... Plea specify a video")
