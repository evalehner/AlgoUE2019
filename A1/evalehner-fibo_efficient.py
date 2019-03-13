import argparse
import time

parser = argparse.ArgumentParser(prog="This Program calcuates fibonnaci numbers efficiently")

parser.add_argument('-n', '-number', required=True, type=int, help= " Please enter a number. Program will return respective fibonnaci number")
parser.add_argument('--all', action='store_true', default=False, help='Include preceeding fibonnaci numbers in output')
args = parser.parse_args()

def fibonnaciArray(n):
    storageArray = []
    firstNumber = 1
    secondNumber = 1
    if (n == 1 ):
        storageArray.append(firstNumber)
    elif (n == 2):
        storageArray.append(firstNumber)
        storageArray.append(secondNumber)
    elif ( n == 0 ):
        return "Restart and enter number above 0"
    else:
        for i in range(0, n):
            currentNumber = firstNumber + secondNumber
            storageArray.append(firstNumber)
            firstNumber = secondNumber
            secondNumber = currentNumber

    return storageArray

if __name__ == "__main__":

    start = time.time()
    if args.all:
        resultArray = fibonnaciArray(args.n)
        print(resultArray)
    else:
        resultArray = fibonnaciArray(args.n)
        print(resultArray[-1])
    end = time.time()
    runTime = end - start

    recordNonRecursive = open("nonRecursiveRuntime.txt", 'a')
    recordNonRecursive.write(str(args.n) + '\t' + str(runTime) + '\n')
    recordNonRecursive.close()