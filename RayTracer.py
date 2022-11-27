import sys
from collections import namedtuple
from dataclasses import dataclass




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


@dataclass
class Light:
    name: str
    xPos: float
    yPos: float
    zPos: float

    r: float
    g: float
    b: float




















def main():
    filename = sys.argv[1]
    
    with open(filename, "r") as fp:

        lines = fp.read().splitlines()

        spheres = []
        lights = []
        
        near = lines[0].split()[1]
        left = lines[1].split()[1]
        right = lines[2].split()[1]
        bottom = lines[3].split()[1]
        top = lines[4].split()[1]

        res = Resolution(lines[5].split()[1], lines[5].split()[2])

        for line in lines[6:]:
            l = line.split()
            if l[0] == "SPHERE": #fills spheres list with sphere instances
                spheres.append(Sphere(l[1], float(l[2]), float(l[3]),
                                        float(l[4]), float(l[5]), float(l[6]),
                                        float(l[7]), float(l[8]), float(l[9]),
                                        float(l[10]), float(l[11]), float(l[12]),
                                        float(l[13]), float(l[14])))

            elif l[0] == "LIGHT": #fills lights list with light instances
                lights.append(Light(l[1], float(l[2]), float(l[3]), float(l[4]),
                                    float(l[5]), float(l[6]), float(l[7])))

            elif l[0] == "BACK":
                back = Back(l[1], l[2], l[3])
            
            elif l[0] == "AMBIENT":
                ambient = Ambient(l[1], l[2], l[3])

            elif l[0] == "OUTPUT":
                output = l[1]

    return

if __name__ == "__main__":
    main()
