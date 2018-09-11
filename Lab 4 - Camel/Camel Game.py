#http://programarcadegames.com/index.php?chapter=lab_camel&lang=en
from os import system 
import math

class Game():
    def __init__(self, desertSize, **kwargs):
        self.desertSize = desertSize
        self.escaped = False
        self.player = 0
        self.natives = -20
        self.drinks = 5
        print("Welcome to Camel!")
        print("You have stolen a camel to make your way across the great Mobi desert.")
        print("The natives want their camel back and are chasing you down! Survive your")
        print("desert trek and out run the natives.")
        

    def Start(self):
        while not self.escaped:
            #Clear Console
            system('cls') 
            self.choice = self.AskChoices()
    
    def AskChoices(self):
        #TODO Create an action class that has a label and a "action" method
        print("")
        print("A. Drink from your canteen.")
        print("B. Ahead moderate speed.")
        print("C. Ahead full speed.")
        print("D. Stop for the night.")
        print("E. Status check.")
        print("Q. Quit.")
        return self.AskInput()
    
    def AskInput(self):
        choice = ""
        valid_input = False
        available_options = "ABCDEQ"
        while not valid_input:
            choice = input("What do you want to do?")
            if choice.upper() not in available_options:
                print("Invalid Choice, please try again\r\n")

    def Status(self):
        print("Miles traveled:  {}".format(self.player))
        print("Drinks in canteen:  {}".format(self.drinks))
        print("The natives are 10 miles behind you.".format(math.abs(self.player - self.natives)))

    def DrawMap(self):
        #TODO DrawMap

class Main():
    def __init__(self, *args, **kwargs):
        game = Game(200)
        game.Start()

if __name__ == '__main__':
    Main()
