import matplotlib.pyplot as plt
import numpy as np
import time

# Add aspect ratio, to prevent distortion
figure, axes = plt.subplots()
axes.set_aspect(1)
# Set up axis
plt.axis([-10, 10, -10, 10])

def plot_shape(shape, local_coords, global_coords):
    for face in shape:
        plot_coords(face, local_coords, global_coords)

def plot_coords(face, local_coords, global_coords):
    for i in range(len(face)):
        current = local_coords[face[i] - 1]
        next = local_coords[face[(i+1) % len(face)] - 1]
        plt.plot([current['x'] + global_coords[0], next['x'] + global_coords[0]], [current['y'] + global_coords[1], next['y'] + global_coords[1]], color='k')

def rotate(local_coords, global_coords, angle, matrix):
    final_coords = []
    for i in range(len(matrix)):
        final_coords.append(np.inner(matrix[i], local_coords))
    return final_coords

def rotate_list(all_coords, shape, global_coords, angle, axis):
    coord_list = []
    for i in range(len(all_coords)):
        coord_list.append(convert_list_to_coord(rotate(convert_coord_to_list(all_coords[i]), global_coords, angle, generate_matrix(axis, angle))))
    # print(coord_list)
    plot_shape(shape, coord_list, global_coords)
    return coord_list

def convert_coord_to_list(coord):
    return [coord['x'], coord['y'], coord['z']]

def convert_list_to_coord(list_coord):
    return {'x': list_coord[0], 'y': list_coord[1], 'z': list_coord[2]}

def generate_matrix(axis, angle):
    matrices = {
        'x': [[1, 0, 0], [0, np.cos(np.radians(angle)), -1 * np.sin(np.radians(angle))], [0, np.sin(np.radians(angle)), np.cos(np.radians(angle))]],
        'y': [[np.cos(np.radians(angle)), 0, np.sin(np.radians(angle))], [0, 1, 0], [- np.sin(np.radians(angle)), 0, np.cos(np.radians(angle))]],
        'z': [[np.cos(np.radians(angle)), -1 * np.sin(np.radians(angle)), 0], [np.sin(np.radians(angle)), np.cos(np.radians(angle)), 0], [0, 0, 1]]
    }
    return matrices[axis]



def read_file():
    test = None
    coord_list = []
    obj_faces = {}
    current_obj = "none"
    with open("plane.obj", 'r') as f:
        test = f.readlines()
    for line in test:
        if 'o ' in line:
            # print(line)
            current_obj = line
            obj_faces[current_obj] = []
        if 'v' in line:
            coord = handle_vertices(line)
            if coord is not None:
                coord_list.append(coord)
        if 'f' in line:
            faces = handle_faces(line)
            if faces is not None:
                obj_faces[current_obj].append(faces)
    # print(coord_list)
    # print(obj_faces)
    for i in obj_faces:
        rotate_list(coord_list, obj_faces[i], [0, 0, 0], -45, 'y')


def handle_vertices(line):
    vertices = line.split(" ")
    if vertices[0] != 'v':
        return None
    return {'x': vertice_to_float(vertices[1]), 'y': vertice_to_float(vertices[2]), 'z': vertice_to_float(vertices[3])}

def handle_faces(line):
    faces = line.split(" ")
    if faces[0] != 'f':
        return None
    faces.pop(0)
    final_faces = []
    for face in faces:
        final_faces.append(face_to_int(face))
    return final_faces


def vertice_to_float(vertex):
    # For z values, remove the \n
    vert = vertex.replace("\n", "")
    return float(vert)

def face_to_int(face):
    face = face.replace("\n", "")
    return int(face)

def main():
    # continueInput = True
    # while continueInput:
    #    print("Direction")


    read_file()
    plt.show()

def handle_input():
    print("Direction (x, y, z, defaults to x)")
    dir = input()
    dir = verify_dir(dir)
    print("Angle")
    angle = input()
    return [dir, angle]

def verify_dir(dir):
    if dir in 'x' or dir in 'y' or dir in 'z':
        return dir
    return 'x'



main()
