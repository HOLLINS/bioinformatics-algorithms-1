import os
import csv
import sys
import re
import importlib
import networkx as nx

# settings
#curDir = 'E:/Copy/Coursera/Bioinformatics Algorithms (part-I)/MyPrograms/week6-python'
curDir = 'D:/Copy/Coursera/Bioinformatics Algorithms (part-I)/MyPrograms/week6-python'
inputFile = './data/6.local_alignment-2.txt'
#inputFile = 'C:/Users/Ashis/Downloads/dataset_247_9.txt'
outputFile = './results/6.local_alignment.txt'
scoreFile = './data/PAM250_1.txt'

# set current directory
os.chdir(curDir)

## read input
with open(inputFile) as f:
    inputs = f.readlines()

protein1 = inputs[0].strip()
protein2 = inputs[1].strip()

## read pam score matrix
## colIndex is map from amino acid to its index
## pam is a 2D matrix
with open(scoreFile) as f:
    lines = f.readlines()
    cols = re.split("\\s*", lines[0].strip())
    colIndex = {cols[i]:i for i in range(0,len(cols))}
    pam = [[int(i) for i in re.split("\\s*", row.strip())[1:]] for row in lines[1:]]

#print(pam)

## indel penalty
sigma = 5



## create scores and backtrack arrays
len1 = len(protein1)
len2 = len(protein2)
scores = [[0]*(len2+1) for x in range(len1+1)]
backtrack = [[3]*(len2+1) for x in range(len1+1)]     # 0: top, 1:left, 2:diag, 3:start


## put first row and first column of scores and backtrack arrays
#for i in range(1,len1+1):
#    scores[i][0] = scores[i-1][0] - sigma
#    backtrack[i][0] = 0
    
#for j in range(1,len2+1):
#    scores[0][j] = scores[0][j-1] - sigma
#    backtrack[0][j] = 1


## update scores in greedy approach
for i in range(1,len1+1):
    for j in range(1,len2+1):
        topScore = scores[i-1][j] - sigma
        leftScore = scores[i][j-1] - sigma
        diagScore = scores[i-1][j-1] + pam[colIndex[protein1[i-1]]][colIndex[protein2[j-1]]]
        startScore = 0
        candidateScores = [topScore, leftScore, diagScore, startScore]
        scores[i][j] = max(candidateScores)
        backtrack[i][j] = candidateScores.index(scores[i][j])

## max score node is the
maxScore = float("-inf")
maxi = -1
maxj = -1
for i in range(1,len1+1):
    for j in range(1,len2+1):
        if scores[i][j] > maxScore:
            maxScore = scores[i][j]
            maxi = i
            maxj = j

        
## max score
#maxScore = scores[len1][len2]

## backtrack and find alignment
alignment1 = []
alignment2 = []

i = maxi
j = maxj
while i!=0 or j!=0:
    if backtrack[i][j] == 0:        # top
        alignment1.append(protein1[i-1])
        alignment2.append('-')
        i = i-1
    elif backtrack[i][j] == 1:      # left
        alignment1.append('-')
        alignment2.append(protein2[j-1])
        j = j-1
    elif backtrack[i][j] == 2:      # diag
        alignment1.append(protein1[i-1])
        alignment2.append(protein2[j-1])
        i = i-1
        j = j-1
    else:                           # start
        i = 0
        j = 0
    
alignment1.reverse()
alignment2.reverse()

print(maxScore)
#print(alignment1)
#print(alignment2)

# output
with open(outputFile, "w") as f:
    f.writelines(str(maxScore) + "\n")
    f.writelines("".join(alignment1) + "\n")
    f.writelines("".join(alignment2) + "\n")

