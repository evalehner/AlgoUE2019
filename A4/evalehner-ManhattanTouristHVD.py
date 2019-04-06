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
diaGrid = []

G_down_bool = False
G_right_bool = False
G_dia_bool = False

for line in file:
    if not line.startswith('---'):
        current = line.split("   ") # scoring entries seperated by 3 spaces

        if current[0].startswith('G_down'):
            G_down_bool = True
        if current[0].startswith('G_right'):
            G_right_bool = True
            G_down_bool = False
        if current[0].startswith('G_diag'):
            G_dia_bool = True
            G_right_bool = False

        # create list of lists, remove newlines and convert str to float
        if (G_down_bool == True) and (len(current) > 3):
            current_int = [float(i.strip()) for i in current]
            downGrid.append(current_int)
        if (G_right_bool == True) and (len(current) > 3) and (G_down_bool == False):
            current_int = [float(i.strip()) for i in current]
            rightGrid.append(current_int)
        if (G_dia_bool == True) and (len(current) > 3):
            current_int = [float(i.strip()) for i in current]
            diaGrid.append(current_int)


file.close()

# get dimentions
idown = len(downGrid[0])
iright = len(rightGrid)
idia = len(diaGrid[0])

def ManhattanTourist(scoringCostsDown, scoringCostsRight, scoringCostsDia, allVertical, allHorizontal, allDia):
    scoringMatrix = [0] * allHorizontal # initialize matrix dimention
    for i in range(0, allHorizontal):
        scoringMatrix[i] = [0]*allHorizontal

    # initialization
    for pathVertical in range(1, allVertical):
        scoringMatrix[pathVertical][0] = (scoringMatrix[pathVertical-1][0] + float(scoringCostsDown[pathVertical-1][0]))
    for pathHorizontal in range(1, allHorizontal):
        scoringMatrix[0][pathHorizontal] = scoringMatrix[0][pathHorizontal-1] + float(scoringCostsRight[0][pathHorizontal-1])

    # fill up the missing values in scoring matrix
    for pathVertical in range(1, allVertical ):
        for pathHorizontal in range(1, allHorizontal ):
            verticalScore = scoringMatrix[pathVertical-1][pathHorizontal] + scoringCostsDown[pathVertical-1][pathHorizontal]
            horizontalScore = scoringMatrix[pathVertical][pathHorizontal-1] + scoringCostsRight[pathVertical][pathHorizontal-1]
            diaScore = scoringMatrix[pathVertical-1][pathHorizontal-1] + scoringCostsDia[pathVertical-1][pathHorizontal-1]
            scoringMatrix[pathVertical][pathHorizontal] = max(verticalScore, horizontalScore, diaScore)

    return scoringMatrix


if __name__ == '__main__':
    result = ManhattanTourist(downGrid, rightGrid, diaGrid, idown, iright, idia)
    print(result[idown-1][iright-1])



