#!/bin/bash
import argparse
import time
# command line input
parser = argparse.ArgumentParser(prog="This Program calcuates fibonnaci numbers inefficiently")

parser.add_argument('-n', '-number', required=True, type=int, help= " Please enter a number. Program will return respective fibonnaci number")
parser.add_argument('--all', action='store_true', default=False, help='Include preceeding fibonnacinumbers in output')
args = parser.parse_args()


def recursiveFibonnacci(n):
    if (n <= 2 and n > 0 ):
        return 1
    elif ( n == 0):
        return "Restart and enter number above 0"
    else:
        return recursiveFibonnacci(n-1) + recursiveFibonnacci(n-2)

if __name__ == "__main__":

    start = time.time()
    if args.all:
        allFibonnaciNumbers = []
        for i in range(1, (args.n+1)):
            allFibonnaciNumbers.append(recursiveFibonnacci(i))
        print(allFibonnaciNumbers)
    else:
        result = recursiveFibonnacci(args.n)
        print(result)
    end = time.time()
    runTime = end-start

    recordRecursive = open("recursiveRuntime.txt", 'a')
    recordRecursive.write(str(args.n) + '\t' + str(runTime) + '\n')
    recordRecursive.close()

