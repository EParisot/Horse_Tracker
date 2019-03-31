import os, sys

for img_name in os.listdir(sys.argv[1]):
    os.rename(os.path.join(sys.argv[1], img_name), os.path.join(sys.argv[1], img_name.split("_")[0] + "_1_" + img_name.split("_")[1] + "_" + img_name.split("_")[2]))

