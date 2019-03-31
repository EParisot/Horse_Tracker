from keras.models import load_model
import numpy as np
import cv2
import os

i = 0
directory = "ML/Yolo_Datas/Val"
images = [file if ".png" in file else None for file in os.listdir(directory)]
img = None
model = load_model("model_YOLO.h5")
w = int(model.layers[-2].output_shape[-1])
h = int(model.layers[-1].output_shape[-1])
print("Model Loaded", "outputs = ", str(w), " " + str(h), flush=True)



while True:
    if i >= 0 and i < len(images) and images[i] != None:
        # open image and draw ROI
        img = cv2.imread(os.path.join(directory, images[i]))
        img_to_pred = np.array([img]) / 255.0
        # predict
        pred = model.predict(img_to_pred)
        for j, elem in enumerate(pred):
            pred[j] = np.argmax(elem)
        x = int(img.shape[1] / w) * pred[0] + int((img.shape[1] / w) / 2)
        y = int(img.shape[0] / h) * pred[1] + int((img.shape[0] / h) / 2)
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