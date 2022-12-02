
import random


# Output in P3 format, a text file containing:
# P3
# ncolumns nrows
# 255
# r1 g1 b1 r2 g2 b2 .....
def save_imageP3(width: int, height: int, fname: str, pixels):
    
    with open(fname + ".ppm", "w") as fp:

        #writes the following:
        #P3
        #<width> <height>
        #255
        fp.write("P3\n" + str(width) + " " + str(height) + "\n255\n")

        k = 0

        for j in range(0, height):

            for i in range(0, width):

                fp.write( " " + pixels[k] + " " + pixels[k+1] + " " + pixels[k+2])
                k += 3
            
            fp.write("\n")





        
pixelArray = [str(random.randint(0, 255)) for index in range(0, 30000)]

save_imageP3(100, 100, "tester", pixelArray)
