import os, sys

for img_name in os.listdir(sys.argv[1]):
    os.rename(os.path.join(sys.argv[1], img_name), os.path.join(sys.argv[1], img_name.split("_")[0] + "_0_0.0_0.0.png"))
