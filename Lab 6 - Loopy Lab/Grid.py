import pygame, os, math, random, wave, struct, urllib, time, array, winsound, threading
pygame.init()


box_size = 10

canvas_size = (700, 500)

GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIME_GREEN = (20, 80, 20)
BLUE = (0, 0 , 255)
BROWN = (40 + 20, 26 + 20, 13 + 20)
col_list = [GREEN, WHITE,BLACK, LIME_GREEN, BLUE, BROWN]
pygame.display.set_caption("My Game")

WIDTH = canvas_size[0]
HEIGHT = canvas_size[1]

screen = pygame.display.set_mode(canvas_size)

clock = pygame.time.Clock()
TICK = 60

done = False
screen.fill(BLACK)

def translate(value, value_min, value_max, final_min, final_max):
    left_lenght = value_max - value_min
    right_lenght = final_max - final_min
    scaled_value = float(value - value_min) / float(left_lenght)
    return final_min + (scaled_value * right_lenght)

def lerp(v0, v1, t):
  return (1 - t) * v0 + t * v1;

def truncate_col(col):
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
    return (r,g,b)

def rand_col(col):
    r = lerp(col[0],
                col[0] + random.randint(-20, 20),
                damp)
    g = lerp(col[1],
                 col[1] + random.randint(-20, 20),
                damp)
    b = lerp(col[2],
                 col[2] + random.randint(-20, 20),
                damp)
    new_col = truncate_col((r,g,b))
    
    return new_col

def beep_anoying_audio(duration):
    global damp
    while True:
        d2 = translate(damp, 0, 20, 38, 5000)
        
        winsound.Beep(int(d2), duration)


damp = 0


t = threading.Thread(target=beep_anoying_audio, args=   (300,) )
#Do not uncoment
#t.start()

amplitude = 0.5
some_color = GREEN
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    damp =  math.sin(time.time()*amplitude)
    damp = translate(damp, -1, 1, 0, 20)
    if int(damp) == 19:
        some_color = (lerp(some_color[0] ,random.randint(0,255), 0.4),
                        lerp(some_color[1] ,random.randint(0,255), 0.4),
                        lerp(some_color[2] ,random.randint(0,255), 0.4))
    for y in range(0, HEIGHT, box_size*2):
        for x in range(0, WIDTH, box_size*2):
            pygame.draw.rect(screen, rand_col(some_color), (x, y, box_size, box_size), 0)
    
  
    
    pygame.display.update()

    screen.fill(BLACK)
    clock.tick(TICK)

# Close the window and quit.
pygame.quit()