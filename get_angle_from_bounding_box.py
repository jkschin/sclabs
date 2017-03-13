import numpy as np
import math
import random

def get_vector(coord1, coord2):
    return coord2 - coord1

def get_vector_length(vector):
    return np.linalg.norm(vector)

def get_major_axis(vector1, vector2):
    vector1_length = get_vector_length(vector1)
    vector2_length = get_vector_length(vector2)
    return vector1 if vector1_length >= vector2_length else vector2

def get_angle(vector):
    x_axis = np.array([1, 0])
    vector = np.abs(vector)
    dot_product = np.dot(vector, x_axis)
    angle = math.acos(dot_product / get_vector_length(vector))
    if dot_product >= 0:
        return angle
    else:
        return angle + math.pi/2

def get_angle_from_box(box):
    vector1 = get_vector(box[0], box[1])
    vector2 = get_vector(box[1], box[2])
    vector = get_major_axis(vector1, vector2)
    return get_angle(vector)

def rotate_box(box, angle):
    R = np.array([  [math.cos(angle), -math.sin(angle)],
                    [math.sin(angle), math.cos(angle)]])
    new_coords = []
    for coord in box:
        new_coords.append(np.matmul(R, coord))
    return new_coords

def test():
    w = 10
    h = 5
    boxes = []
    for i in xrange(100):
        UL = [random.randint(1, 100) for i in xrange(2)]
        UR = [UL[0] + w, UL[1]]
        BL = [UL[0], UL[1] + h]
        BR = [UL[0] + w, UL[1] + h]
        box = [UL, UR, BR, BL]
        angle = math.pi/random.randint(1,10)
        rotated_box = rotate_box(box, angle)
        computed_angle = get_angle_from_box(rotated_box)
        if computed_angle == 0.0:
            computed_angle = math.pi
        assert (angle - computed_angle) <= 0.00001

if __name__ == '__main__':
    test()
    print 'Tests passed'




