import pickle
import string
import random
import argparse
from os import path
SAVED_FILE_NAME = "questions.pickle"
ALPHABET = list(string.ascii_uppercase)

parser = argparse.ArgumentParser(description="A simple quiz made with python")
parser.add_argument('--add', '-a', nargs='+',
                    help='Question | Correct Answer | *Alternatives')



args = parser.parse_args()


class Question():
    def __init__(self, question, correct_choice, *options, ):
        self.question = question
        self.correct_choice = correct_choice
        self.multiple_option_question = False
        if len(options) >= 2:
            self.options = dict()
            charCount = 0
            new_correct_choice = None
            for q in options:

                if q == correct_choice:
                    new_correct_choice = ALPHABET[charCount]

                self.options[ALPHABET[charCount]] = q
                charCount += 1

            if new_correct_choice != None:
                self.correct_choice = new_correct_choice
            else:
                print("Correct choice does not exist in options")
            self.multiple_option_question = True
            

    def Ask(self):
        print(self.question)
        if self.multiple_option_question:
           Question.ShowOptions(self)
        answer = input()
        if answer.upper() == self.correct_choice.upper():
            print("You got it")
            return True
        else:
            print("Wrong! The answer was {}".format(self.correct_choice.upper()))
            return False

    def ShowOptions(self):
        for k in self.options:
            print(k + ": " + self.options[k])
        
class PickleManager():
    global question_list
    def SaveQuestions():
        pickle_out = open(SAVED_FILE_NAME, "wb")
        pickle.dump(question_list, pickle_out)

    def TryLoadQuestions():
        if path.exists(SAVED_FILE_NAME):
            pickle_in = open(SAVED_FILE_NAME, "rb")
            question_list = pickle.load(pickle_in)
        else:
            print("Question file was not found")


    def AddQuestion(question, correct_choice, *options):
        question_list.append(Question(question,correct_choice, options))
        PickleManager.SaveQuestions()

question_list = list()

question_list =[
    Question("whats the US president's firt name?", "donald"),
    Question("How does a cow do math?", "With a cow-culator",  "Moo-tiplicating the equations", "Using convolutional neural networks","With a cow-culator", "Using google"),
    Question("How many classes did I use to make this program?", "2", "1", "2", "4","5"),
    Question("Whats the answer of everything?", "42")
    ]


if __name__ == "__main__":
    if args.add:
        PickleManager.AddQuestion(args.add[0], args.add[1], args.add[2:-1])
    PickleManager.TryLoadQuestions()

    random.shuffle(question_list)
    questions_got_right = 0
    for x in question_list:
        if  x.Ask():
            questions_got_right += 1
        print()

    percentage = (questions_got_right * 100) / len(question_list)
    print("\r\nYou Got {0}% of the questions right".format(round(percentage, 3)))