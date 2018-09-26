import pygame
pygame.init()

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


canvas_size = (700, 500)

GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIME_GREEN = (20, 80, 20)
BLUE = (0, 0 , 255)
YELLOW = (255, 255, 0)
GREEN_YELLOW = (173, 255, 47)
BROWN = (40 + 20, 26 + 20, 13 + 20)

WIDTH = canvas_size[0]
HEIGHT = canvas_size[1]

screen = pygame.display.set_mode(canvas_size)

clock = pygame.time.Clock()
TICK = 60

done = False
gradient_size = HEIGHT/2 #change this value
gradient_size = int(gradient_size)
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    
    for x in range(gradient_size):
        end_pos = x/gradient_size
        r = lerp(YELLOW[0], BROWN[0], end_pos) 
        g = lerp(YELLOW[1], BROWN[1], end_pos)
        b = lerp(YELLOW[2], BROWN[2], end_pos)
        new_col = (r, g, b)
  
        pygame.draw.line(screen, new_col, (0, x), (WIDTH, x))
    
    pygame.display.update()

    screen.fill(BLACK)
    clock.tick(TICK)

# Close the window and quit.
pygame.quit()
