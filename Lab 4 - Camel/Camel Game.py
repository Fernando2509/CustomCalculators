#Used to clean the console
from os import system 
#Math is used to get the absolute value of the ditance between him and the natives
#subprocess is used to allow ANSI character to be drawn on screen
import math, random, subprocess, os, sys, time, winsound, pygame, threading, urllib
import msvcrt as m

pygame.mixer.pre_init(frequency=44100, size=-16, channels=1)
pygame.init()

play_music = True
BGM_LINK = "http://www.gamemusicthemes.com/sheetmusic/gameboy/supermarioland/eastonkingdom/Super_Mario_Land_-_Easton_Kingdom_by_Knightlitespeed.mid"
VICTORY_LINK = "https://files.khinsider.com/midifiles/nes/super-mario-bros./level-complete.mid"
def download_bgm_async():
    if not os.path.exists(os.getcwd() + "\\" + "music.mid"):
        urllib.request.urlretrieve(BGM_LINK, "music.mid")
    if not os.path.exists(os.getcwd() + "\\" + "victory.mid"):
        urllib.request.urlretrieve(VICTORY_LINK, "victory.mid")
 
t = threading.Thread(target=download_bgm_async)
t.start()

#Set console size
os.system('mode con: cols=40 lines=20')


#Used subprocess to allow ASCI characters
subprocess.call('', shell=True)


#Write a layer text before printing something
def stdout(message):
    sys.stdout.write(message)
    sys.stdout.write('\b' * len(message)) 

#Text colors (I may not have used all of them)
#To know more about coloring the terminal's bg and fg see
#http://ozzmaker.com/add-colour-to-text-in-python/
FAIL = '\033[91m'
OKBLUE = '\033[94m'
PLAYER = '\033[1;44;37;2m'
NATIVES = '\033[1;41;37;2m'
YELLOW = "\33[1;37;43m"
WHITE = "\33[37m"
GREEN = "\33[32m"
BLANK = "\33[47m"
ENDC = '\033[0m'
DEFAULT = '\033[37;40;0m'

#Game variables
DESERT_SIZE = 200

player = 0
natives = -20
drinks = 3
camel = 0
thirst = 0



#region Move Functions
def move_natives(min_val, max_val):
    global natives
    natives += random.randint(min_val, max_val)

def move_player(min_val, max_val):
    global player
    random_val = random.randint(min_val, max_val)
    player += random_val
    if DESERT_SIZE - player > 0:
        print("You moved {0} miles {1} left".format(change_text_color(random_val, OKBLUE), change_text_color(DESERT_SIZE - player, OKBLUE)))
    else: 
        pass
    
#endregion

#region User Input
def show_choices():
        #TODO Create an action class that has a label and a "action" method
        if player < DESERT_SIZE:
            DrawMap()
        procedual_write(change_text_color( "A.",FAIL) + " Drink from your canteen.", 0.001)
        procedual_write(change_text_color( "B.",FAIL) + " Ahead moderate speed." , 0.001)
        procedual_write(change_text_color( "C.",FAIL) + " Ahead full speed.", 0.001)
        procedual_write(change_text_color( "D.",FAIL) + " Stop for the night.", 0.001)
        procedual_write(change_text_color( "E.",FAIL) + " Status check.", 0.001)
        procedual_write(change_text_color( "Q.",FAIL) + " Quit.", 0.001)
        return ask_input()

def ask_input():
        choice = "error"
        valid_input = False
        available_options = "ABCDEQ"
        while not valid_input:
            procedual_write("What do you want to do?", 0.001)
            
            choice = m.getwch()
            if choice.upper() not in available_options:
                clear_console()

                procedual_write("Invalid choice", 0.001)
                return show_choices()
            else: 
                valid_input = True
            sys.stdout.flush()
        return choice
#endregion 

def drink_from_canteen():
    global drinks, thirst
    if drinks > 0:
        drinks -= 1
        thirst = 0
        procedual_write(change_text_color("\nDrinking water...", GREEN), 0.001)
        status()
    else:
        procedual_write("No drinks left", 0.01)

def go_moderate_speed():
    global thirst, camel
    procedual_write(change_text_color("\nGoing moderate speed!", GREEN), 0.001)
    move_player(5, 12)
    thirst += 1
    camel += 1
    move_natives(7,14)

def go_full_speed():
    global thirst, camel
    procedual_write(change_text_color("\nGoing full speed!", GREEN), 0.001)
    move_player(10, 20)
    thirst += 1
    camel += random.randint(1,3)
    move_natives(7,14)

def stop_for_the_night():
    global camel
    procedual_write(change_text_color("\nTaking a rest", GREEN), 0.005)
    procedual_write("Camel is happy :)", 0.005)
    camel = 0
    move_natives(7,14)

