#http://programarcadegames.com/index.php?chapter=lab_camel&lang=en

class Game():
    def __init__(self, desertSize, **kwargs):
        self.desertSize = desertSize
        self.escaped = False
        print("Welcome to Camel!")
        print("You have stolen a camel to make your way across the great Mobi desert.")
        print("The natives want their camel back and are chasing you down! Survive your")
        print("desert trek and out run the natives.")
        

    def Start(self):
        self.player = 0
        self.natives =0 
        while not self.escaped:
            self.choice = self.AskChoices()
    
    def AskChoices(self):
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

class Main():
    def __init__(self, *args, **kwargs):
        game = Game(200)
        game.Start()

if __name__ == '__main__':
    Main()
