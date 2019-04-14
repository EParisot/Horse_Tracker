import cv2
import os
import ctypes

i = 0
images = [file if ".png" in file else None for file in os.listdir('.')]
img = None
key = None

print("N : next \nP: previous \nD : delete", flush=True)

def mouse_drawing(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        global images, img, i
        img = cv2.imread(images[i])
        cv2.circle(img,(x, y), 50, (0, 0, 255), 2)
        # rename file
        os.rename(images[i], images[i].split('_')[0] + "_1_" + str(round(x/img.shape[1], 2)) + "_" + str(round(y/img.shape[0], 2)) + ".png")
        images = os.listdir('.')
        cv2.imshow('Frame',img)
        
cv2.namedWindow("Frame")
cv2.setMouseCallback("Frame", mouse_drawing)

while True:
    if i >= 0 and i < len(images) and images[i] != None and "png" in images[i]:
        # open image and draw ROI
        img = cv2.imread(images[i])
        x = int(float(images[i].split('_')[2]) * img.shape[1])
        y = int(float(images[i].split('_')[3].split('.png')[0]) * img.shape[0])
        cv2.circle(img,(x, y), 50, (0, 255, 0), 2)        
        cv2.imshow('Frame',img)
        # key events
        key = cv2.waitKey(0)
        if key == 27:
            break
        elif key == ord('n') and i < len(images) - 1:
            i += 1
        elif key == ord('p') and i > 0:
            i -= 1
        elif key == ord('d'):
            # Remove file
            if ctypes.windll.user32.MessageBoxW(0, "This will remove file !", "Warning", 1) == 1:
                os.remove(images[i])
                images[i] = None
                i += 1
    elif i >= 0 and i < len(images) and images[i] == None:
        if key == ord('p'):
            i -= 1
        else:
            i += 1
    else:
        break
cv2.destroyAllWindows()
