import random
import os
import subprocess
import time
import msvcrt as m
#Used subprocess to allow ASCI characters
subprocess.call('', shell=True)

CELL_SIZE = 6
SIZE_Y = 5
NUMBER_OF_ROOMS = SIZE_Y * SIZE_Y
CENTER = int(SIZE_Y / 2)

DOWN_ARROW = 80
LEFT_ARROW = 75
RIGHT_ARROW = 77
UP_ARROW = 72
ESC = 27


DESCRIPTION = 0

NORTH = 1
EAST = 2
SOUTH = 3
WEST = 4

HAVE_PLAYER = 5

#Future features 
##HAVE_ITEM = 7
##ITEM_NAME = 8
##ITEM_DESCRIPTION = 9
##HAVE_EVENT = 10
##EVENT_NAME = 11

def change_text_color(text, col):
    return col + text + DEFAULT

DOORS = '\033[94m'
GREEN = "\33[32m"
WALLS = '\033[91m'
DEFAULT = '\033[37;40;0m'
WALL = change_text_color(" " ,WALLS)
DOOR = change_text_color("█" ,DOORS)
PLAYER = change_text_color("█" ,GREEN)
MID_WALL = '{}████{}'.format(WALL, WALL)

def get_room_number(x, y):
    global SIZE_Y
    return y * SIZE_Y + x

starting_room = 0
pos = starting_room
inventory = []
#Maze visualized
#1 2 3
#4 5 6
#7 8 9
#And so on

#x coord = x//size
#y coord = x%size
def render_game():
    '''Renders the whole board'''
    for y in range(SIZE_Y):
        #Top ROW
        for x in range(SIZE_Y):
            room = rooms[x + SIZE_Y * y]
            if room == False:
                r = list(WALL * CELL_SIZE)
                print("".join(r), end="")
                continue
            r = list(WALL * CELL_SIZE)
            if room[NORTH]:
                r = WALL + WALL + DOOR + DOOR + WALL + WALL
            print("".join(r), end="")
        print()
        print(MID_WALL * SIZE_Y)

        #Mid ROW
        for x in range(SIZE_Y):
            room = rooms[x + SIZE_Y * y]
            if room == False:
                print(MID_WALL, end="")
                continue
            r = list(MID_WALL)
            #Check room without player
            if room[EAST]:
                r = WALL + '█' * int(CELL_SIZE - 2) + DOOR
            if room[WEST]:
                r = DOOR + '█' * int(CELL_SIZE - 2) + WALL
            if room[EAST] and room[WEST]:
                r = DOOR + '█' * int(CELL_SIZE - 2) + DOOR

            #Check if room have player
            #PS: I Cannot use r[x] because I am using Ascii character
            #ex: \098[1m have an escape code but it is not 0 nor 1 character
            if room[EAST] and room[HAVE_PLAYER]:
                r = WALL + '█' + PLAYER * 2 + '█' + DOOR
            if room[WEST] and room[HAVE_PLAYER]:
                r = DOOR + '█' + PLAYER * 2 + '█' + WALL
            if room[EAST] and room[WEST] and room[HAVE_PLAYER]:
                r = DOOR + '█' + PLAYER * 2 + '█' + DOOR
            if room[NORTH] and room[SOUTH] and room[HAVE_PLAYER]:
                r = WALL + '█' + PLAYER * 2 + '█' + WALL

            print("".join(r), end="")
        print()
        print(MID_WALL * SIZE_Y)

        #Bottom ROW

        for x in range(SIZE_Y):
            room = rooms[x + SIZE_Y * y]
            if room == False:
                continue
            r = list(WALL * CELL_SIZE)
            if room[SOUTH]:
                r = WALL + WALL + DOOR + DOOR + WALL + WALL
            print("".join(r), end="")

        print()

def render_ui():
    if rooms[pos] == False:
        print("Room : {}\nIs invalid".format(pos))
    print(rooms[pos][NAME])
    print(rooms[pos][DESCRIPTION])

def input_events():
    choice = ord(m.getwch())
    dirt = False
    if choice == LEFT_ARROW:
        move(WEST)
        dirt = True
    elif choice == UP_ARROW:
        move(NORTH)
        dirt = True
    elif choice == DOWN_ARROW:
        move(SOUTH)
        dirt = True
    elif choice == RIGHT_ARROW:
        move(EAST)
        dirt = True
    elif choice == ESC:
        dirt = True
        quit_choice = input("Do you really want to quit?\n")
        if quit_choice[0].upper() == "Y":
            quit()
        else:
            print("I'm taking that as a no...")
            time.sleep(0.5)
    if (not dirt) and choice != 224:
        first_char = chr(choice)
        print(first_char, end="")
        actual_choice = input()
        actual_choice = first_char + actual_choice
        process_text(actual_choice)

