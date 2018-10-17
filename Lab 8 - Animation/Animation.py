import sys, random, math

import pygame
#Include constants for pygame
from pygame.locals import * 

pygame.init()

#Variables
gradient_size = 300
WIDTH, HEIGHT = 640, 480
tick = 60
damp = 0.1
rand_variation = 20



#Tools
LINE = 0
CIRCLE = 1
POLYGON = 2 #TODO
ToolsDel = [None] * 3

#Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SILHOUETTE_COLOR = (22, 35, 26)
ALTOS_GREEN = (75, 150, 128)
YELLOW = (255, 255, 0)
TRANSPARENCY=(0, 0, 0, 0)
DAY_YELLOW = (240,212,66)

def text_object(text, font):
    text_surface = font.render(text, True, WHITE)
    return text_surface, text_surface.get_rect()

def message_display(text, x, y, size):
    font = pygame.font.Font('freesansbold.ttf', size)
    text_surf, text_rect = text_object(text, font)
    text_rect.center = (x, y)
    return screen.blit(text_surf, text_rect)

def col_lerp(col_1, col_2, t):
    r = lerp(col_1[0],
                col_2[0],
                t)
    g = lerp(col_1[1],
                col_2[1],
                t)
    b = lerp(col_1[2],
                col_2[2],
                t)
    new_col = truncate_col((r,g,b))
    
    return new_col

def rand_col(col, alpha= 255):
    r = lerp(col[0],
                col[0] + random.randint(-rand_variation, rand_variation),
                damp)
    g = lerp(col[1],
                 col[1] + random.randint(-rand_variation, rand_variation),
                damp)
    b = lerp(col[2],
                 col[2] + random.randint(-rand_variation, rand_variation),
                damp)
    new_col = truncate_col((r,g,b), alpha)
    
    return new_col

def truncate(val, minval, maxval):
    return max(min(maxval, val), minval)

def truncate_col(col, alpha=255):
    r = col[0]
    g = col[1]
    b = col[2]
    if r > 255:
        r = 255
    if r < 0:
        r = 0

    if g > 255:
        g = 255
    if g < 0:
        g = 0

    if b > 255:
        b = 255
    if b < 0:
        b = 0
    return (r,g,b, alpha)

def translate(value, value_min, value_max, final_min, final_max):
    left_lenght = value_max - value_min
    right_lenght = final_max - final_min
    scaled_value = float(value - value_min) / float(left_lenght)
    return final_min + (scaled_value * right_lenght)

def lerp(v0, v1, t):
  return (1 - t) * v0 + t * v1

def draw_gradient(c0, c1, gradient_size=HEIGHT):
     for x in range(gradient_size):
        end_pos = x / gradient_size
        r = lerp(c0[0], c1[0], end_pos)
        g = lerp(c0[1], c1[1], end_pos)
        b = lerp(c0[2], c1[2], end_pos)
        new_col = (r, g, b)

        pygame.draw.line(screen, new_col, (0, x), (WIDTH, x))

def move_sun():
    rotation += pygame.time.get_ticks() / 60

def line_drawing():
    global pressing_m0, p_start, p_final
    
    if not mouse[0]:
        pressing_m0 = False
    if mouse[0] and pressing_m0 == False:
        pressing_m0 = True
        p_start = pygame.mouse.get_pos()

    elif mouse[2] and not pressing_m0:
        points.pop()
        pygame.time.delay(300)
    if pressing_m0 and mouse[2]:
        points.append((p_start, p_final))
        pygame.time.delay(300)
    if pressing_m0:
        pygame.draw.aaline(screen, BLACK, p_start, p_final, 0)
        p_final = pygame.mouse.get_pos()

