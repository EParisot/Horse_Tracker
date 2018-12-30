import os
import sys

for path in os.listdir("raw"):
    directory = os.path.join("raw", path)
    if os.path.isdir(directory):
        for elem in os.listdir(directory):
            if "_" not in elem:
                os.rename(os.path.join(directory, elem), os.path.join("labelized", path + "_" + elem))
