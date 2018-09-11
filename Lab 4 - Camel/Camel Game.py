#Used to clean the console
from os import system 
#Math is used to get the absolute value of the ditance between him and the natives
import math
import random

#Game variables
DESERT_SIZE = 200

player = 0
natives = -20
drinks = 3
camel = 0
thirst = 0

#Or I could have uses 4 print statements
print
('''
Welcome to Camel!
You have stolen a camel to make your way across the great Mobi desert.
The natives want their camel back and are chasing you down! Survive your
desert trek and out run the natives.
''')


#region Move Functions
def move_natives(min_val, max_val):
    global natives
    natives += random.randint(min_val, max_val)

def move_player(min_val, max_val):
    global player
    random_val = random.randint(min_val, max_val)
    player += random_val
    if DESERT_SIZE - player > 0:
        print("You moved {0} miles {1} left".format(random_val, DESERT_SIZE - player))
    else: 
        pass
    
#endregion

#region User Input
def show_choices():
        #TODO Create an action class that has a label and a "action" method
        print("")
        print("A. Drink from your canteen.")
        print("B. Ahead moderate speed.")
        print("C. Ahead full speed.")
        print("D. Stop for the night.")
        print("E. Status check.")
        print("Q. Quit.")
        return ask_input()

def ask_input():
        choice = "error"
        valid_input = False
        available_options = "ABCDEQ"
        while not valid_input:
            choice = input("What do you want to do?")
            if choice.upper() not in available_options:
                print("Invalid Choice, please try again\r\n")
            else: valid_input = True
        return choice
#endregion 

def drink_from_canteen():
    global drinks, thirst
    if drinks > 0:
        drinks -= 1
        thirst = 0
        print("Drinking water...")
        status()
    else:
        print("No drinks left")

def go_moderate_speed():
    global thirst, camel
    move_player(5, 12)
    thirst += 1
    camel += 1
    move_natives(7,14)

def go_full_speed():
    global thirst, camel
    print("\nGoing full speed!")
    move_player(10, 20)
    thirst += 1
    camel += random.randint(1,3)
    move_natives(7,14)

def stop_for_the_night():
    global camel
    print("Taking a rest")
    print("Camel is happy :)")
    camel = 0
    move_natives(7,14)

def status():
        print("Miles traveled:  {}".format(player))
        print("Drinks in canteen:  {}".format(drinks))
        if player < DESERT_SIZE:
            print("The natives are {} miles behind you.".format(math.fabs(player - natives)))
        else: print("You crossed the desert!")
        
def DrawMap():
    global DESERT_SIZE, player, natives
    map = list("*********************")    
    map[int(player/10)] = "P"
    if natives > 0:
        map[int(natives/10)] = "N"
    print("*".join(map))

def quit_game():
    print("\nThanks for playing\n")
    input("Press enter to exit...")
    quit()

def clear_console():
    system('cls')

clear_console()

#the boolean "escaped" is substituted by quit_game()
while True:
    #region Game Checks
    if natives >= player:
        print("The natives got you, you lost")
        quit_game()
    elif math.fabs(natives - player) < 15:
        print("The natives are getting close")


    if thirst > 6 :
        print("You died from thirsty")
        quit_game()
    elif thirst > 4:
        print("You are getting thirsty")

    if camel > 8:
        print("Your camel died")
        quit_game()
    elif camel > 5:
        print("Your camel is getting tired")

    if player >= DESERT_SIZE:
        print("You crossed the desert!")
        quit_game()

    rng = random.randint(1,20)
    if rng == 1:
        print("You found an oasis")
        print("You refilled your canteen and rested")
        drinks = 3
        camel = 0
        thirst = 0


    #endregion
    if player < DESERT_SIZE:
        DrawMap()
    choice = show_choices().upper()
    
    clear_console()

    #region Options
    if choice == "Q":
        quit_game()

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
    #endregion

        
    
    
    

    
    


