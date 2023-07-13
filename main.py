import numpy as np
import time
from subroutines import read_las, print_las_info, save_las
from subroutines import create_geometry, pick_points, crop_geometry

# Read las file
filePath = ".\\data\\"
filename = "2020_Drone_M.las"
las = read_las(filePath+filename)
print_las_info(las)

# Subsample
factor = 5
points = las.xyz
colors = np.vstack((las.red, las.green, las.blue)).transpose()
# normals = np.vstack((las.normalx, las.normaly, las.normalz)).transpose()
if factor != 1:
    points = points[::factor]
    colors = colors[::factor]
    # normals = normals[::factor]

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
