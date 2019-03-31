import os, sys

for img_name in os.listdir(sys.argv[1]):
    os.rename(os.path.join(sys.argv[1], img_name), os.path.join(sys.argv[1], img_name.split("_")[1].split(".png")[0] + "_0.1_0.1.png"))
