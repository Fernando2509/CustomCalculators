#Part 1



def square_triangle(height):
    count = 1
    num = 10
    for x in range(height):
        for j in range(count):
            print(num, end=" ")
            num +=1
        count += 1
        print()

HEIGHT = int(input("Square Triangle Height: "))
square_triangle(HEIGHT)

#############################
print()
#############################

#Part 2



def box(rows):
    print("*" * rows * 2)
    for x in range(rows-2):
        print("*" + (" " * ((rows*2) - 2)) + "*")
    print("*" * rows * 2)

SIZE = int(input("Box size: "))
box(SIZE)

#############################
print()
#############################

#Part 3
#TODO

def box2(rows):
    for i in range(rows):
        # Print leading spaces
        for j in range(abs(int((rows/2)-i))):
            print ("*",end=" ")

       
        print()

    '''
    for i in range(rows):
        # Print leading spaces
        for j in range(i+2):
            print ("*",end=" ")
        # Count up
        for j in range(1,9-i):
            print (" ",end=" ")
        # Count down
        for j in range(7-i,0,-1):
            print (" ",end=" ")
        for j in range(i+2):
            print ("*",end=" ")
 
        print()
    '''

ROWS = int(input("Size of a box with a box size: ")) * 2
box2(ROWS)