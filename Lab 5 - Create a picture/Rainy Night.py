import pygame, os, math, random, wave, struct, urllib.request, time
################
you_want_to_hear_an_annoying_music = True
################




pygame.mixer.pre_init(frequency=44100, size=-16, channels=1)
pygame.init()

canvas_size = (800, 400)

tree_trunk_size = 100
raindrop_instances = 100
ticks = 60
#Weighted random choices
wind_choices = [-2] * 1 + [-1] * 2 + [0] * 3 + [1] * 2 + [2] * 1


#region Do not touch

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIME_GREEN = (20, 80, 20)
BLUE = (0, 0 , 255/1.5)
DIM_GRAY = (40, 40, 40)
DARK_BROWN = (40 + 20, 26 + 20, 13 + 20)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIME_GREEN = (20, 80, 20)
BLUE = (0, 0 , 255)
YELLOW = (255, 255, 0)
GREEN_YELLOW = (173, 255, 47)
BROWN = (40 + 20, 26 + 20, 13 + 20)

#Background music url
BGM_LINK = r"https://www.dropbox.com/s/e82yzy7a8o7z7ne/music.ogg?dl=1"

clock = pygame.time.Clock()
WIDTH = canvas_size[0]
HEIGHT = canvas_size[1]
BOTTOM_CENTER = (WIDTH/2, HEIGHT)
screen = pygame.display.set_mode(canvas_size)
#endregion

pygame.display.set_caption("Rainy Night")

#Linear Interpolation
#
#Used to make the branches of the trees
#come back to a percentage of their original
#position after some time
def lerp(v0, v1, t):
  return (1 - t) * v0 + t * v1;


#Check if you have the necesasary files to play.
#If you dont have "x" file it will be created or downloaded
def generate_audio_files():
    #Creates a white noise file to represent the rain
    if not os.path.exists(os.getcwd() + "\\" + "noise.wav"):
        print("noise.wav not found, creating...")
        lenght = 4000 * 8  
        noise_output = wave.open('noise.wav', 'w')
        noise_output.setparams((1, 1, 20000, 0, 'NONE', 'not compressed'))


        for i in range(0,lenght):
            value = random.randint(-32768 + 1, 32767)
            packed_value = struct.pack('h', value)
            noise_output.writeframes(packed_value)
        noise_output.close()
        print("Sucess")

    ###################
    #Creates a thunder file to represent a thunder(very badly)
    if not os.path.exists(os.getcwd() + "\\" + "thunder.wav"):
        print("thunder.wav not found, creating...")
        lenght = 2000 * 8  
        noise_output = wave.open('thunder.wav', 'w')
        noise_output.setparams((1, 1, 14000, 0, 'NONE', 'not compressed'))
    

        for i in range(0,lenght):
            value = random.randint(-10000 + 1, 10000)
            packed_value = struct.pack('h', value)
            noise_output.writeframes(packed_value)
        noise_output.close()
        print("Sucess")

    ############
    #Fetch a music file from a dropbox link
    if not os.path.exists(os.getcwd() + "\\" + "music.wav"):
        print("music.wav not found, creating...")
        bgm = urllib.request.urlretrieve(BGM_LINK, "music.wav")
        print("Sucess")

def translate(value, value_min, value_max, final_min, final_max):
    left_lenght = value_max - value_min
    right_lenght = final_max - final_min
    scaled_value = float(value - value_min) / float(left_lenght)
    return final_min + (scaled_value * right_lenght)

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

def change_color_through_time(col):
    amplitude = 1000
    color_variation = math.sin(time.time()*amplitude)
    remap_variation = translate(color_variation, -1, 1, -15, 15)
    
    r = lerp(col[0], col[0] + remap_variation, 0.1)
    g = lerp(col[1], col[1] + remap_variation, 0.1)
    b = lerp(col[2], col[2] + remap_variation, 0.1)

    ret_val = ( r, g, b)
    
    return truncate_col(ret_val)

def thunder():
    screen.fill(WHITE)
    pygame.mixer.Sound.play(thunder_audio)
    


