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
NAME = 6
HAVE_ITEM = 7
ITEM_NAME = 8
ITEM_DESCRIPTION = 9
HAVE_EVENT = 10
EVENT_NAME = 11
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

starting_room = 12
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
                continue
            r = list(MID_WALL)
            #Check room without player
            if room[EAST]:
                r = DOOR + '█' * int(CELL_SIZE - 2) + WALL
            if room[WEST]:
                r = WALL + '█' * int(CELL_SIZE - 2) + DOOR
            if room[EAST] and room[WEST]:
                r = DOOR + '█' * int(CELL_SIZE - 2) + DOOR

            #Check if room have player
            #PS: I Cannot use r[x] because I am using Ascii character
            #ex: \098[1m have an escape code but it is not 0 nor 1 character
            if room[EAST] and room[HAVE_PLAYER]:
                r = DOOR + '█' + PLAYER * 2 + '█' + WALL
            if room[WEST] and room[HAVE_PLAYER]:
                r = WALL + '█' + PLAYER * 2 + '█' + DOOR
            if room[EAST] and room[WEST] and room[HAVE_PLAYER]:
                r = DOOR + '█' + PLAYER * 2 + '█' + DOOR

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
    print(rooms[pos][NAME])
    print(rooms[pos][DESCRIPTION])

def input_events():
    choice = ord(m.getwch())
    dirt = False
    if choice == LEFT_ARROW:
        move(-1, 0)
        dirt = True
    elif choice == UP_ARROW:
        move(0, -1)
        dirt = True
    elif choice == DOWN_ARROW:
        move(0, 1)
        dirt = True
    elif choice == RIGHT_ARROW:
        move(1, 0)
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

def move(v1, v2):
    global pos

    #Check right wall
    if not rooms[pos][EAST] and v1 > 0:
        return

    #Check left wall
    if not rooms[pos][WEST] and v1 < 0:
        return

    #Check top wall
    if not rooms[pos][NORTH] and v2 == -1:
        return

    #Check bottom wall
    if not rooms[pos][SOUTH] and v2 == 1:
        return

    rooms[pos][5] = False
    pos += SIZE_Y * v2 + v1
    rooms[pos][5] = True

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
        r34 = DOOR + ' ' * int(CELL_SIZE - 2) + WALL
    if room[WEST]:
        r34 = WALL + ' ' * int(CELL_SIZE - 2) + DOOR
    if room[EAST] and room[WEST]:
        r34 = DOOR + ' ' * int(CELL_SIZE - 2) + DOOR

    #Check if room have player
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

rooms = [['You are in a dark room', False, False, False, True, False, 'The abyss', False, False, False, True, 'death'], ['You enter in a narrow corner and it appears to be a dark room ahead', False, True, False, True, False, 'Narrow Corner', False, 'skull', 'A mysterious ancient skull', True, 'got_skull'], ['An empty room with 3 doors: One in the west, one in the south and one in the east', False, True, True, True, False, ' North Room', False, False, False, False, '_'], ['You are on the furthest northeast corner on the room, but there is a door on your other to your right and a room on your left', False, False, True, True, False, 'Northeastern Room', False, False, False, False, '_'], ['You are facing a door, it appears to be locked, you can turn back by going west', False, False, False, False, False, 'The Door', False, False, False, True, 'Exit'], False, ['You entered a bedroom, the is a key on the table.', False, True, False, False, False, 'Bedroom', False, 'Key', 'A normal key, probably could open a door (or not)', False, '_'], ['Middle of the corridor', True, True, True, True, False, 'You are in the middle of a corridor', False, False, False, False, '_'], ['A continuation of the corridor, there is a room on the right', False, True, False, True, False, 'East corridor', False, False, False, False, '_'], ['An empty room, there is nothing to do here', False, False, False, True, False, 'Empty Room', False, False, False, False, '_'], False, ['Library', False, True, False, False, False, 'A mini library over a table with a box on the corner of the table', False, 'box', "A box with a key lock, it won't open without a key", False, '_'], ['A dark room, I can see a bright lights coming throught 2 doors on the west and the north', True, False, False, True, True, 'Dark room', False, False, False, False, '_'], False, False, False, False, False, False, False, False, False, False, False, False]

rooms[starting_room][HAVE_PLAYER] = True

done = False
while not done:
    os.system("cls")
    render_game()
    render_ui()
    input_events()