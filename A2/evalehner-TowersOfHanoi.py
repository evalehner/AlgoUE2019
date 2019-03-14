import argparse
import sys

parser = argparse.ArgumentParser(prog="Towers of hanoi")
parser.add_argument('-n', type=int, help="Enter tower hight")
args = parser.parse_args()

def TowersOfHanoi(discNumber, sourcePeg = 1, destinationPeg = 3):
    global count
    if (discNumber == 1):
        print("move disk from peg " + str(sourcePeg) + " to peg " + str(destinationPeg))
        count = count + 1
        return
    unusedPeg = (6 - sourcePeg - destinationPeg)
    TowersOfHanoi(discNumber-1, sourcePeg, unusedPeg)
    print("move disk from peg " + str(sourcePeg) + " to peg " + str(destinationPeg))
    count = count + 1
    TowersOfHanoi(discNumber-1, unusedPeg, destinationPeg)
    return # "Anzahl der benötigten Schritte ist " + str(count)

if __name__ == '__main__':
    count = 0
    print(TowersOfHanoi(args.n, 1, 3))
    print("Anzahl der benötigten Schritte ist " + str(count), file=sys.stderr)