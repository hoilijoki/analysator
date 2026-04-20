import imageio.v2 as imageio
import os

path_to_files="/home/hoilijok/proj/analysator/scripts/Sanni_trace_FTEs"

# Sorted list of PNG files
filenames = sorted([f for f in os.listdir(path_to_files) if f.endswith(".png")])

# Create gif
images = [imageio.imread(f"{f}") for f in filenames]
imageio.mimsave("FID_fields.gif", images, duration=0.2)



