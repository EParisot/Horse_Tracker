import cv2
import sys
import os

location = None
if len(sys.argv) > 1:
    location = sys.argv[1]

for image in os.listdir(location) if location != None else os.listdir('.'):
    if ".png" in image:
        img = cv2.imread(image)
        x = int(float(image.split('_')[1]) * img.shape[1])
        y = int(float(image.split('_')[2].split('.png')[0]) * img.shape[0])
        cv2.circle(img,(x,y), 50, (0,255,0), 2)
        
        cv2.imshow('image',img)

        key = cv2.waitKey(0)
        if key == 27:
            break

cv2.destroyAllWindows()
