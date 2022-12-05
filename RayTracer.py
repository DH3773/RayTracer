import sys
from collections import namedtuple
from dataclasses import dataclass, field
import ppm
import numpy as np
import math


Resolution = namedtuple("Resolution", ["x", "y"])
Back = namedtuple("Back", ["r", "g", "b"])
Ambient = namedtuple("Ambient", ["r", "g", "b"])


@dataclass
class Sphere:
    name: str
    xPos: float
    yPos: float
    zPos: float

    #What are these?
    xSCL: float
    ySCL: float
    zSCL: float

    r: float
    g: float
    b: float

    ambient: float
    diffuse: float
    spectral: float

    #what is this?
    n: float

    M_Inv: any = field(init=False)

    def generateInverseMatrix(self):
        M = np.array([[self.xSCL, 0, 0, self.xPos],
                      [0, self.ySCL, 0, self.yPos],
                      [0, 0, self.zSCL, self.zPos],
                      [0,   0,   0,  1]], dtype=float)
                    
        self.M_Inv = np.linalg.inv(M)



@dataclass
class Light:
    name: str
    xPos: float
    yPos: float
    zPos: float

    r: float
    g: float
    b: float

@dataclass
class Ray:
    pos: any
    direction: any



def Trace(ray, depth):

    #CONSIDER FLOATING POINT ERRORS
    if depth == 4 :
        point, sphere = compute_closest_intersection(ray, True)
    else: 
        point, sphere = compute_closest_intersection(ray, False)
    
    #if no intersection, return background colour
    if point == None: 
        return 255, 255, 255
    
    colour_local = [0, 0, 0]

    # for light in lights:
    #   colour_local += shadowRay(light, point)
    
    # if depth != 0:
    #   colour_reflect = Trace(reflect(ray), lights, depth-1)
    # else:
    #   colour_reflect = [0, 0, 0]

    # colour_total = colour_local + k_reflection * colour_reflect


    r = 1
    g = 0.5
    b = 0.5

    #TODO clamp the values to 1
    return int(255*r), int(255*g), int(255*b)




def shadow_ray(light, point):

    r, g, b = 0

    for l in lights:
        ray = Ray([point[0], point[1], point[2]],
                  [l.xPos, l.yPos, l.zPos])
        for s in spheres:

            M = np.array([[s.xSCL, 0, 0, s.xPos],
                        [0, s.ySCL, 0, s.yPos],
                        [0, 0, s.zSCL, s.zPos],
                        [0,   0,   0,  1]], dtype=float)

            M_Inv = np.linalg.inv(M)

            S = np.array([[ray.pos[0]],
                        [ray.pos[1]],
                        [ray.pos[2]],
                            [1]      ], dtype=float)

            c = np.array([[ray.direction[0]],
                        [ray.direction[1]],
                        [ray.direction[2]],
                                [0]         ], dtype=float)

            S_Prime = np.matmul(M_Inv, S)

            c_Prime = np.matmul(M_Inv, c)

            A = np.linalg.norm(c_Prime)**2
            B = np.dot( np.transpose(S_Prime).flatten(), np.transpose(c_Prime).flatten() )
            C = np.linalg.norm(S_Prime)**2 - 1

            if (B**2) - (A*C) >= 0 : #if there's solutions then light is obstructed
                continue
            else:
                r += l.r
                g += l.g
                b += l.b

    return r, g, b
            



