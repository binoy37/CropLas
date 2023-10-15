import numpy as np
import time
from subroutines import read_las, print_las_info, get_points, save_las
from subroutines import create_geometry, pick_points, crop_geometry

# Read las file
filePath = ".\\data\\"
filename = "2020_Drone_M.las"

las = read_las(filePath+filename)
print_las_info(las)

factor = 1  # Subsample
points, colors, normals = get_points(las, sampling_factor=1)

# Visualize point cloud
pointCloud = create_geometry(points, colors, view=False)

# Pick some points
pickedPoints = pick_points(pointCloud)

# Crop some part and save it as las file
croppedPointCloud = crop_geometry(pointCloud)
outFilename = filePath + 'cropped-' + filename[:-4] + \
              time.strftime("-%Y%m%d-%H%M%S") + '.las'
save_las(croppedPointCloud, outFilename, las, view=True)

print('\nCompleted successfully')
