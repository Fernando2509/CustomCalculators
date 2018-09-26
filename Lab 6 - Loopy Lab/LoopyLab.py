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



def box2(rows):
    for i in range(1, rows, 2):
        for x in range(i, rows, 2):
            print (x,end=" ")
        for w in range(i-1):
            print (" ",end=" ")
        for x in range(rows-1, i-1, -2):
            print (x,end=" ")            
        #if i != rows-1:
        print()
        

    for i in range(rows-1, 0, -2):
        for x in range(-i, -rows, -2):
            print (-x,end=" ")
        for w in range(i-1):
            print (" ",end=" ")
        for x in range(-rows+1, -i+1, 2):
            print (-x,end=" ")
            # rows -x -1
        print()
    
       




ROWS = int(input("Size of a box with a box size: ")) * 2
box2(ROWS)

input("Press emter to exit\r\n")
