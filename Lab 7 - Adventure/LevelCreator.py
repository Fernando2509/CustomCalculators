import pygame
import msvcrt as m
from itertools import chain
pygame.init()

SCREEN_SIZE = 700
RESOLUTION = (SCREEN_SIZE, SCREEN_SIZE)
GAME_TICK = 60

screen = pygame.display.set_mode(RESOLUTION)
pygame.display.set_caption("Text Adventure Level Editor")
clock = pygame.time.Clock()

C_BLACK = (0, 0, 0)
C_WHITE = (255, 255, 255)
C_GRAY = (144, 144, 144)

C_DIM_BLACK = (30, 30, 30)
C_BRIGHT_GRAY = (160, 160, 160)

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

def truncline(text, maxwidth):
        real = len(text)
        stext = text
        l = font.size(text)[0]
        cut = 0
        a = 0
        done = 1
        old = None
        while l > maxwidth:
            a = a + 1
            n = text.rsplit(None, a)[0]
            if stext == n:
                cut += 1
                stext = n[:-cut]
            else:
                stext = n
            l = font.size(stext)[0]
            real = len(stext)
            done = 0
        return real, done, stext

def wrapline(text, maxwidth):
    done = 0
    wrapped = []

    while not done:
        nl, done, stext = truncline(text, maxwidth)
        wrapped.append(stext.strip())
        text = text[nl:]
    return wrapped

def wrap_multi_line(text, font, maxwidth):
    """ returns text taking new lines into account.
    """
    lines = chain(*(wrapline(line, maxwidth) for line in text.splitlines()))
    return list(lines)

def get_room_from_coord(x, y):
    global grid_size
    return y * grid_size + x

def get_room_from_number(n):
	x = n % grid_size
	y = n // grid_size
	return (x,y)

def text_object(text, font):
	text_surface = font.render(text, True, C_WHITE)
	return text_surface, text_surface.get_rect()

def message_display(text, x, y, size):
	font = pygame.font.Font('freesansbold.ttf', size)
	text_surf, text_rect = text_object(text, font)
	text_rect.center = (x, y)
	return screen.blit(text_surf, text_rect)

def rect_object(size, col):
	rect_surface = font.render(text, True, C_WHITE)
	return text_surface, text_surface.get_rect()

def draw_whole_room(x, y, size):
	coord = pixel_to_coord(x,y)

	if x + box_size > mouse[0] > x and y + box_size > mouse[1] > y:
		active = True
		if click[0] == 1:
			edit_room(pixel_to_room(x,y), pixel_to_coord(x,y))
	else:
		active = False
	col = C_BRIGHT_GRAY if active else C_GRAY
	room = pixel_to_room(x,y)
	if room == False:
		col = C_DIM_BLACK

	rect = pygame.draw.rect(screen, col, (x, y, size, size), 0)
	if room == False:
		return
	font_size = int((size / 3) - offset)
	message_display("{}, {}".format(coord[0], coord[1]), x + size / 2, y + size / 2, font_size)

def edit_room(room, coord):
	editing = True
	edit_surface = pygame.Surface((SCREEN_SIZE - 200, SCREEN_SIZE - 200))
	while editing:
		#Input Events
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				editing = False

		#logic
		if room == False:
			return
		 #todo

		#draw

		#Overlay
		r = pygame.draw.rect(screen, C_BLACK, (0,0, SCREEN_SIZE,  SCREEN_SIZE))

		#Name of the room label
		message_display("-----NAME OF THE ROOM-----", SCREEN_SIZE / 2, 50, 50)
		t = wrapline(room[NAME], 240)
		line = 1
		for x in t:
			message_display(x, SCREEN_SIZE / 2, 50 + line * 50, 50)
			line += 1

		#Room description
		line+= 1
		message_display("----------DESCRIPTION----------", SCREEN_SIZE / 2, 50 * line, 50)
		t = wrapline(room[DESCRIPTION], 200)
		for x in t:
			message_display(x, SCREEN_SIZE / 2, 50 + line * 50, 50)
			line += 1

		#Doors
		line+= 1
		message_display("----------COORDINATES----------", SCREEN_SIZE / 2, 50 * line, 50)
		#todo
		for x in range(4):
			_ = 0
			#message_display(x, SCREEN_SIZE / 2, 50 + line * 50, 50)

		pygame.display.update(r)
		clock.tick(GAME_TICK)
	#bg_surface.set_alpha(200)
	print(room)

