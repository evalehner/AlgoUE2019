#!/usr/local/bin/python3

# pairwise global sequence alignment
from Bio import SeqIO
from argparse import ArgumentParser
import sys

parser = ArgumentParser(prog="Needleman Wunsch")
parser.add_argument('-f', '--fasta', type=str, required=True, help="Please prowide two sequences in fasta format you want to align")
parser.add_argument('-m', '--match', type=int, default=1, help="Please specify alignemnt score for a match")
parser.add_argument('-mi', '--mismatch', type=int, default=-1, help="Please specify alignemnt score for a mismatch")
parser.add_argument('-g', '--gap', type=int, default=-2, help="Please specify alignemnt score for a gap")
args = parser.parse_args()

fa = args.fasta


allID = []
allSeq = []
for record in SeqIO.parse(fa, "fasta"):
    allID.append(record.id)
    allSeq.append(record.seq)

seq1 = allSeq[0]
seq2 = allSeq[1]

# scoring
match = args.match
mismatch = args.mismatch
gap = args.gap

def scoring(char1, char2, matchCost=1, mismatchCost=-1, gapCost=-2):

    alphabet = ["A", "G", "T", "C", "a", "g", "t", "c"]
    if char1 in alphabet and char2 in alphabet:
        if char1 == char2:
            return matchCost
        elif char1 != char2:
            return mismatchCost
    elif (char1 == '-') or (char2 == '-') :
        return gapCost


def similarity(HorizontalString, VerticalString):
    # initialisieren der matrix dimesion
    horizontalLen = len(HorizontalString) + 1
    verticalLen = len(VerticalString) + 1
    scoringMatrix = [[0 for i in range(horizontalLen)] for j in range(verticalLen)]

    # initialisieren der seitlichen gaps
    for pathVertical in range(1, verticalLen):
        scoringMatrix[pathVertical][0] = (scoringMatrix[pathVertical - 1][0] + gap)
    for pathHorizontal in range(1, horizontalLen):
        scoringMatrix[0][pathHorizontal] = scoringMatrix[0][pathHorizontal - 1] + gap

    # fill up the missing values in scoring matrix
    for pathVertical in range(1, verticalLen):

        for pathHorizontal in range(1, horizontalLen):

            diaScore = scoringMatrix[pathVertical - 1][pathHorizontal - 1] + scoring(HorizontalString[pathHorizontal-1],VerticalString[pathVertical-1])
            verticalScore = scoringMatrix[pathVertical - 1][pathHorizontal] + scoring(VerticalString[pathVertical-1], '-')
            horizontalScore = scoringMatrix[pathVertical][pathHorizontal - 1] + scoring(HorizontalString[pathHorizontal-1], '-')
            scoringMatrix[pathVertical][pathHorizontal] = max(verticalScore, horizontalScore, diaScore)

    return scoringMatrix


def backtracking(colSeq, rowSeq, scoringMatrix):
    nCol = len(colSeq)
    mRow = len(rowSeq)

    aln1 = ""
    aln2 = ""
    decoration = ""

    while nCol != 0 or mRow != 0:

        current = scoringMatrix[mRow][nCol]
        diaScore = scoringMatrix[mRow-1][nCol-1]
        vertScore = scoringMatrix[mRow-1][nCol]
        horScore = scoringMatrix[mRow][nCol-1]

        if current == diaScore + match:
            aln1 += colSeq[nCol-1]
            aln2 += rowSeq[mRow-1]
            nCol = nCol-1
            mRow = mRow -1
            decoration += '*'

        elif current == diaScore + mismatch:
            aln1 += colSeq[nCol - 1]
            aln2 += rowSeq[mRow - 1]
            nCol = nCol - 1
            mRow = mRow - 1
            decoration += ' '

        elif current == vertScore + gap:
            aln2 += rowSeq[mRow-1]
            aln1 += '-'
            mRow -= 1
            decoration += ' '

        elif current == horScore + gap:
            aln1 += colSeq[nCol-1]
            aln2 += '-'
            nCol -= 1
            decoration += ' '

        if nCol == 0:
            aln1 += '-'
            aln2 += rowSeq[mRow-1]
            mRow -= 1
            decoration += ' '

        elif mRow == 0:
            aln2 += '-'
            aln1 += colSeq[nCol - 1]
            nCol -= 1
            decoration += ' '

    aln1 = aln1[::-1]
    aln2 = aln2[::-1]
    decoration = decoration[::-1]

    return aln1, aln2 , decoration

def clustalFormat(allID, align1, align2, decor):
    print("CLUSTAL")
    print('\n')
    header1 = True
    header2 = False

    length = len(align1)
    while length > 0:
        if length > 60:
            stop = 61
        else:
            stop = len(align1) + 1

        while header1 == True:
            print(allID[0] + "\t" + align1[0:stop])
            align1 = align1[stop:length+1]
            header1 = False
            header2 = True

        while header2 == True:
            print(allID[1] + "\t" + align2[0:stop])
            print((len(allID[1]) * ' ') + "\t" + decor[0:stop])
            align2 = align2[stop:length+1]
            header2 = False
            header1 = True
            length = len(align1)
        print('\n')


if __name__ == "__main__":
    #calculate score
    score = similarity(seq1 , seq2)

    # apply backtracking
    al1 , al2, dec= backtracking(seq1 , seq2, score)

    #print everything to stdout
    clustalFormat(allID, al1, al2, dec)

    #write score to stderr
    sys.stderr.write(str(score[len(seq2)][len(seq1)]))




