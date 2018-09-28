import math, array, pickle

save = pickle.load("Save.dat", "wb")


SIZE_Y = 4
NUMBER_OF_ROOMS = SIZE_Y * SIZE_Y
CENTER = int(SIZE_Y/2)

def get_room_number(x, y):
    global SIZE_Y
    return y * SIZE_Y + x

STARTING_ROOM = get_room_number(CENTER, CENTER)
rooms = [None] * NUMBER_OF_ROOMS

for x, y in range(SIZE_Y, SIZE_Y):
    print("Creating room {0}, {1}:".format(x, y))
    room = ["None"] * 4
    room[0] = input("Description of room: ")
    if get_room_number(x,y-1) > 0:
        room[1] = "North"
    if get_room_number(x-1,y) > 0:
        room[2] = "East"
    if get_room_number(x+1,y) < SIZE_Y * (y+1):
        room[3] = "West"
    if get_room_number(x+1,y) < SIZE_Y * (y+1):
        room[3] = "South"
    

rooms[get_room_number(0,0)] = 5
