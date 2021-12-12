from utils import *

lines = get_day(2).split("\n")
########################################
x, z = 0, 0
for line in lines:
    command, dist = line.split(" ")
    dist = int(dist)
    if command == "forward":
        x += dist
    elif command == "up":
        z += dist
    elif command == "down":
        z -= dist
print(x * z)
#########################################
x, z, aim = 0, 0, 0
for line in lines:
    command, dist = line.split(" ")
    dist = int(dist)
    if command == "forward":
        x += dist
        z += aim * dist
    elif command == "up":
        aim -= dist
    elif command == "down":
        aim += dist
    else:
        print(command)
        exit()
    debug_print(f"{line} {x=} {z=} {aim=}")
print(x * z)
