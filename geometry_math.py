import math

def vector(v1, v2):
        return [
            v2[0] - v1[0],
            v2[1] - v1[1],
            v2[2] - v1[2]
        ]

def cross_product(a, b):
    return [
        a[1]*b[2] - a[2]*b[1],
        a[2]*b[0] - a[0]*b[2],
        a[0]*b[1] - a[1]*b[0]
    ]


def normalize(vector):
    x = vector[0]
    y = vector[1]
    z = vector[2]
    length = math.sqrt(x*x + y*y + z*z)

    if length == 0:
        return [0, 0, 0]

    x = x / length
    y = y / length
    z = z / length

    return [x, y, z]