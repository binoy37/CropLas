import numpy as np
import laspy as lp
import open3d as o3d


def read_las(full_file_name):  # Read a las or laz file
    print('\nLoading:', full_file_name, '...')
    las = lp.read(full_file_name)
    print('Finished loading.')
    return las


def print_las_info(las):  # Print las details
    print('\nLas version: ', las.header.version)
    # print('Classification: ', np.unique(las.classification))
    point_format = las.point_format
    print('Point format: ', point_format.id)
    print('Number of points: ', las.header.point_count)
    print("Printing available dimensions' name and type...")
    # print('Both Standard and Extra dimensions:')
    for dim in point_format.dimensions:
        print(dim.name, dim.dtype)
    return


def check_dimension(las, dimension_name):   # Check for given dimension name
    presence = False
    for dim in las.point_format.dimensions:
        if dim.name == dimension_name:
            presence = True
            break
    print("")
    if presence is False:
        print(dimension_name, "is not present.")
    else:
        print(dimension_name, "is present.")
    return presence


def check_dimension(las, dimension_name):  # Check for given dimension name
    presence = False
    for dim in las.point_format.dimensions:
        if dim.name == dimension_name:
            presence = True
            break
    print("")
    if presence is False:
        print(dimension_name, "is not present.")
    else:
        print(dimension_name, "is present.")
    return presence


def get_points(las, sampling_factor=1):
    points = las.xyz
    points = points[::sampling_factor]
    if check_dimension(las, 'red'):
        colors = np.vstack((las.red, las.green, las.blue)).transpose()
        colors = colors[::sampling_factor]
    else:
        colors = None
    if check_dimension(las, 'normalx'):
        normals = np.vstack((las.normalx, las.normaly, las.normalz)).transpose()
        normals = normals[::sampling_factor]
    else:
        normals = None
    return points, colors, normals


def create_geometry(points, colors=None, normals=None, view=False):
    point_cloud = o3d.geometry.PointCloud()
    point_cloud.points = o3d.utility.Vector3dVector(points)
    if colors is not None:
        point_cloud.colors = o3d.utility.Vector3dVector(colors/65535)
    if normals is not None:
        point_cloud.normals = o3d.utility.Vector3dVector(normals)
    if view is True:
        disp_geometry(point_cloud)
    return point_cloud


def disp_geometry(point_cloud):  # Visualize geometry
    o3d.visualization.draw_geometries([point_cloud])
    return


def pick_points(point_cloud):  # Pick few points
    print("\n1) Please pick points using [shift + left click]")
    print("2) Press [shift + right click] to undo point picking")
    print("3) After picking points, press 'Q' to close the window")
    vis = o3d.visualization.VisualizerWithEditing()
    vis.create_window()
    vis.add_geometry(point_cloud)
    vis.run()  # user picks points
    vis.destroy_window()
    picked_points = vis.get_picked_points()
    return picked_points


def crop_geometry(point_cloud):
    print("\n1) Please crop the required volume by Ctrl + mouse buttons")
    print("2) Press K to Lock / unlock camera")
    print("3) Hold Ctrl key to draw a selection polygon")
    print("   Left mouse button to add a point")
    print("   Right mouse button to remove point")
    print("   Release Ctrl key to close the polygon")
    print("4) Press C to Crop the geometry with selection region")
    print("5) After cropping, press 'Q' to close the window")
    vis = o3d.visualization.VisualizerWithEditing()
    vis.create_window()
    vis.add_geometry(point_cloud)
    vis.run()  # user crops
    vis.destroy_window()
    cropped_point_cloud = vis.get_cropped_geometry()
    print('\nNumber of points: ', np.asarray(cropped_point_cloud.points).shape[0])
    print('X, Y and Z maxima = ', np.asarray(cropped_point_cloud.points).max(axis=0))
    print('X, Y and Z minima = ', np.asarray(cropped_point_cloud.points).min(axis=0))
    return cropped_point_cloud


def save_las(cropped_point_cloud, file_name, source_las, view=False):
    if view is True:
        disp_geometry(cropped_point_cloud)
    # TODO: Check whether creating LasData from the header of the source file is better or not
    # las = lp.LasData(source_las.header)
    header = lp.LasHeader(point_format=source_las.point_format, version=source_las.header.version)
    las = lp.LasData(header)
    las.x = np.asarray(cropped_point_cloud.points)[:, 0]
    las.y = np.asarray(cropped_point_cloud.points)[:, 1]
    las.z = np.asarray(cropped_point_cloud.points)[:, 2]

    if hasattr(cropped_point_cloud, 'colors'):  # cropped_point_cloud.has_colors() ??
        colors = np.asarray(cropped_point_cloud.colors)
        if colors.shape[0] != 0:
            las.red   = colors[:, 0] * 65535
            las.green = colors[:, 1] * 65535
            las.blue  = colors[:, 2] * 65535

    if hasattr(cropped_point_cloud, 'normals'):  # cropped_point_cloud.has_normals() ??
        normals = np.asarray(cropped_point_cloud.normals)
        if normals.shape[0] != 0:
            las.normalx = normals[:, 0]
            las.normaly = normals[:, 1]
            las.normalz = normals[:, 2]

    las.write(file_name)
    return