def status():
        procedual_write("\nMiles traveled:  {}".format(change_text_color(player, OKBLUE)), 0.001)
        procedual_write("Drinks in canteen:  {}".format(change_text_color(drinks, OKBLUE)), 0.001)
        if player < DESERT_SIZE:
            procedual_write("The natives are {} miles behind you.".format(change_text_color(str(math.fabs(player - natives)), OKBLUE)), 0.001)
        else: 
            procedual_write("You crossed the desert!", 0.05)
            

        
def DrawMap():
    global DESERT_SIZE, player, natives
    map = list("********************")    
    map[int(player/10)] = PLAYER + "P" + YELLOW
    if natives > 0:
        map[int(natives/10)] = NATIVES + "N" + YELLOW
    map = YELLOW + "*".join(map) + ENDC + "\n" + ENDC + "\r"
    procedual_write(map, 0.001)

def change_text_color(text, col):
    text = str(text)
    return col + text + DEFAULT

def quit_delayed():
    time.sleep(3)
    clear_console()
    procedual_write("Thanks for playing" + "\nPress esc to exit...", 0.05)
    while True:
        k = m.getch()
        #k = bytes.decode(k, "utf-8", "replace")
        if k == chr(27).encode():
            break
    quit()

def quit_normal():
    clear_console()
    procedual_write("Thanks for playing" + "\nPress esc to exit...", 0.03)
    while True:
        k = m.getch()
        #k = bytes.decode(k, "utf-8", "replace")
        if k == chr(27).encode():
            break
    quit()
    

def clear_console():
    system('cls')

clear_console()

#the boolean "escaped" is substituted by quit_game()
last_player_pos = 0
first_round = True

def play_sound():
    winsound.Beep(400, 100)

def procedual_write(text, ms):
    
    for char in text:
        time.sleep(ms)
        
        sys.stdout.write(char)
        sys.stdout.flush()
    print()

def procedual_intro(text, ms):
    import threading
    for char in text:
        time.sleep(ms)
        if str.isalpha(char):
            threading.Thread(target=play_sound).start()
        sys.stdout.write(char)
        sys.stdout.flush()
    print()

def game_check():
    if natives >= player:
        print("The " + change_text_color("natives", FAIL) + " got you, you lost")
        winsound.Beep(4500, 1000)
        quit_delayed()
    elif math.fabs(natives - player) < 15:
        print("The " + change_text_color("natives", FAIL) + " are getting " + change_text_color("close", OKBLUE))
    
    
    if thirst > 6 :
        print("You " + change_text_color("died", FAIL) + " from thirst")
        winsound.Beep(4500, 1000)
        quit_delayed()
    elif thirst > 4:
        print("You are getting " + change_text_color("thirsty", OKBLUE))
    
    if camel > 8:
        print("Your camel " + change_text_color("died", FAIL))
        winsound.Beep(4500, 1000)
        quit_delayed()
    elif camel > 5:
        print("Your camel is getting " + change_text_color("tired", OKBLUE))
    
    if player >= DESERT_SIZE:
        clear_console()
        winsound.Beep(250, 4)
        print("You crossed the desert!")
        pygame.mixer.music.load("victory.mid")
        pygame.mixer.music.play(1)
        pygame.mixer.music.set_volume(0.2)
        quit_delayed()


def play_boring_intro():
    clear_console()
    #Or I could have used 4 print statements
    procedual_intro("Welcome to Camel!", 0.03)

    time.sleep(1)

    procedual_intro(
    '''
You have stolen a camel to make your
way across the great Mobi desert.
    ''', 0.05)

    time.sleep(2)

    procedual_intro(
    '''The natives want their camel back 
and are chasing you down! 
    ''', 0.03)

    time.sleep(2)

    procedual_intro(
    '''Survive the desert 
and out-run the natives.
    ''', 0.03)


    time.sleep(2)

    procedual_intro(
    '''
Good Luck.
    ''', 0.03)
    time.sleep(3)



play_boring_intro()
if play_music:
    pygame.mixer.music.load("music.mid")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.1)
while True:
    clear_console()

    
    #region Game Checks
    game_check()
    #endregion
    choice = show_choices().upper()

    #region Options
    if choice == "Q":
        quit_normal()

    elif choice == "A":
        drink_from_canteen()

    elif choice == "E":
        status()

    elif choice == "D":
        stop_for_the_night()
    
    elif choice == "C":
        go_full_speed()

    elif choice == "B":
        go_moderate_speed()

    rng = random.randint(1,20)
    if rng == 1 and player != last_player_pos:
        print("You found an " + change_text_color("oasis", YELLOW))
        print("You refilled your canteen and rested")
        drinks = 3
        camel = 0
        thirst = 0
    last_player_pos = player

    game_check()
    #endregion

    print("Press " + change_text_color("enter", OKBLUE)+ " for next round")
    while True:
        k = m.getch()
        k = bytes.decode(k, "utf-8", "replace")
        if k == "\r":
            break

        
    
    
    

    
    