def circle_drawing():
    global pressing_m0, p_start, p_final
    c_size = pygame.math.Vector2(p_start).distance_to(p_final)
    c_size = int(abs(c_size))
    if not mouse[0]:
        pressing_m0 = False
    if mouse[0] and pressing_m0 == False:
        pressing_m0 = True
        p_start = pygame.mouse.get_pos()

    elif mouse[2] and not pressing_m0:
        circles.pop()
        pygame.time.delay(300)
    if pressing_m0 and mouse[2]:
        circles.append((p_start, c_size))
        pygame.time.delay(300)
    if pressing_m0:
        pygame.draw.circle(screen, WHITE, p_start, c_size)
        p_final = pygame.mouse.get_pos()

def polygon_drawing():
    global pressing_m0, p_start, p_final
    if not mouse[0]:
        pressing_m0 = False
    if mouse[0] and pressing_m0 == False:
        pressing_m0 = True
        p_start = pygame.mouse.get_pos()
        polygon_temp_points.append(p_start)
    elif mouse[2] and not pressing_m0:
        if len(polygon_temp_points) > 0:
            polygon_temp_points.pop()
        pygame.time.delay(300)
    if pressing_m0 and mouse[2]:
        polygon_temp_points[-1] = pygame.mouse.get_pos()
        pygame.time.delay(300)
    if pressing_m0:
        if len(polygon_temp_points) != 0:
            pygame.draw.aaline(screen, BLACK, p_start, p_final, 0)
        p_final = pygame.mouse.get_pos()

    if len(polygon_temp_points) > 1:
        pygame.draw.polygon(screen, BLACK, polygon_temp_points, 1)
    
#Defining Mountains
far_left_big_mountain = [(0, 117), (329, 478), (0, 479)]
bottom_right_small_mountain = [(342, 480), (565, 382), (640, 414), (639, 480)]
far_right_big_mountain = [(0, 640), (218, 387), (224, 369), (313, 310), (361, 357), (492, 247), (526, 279), (640, 170), (640, 480)]
#The order of the list is paramount for it to work
polygon_points = [far_left_big_mountain, bottom_right_small_mountain, far_right_big_mountain]

#This list is pointless, these are just the
#points that I used to make polygons
points = []
#points = [((224, 369), (312, 311)), ((224, 369), (312, 311)), ((313, 310), (361, 357)), ((313, 310), (361, 357)), ((361, 356), (490, 248)), ((361, 356), (490, 248)), ((491, 247), (522, 276)), ((491, 247), (522, 276)), ((532, 261), (639, 166)), ((532, 261), (639, 166)), ((243, 356), (431, 440)), ((243, 356), (431, 440)), ((567, 383), (342, 479)), ((567, 383), (342, 479)), ((567, 384), (639, 413)), ((567, 384), (639, 413)), ((225, 369), (331, 479)), ((225, 369), (331, 479)), ((226, 370), (0, 115)), ((226, 370), (0, 115)), ((535, 259), (524, 276))]

#Circles aka lazy stars
circles = []
circles = [((482, 77), 4), ((354, 22), 3), ((615, 62), 3), ((271, 89), 2), ((119, 111), 2), ((69, 50), 5), ((206, 103), 4)]
#PS: The sun is a seperate object

#Used on the polygon_drawing function
polygon_temp_points = []

#Things used on drawing functions
p_start = (0,0)
p_final = (0,0)
current_tool = LINE
pressing_m0 = False
already_using_polygon = False

#Drawing tools (ps: is there a name for this patter?
#                   using a list to store function
ToolsDel[LINE] = line_drawing
ToolsDel[CIRCLE] = circle_drawing
ToolsDel[POLYGON] = polygon_drawing


#Pygame stuff
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))


#Sun Stuff
SUN_START_POS = (int(WIDTH/1.5), int(HEIGHT*0.85)) #Better not touch this. You'll mess up the "translate" function if the sun is on a weird position

sun_x = SUN_START_POS[0] 
sun_y = SUN_START_POS[1] 
angle = 90
angle *= 0.0174532925 #Converting to radians (actual angles eg:45, 90)

