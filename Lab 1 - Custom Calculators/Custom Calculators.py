from math import pi
import argparse

parser = argparse.ArgumentParser(description="Calculate some silly functions")

parser.add_argument('--trapezoid', '-t', type=int, nargs=3, metavar=('height','bottom','top'),
                    help='Finds the area of a trapezoid')

parser.add_argument('--ftc', '-f', type=int, nargs=1, metavar=('temp'),
                    help='Convert F to C')

parser.add_argument('--area','-a', type=int,nargs=1, metavar=('radius'),
                    help='Finds the area of a circle')

def FtoC(temp):
    return (temp - 32) * 0.5556

def FindAreaOfACirlce(radius):
    try:
        realNumberCheck = pi * radius * radius
    except :
        print("Parsing error! please...")
        radius = int(input("Enter radius: "))
    return math.pi * math.pow(radius, 2)

def FindAreaOfTrapezoid(height, bottom, top):
    try:
        realNumberCheck = (1 / 2) * (bottom + top) * height
    except :
        print("Parsing error! please...")
        height = int(input("Enter height of trapezoid : "))
        bottom = int(input("Enter width of bottom trapezoid : "))
        top = int(input("Enter width of top trapezoid : "))
    return (1 / 2) * (bottom + top) * height

if __name__ == "__main__":
    args = parser.parse_args()
    if args.trapezoid:
        print("The area of the trapezoid is")
        print(FindAreaOfTrapezoid(args.trapezoid[0], args.trapezoid[1], args.trapezoid[2]))
    elif args.area:
        print("The area of the circle is")
        print(FindAreaOfACirlce(args.area[0]))
    elif args.ftc:
        print("The temperature in celsius is")
        print(FtoC(args.ftc[0]))
    else:
        print("No arguments selected, please use \"-h\" for options")
        input("Press enter to exit...")