def move(flag):
    global pos

    if rooms[pos][NORTH] and flag == NORTH:
        rooms[pos][HAVE_PLAYER] = False
        pos += SIZE_Y * -1 + 0
        rooms[pos][HAVE_PLAYER] = True
        return

    if rooms[pos][SOUTH] and flag == SOUTH:
        rooms[pos][HAVE_PLAYER] = False
        pos += SIZE_Y * 1 + 0
        rooms[pos][HAVE_PLAYER] = True
        return

    if  rooms[pos][EAST] and flag == EAST :
        rooms[pos][HAVE_PLAYER] = False
        pos += SIZE_Y * 0 + 1
        rooms[pos][HAVE_PLAYER] = True
        return


    if  rooms[pos][WEST] and flag == WEST:
        rooms[pos][HAVE_PLAYER] = False
        pos += SIZE_Y * 0 - 1
        rooms[pos][HAVE_PLAYER] = True
        return




def process_text(text):
    pass

def render_room(room):
    '''Renders a single room'''
    empty = '██████'
    r1 = list('██████')
    r34 = list('██████')
    r6 = list('██████')
    if room[NORTH]:
        r1 = WALL + WALL + DOOR + DOOR + WALL + WALL
    if room[SOUTH]:
        r6 = WALL + WALL + DOOR + DOOR + WALL + WALL

    #Check room without player
    if room[EAST]:
        r34 = WALL + ' ' * int(CELL_SIZE - 2) + DOOR
    if room[WEST]:
        r34 = DOOR + ' ' * int(CELL_SIZE - 2) + WALL
    if room[EAST] and room[WEST]:
        r34 = DOOR + ' ' * int(CELL_SIZE - 2) + DOOR

    #Check if room have player
    if room[HAVE_PLAYER]:
        r34 = WALL + '█' + PLAYER * 2 + '█' + WALL
    if room[EAST] and room[HAVE_PLAYER]:
        r34 = DOOR + '█' + PLAYER * 2 + '█' + WALL
    if room[WEST] and room[HAVE_PLAYER]:
        r34 = WALL + '█' + PLAYER * 2 + '█' + DOOR
    if room[EAST] and room[WEST] and room[HAVE_PLAYER]:
        r34 = DOOR + '█' + PLAYER * 2 + '█' + DOOR

    print("".join(r1))
    print(empty)
    print("".join(r34))
    print("".join(r34))
    print(empty)
    print("".join(r6))

def yes_no_switch():
    while True:
        choice = ord(m.getch())
        if choice == 121:
            return True
        elif choice == 110:
            return False

rooms = [  
   [  
      'The room is pitch black, but you can see 2 doors: one at your left, and the other to your right',
      False,
      True,
      True,
      False,
      False,
      'Dark bedroom\r',
      False,
      False,
      False,
      False,
      False
   ],
   [  
      'The bathroom looks abandoned and it smells',
      False,
      False,
      False,
      True,
      False,
      'Bathroom',
      False,
      False,
      False,
      False,
      False
   ],
   False,
   [  
      'New room',
      False,
      False,
      False,
      False,
      False,
      'New room',
      False,
      False,
      False,
      False,
      False
   ],
   False,
   [  
      'There is a corridor and a door at the end of the corridor to the east',
      True,
      True,
      False,
      False,
      False,
      'Corridor',
      False,
      False,
      False,
      False,
      False
   ],
   [  
      'Walking along the corridor you see a new pathway to the south. It looks like a very long corridor so you keep your way through the normal path',
      False,
      True,
      True,
      True,
      False,
      'Corridor',
      False,
      False,
      False,
      False,
      False
   ],
   [  
      'At the end of the corridor you see the door half open',
      False,
      True,
      False,
      True,
      False,
      'Corridor',
      False,
      False,
      False,
      False,
      False
   ],
   [  
      'Opening the door you find yourself in a deserted highway',
      False,
      False,
      False,
      True,
      False,
      'Exit',
      False,
      False,
      False,
      False,
      False
   ],
   False,
   False,
   [  
      'The path looks a lot worse compared to the one you were before, most windows look broken and you are not confortable being there',
      True,
      False,
      True,
      False,
      False,
      'South Corridor',
      False,
      False,
      False,
      False,
      False
   ],
   [  
      "You are bursting and don't hesitate in using it. You are filled with D E T E R M I N A T I O N\x1b",
      False,
      False,
      True,
      False,
      False,
      'Visitors restroom',
      False,
      False,
      False,
      False,
      False
   ],
   False,
   False,
   [  
      'There is a sofa  and some old fancy chairs. I could take a nap there...hmmm better not',
      False,
      True,
      False,
      False,
      False,
      'Waiting room',
      False,
      False,
      False,
      False,
      False
   ],
   [  
      'It looks like a hall of some kind of hotel, but no one appears to be in the building. There is a path to east and west',
      True,
      True,
      False,
      True,
      False,
      'Hall',
      False,
      False,
      False,
      False,
      False
   ],
   [  
      'Looks like the main entrace the door is broken and there is glass all over the floor, but there is a door to the north that appears to be the restroom',
      True,
      False,
      False,
      True,
      False,
      'Main entrance',
      False,
      False,
      False,
      False,
      False
   ],
   False,
   False,
   False,
   False,
   False,
   False,
   False
]

rooms[0][HAVE_PLAYER] = True

done = False
while not done:
    os.system("cls")
    render_game()
    render_ui()
    input_events()
