
DESCRIPTION = 0
NORTH = 1
EAST = 2
SOUTH = 3
WEST = 4
HAVE_PLAYER = 5
NAME = 6
HAVE_ITEM = 7
ITEM_NAME = 8
ITEM_DESCRIPTION = 9
HAVE_EVENT = 10
EVENT_NAME = 11
SIZE_Y = 5
NUMBER_OF_ROOMS = SIZE_Y * SIZE_Y
starting_room = 12
def get_room_number(x, y):
    global SIZE_Y
    return y * SIZE_Y + x

def yes_no_switch():
    while True:
        print("Yes or no")
        choice = input()
        if choice == "y":
            return True
        elif choice == "n":
            return False

rooms = [False] * NUMBER_OF_ROOMS
#It just works!
for y in range(SIZE_Y):
    for x in range(SIZE_Y):
        print("\nCreating room {0}, {1}:".format(x, y))
        room = [None] * 12
        print("Skip room?")
        if yes_no_switch():
            continue
        
        room[DESCRIPTION] = input("Description of room: ")
        room[NAME] = input("Name of the room: ")
        room_num = get_room_number(x,y)
        room[HAVE_PLAYER] = False

        if room_num > SIZE_Y - 1:   
            print("North?")
            room[NORTH] = yes_no_switch()
        if room_num < (SIZE_Y * SIZE_Y) - SIZE_Y + x:
            print("South?")
            room[SOUTH] = yes_no_switch() 
        if room_num > SIZE_Y * y :
            print("East?")
            room[EAST] = yes_no_switch()
        if room_num < (SIZE_Y * y) + SIZE_Y-1:
            print("West?")
            room[WEST] = yes_no_switch()

        print("Have item in it?")
        if yes_no_switch():
            room[ITEM_NAME] = input("Item name: ")
            room[ITEM_DESCRIPTION] = input("Item description: ")


        print("Have event?")
        room[HAVE_EVENT] = yes_no_switch()
        if HAVE_EVENT:
            room[EVENT_NAME] = input("Event name: ")
        
        rooms[room_num] = room

rooms[starting_room][HAVE_PLAYER] = True 