def compute_closest_intersection(ray, fromEye: bool):
    
    # for EACH sphere:
    #   inverse transpose ray to get S'+c't
    #   find the intersection th (both t of two solutions [if we get 2], one could be before the near plane and one after)
    #   use th in the untransformed ray S+ct to find the intersection point
    #   for the normal, use the inverse transpose
    # Choose the sphere in which th is the minimum
    # return the intersection point on that sphere

    min_dist_sphere = None
    min_th = float("inf")

    for s in spheres:

        S = ray.pos

        c = ray.direction

        S_Prime = np.matmul(s.M_Inv, S)

        c_Prime = np.matmul(s.M_Inv, c)

        A = np.linalg.norm(c_Prime)**2
        B = 2 * np.dot( np.transpose(S_Prime).flatten(), np.transpose(c_Prime).flatten() )
        C = np.linalg.norm(S_Prime)**2 - 1

        solutions = (B**2) - (A*C)

        if solutions < 0 : #no solution case
            continue

        elif solutions > 0 : #if there's multiple solutions then we compute the two th's
            #print("hit sphere", s, ray)
            th1 = (-B/A) + math.sqrt( (B**2) - (A*C) )/A
            th2 = (-B/A) - math.sqrt( (B**2) - (A*C) )/A

        #single solution means ray is tangent to the curve, we ignore this case

        #check if the new solutions are smaller than the prior minimum.
        #if this ray is coming from the eye, check both solutions incase sphere clips the near plane

        if min_th > th1:
            if not fromEye or th1 >= near:
                min_th = th1
                min_dist_sphere = s
        
        if min_th > th2:
            if not fromEye or th2 >= near:
                min_th = th2
                min_dist_sphere = s

    if min_th == float("inf"): #case of no intersections
        return None, None

    else:
    #calculate point of intersection and return the sphere it's on
        point = (ray.pos[0] + min_th * ray.direction[0], 
                ray.pos[1] + min_th * ray.direction[1],
                ray.pos[2] + min_th * ray.direction[2])

        return point, min_dist_sphere






def main():
    filename = sys.argv[1]
    
    with open(filename, "r") as fp:

        lines = fp.read().splitlines()

        global spheres, lights, near, left, right, top, bottom, back, ambient
       
        spheres = []
        lights = []

        
        #performs the file parsing
        for line in lines:
            if line == "":
                continue

            l = line.split()

            if l[0] == "NEAR":
                near = int(l[1])
            
            elif l[0] == "LEFT":
                left = int(l[1])

            elif l[0] == "RIGHT":
                right = int(l[1])

            elif l[0] == "TOP":
                top = int(l[1])

            elif l[0] == "BOTTOM":
                bottom = int(l[1])

            elif l[0] == "RES":
                res = Resolution(int(l[1]), int(l[2]))

            elif l[0] == "SPHERE": #fills spheres list with sphere instances
                s = Sphere(l[1], float(l[2]), float(l[3]),
                                 float(l[4]), float(l[5]), float(l[6]),
                                 float(l[7]), float(l[8]), float(l[9]),
                                 float(l[10]), float(l[11]), float(l[12]),
                                 float(l[13]), float(l[14]))
                s.generateInverseMatrix()
                spheres.append(s)

            elif l[0] == "LIGHT": #fills lights list with light instances
                lights.append(Light(l[1], float(l[2]), float(l[3]), float(l[4]),
                                    float(l[5]), float(l[6]), float(l[7])))

            elif l[0] == "BACK":
                back = Back(float(l[1]), float(l[2]), float(l[3]))
            
            elif l[0] == "AMBIENT":
                ambient = Ambient(float(l[1]), float(l[2]), float(l[3]))

            elif l[0] == "OUTPUT":
                output = l[1]


    #performs tracing and output immediately to file after each trace
    with open(output, "w") as fp:

        #writes the following:
        #P3
        #<width> <height>
        #255
        fp.write("P3\n" + str(res.x) + " " + str(res.y) + "\n255\n")

        for r in range(0, res.y):

            #calculate y coordinate of pixel
            H = (top - bottom) / 2
            v = H - ( H * 2 * r / res.y )

            for c in range(0, res.x):

                #calculate x coordinate of pixel
                W = (right - left) / 2
                u = -W + (W * 2 * c / res.x)

                #generate ray
                eye = np.array([[0],
                                [0],
                                [0],
                                [1]], dtype=float)

                direction = np.array([[u],
                                      [v],
                                      [-near],
                                      [0]], dtype=float)
                ray = Ray(eye, direction)

                #trace ray
                r, g, b = Trace(ray, 4)
                fp.write( " " + str(r) + " " + str(g) + " " + str(b))
            
            fp.write("\n")



    return

if __name__ == "__main__":
    main()
