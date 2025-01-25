import math
import numpy as np

"""Matrices written in row-major form. The reason for using homogenous coordinates is precisely the same reason as to why they are called homogenous.
It provides a unifying method for transposing, rotating and scaling both vectors and points as an alternative to using affine transformations. This allows us to
ultimately use only a single matrix to represent the final transformation. It is also useful later on with the perspective projection as we can represent the
division by depth"""

def translate(pos):
    """This matrix translates 3d-objekts in 3d-space using a 4x4 matrix 
    (homogeneous coordinates for the projective plane). The functions takes
    the parameter for pos for position to translate to."""
    tx, ty, tz = pos
    return np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0], 
        [0, 0, 1, 0],
        [tx, ty, tz, 1]
    ])

def rotateX(a):
    """Rotates around the x-axis with an angle a."""
    return np.array([
        [1, 0, 0, 0],
        [0, math.cos(a), math.sin(a), 0],
        [0, -math.sin(a), math.cos(a), 0],
        [0, 0, 0, 1]
    ])

def rotateY(a):
    """Rotates around the y-axis with an angle a."""
    return np.array([
        [math.cos(a), 0, -math.sin(a), 0],
        [0, 1, 0, 0],
        [math.sin(a), 0, math.cos(a), 0],
        [0, 0, 0, 1]
    ])

def scale(n):
    """Scales with a factor n."""
    return np.array([
        [n, 0, 0, 0],
        [0, n, 0, 0],
        [0, 0, n, 0],
        [0, 0, 0, 1]
    ])