#Branch
class Branch():
    def __init__(self, start, end, col=DARK_BROWN, thickness=5):
        self.start = pygame.math.Vector2(start[0], start[1])
        self.end = pygame.math.Vector2(end[0], end[1])
        self.end_copy = self.end
        self.damping = 0.65
        self.color = col
        self.shakes = 0
        self.thicness = thickness

    def shake(self, dir):
        self.shakes += 1
        rnd_dir = random.randint(-1,1)
        self.end += (dir*3 ,  dir * 3 * rnd_dir)
        if self.shakes > 10:
            self.shakes = 0
            self.end = lerp(self.end, self.end_copy, 0.15)
        

    def render(self):
        pygame.draw.line(screen, self.color, self.start, self.end, self.thicness)

    def create_right(self):
      
        dot = self.start.distance_to(self.end)
        #Rotate Functions 
        x = -math.cos(math.radians(-math.pi/ dot)) *  dot * self.damping 
        y = math.sin(math.radians(math.pi /4)) * dot - x
        
        right_rot = pygame.math.Vector2(x,y)
        new_right = self.end - right_rot
        rb = Branch(self.end, new_right, LIME_GREEN, 2)

        return rb

    def create_left(self):
      
        dot = self.start.distance_to(self.end)
        #Rotate Functions
        x = math.cos(math.radians(math.pi/ 4)) * dot * self.damping   
        y = math.sin(math.radians(math.pi /4)) * dot + x
        left_rot = pygame.math.Vector2(x,y)
        new_left = self.end - left_rot
        lb = Branch(self.end, new_left, LIME_GREEN, 2)
        return lb

class Raindrop():
    global WIDTH, HEIGHT
    def __init__(self, *args, **kwargs):
        self.x =  random.randint(0, WIDTH)
        self.y = random.randint(-100, HEIGHT)
        self.speed = random.randint(10, 20)
        self.size = random.randint(3, 10)
        self.thickness = random.randint(1,2)

    def fall(self, wind):
        self.y += self.speed
        self.x += wind
        self.speed += 0.05
        if self.y > HEIGHT:
            self.thickness = random.randint(1,2)
            self.size = random.randint(3, 10)
            self.speed = random.randint(10, 20)
            self.y = random.randint(-200, -100)
            self.x =  random.randint(0, WIDTH)

    def render(self):
        pygame.draw.line(screen, BLUE, (self.x,self.y), (self.x, self.y + self.size), self.thickness )

def create_branch():
    global tree
    i = len(tree) - 1
    while True:
        if i <= 0:
            break
        tree.append(tree[i].create_left())
        tree.append(tree[i].create_right())     
        i -= 1

#region Tree Creator
tree = []
root = Branch(BOTTOM_CENTER, (BOTTOM_CENTER[0], HEIGHT - tree_trunk_size, DARK_BROWN))
tree.append(root)
tree.append(root.create_left())
tree.append(root.create_right())
for x in range(4):
    create_branch()
#endregion

#region Rain Creator
drops = []
for x in range(raindrop_instances):
    drops.append(Raindrop())
#endregion

print("Getting audio files...")
generate_audio_files()

print("Setting up audio files")
music_audio = pygame.mixer.Sound("music.wav")
music_audio.set_volume(0.3)
music_audio.fadeout(200)


rain_audio = pygame.mixer.Sound('noise.wav')
rain_audio.set_volume(0.01)

thunder_audio = pygame.mixer.Sound('thunder.wav')
thunder_audio.set_volume(0.02)
thunder_audio.fadeout(200)
print("Audio files set up")

if you_want_to_hear_an_annoying_music:
    pygame.mixer.Sound.play(music_audio, -1)

pygame.mixer.Sound.play(rain_audio, -1)

bg_col = DIM_GRAY
done = False

gradient_size = HEIGHT/2 #change this value
gradient_size = int(gradient_size)

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            pass
            #You can uncomment this, but it's going the be pretty laggy
            #create_branch()

    
   
    wind = wind_choices[ random.randint(0, len(wind_choices) - 1) ]

    bg_col = change_color_through_time(bg_col)
    screen.fill(bg_col)

    gradient_size = int(gradient_size)
    gradient_size = translate(math.sin(time.time()), -1, 1, HEIGHT/1.3, HEIGHT)
    
    for x in range(int(gradient_size)):
        end_pos = x/gradient_size
        r = lerp(BLACK[0], bg_col[0], end_pos) 
        g = lerp(BLACK[1], bg_col[1], end_pos)
        b = lerp(BLACK[2], bg_col[2], end_pos)
        new_col = (r, g, b)
  
        pygame.draw.line(screen, new_col, (0, x), (WIDTH, x))
    
    skip_first = True
    for x in tree:
        x.render()
        if skip_first:
            skip_first = False
            continue
        x.shake(wind)

    for x in drops:
        x.fall(wind)
        x.render()
    if random.randint(0, 400) == 0 :
        thunder()    
    pygame.display.update()
 
    clock.tick(ticks)
 
# Close the window and quit.
pygame.quit()
