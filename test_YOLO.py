from keras.models import load_model
import numpy as np
import cv2
import os
import sys

usage = "usage: python test_YOLO.py --m model.h5 --p path/to/my_pics"

model = None
directory = None

if len(sys.argv) > 1:
    for i, arg in enumerate(sys.argv):
        if arg == "--m":
            if ".h5" in sys.argv[i + 1]:
                model = load_model(sys.argv[i + 1])
                w = int(model.layers[-2].output_shape[-1])
                h = int(model.layers[-1].output_shape[-1])
                print("Model ", sys.argv[i + 1], " Loaded\n", "outputs = ", str(w), " " + str(h), flush=True)
            else:
                print("No model provided, please specify a model (--m model.h5)")
                exit()
        elif arg == "--p":
            if os.path.isdir(sys.argv[i + 1]):
                directory = sys.argv[i + 1]
            else:
                print("No pictures path provided, please specify a path where to find pictures (--p path/to/my_images)")

if directory and model:
    images = [file if ".png" in file else None for file in os.listdir(directory)]
    img = None
    i = 0
    while True:
        if i >= 0 and i < len(images) and images[i] != None:
            # open image and draw ROI
            img = cv2.imread(os.path.join(directory, images[i]))
            img_to_pred = np.array([img]) / 255.0
            # predict
            pred = model.predict(img_to_pred)
            for j, elem in enumerate(pred):
                pred[j] = np.argmax(elem)
            pres = pred[0]
            if pres == 1:
                x = int(img.shape[1] / w) * pred[1] + int((img.shape[1] / w) / 2)
                y = int(img.shape[0] / h) * pred[2] + int((img.shape[0] / h) / 2)
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
        elif i >= 0 and i < len(images) and images[i] == None:
            i += 1
        else:
            break
    cv2.destroyAllWindows()
else:
    print(usage)
