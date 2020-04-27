import math
from display import *


  # IMPORANT NOTE

  # Ambient light is represeneted by a color value

  # Point light sources are 2D arrays of doubles.
  #      - The fist index (LOCATION) represents the vector to the light.
  #      - The second index (COLOR) represents the color.

  # Reflection constants (ka, kd, ks) are represened as arrays of
  # doubles (red, green, blue)

AMBIENT = 0
DIFFUSE = 1
SPECULAR = 2
LOCATION = 0
COLOR = 1
SPECULAR_EXP = 4

#lighting functions
def get_lighting(normal, view, ambient, light, areflect, dreflect, sreflect ):
    ambient = calculate_ambient(ambient, areflect)
    diffuse = calculate_diffuse(light, dreflect, normal)
    specular = calculate_specular(light, sreflect, view, normal)

    red = ambient[0] + diffuse[0] + specular[0]
    blue = ambient[1] + diffuse[1] + specular[1]
    green = ambient[2] + diffuse[2] + specular[2]

    return [limit_color(red), limit_color(blue), limit_color(green)]

def calculate_ambient(alight, areflect):
    red = alight[0] * areflect[0]
    blue = alight[1] * areflect[1]
    green = alight[2] * areflect[2]
    return [red, blue, green]

def calculate_diffuse(light, dreflect, normal):
    normalize(light[0])
    normalize(normal)

    red = light[1][0] * dreflect[0] * dot_product(light[0], normal)
    blue = light[1][1] * dreflect[1] * dot_product(light[0], normal)
    green = light[1][2] * dreflect[2] * dot_product(light[0], normal)
    return [red, blue, green]

def calculate_specular(light, sreflect, view, normal):
    normalize(light[0])
    normalize(normal)
    scale = 2 * dot_product(light[0], normal)
    costheta = dot_product([normal[0] * scale - light[0][0], normal[1] * scale - light[0][1], normal[2] * scale - light[0][2]], view)
    red = light[1][0] * sreflect[0] * costheta
    blue = light[1][1] * sreflect[1] * costheta
    green = light[1][2] * sreflect[2] * costheta
    return [red, green, blue]

def limit_color(color):
    if color > 255:
        return 255
    if color < 0:
        return 0
    return int(color)

#vector functions
#normalize vetor, should modify the parameter
def normalize(vector):
    magnitude = math.sqrt( vector[0] * vector[0] +
                           vector[1] * vector[1] +
                           vector[2] * vector[2])
    for i in range(3):
        vector[i] = vector[i] / magnitude

#Return the dot porduct of a . b
def dot_product(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]

#Calculate the surface normal for the triangle whose first
#point is located at index i in polygons
def calculate_normal(polygons, i):

    A = [0, 0, 0]
    B = [0, 0, 0]
    N = [0, 0, 0]

    A[0] = polygons[i+1][0] - polygons[i][0]
    A[1] = polygons[i+1][1] - polygons[i][1]
    A[2] = polygons[i+1][2] - polygons[i][2]

    B[0] = polygons[i+2][0] - polygons[i][0]
    B[1] = polygons[i+2][1] - polygons[i][1]
    B[2] = polygons[i+2][2] - polygons[i][2]

    N[0] = A[1] * B[2] - A[2] * B[1]
    N[1] = A[2] * B[0] - A[0] * B[2]
    N[2] = A[0] * B[1] - A[1] * B[0]

    return N
