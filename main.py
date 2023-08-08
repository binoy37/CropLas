import numpy as np
import time
from subroutines import read_las, print_las_info, check_dimension, save_las
from subroutines import create_geometry, pick_points, crop_geometry

# Read las file
filePath = ".\\data\\"
filename = "S1.las"  # "2020_Drone_M.las"
las = read_las(filePath+filename)
print_las_info(las)

factor = 10  # Subsample
points = las.xyz
points = points[::factor]
if check_dimension(las, 'red'):
    colors = np.vstack((las.red, las.green, las.blue)).transpose()
    colors = colors[::factor]
else:
    colors = None
if check_dimension(las, 'normalx'):
    normals = np.vstack((las.normalx, las.normaly, las.normalz)).transpose()
    normals = normals[::factor]
else:
    normals = None

# Visualize point cloud
pointCloud = create_geometry(points, colors, view=False)

# Pick some points
pickedPoints = pick_points(pointCloud)

# Crop some part and save it as las file
croppedPointCloud = crop_geometry(pointCloud)
outFilename = filePath + 'cropped-' + filename[:-4] + \
              time.strftime("-%Y%m%d-%H%M%S") + '.las'
save_las(croppedPointCloud, outFilename, las, view=False)

print('\nCompleted successfully')
