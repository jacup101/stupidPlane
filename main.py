'''
Student Author Name: Joshua Pulido
Project 2
Fall 2022
COMP 313: Computer Graphics
Professor Schiffer

'''
import matplotlib.pyplot as plt
import numpy as np

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

def rotate_list(all_coords, shape, global_coords, angle, axis, plot = False):
    coord_list = []
    for i in range(len(all_coords)):
        coord_list.append(convert_list_to_coord(rotate(convert_coord_to_list(all_coords[i]), global_coords, angle, generate_matrix(axis, angle))))
    # print(coord_list)
    if plot:
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

# Plots an object file
# Takes center_vector, objects (list of file names, without .obj), and inputs (list of rotation inputs in the format [angle, axis]) as params
def plot_obj_file(center_vector, objects, inputs):
    test = None
    obj_coords = {}
    obj_faces = {}
    current_obj = "none"

    for obj in objects:
        current_obj = obj
        obj_faces[current_obj] = []
        obj_coords[current_obj] = []
        
        with open("{object}.obj".format(object = current_obj), 'r') as f:
            lines = f.readlines()
        f.close()
        for line in lines:
            if 'v' in line:
                coord = handle_vertices(line)
                if coord is not None:
                    obj_coords[current_obj].append(coord)
            if 'f' in line:
                faces = handle_faces(line)
                if faces is not None:
                    obj_faces[current_obj].append(faces)

    for i in objects:
        for input in inputs:
            obj_coords[i] = rotate_list(obj_coords[i], obj_faces[i], center_vector, input[0], input[1])
        plot_shape(obj_faces[i], obj_coords[i], center_vector)


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

# Convert vertices to float values, from strings
def vertice_to_float(vertex):
    # For z values, remove the \n
    vert = vertex.replace("\n", "")
    return float(vert)

# Convert faces to int values, from strings
def face_to_int(face):
    face = face.replace("\n", "")
    return int(face)

def main():
    # Adjust the center vector
    center_vector = [0, 0, 0]
    # Objects (please do not modify)
    objects = [
        "toy_plane_body",
        "toy_plane_left_front_wheel",
        "toy_plane_right_front_wheel",
        "toy_plane_left_back_wheel",
        "toy_plane_right_back_wheel",
        "toy_plane_propellor"
    ]
    inputs = []
    # I have set this up so that you can use legacy input (i.e. RxRyRz in combination with x, y, z angles). This is turned on by default
    # Alternatively, I have also implemented a command prompt input system which allows for multiple angles to be changed at will
    # This can be turned on by setting use_legacy_input bool to false
    use_legacy_input = True
    
    if use_legacy_input:
        # Use legacy input
        x_angle = 45
        y_angle = 90
        z_angle = 60
        direction = "RyRzRx"
        inputs = handle_legacy_input([x_angle, y_angle, z_angle], direction)
    else: 
        # Use command prompt input
        continueInput = True

        while continueInput:
            inputs.append(handle_input())
            print("Add another angle?")
            cont = input()
            if "y" not in cont:
                continueInput = False

    # print(inputs)
    # Plot the object file(s)
    plot_obj_file(center_vector, objects, inputs)
    plt.show()

# Used to handle dynamic input
def handle_input():
    print("Direction (x, y, z, defaults to x)")
    dir = input()
    dir = verify_dir(dir)
    print("Angle (defaults to 90)")
    angle = input()
    angle = verify_angle(angle)
    return [angle, dir]

# Used to process legacy input
def handle_legacy_input(angles, input):
    inputs = []
    for i in range(len(input)):
        if input[i:i+1] == "x":
            inputs.append([angles[0], "x"])
        if input[i:i+1] == "y":
            inputs.append([angles[1], "y"])
        if input[i:i+1] == "z":
            inputs.append([angles[2], "z"])
    return inputs

# Used to verify direction input, defaults to x axis
def verify_dir(dir):
    if dir in 'x' or dir in 'y' or dir in 'z':
        return dir
    return 'x'

# Used to verify angle input, defaults to 90 deg
def verify_angle(angle):
    try:
        return int(angle)
    except:
        return 90

# Run the main method
main()