def pixel_to_room(x,y):

	x = x // (SCREEN_SIZE // grid_size)
	y = y // (SCREEN_SIZE // grid_size)
	return rooms[grid_size * y + x]

def pixel_to_coord(x,y):
	x = x // (SCREEN_SIZE // grid_size)
	y = y // (SCREEN_SIZE // grid_size)
	return (x,y)

def get_room_number(x, y):
    global grid_size
    return y * grid_size + x

def yes_no_switch():
	while True:
		choice = ord(m.getch())
		if choice == 121:
			return True
		elif choice == 110:
			return False

#Initialization
done = False
grid_size = 5
offset = int(grid_size / 2)
box_size = int(SCREEN_SIZE / grid_size - offset)
number_of_rooms = grid_size * grid_size
rooms = [None] * number_of_rooms
rooms = [['You are in a dark room', False, False, False, True, False, 'The abyss', False, False, False, True, 'death'], ['You enter in a narrow corner and it appears to be a dark room ahead', False, True, False, True, False, 'Narrow Corner', False, 'skull', 'A mysterious ancient skull', True, 'got_skull'], ['An empty room with 3 doors: One in the west, one in the south and one in the east', False, True, True, True, False, ' North Room', False, False, False, False, '_'], ['You are on the furthest northeast corner on the room, but there is a door on your other to your right and a room on your left', False, False, True, True, False, 'Northeastern Room', False, False, False, False, '_'], ['You are facing a door, it appears to be locked, you can turn back by going west', False, False, False, False, False, 'The Door', False, False, False, True, 'Exit'], False, ['You entered a bedroom, the is a key on the table.', False, True, False, False, False, 'Bedroom', False, 'Key', 'A normal key, probably could open a door (or not)', False, '_'], ['Middle of the corridor', True, True, True, True, False, 'You are in the middle of a corridor', False, False, False, False, '_'], ['A continuation of the corridor, there is a room on the right', False, True, False, True, False, 'East corridor', False, False, False, False, '_'], ['An empty room, there is nothing to do here', False, False, False, True, False, 'Empty Room', False, False, False, False, '_'], False, ['Library', False, True, False, False, False, 'A mini library over a table with a box on the corner of the table', False, 'box', "A box with a key lock, it won't open without a key", False, '_'], ['A dark room, I can see a bright lights coming throught 2 doors on the west and the north', True, False, False, True, True, 'Dark room', False, False, False, False, '_'], False, False, False, False, False, False, False, False, False, False, False, False]

'''
#It just works!
for y in range(grid_size):
    for x in range(grid_size):
        print("\nCreating room {0}, {1}:".format(x, y))
        room = ["Sapo"] * 12
        print("Skip room?")

        room[DESCRIPTION] = input("Description of room: ")
        room[NAME] = input("Name of the room: ")
        room_num = get_room_number(x,y)
        room[HAVE_PLAYER] = False

        if room_num > grid_size - 1:
            print("North?")
            room[NORTH] = yes_no_switch()
        if room_num < (grid_size * grid_size) - grid_size + x:
            print("South?")
            room[SOUTH] = yes_no_switch()
        if room_num > grid_size * y :
            print("East?")
            room[EAST] = yes_no_switch()
        if room_num < (grid_size * y) + grid_size - 1:
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
'''

#print(rooms)
click = (0, 0, 0)
mouse = (0, 0)

font = pygame.font.Font('freesansbold.ttf', 15)
while not done:
    #Input Events
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True

	mouse = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()
	#Logic (from input)
	#todo

	#Draw
	screen.fill(C_BLACK)

	for x in range(offset, 500, box_size + offset):
		for y in range(offset, 500, box_size + offset):
			draw_whole_room(x, y, box_size)

	pygame.display.update()

    #End of frame
	clock.tick(GAME_TICK)

pygame.quit()