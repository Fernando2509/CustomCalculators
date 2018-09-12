import pygame

pygame.init()
 

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0 , 255)

size = (800, 600)
screen = pygame.display.set_mode(size)
 
pygame.display.set_caption("The starving artist")

done = False
 
clock = pygame.time.Clock()


while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
 
   
    screen.fill(WHITE)
 
    pygame.display.update()
 
    clock.tick(60)
 
# Close the window and quit.
pygame.quit()
quit()