hours = 12
speed = 0.1    #Works better with values between 0.01 - 0.04
speed_copy = speed
radius =  350
sun_rect = pygame.draw.circle(screen, YELLOW, SUN_START_POS, 5)
sun_layer = pygame.Surface((WIDTH, HEIGHT)).convert_alpha()
sun_layer.fill(TRANSPARENCY)

#Mountains Stuff
mountain_layer = pygame.Surface((WIDTH, HEIGHT)).convert_alpha()
mountain_layer.fill(TRANSPARENCY)
col = [rand_col(SILHOUETTE_COLOR, alpha=177),rand_col(SILHOUETTE_COLOR,alpha=160),rand_col(SILHOUETTE_COLOR, alpha=144)]



done = False
# Game loop.
while not done:    
    mouse = pygame.mouse.get_pressed()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                current_tool = LINE
                print("Current tool: Line")
            elif event.key == pygame.K_2:
                current_tool = CIRCLE
                print("Current tool: Circle")
            elif event.key == pygame.K_3:
                current_tool = POLYGON
                print("Current tool: Polygon")
                
            if event.key == pygame.K_LEFT:
                speed -= 0.1
            if event.key == pygame.K_RIGHT:
                speed += 0.05
            if event.key == pygame.K_SPACE:
                speed = speed_copy
           

    # Update
    if current_tool == POLYGON and not already_using_polygon:
        already_using_polygon = True
        polygon_temp_points = []
    ToolsDel[current_tool]()
    #angle(var)+ | hour
    #0 or 360 = 18hr
    #45 = 21hr
    #90 = 24hr
    #180 = 6hr
    #270 = 12hr
    angle = angle % 6.28319
    angle += 0.0174532925 * speed

    radians = angle * 57.2958
    
    if 270+15 > radians > 90+15:
        hours = translate(radians, 90+15, 270, 1, 12)
    if 270+15 < radians:
        hours = translate(radians, 270+15, 360, 1, 6)
    if radians < 90+15:
        hours = translate(radians, 0, 90, 6, 12)
    hours = int(hours+0.1)
    minutes = translate(radians % 14.1, 0, 15, 0, 60)
    
    
    sun_x = SUN_START_POS[0] + math.cos(angle) * radius 
    sun_y = SUN_START_POS[1] + math.sin(angle) * radius 
    #print(str(sun_x) + " " + str(sun_y))
    sun_x = int(sun_x )
    sun_y = int(sun_y )

    sun_alpha = abs(int(translate(sun_y, 0, HEIGHT , 255, 50)))

    stars_alpha = abs(int(translate(sun_alpha, 255, 0, -100, 255)))
    stars_alpha = truncate(stars_alpha, 0, 255)
    
    
    # Draw
    screen.fill(ALTOS_GREEN)
    sun_layer.fill(TRANSPARENCY)
    
    
    damp = sun_y
    damp = translate(damp, 200, HEIGHT, 0, 1)
    draw_gradient(ALTOS_GREEN, col_lerp(DAY_YELLOW, BLACK, damp))

    
    for pt in points:
        pygame.draw.line(screen, BLACK, pt[0], pt[1], 1)

    for c in circles:
        pygame.draw.circle(sun_layer, (255,255,255,stars_alpha), c[0], c[1])

    for x in range(len(polygon_points)):
        pygame.draw.polygon(mountain_layer, col[x-1], polygon_points[x-1])

    sun = pygame.draw.circle(sun_layer, (255,255,0, sun_alpha), (sun_x, sun_y ), 23)

    screen.blit(sun_layer, (0,0))
    screen.blit(mountain_layer, (0,0))

    #Display hours
    hour_str = str(int(hours))
    min_str = str(int(minutes))
    if len(hour_str) <= 1:
        hour_str = "0" + hour_str
    if len(min_str) <= 1:
        min_str = "0" + min_str
    message_display("{}:{}".format(hour_str, min_str), 100, 25, 36)
    
    pygame.display.flip()
    clock.tick(tick)
