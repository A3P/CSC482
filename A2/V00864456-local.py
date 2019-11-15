# Amir Afshar
# V00864456
# Assignment CSC482B
import numpy as np
import sys

gap=2

alignments=[]

# Used for keeping track of the highest scores on the matrix
maxIndices=[]
maxScore=0

# Assigns a score based on the y and x coordinates.
# This only works if x-1 and y-1 are already assigned in the Matrix.
def score(y, x):
    if x!=0 and y!=0:
        # Scores for a match
        if seq1[y-1] == seq2[x-1]:
            matrix[y,x] = matrix[y-1,x-1] + 2
        # Scores for a mismatch
        else:
            matrix[y,x] = matrix[y-1,x-1] -1
        # Scores for horizontal and vertical gap penalties
        if matrix[y-1,x] - gap > matrix[y,x]:
            matrix[y,x] = matrix[y-1,x] - gap
        if matrix[y,x-1] - gap > matrix[y,x]:
            matrix[y,x] = matrix[y,x-1] - gap
        
        # Min value will always be 0
        if(0>matrix[y,x]):
            matrix[y,x]=0

        global maxScore
        global maxIndices
        # Stores the location of the highest scores on the matrix
        if(matrix[y,x]!=0 and matrix[y,x]>=maxScore):
            if(matrix[y,x]>maxScore):
                maxIndices=[]
                maxScore = matrix[y,x]
                
            maxIndices.append((y,x))
            

# Backtracks starting from the bottom left index of the matrix while using recursion until it hits the base case,
# which is the top left index.
def backtrack(align1, align2, y, x):
    if matrix[y,x]==0:
        print(align1, align2)
        alignments.append((align1, align2))
    else:

        print(matrix[y,x])
        print("y and x not 0:", align1, align2)

        # Checks for horizontal linear gaps during the backtrack
        if x != 0 and matrix[y,x-1] - gap == matrix[y,x]:
            backtrack("-" + align1, seq2[x-1] + align2, y, x-1)

        # Checks for horizontal linear gaps during the backtrack
        if y!= 0 and matrix[y-1,x] - gap == matrix[y,x]:
            backtrack(seq1[y-1] + align1, "-" + align2, y-1, x)

        # Checks the diagonal path in the matrix for the matches and mismatches.
        if x!= 0 and y!= 0 and ( 
        (matrix[y-1,x-1] + 2 == matrix[y,x] and seq1[y-1] == seq2[x-1]) 
        or (matrix[y-1,x-1] - 1 == matrix[y,x] and seq1[y-1] != seq2[x-1])):
            backtrack(seq1[y-1] + align1, seq2[x-1] + align2, y-1, x-1)


print "Input file name:", sys.argv[1]

# reads the sequences and formats to prepare for other functions 
seq1=""
seq2=""
with open(sys.argv[1]) as f:
    seq1 = f.readline().strip()
    seq2 = f.readline().strip()

# Create a 2d matri based on the length of the sequences
matrix = np.zeros([len(seq1)+1, len(seq2)+1], dtype=int)

# Traverses the matrix and scores from top left to bottom right
for x in range(0, len(seq2)+1):
    for y in range(0, len(seq1)+1):
        score(y, x)

for x in maxIndices:
    backtrack("", "", x[0], x[1])

print(alignments)
print(matrix)

print(maxIndices)

# Printing methods for outputing all the answers to seperate files

f1 = open("2.o1", "w+")
f1.write(str(maxScore))
f1.close()

f2 = open("2.o2", "w+")
f2.write(str(matrix))
f2.close()

f3 = open("2.o3", "w+")
f3.write(str(alignments[0][0]+ "\n"))
f3.write(str(alignments[0][1]))
f3.close()

# print(len(alignments))
f4 = open("2.o4", "w+")
if(len(alignments) > 1):
    f4.write("YES")
else:
    f4.write("NO")
f4.close()

f5 = open("2.o5", "w+")
f5.write(str(len(alignments))+"\n")
for x in alignments:
    f5.write(str(x[0]+ "\n"))
    f5.write(str(x[1] + "\n\n"))
f5.close()