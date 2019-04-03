import os
import argparse

parser = argparse.ArgumentParser(prog="Returns highest manhattan tourist score")
parser.add_argument('-f', '--file', required=True, type=str, help="please provide scoring matrix for horizontal and vertical edges")
args = parser.parse_args()

# read in and store grid values in list
f = args.file
file = open(f , 'r')

downGrid = []
rightGrid = []

G_down_bool = False
G_right_bool = False

for line in file:
    if not line.startswith('---'):
        current = line.split("   ") # scoring entries seperated by 3 spaces

        if current[0].startswith('G_down'):
            G_down_bool = True
            G_right_bool = False
        if current[0].startswith('G_right'):
            G_right_bool = True
            G_down_bool = False

        # create list of lists, remove newlines and convert str to float
        if (G_down_bool == True) and (len(current) > 3):
            current_int = [float(i.strip()) for i in current]
            downGrid.append(current_int)
        if (G_right_bool == True) and (len(current) > 3) and (G_down_bool == False):
            current_int = [float(i.strip()) for i in current]
            rightGrid.append(current_int)

file.close()

# get dimentions
idown = len(downGrid[0])
iright = len(rightGrid)


def ManhattanTourist(scoringCostsDown, scoringCostsRight, allVertical, allHorizontal):
    scoringMatrix = [0] * allHorizontal # initialize matrix dimention
    for i in range(0, allHorizontal):
        scoringMatrix[i] = [0]*allHorizontal

    # initialization
    for pointVertical in range(1, allVertical):
        scoringMatrix[pointVertical][0] = (scoringMatrix[pointVertical-1][0] + float(scoringCostsDown[pointVertical-1][0]))
    for pointHorizontal in range(1, allHorizontal):
        scoringMatrix[0][pointHorizontal] = scoringMatrix[0][pointHorizontal-1] + float(scoringCostsRight[0][pointHorizontal-1])

    # fill up the missing values in scoring matrix
    for pointVertical in range(1, allVertical ):
        for pointHorizontal in range(1, allHorizontal ):
            verticalScore = scoringMatrix[pointVertical-1][pointHorizontal] + scoringCostsDown[pointVertical-1][pointHorizontal]
            horizontalScore = scoringMatrix[pointVertical][pointHorizontal-1] + scoringCostsRight[pointVertical][pointHorizontal-1]
            scoringMatrix[pointVertical][pointHorizontal] = max(verticalScore, horizontalScore)

    return scoringMatrix


if __name__ == '__main__':
    result = ManhattanTourist(downGrid, rightGrid, idown, iright)
    print(result[idown-1][iright-1])
